"""M3 dynamometer-card classifier: 1-D CNN (~150k params) on 128-pt surface card + computed downhole card.

Input channels (128 points): surface position, surface load, Gibbs downhole position, downhole load (all normalised per
card) and four broadcast scalars (log load range, mean/range, position range, spm). Trained on S4 with its augmentations
plus on-the-fly noise/gain, temperature-scaled, exported to ONNX (served with onnxruntime). Baseline: Fourier
descriptors + kNN. Also returns the "impact" location (steepest downstroke load drop) for M5.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

from mantle_physics import DYNO_CLASSES, downhole_card, synthesize_cards

from .. import common, data

ID = "M3"
N_PTS = 128
N_CH = 8
NC = len(DYNO_CLASSES)


# ---------------------------------------------------------------- preprocessing


def _norm(x):
    lo = x.min(axis=1, keepdims=True)
    rng = np.maximum(np.ptp(x, axis=1, keepdims=True), 1e-9)
    return (x - lo) / rng


def prepare(pos, load, spm) -> np.ndarray:
    """(B,128) position (m), load (N), spm -> (B,8,128) float32 network input."""
    pos = np.atleast_2d(np.asarray(pos, dtype=np.float64))
    load = np.atleast_2d(np.asarray(load, dtype=np.float64))
    spm = np.broadcast_to(np.asarray(spm, dtype=np.float64), (len(pos),))
    period = 60.0 / np.maximum(spm, 0.3)
    dpos, dload = downhole_card(pos, load, period, damping=0.1)
    dpos, dload = np.nan_to_num(dpos), np.nan_to_num(dload)
    ptp_l = np.maximum(np.ptp(load, axis=1), 1.0)
    ptp_p = np.maximum(np.ptp(pos, axis=1), 1e-6)
    mean_l = load.mean(axis=1)
    ch = [
        _norm(pos),
        (load - mean_l[:, None]) / ptp_l[:, None] + 0.5,
        _norm(dpos),
        np.clip((dload - mean_l[:, None] + mean_l[:, None] * 0) / ptp_l[:, None], -3, 3) * 0.5 + 0.5,
    ]
    sc = [(np.log10(ptp_l) - 4.0), np.clip(mean_l / ptp_l, 0, 20) / 5.0, ptp_p / 3.0, spm / 10.0]
    x = np.stack(ch + [np.repeat(s[:, None], pos.shape[1], axis=1) for s in sc], axis=1)
    return np.clip(np.nan_to_num(x), -5, 5).astype(np.float32)


def impact_index(pos, load) -> dict:
    """Steepest downstroke load drop: card index, position (m and fraction of stroke) and size (kN, fraction of range)."""
    pos, load = np.asarray(pos, dtype=float), np.asarray(load, dtype=float)
    n = len(pos)
    i1, i0 = int(np.argmax(pos)), int(np.argmin(pos))
    idx = (np.arange(i1, i1 + ((i0 - i1) % n) + 1)) % n
    if len(idx) < 4:
        return {"index": 0, "x_m": float(pos[0]), "x_frac": 0.0, "drop_kn": 0.0, "severity": 0.0}
    seg = load[idx]
    w = 3
    d = seg[w:] - seg[:-w]                       # load change over a 3-sample window
    j = int(np.argmin(d))
    k = int(idx[min(j + w, len(idx) - 1)])
    span = max(float(np.ptp(pos)), 1e-9)
    rng = max(float(np.ptp(load)), 1e-9)
    drop = float(-d[j])
    return {"index": k, "x_m": float(pos[k]), "x_frac": float((pos[k] - pos.min()) / span),
            "drop_kn": max(drop, 0.0) / 1000.0, "severity": float(max(drop, 0.0) / rng)}


# ---------------------------------------------------------------- network


def build_net():
    import torch.nn as nn

    class Net(nn.Module):
        def __init__(self):
            super().__init__()

            def blk(i, o, k, s):
                return nn.Sequential(nn.Conv1d(i, o, k, s, k // 2, bias=False), nn.BatchNorm1d(o), nn.ReLU())

            self.f = nn.Sequential(blk(N_CH, 32, 5, 1), blk(32, 48, 5, 2), blk(48, 64, 5, 1), blk(64, 96, 3, 2),
                                   blk(96, 128, 3, 1), blk(128, 160, 3, 2))
            self.head = nn.Sequential(nn.Linear(320, 96), nn.ReLU(), nn.Dropout(0.1), nn.Linear(96, NC))

        def forward(self, x):
            import torch

            h = self.f(x)
            return self.head(torch.cat([h.mean(-1), h.amax(-1)], dim=1))

    return Net()


def n_params(net) -> int:
    return int(sum(p.numel() for p in net.parameters()))


# ---------------------------------------------------------------- baseline: Fourier descriptors + kNN


def fourier_descriptors(pos, load, k: int = 16) -> np.ndarray:
    pos, load = np.atleast_2d(pos).astype(float), np.atleast_2d(load).astype(float)
    z = _norm(pos) + 1j * ((load - load.mean(1, keepdims=True)) / np.maximum(np.ptp(load, axis=1, keepdims=True), 1e-9))
    c = np.abs(np.fft.fft(z, axis=1))[:, 1: k + 1]
    c = c / np.maximum(c[:, :1], 1e-9)
    ptp = np.maximum(np.ptp(load, axis=1), 1.0)
    return np.concatenate([c, np.log10(ptp)[:, None], (np.abs(np.fft.fft(z, axis=1))[:, :1] > 0) * 0.0], axis=1)


# ---------------------------------------------------------------- perturbed ("hand-labelled-like") test set


def perturb_rows(pos: np.ndarray, load: np.ndarray, r: np.random.Generator, warp: float, gain: tuple[float, float],
                 nonlin: bool, ripple: bool) -> tuple[np.ndarray, np.ndarray]:
    """Shape perturbations: smooth cyclic time warp, position/load gain, optional position non-linearity and load ripple."""
    pos, load = pos.astype(np.float64).copy(), load.astype(np.float64).copy()
    t = np.linspace(0, 1, N_PTS, endpoint=False)
    xs = np.arange(N_PTS + 1)
    for i in range(len(pos)):
        a = r.uniform(-warp, warp)
        idx = ((t + a * np.sin(2 * np.pi * t + r.uniform(0, 6.28))) % 1.0) * N_PTS
        pos[i] = np.interp(idx, xs, np.append(pos[i], pos[i][0]))
        load[i] = np.interp(idx, xs, np.append(load[i], load[i][0]))
        pos[i] *= r.uniform(*gain)
        load[i] *= r.uniform(*gain)
        if nonlin:
            pos[i] += 0.03 * np.ptp(pos[i]) * np.sin(2 * np.pi * pos[i] / max(np.ptp(pos[i]), 1e-6))
        if ripple:
            load[i] += 0.03 * np.ptp(load[i]) * np.sin(2 * np.pi * (t * r.uniform(1, 3) + r.uniform(0, 1)))
    return pos, load


def perturbed_set(n: int, seed: int = 777) -> dict[str, np.ndarray]:
    """Independent draws with stronger/different perturbations than training applies (warp 6 %, gain 0.9-1.15,
    position non-linearity, load ripple): the stand-in for the hand-labelled shape-perturbed set (none exists)."""
    r = np.random.default_rng(seed)
    cards = synthesize_cards(n, r, noise=0.01)
    pos, load = perturb_rows(cards.surface_pos, cards.surface_load, r, 0.06, (0.9, 1.15), True, True)
    return {"surface_pos": pos.astype(np.float32), "surface_load": load.astype(np.float32),
            "spm": cards.params["spm"], "label_idx": cards.labels}


# ---------------------------------------------------------------- inference


class DynoClassifier:
    def __init__(self, session, temperature: float, meta: dict):
        self.sess, self.T, self.meta = session, float(temperature), meta

    @classmethod
    def load(cls, d: Path) -> DynoClassifier:
        import onnxruntime as ort

        d = Path(d)
        meta = json.loads((d / "meta.json").read_text())
        so = ort.SessionOptions()
        so.intra_op_num_threads = 1
        return cls(ort.InferenceSession(str(d / "model.onnx"), so, providers=["CPUExecutionProvider"]), meta["temperature"], meta)

    def logits(self, x: np.ndarray) -> np.ndarray:
        return self.sess.run(None, {"card": x.astype(np.float32)})[0]

    def probs(self, x: np.ndarray) -> np.ndarray:
        z = self.logits(x) / self.T
        z -= z.max(axis=1, keepdims=True)
        e = np.exp(z)
        return e / e.sum(axis=1, keepdims=True)

    def classify(self, pos, load, spm: float) -> dict:
        x = prepare(np.asarray(pos)[None], np.asarray(load)[None], spm)
        p = self.probs(x)[0]
        k = int(p.argmax())
        return {"cls": DYNO_CLASSES[k], "conf": float(p[k]), "probs": {c: float(v) for c, v in zip(DYNO_CLASSES, p, strict=True)},
                "impact": impact_index(pos, load), "model": ID, "version": self.meta["version"], "source": self.meta["source"]}

    def classify_batch(self, pos, load, spm) -> tuple[np.ndarray, np.ndarray]:
        p = self.probs(prepare(pos, load, spm))
        return p.argmax(1), p.max(1)


# ---------------------------------------------------------------- training


def _macro_f1(y, p) -> float:
    from sklearn.metrics import f1_score

    return float(f1_score(y, p, average="macro"))


def train(out_dir: Path, quick: bool = False) -> dict:
    import torch
    import torch.nn.functional as fn

    torch.manual_seed(common.SEED)
    torch.set_num_threads(int(os.environ.get("MANTLE_TORCH_THREADS", "1")))   # >1 only in the isolated trainer subprocess
    if quick:
        data.ensure_small_data()
    with common.timer() as tm:
        n_train, n_test, epochs = (3000, 600, 4) if quick else (60_000, 12_000, 12)
        c = data.read_cards(n_train + n_test, seed=1)
        n_have = len(c["label_idx"])
        if n_have < n_train + n_test:                       # small data set: keep an 80/20 split
            n_test = n_have // 5
            n_train = n_have - n_test
        Xall = prepare(c["surface_pos"], c["surface_load"], c["spm"])
        y = c["label_idx"].astype(np.int64)
        Xtr, ytr, Xte, yte = Xall[:n_train], y[:n_train], Xall[n_train: n_train + n_test], y[n_train: n_train + n_test]
        n_val = max(200, n_train // 10)
        raw_pos, raw_load, raw_spm = c["surface_pos"][n_val:n_train], c["surface_load"][n_val:n_train], c["spm"][n_val:n_train]
        Xva, yva, Xtr, ytr = Xtr[:n_val], ytr[:n_val], Xtr[n_val:], ytr[n_val:]
        prng = np.random.default_rng(3)
        # baseline
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.preprocessing import StandardScaler

        nb = min(len(Xtr), 20_000)
        fd_tr = fourier_descriptors(c["surface_pos"][n_val: n_val + nb], c["surface_load"][n_val: n_val + nb])
        sc = StandardScaler().fit(fd_tr)
        knn = KNeighborsClassifier(5).fit(sc.transform(fd_tr), y[n_val: n_val + nb])
        fd_te = fourier_descriptors(c["surface_pos"][n_train: n_train + n_test], c["surface_load"][n_train: n_train + n_test])
        f1_knn = _macro_f1(yte, knn.predict(sc.transform(fd_te)))
        # CNN
        net = build_net()
        opt = torch.optim.AdamW(net.parameters(), 2e-3, weight_decay=1e-4)
        bs = 64 if quick else 256
        steps = epochs * int(np.ceil(len(Xtr) / bs))
        sched = torch.optim.lr_scheduler.OneCycleLR(opt, 4e-3, total_steps=steps)
        Xt, yt = torch.from_numpy(Xtr), torch.from_numpy(ytr)
        g = torch.Generator().manual_seed(0)
        for _ep in range(epochs):
            net.train()
            perm = torch.randperm(len(Xt), generator=g)
            for i in range(0, len(Xt), bs):
                idx = perm[i: i + bs]
                xb = Xt[idx].clone()
                k = int(len(idx) * 0.4)               # 40 % of each batch: on-the-fly shape perturbation, recomputed downhole
                if k:
                    sel = idx[:k].numpy()
                    pp, ll = perturb_rows(raw_pos[sel], raw_load[sel], prng, 0.04, (0.92, 1.1), False, False)
                    xb[:k] = torch.from_numpy(prepare(pp, ll, raw_spm[sel]))
                xb[:, :4] += 0.01 * torch.randn_like(xb[:, :4])           # on-the-fly noise
                xb[:, :4] *= 1 + 0.03 * (torch.rand(len(xb), 1, 1) - 0.5)   # gain jitter
                loss = fn.cross_entropy(net(xb), yt[idx], label_smoothing=0.05)
                opt.zero_grad()
                loss.backward()
                opt.step()
                sched.step()
        net.eval()

        def logits_of(X):
            with torch.no_grad():
                return torch.cat([net(torch.from_numpy(X[i: i + 2048])) for i in range(0, len(X), 2048)]).numpy()

        # temperature scaling on the validation split
        zv = torch.from_numpy(logits_of(Xva))
        logT = torch.zeros(1, requires_grad=True)
        o = torch.optim.LBFGS([logT], lr=0.1, max_iter=60)

        def closure():
            o.zero_grad()
            l = fn.cross_entropy(zv / logT.exp(), torch.from_numpy(yva))
            l.backward()
            return l

        o.step(closure)
        temp = float(logT.exp().item())
        zt = logits_of(Xte)
        pt = np.exp((zt - zt.max(1, keepdims=True)) / temp)
        pt /= pt.sum(1, keepdims=True)
        ece = _ece(pt, yte)
        f1_cnn = _macro_f1(yte, zt.argmax(1))
        pert = perturbed_set(400 if quick else 3000)
        Xp = prepare(pert["surface_pos"], pert["surface_load"], pert["spm"])
        f1_pert = _macro_f1(pert["label_idx"], logits_of(Xp).argmax(1))
        fd_p = fourier_descriptors(pert["surface_pos"], pert["surface_load"])
        f1_pert_knn = _macro_f1(pert["label_idx"], knn.predict(sc.transform(fd_p)))
    # save
    d = common.model_dir(ID, out_dir)
    torch.save(net.state_dict(), d / "model.pt")
    dummy = torch.zeros(2, N_CH, N_PTS)
    torch.onnx.export(net, (dummy,), str(d / "model.onnx"), input_names=["card"], output_names=["logits"],
                      dynamic_axes={"card": {0: "batch"}, "logits": {0: "batch"}}, opset_version=17, dynamo=False)
    meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "temperature": temp,
            "classes": list(DYNO_CLASSES), "params": n_params(net), "trained_at": common.now_iso(),
            "n_train": int(len(Xtr)), "epochs": epochs, "data_hash": common.data_hash([Xtr[:200]])}
    (d / "meta.json").write_text(json.dumps(meta))
    met = {"macro_f1_cnn": f1_cnn, "macro_f1_fourier_knn": f1_knn, "macro_f1_perturbed_cnn": f1_pert,
           "macro_f1_perturbed_fourier_knn": f1_pert_knn, "ece_after_temperature": ece, "temperature": temp,
           "params": n_params(net), "n_train": int(len(Xtr)), "n_test": int(len(Xte)), "epochs": epochs}
    ev = {"metrics": met, "primary": {"name": "macro_f1_synthetic_test", "value": f1_cnn, "target": 0.95,
                                     "baseline_name": "fourier_knn", "baseline": f1_knn, "direction": "higher",
                                     "secondary": {"name": "macro_f1_perturbed", "value": f1_pert, "target": 0.90,
                                                   "baseline": f1_pert_knn}},
          "train_seconds": tm["seconds"], "source": "physics_synthetic", "version": meta["version"],
          "data_hash": meta["data_hash"], "quick": quick}
    card = f"""# M3 dyno card classifier
1-D CNN, {n_params(net):,} parameters, 12 classes, temperature-scaled (T={temp:.2f}), exported to ONNX (`model.onnx`).
**Source: physics_synthetic** (S4 cards from the Gibbs wave-equation synthesiser, {len(Xtr):,} training cards, {epochs} epochs on CPU).
No real dynamometer cards were available; the test sets are also synthetic, so scores measure separability of the generator's classes.
- Input: 8 x 128 (surface pos/load, computed downhole pos/load with default damping 0.1, log load range, mean/range, position range, spm).
- Metrics: {json.dumps(met)}. "Perturbed" = independent draws with time warp, position non-linearity, load ripple and gain the training set never saw (stand-in for the hand-labelled set, which does not exist).
- Baseline: 16 Fourier-descriptor magnitudes + log load range, 5-NN (20k cards).
- Impact index: `impact_index(pos, load)` = steepest 3-sample downstroke load drop (index, x, drop kN, severity) used by M5.
- Limits: classes are physics-generated and idealised; real cards with unmodelled faults will be over-confident despite temperature scaling.
"""
    return common.write_eval(d, ID, ev, card)


def _ece(p: np.ndarray, y: np.ndarray, bins: int = 15) -> float:
    conf, pred = p.max(1), p.argmax(1)
    acc = (pred == y).astype(float)
    e = 0.0
    edges = np.linspace(0, 1, bins + 1)
    for lo, hi in zip(edges[:-1], edges[1:], strict=True):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            e += m.mean() * abs(acc[m].mean() - conf[m].mean())
    return float(e)
