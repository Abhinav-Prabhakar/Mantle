"""M6 streaming anomaly detector: shared per-channel LSTM autoencoder + IsolationForest ensemble on 1-minute steps.

* Input: per-minute channel values (3W: tubing/annulus/choke pressure and temperatures; S3: load mean/std, amps, THP,
  CHP, flowline T). Each channel is z-scored against a baseline (first minutes of the stream, or a supplied one) and
  the last 24 minutes form a window.
* The LSTM autoencoder is univariate and channel-agnostic, so weights **pre-trained on real Petrobras 3W** normal
  windows transfer and are **fine-tuned on S3** normal windows. An IsolationForest on window summary features is
  fitted per data set. Score = mean of three percentile-of-normal scores (AE error, IsolationForest, max |z| of the 3-sigma rule).
* Event detection: flagged runs (>= 3 consecutive minutes above a threshold picked on a validation split) merged when
  closer than 5 minutes. Event F1 counts a predicted event as TP if it overlaps a labelled event.
* Baseline: 3-sigma rule (any channel |z| > 3 for 3 consecutive minutes).
* Event type (S3 labels) from a LightGBM on per-channel errors and window features.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
from sklearn.ensemble import IsolationForest

from .. import common, data

ID = "M6"
L = 24
CH_3W = ["p_tpt", "p_mon_ckp", "p_anular", "t_tpt", "t_jus_ckp"]
CH_S3 = ["load_mean", "load_std", "amps", "thp", "chp", "flow_t"]
S3_LABELS = ["normal", "pump_off", "gas_lock", "load_cell_fault", "tubing_leak_onset", "vfd_trip"]
GAP, MIN_RUN = 5, 3


# ---------------------------------------------------------------- normalisation and windows


def zscore(x: np.ndarray, n_base: int, base: tuple[np.ndarray, np.ndarray] | None = None):
    """x (T,C) -> z (T,C) with NaN->0, mask (T,C), and the (median, scale) used."""
    if base is None:
        seg = x[:n_base]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            med = np.nanmedian(seg, axis=0)
            sd = np.nanstd(seg, axis=0)
        med = np.where(np.isfinite(med), med, 0.0)
        sc = np.maximum(np.where(np.isfinite(sd), sd, 0.0), 1e-3 * np.abs(med) + 1e-6)
    else:
        med, sc = base
    z = (x - med) / sc
    mask = np.isfinite(z)
    return np.clip(np.where(mask, z, 0.0), -20, 20).astype(np.float32), mask, (med, sc)


def windows(z: np.ndarray) -> np.ndarray:
    """(T,C) -> (T-L+1, C, L) sliding windows (window i ends at step i+L-1)."""
    return sliding_window_view(z, L, axis=0).astype(np.float32)


def window_features(w: np.ndarray, mask_last: np.ndarray) -> np.ndarray:
    """Summary features per window and channel: last-6 mean, std, slope, max |z|; masked channels -> 0."""
    m6 = w[:, :, -6:].mean(-1)
    sd = w.std(-1)
    x = np.arange(L, dtype=np.float32) - (L - 1) / 2
    slope = (w * x).sum(-1) / (x**2).sum()
    mx = np.abs(w).max(-1)
    f = np.stack([m6, sd, slope, mx], axis=-1) * mask_last[..., None]
    return f.reshape(len(w), -1)


# ---------------------------------------------------------------- LSTM autoencoder


def build_ae(hidden: int = 16):
    import torch
    import torch.nn as nn

    class AE(nn.Module):
        def __init__(self):
            super().__init__()
            self.enc = nn.LSTM(1, hidden, batch_first=True)
            self.dec = nn.LSTM(hidden, hidden, batch_first=True)
            self.out = nn.Linear(hidden, 1)

        def forward(self, x):                       # x (B, L)
            _, (h, _) = self.enc(x.unsqueeze(-1))
            d, _ = self.dec(h[-1].unsqueeze(1).expand(-1, x.shape[1], -1).contiguous())
            return self.out(d).squeeze(-1)

    del torch
    return AE()


class OnnxAE:
    """The LSTM autoencoder served with onnxruntime (the API process never imports torch)."""

    def __init__(self, path: Path):
        import onnxruntime as ort

        so = ort.SessionOptions()
        so.intra_op_num_threads = 1
        self.sess = ort.InferenceSession(str(path), so, providers=["CPUExecutionProvider"])

    def errors(self, flat: np.ndarray, bs: int = 8192) -> np.ndarray:
        out = np.empty(len(flat), dtype=np.float32)
        for i in range(0, len(flat), bs):
            x = np.ascontiguousarray(flat[i: i + bs], dtype=np.float32)
            out[i: i + bs] = ((self.sess.run(None, {"x": x})[0] - x) ** 2).mean(1)
        return out


def export_onnx(net, path: Path) -> Path:
    """Export the AE (input ``x`` (B, L), dynamic batch) so serving does not need torch."""
    import torch

    net.eval()
    torch.onnx.export(net, (torch.zeros(4, L),), str(path), input_names=["x"], output_names=["y"],
                      dynamic_axes={"x": {0: "batch"}, "y": {0: "batch"}}, dynamo=False)
    return Path(path)


def ae_errors(net, w: np.ndarray, bs: int = 8192) -> np.ndarray:
    """w (N,C,L) -> per-channel reconstruction MSE (N,C)."""
    N, C, _ = w.shape
    if isinstance(net, OnnxAE):
        return net.errors(w.reshape(N * C, L), bs).reshape(N, C)
    import torch

    flat = torch.from_numpy(w.reshape(N * C, L))
    out = np.empty(N * C, dtype=np.float32)
    net.eval()
    with torch.no_grad():
        for i in range(0, len(flat), bs):
            x = flat[i: i + bs]
            out[i: i + bs] = ((net(x) - x) ** 2).mean(1).numpy()
    return out.reshape(N, C)


def train_ae(net, w_flat: np.ndarray, epochs: int, lr: float = 3e-3, seed: int = 0) -> None:
    import torch

    torch.manual_seed(seed)
    opt = torch.optim.Adam(net.parameters(), lr)
    X = torch.from_numpy(w_flat)
    bs = 512
    for _ in range(epochs):
        net.train()
        perm = torch.randperm(len(X))
        for i in range(0, len(X), bs):
            x = X[perm[i: i + bs]]
            loss = ((net(x) - x) ** 2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()


def agg_err(err: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Mean of the two largest channel errors among available channels."""
    e = np.where(mask, err, 0.0)
    top = np.sort(e, axis=1)[:, -2:]
    return top.mean(1)


# ---------------------------------------------------------------- score calibration


class Quantile:
    """Maps a raw score to its percentile among normal training scores (>1 = beyond every normal one)."""

    def __init__(self, ref: np.ndarray):
        self.q = np.quantile(ref, np.linspace(0, 1, 1001))

    def __call__(self, v):
        v = np.asarray(v, dtype=float)
        lo = np.interp(v, self.q, np.linspace(0, 1, 1001))
        top = self.q[-1]
        extra = np.where(v > top, np.log10(np.maximum(v, 1e-12) / max(top, 1e-12)), 0.0)
        return lo + extra


# ---------------------------------------------------------------- events and metrics


def runs(flag: np.ndarray) -> list[tuple[int, int]]:
    out, i, n = [], 0, len(flag)
    while i < n:
        if flag[i]:
            j = i
            while j + 1 < n and flag[j + 1]:
                j += 1
            out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out


def predicted_events(score: np.ndarray, thr: float, valid: np.ndarray | None = None) -> list[tuple[int, int]]:
    flag = score > thr
    if valid is not None:
        flag = flag & valid
    ev = [r for r in runs(flag) if r[1] - r[0] + 1 >= MIN_RUN]
    merged: list[list[int]] = []
    for a, b in ev:
        if merged and a - merged[-1][1] <= GAP:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    return [(a, b) for a, b in merged]


def event_counts(pred: list[tuple[int, int]], gt: list[tuple[int, int]]) -> tuple[int, int, int]:
    def ov(a, b):
        return a[0] <= b[1] and b[0] <= a[1]

    tp_pred = sum(any(ov(p, g) for g in gt) for p in pred)
    fn = sum(not any(ov(p, g) for p in pred) for g in gt)
    return tp_pred, len(pred) - tp_pred, fn


def f1_from(tp: int, fp: int, fn: int) -> float:
    return 2 * tp / max(2 * tp + fp + fn, 1)


# ---------------------------------------------------------------- data sets


class Stream:
    """One evaluated stream: z, mask, per-step label (0 normal), optional type label, valid-from step."""

    def __init__(self, sid: str, z: np.ndarray, mask: np.ndarray, y: np.ndarray, start: int, group: str, klass: int = 0,
                 ytype: np.ndarray | None = None):
        self.sid, self.z, self.mask, self.y, self.start, self.group, self.klass, self.ytype = sid, z, mask, y, start, group, klass, ytype


def load_3w(quick: bool) -> list[Stream]:
    p = data.threew_sample_path()
    if not p.exists():
        return []
    df = pd.read_parquet(p, columns=["timestamp", "instance_id", "class", "event_class", "origin", *CH_3W])
    out = []
    for iid, g in df.groupby("instance_id", sort=True):
        g = g.sort_values("timestamp")
        x = g[CH_3W].to_numpy(dtype=np.float64)
        if len(x) < 60 or np.isfinite(x).sum() == 0:
            continue
        cl = g["class"].to_numpy()
        y = np.where(pd.isna(g["class"]), 0, (np.nan_to_num(cl.astype(float), nan=0) != 0)).astype(np.int8)
        z, mask, _ = zscore(x, 30)
        group = str(iid).split("_")[0] if str(iid).startswith("WELL") else str(iid)
        out.append(Stream(str(iid), z, mask, y, 30, group, int(g["event_class"].iloc[0])))
    if quick:
        out = out[:: max(1, len(out) // 60)]
    return out


def load_s3(quick: bool) -> list[Stream]:
    ev = data.events()
    out = []
    wells = data.telemetry_wells()
    if quick:
        wells = wells[:2]
    nb = 120 if quick else 1440
    cols = ["ts", "load_kn", "amps", "thp_mpa", "chp_mpa", "flowline_t_c"]
    for w in wells:
        t = pd.read_parquet(data.telemetry_path(w), columns=cols)
        n = len(t) // 60 * 60
        a = {c: t[c].to_numpy(dtype=np.float64)[:n].reshape(-1, 60) for c in cols[1:]}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x = np.stack([np.nanmean(a["load_kn"], 1), np.nanstd(a["load_kn"], 1), np.nanmean(a["amps"], 1),
                          np.nanmean(a["thp_mpa"], 1), np.nanmean(a["chp_mpa"], 1), np.nanmean(a["flowline_t_c"], 1)], 1)
        t0 = t["ts"].iloc[0]
        yt = np.zeros(len(x), dtype=np.int8)
        ytype = np.zeros(len(x), dtype=np.int8)
        for r in ev[ev.well_id == w].itertuples():
            a0 = int((pd.Timestamp(r.start_ts) - t0).total_seconds() // 60)
            a1 = int((pd.Timestamp(r.end_ts) - t0).total_seconds() // 60)
            yt[max(a0, 0): a1 + 1] = 1
            ytype[max(a0, 0): a1 + 1] = S3_LABELS.index(r.label)
        z, mask, _ = zscore(x, nb)
        out.append(Stream(w, z, mask, yt, nb, w, 0, ytype))
    return out


def stream_windows(s: Stream) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """windows (N,C,L), mask at window end (N,C), step index of the window end (N,)."""
    w = windows(s.z)
    m = s.mask[L - 1:]
    idx = np.arange(L - 1, len(s.z))
    return w, m, idx


def normal_windows(streams: list[Stream], cap: int, rng: np.random.Generator) -> np.ndarray:
    """Univariate normal windows (n,L) pooled over channels from steps after the baseline with all-normal labels."""
    pool = []
    for s in streams:
        w, m, idx = stream_windows(s)
        ok = idx >= s.start
        lab = np.lib.stride_tricks.sliding_window_view(s.y, L).max(1)
        ok &= lab == 0
        for c in range(w.shape[1]):
            sel = ok & m[:, c]
            if sel.any():
                pool.append(w[sel, c, :][:: 3])
    if not pool:
        return np.zeros((0, L), dtype=np.float32)
    X = np.concatenate(pool)
    if len(X) > cap:
        X = X[rng.choice(len(X), cap, replace=False)]
    return X


class Scorer:
    """AE + IsolationForest scorer for one data set (channel set)."""

    def __init__(self, net, iforest: IsolationForest, qa: Quantile, qi: Quantile, qz: Quantile, n_ch: int):
        self.net, self.iforest, self.qa, self.qi, self.qz, self.n_ch = net, iforest, qa, qi, qz, n_ch

    def raw(self, w: np.ndarray, m: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        err = ae_errors(self.net, w)
        a = agg_err(err, m)
        f = window_features(w, m)
        i = -self.iforest.score_samples(f)
        z = np.where(m, np.abs(w[:, :, -3:].mean(-1)), 0.0).max(1)      # the 3-sigma statistic (max |z| over channels)
        return a, i, z, err

    def score(self, w: np.ndarray, m: np.ndarray) -> dict[str, np.ndarray]:
        a, i, z, err = self.raw(w, m)
        sa, si, sz = self.qa(a), self.qi(i), self.qz(z)
        return {"ae": sa, "if": si, "z": sz, "ens": (sa + si + sz) / 3, "err": err}


def fit_scorer(net, streams: list[Stream], n_ch: int, cap: int, rng: np.random.Generator, trees: int) -> Scorer:
    W: list = []
    M: list = []
    for s in streams:
        w, m, idx = stream_windows(s)
        lab = np.lib.stride_tricks.sliding_window_view(s.y, L).max(1)
        ok = (idx >= s.start) & (lab == 0)
        W.append(w[ok][:: 2])
        M.append(m[ok][:: 2])
    w, m = np.concatenate(W), np.concatenate(M)
    if len(w) > cap:
        k = rng.choice(len(w), cap, replace=False)
        w, m = w[k], m[k]
    err = ae_errors(net, w)
    a = agg_err(err, m)
    f = window_features(w, m)
    iso = IsolationForest(n_estimators=trees, contamination="auto", random_state=0, n_jobs=4).fit(f)
    i = -iso.score_samples(f)
    z = np.where(m, np.abs(w[:, :, -3:].mean(-1)), 0.0).max(1)
    return Scorer(net, iso, Quantile(a), Quantile(i), Quantile(z), n_ch)


def evaluate_streams(sc: Scorer, streams: list[Stream], thr: dict[str, float] | None, grid: np.ndarray | None = None) -> dict:
    """Per-stream scores; if ``thr`` is None returns a threshold grid search result on these streams."""
    scores = {}
    for s in streams:
        w, m, idx = stream_windows(s)
        d = sc.score(w, m)
        full = {k: np.full(len(s.z), -1.0) for k in ("ae", "if", "z", "ens")}
        for k in full:
            full[k][idx] = d[k]
        scores[s.sid] = full
    return scores


def event_f1_for(streams: list[Stream], scores: dict, key: str, thr: float) -> tuple[float, tuple[int, int, int]]:
    tp = fp = fn = 0
    for s in streams:
        sc = scores[s.sid][key]
        valid = np.arange(len(sc)) >= max(s.start, L - 1)
        pred = predicted_events(sc, thr, valid)
        gt = [r for r in runs(s.y.astype(bool)) if r[1] >= s.start]
        a, b, c = event_counts(pred, gt)
        tp, fp, fn = tp + a, fp + b, fn + c
    # gt events counted via tp on the predicted side; recompute FN-adjusted F1
    return f1_from(tp, fp, fn), (tp, fp, fn)


def best_threshold(streams: list[Stream], scores: dict, key: str) -> float:
    allv = np.concatenate([scores[s.sid][key][max(s.start, L - 1):] for s in streams])
    grid = np.unique(np.quantile(allv, np.linspace(0.5, 0.9995, 60)))
    best, bt = -1.0, float(grid[-1])
    for t in grid:
        f, _ = event_f1_for(streams, scores, key, float(t))
        if f > best:
            best, bt = f, float(t)
    return bt


def three_sigma_scores(streams: list[Stream]) -> dict:
    out = {}
    for s in streams:
        zmax = np.where(s.mask, np.abs(s.z), 0).max(1)
        out[s.sid] = {"3sig": zmax}
    return out


def split_groups(streams: list[Stream], seed: int, test_frac: float = 0.3, val_frac: float = 0.2):
    groups = sorted({s.group for s in streams})
    if len(groups) < 4:          # tiny (quick/test) data: no honest split possible, reuse everything
        return streams, streams, streams
    r = np.random.default_rng(seed)
    r.shuffle(groups)
    n_te = max(1, int(len(groups) * test_frac))
    n_va = max(1, int(len(groups) * val_frac))
    te, va, tr = set(groups[:n_te]), set(groups[n_te: n_te + n_va]), set(groups[n_te + n_va:])
    return ([s for s in streams if s.group in tr], [s for s in streams if s.group in va], [s for s in streams if s.group in te])


# ---------------------------------------------------------------- serving


class AnomalyDetector:
    """Loads the S3-fine-tuned scorer (live channels) and the event-type classifier."""

    def __init__(self, scorer: Scorer, thr: float, typer, meta: dict):
        self.scorer, self.thr, self.typer, self.meta = scorer, thr, typer, meta

    @classmethod
    def load(cls, d: Path) -> AnomalyDetector:
        d = Path(d)
        meta = json.loads((d / "meta.json").read_text())
        if (d / "ae_s3.onnx").exists():                 # serving path: no torch
            net: Any = OnnxAE(d / "ae_s3.onnx")
        else:
            import torch

            net = build_ae(meta["hidden"])
            net.load_state_dict(torch.load(d / "ae_s3.pt"))
            net.eval()
        z = joblib.load(d / "scorer_s3.joblib")
        sc = Scorer(net, z["iforest"], z["qa"], z["qi"], z["qz"], len(CH_S3))
        return cls(sc, meta["thr_s3"], joblib.load(d / "typer_s3.joblib"), meta)

    def score_series(self, x: np.ndarray, base: tuple[np.ndarray, np.ndarray] | None = None, n_base: int = 120) -> dict:
        """x (T, 6) per-minute [load_mean, load_std, amps, thp, chp, flow_t] -> per-step score/flag/type arrays."""
        z, mask, base_used = zscore(np.asarray(x, dtype=np.float64), n_base, base)
        T = len(z)
        score = np.full(T, np.nan)
        typ = np.zeros(T, dtype=int)
        if T >= L:
            w = windows(z)
            m = mask[L - 1:]
            d = self.scorer.score(w, m)
            score[L - 1:] = d[self.meta.get("score_key", "ens")]
            feat = np.concatenate([d["err"], window_features(w, m)], axis=1)
            typ[L - 1:] = self.typer.predict(feat)
        flag = np.nan_to_num(score, nan=-1) > self.thr
        return {"score": score, "flag": flag, "type": [S3_LABELS[i] for i in typ], "threshold": self.thr,
                "baseline": base_used, "model": ID, "version": self.meta["version"], "source": self.meta["source"]}


# ---------------------------------------------------------------- training


def train(out_dir: Path, quick: bool = False) -> dict:
    import torch

    torch.set_num_threads(1)     # single-threaded: torch and lightgbm/sklearn OpenMP runtimes must not run in parallel together
    rng = np.random.default_rng(common.SEED)
    if quick:
        data.ensure_small_data()
    with common.timer() as tm:
        hid = 16
        ep3, epf = (1, 1) if quick else (6, 5)
        cap = 4000 if quick else 60_000
        trees = 30 if quick else 150
        notes: list[str] = []
        s3w = load_3w(quick)
        met: dict = {}
        net = build_ae(hid)
        if s3w:
            tr, va, te = split_groups(s3w, 0)
            train_ae(net, normal_windows(tr, cap, rng), ep3)
            sc3 = fit_scorer(net, tr, len(CH_3W), cap, rng, trees)
            sv, st = evaluate_streams(sc3, va, None), evaluate_streams(sc3, te, None)
            thr3 = {k: best_threshold(va, sv, k) for k in ("ae", "if", "z", "ens")}
            for k in ("ae", "if", "z", "ens"):
                met[f"f1_3w_{k}"] = event_f1_for(te, st, k, thr3[k])[0]
            cnt = event_f1_for(te, st, "ens", thr3["ens"])[1]
            met["counts_3w_ens_tp_fp_fn"] = list(cnt)
            real = [s for s in te if s.group.startswith("WELL")]
            if real:
                met["f1_3w_ens_real_only"] = event_f1_for(real, st, "ens", thr3["ens"])[0]
            ts, vs3 = three_sigma_scores(te), three_sigma_scores(va)
            t3 = best_threshold(va, vs3, "3sig") if False else 3.0
            met["f1_3w_3sigma"] = event_f1_for(te, ts, "3sig", t3)[0]
            met["n_3w_test_streams"], met["n_3w_test_events"] = len(te), int(sum(len(runs(s.y.astype(bool))) for s in te))
            torch.save(net.state_dict(), common.model_dir(ID, out_dir) / "ae_3w.pt")
        else:
            notes.append("3W sample not found: pre-training skipped")
        # ---- S3 fine-tune
        s3 = load_s3(quick)
        tr, va, te = split_groups(s3, 1, test_frac=0.3, val_frac=0.2)
        net_ft = build_ae(hid)
        if s3w:
            net_ft.load_state_dict(net.state_dict())
        train_ae(net_ft, normal_windows(tr, cap, rng), epf, lr=1e-3)
        scs = fit_scorer(net_ft, tr, len(CH_S3), cap, rng, trees)
        sv, st = evaluate_streams(scs, va, None), evaluate_streams(scs, te, None)
        thr = {k: best_threshold(va, sv, k) for k in ("ae", "if", "z", "ens")}
        val_f1 = {k: event_f1_for(va, sv, k, thr[k])[0] for k in thr}
        key = max(("ens", "ae", "if"), key=lambda k: val_f1[k])       # deployed scorer picked on the validation wells
        for k in ("ae", "if", "z", "ens"):
            met[f"f1_s3_{k}"] = event_f1_for(te, st, k, thr[k])[0]
        met["counts_s3_ens_tp_fp_fn"] = list(event_f1_for(te, st, "ens", thr["ens"])[1])
        met["s3_deployed_score"] = key
        met["f1_s3_deployed"] = event_f1_for(te, st, key, thr[key])[0]
        met["f1_s3_3sigma"] = event_f1_for(te, three_sigma_scores(te), "3sig", 3.0)[0]
        if s3w:                                  # pre-trained-only AE (no fine-tune) for comparison
            sc0 = fit_scorer(net, tr, len(CH_S3), cap, rng, trees)
            s0v, s0t = evaluate_streams(sc0, va, None), evaluate_streams(sc0, te, None)
            th0 = best_threshold(va, s0v, "ens")
            met["f1_s3_ens_pretrained_only"] = event_f1_for(te, s0t, "ens", th0)[0]
        met["n_s3_test_wells"] = len(te)
        # ---- event typing (S3): fit on train wells, report on test wells at flagged-in-event steps
        def feats(sc: Scorer, streams: list[Stream]):
            X, Y = [], []
            for s in streams:
                w, m, idx = stream_windows(s)
                d = sc.score(w, m)
                ok = idx >= s.start
                X.append(np.concatenate([d["err"], window_features(w, m)], axis=1)[ok])
                Y.append(np.asarray(s.ytype)[idx][ok])
            return np.concatenate(X), np.concatenate(Y)

        Xtr, Ytr = feats(scs, tr)
        Xte, Yte = feats(scs, te)
        cls_ = np.unique(Ytr)
        typer = lgb.LGBMClassifier(n_estimators=40 if quick else 120, learning_rate=0.08, num_leaves=15, min_child_samples=10,
                                   class_weight="balanced", verbose=-1, random_state=0, n_jobs=4).fit(Xtr, Ytr)
        pred = typer.predict(Xte)
        anom = Yte != 0
        met["type_accuracy_on_event_steps"] = float(np.mean(pred[anom] == Yte[anom])) if anom.any() else None
        met["type_classes_seen"] = [S3_LABELS[i] for i in cls_]
    d = common.model_dir(ID, out_dir)
    torch.save(net_ft.state_dict(), d / "ae_s3.pt")
    export_onnx(net_ft, d / "ae_s3.onnx")
    joblib.dump({"iforest": scs.iforest, "qa": scs.qa, "qi": scs.qi, "qz": scs.qz}, d / "scorer_s3.joblib", compress=3)
    joblib.dump(typer, d / "typer_s3.joblib", compress=3)
    meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "real+physics_synthetic", "hidden": hid,
            "thr_s3": thr[key], "score_key": key, "channels_s3": CH_S3, "channels_3w": CH_3W, "window": L,
            "trained_at": common.now_iso(), "data_hash": common.data_hash([str(len(s3w)), str(len(s3)), str(cap)])}
    (d / "meta.json").write_text(json.dumps(meta))
    f13 = met.get("f1_3w_ens")
    ev = {"metrics": met, "primary": {"name": "event_f1_3w_test", "value": f13, "target": 0.8,
                                     "baseline_name": "3-sigma", "baseline": met.get("f1_3w_3sigma"), "direction": "higher",
                                     "secondary": {"name": "event_f1_s3_test", "value": met["f1_s3_deployed"], "baseline": met["f1_s3_3sigma"]}},
          "notes": notes, "train_seconds": tm["seconds"], "source": "real (3W pre-train/validation) + physics_synthetic (S3 fine-tune)",
          "version": meta["version"], "data_hash": meta["data_hash"], "quick": quick}
    card = f"""# M6 streaming anomaly detector
Shared per-channel LSTM autoencoder (hidden {hid}, window {L} min) + IsolationForest ensemble. **Sources: real Petrobras 3W v2.0.0 sample
(CC BY 4.0; used for pre-training and the held-out F1) and physics_synthetic S3 (fine-tuning + S3 F1).** 3W is reduced to 5 channels at one point per minute
(`threew_sample.parquet`, 361 instances of all classes incl. simulated/hand-drawn); the AE is channel-agnostic so 3W weights initialise the S3 model.
- Split by well group (3W: real instances grouped by well; simulated/drawn individually): train / validation (threshold) / test. Metrics: {json.dumps(met)}
- Event F1 = predicted-event overlap with labelled events (transients + faults are events). Baseline: any-channel |z|>3 for 3 min.
- Event typing for S3 labels via LightGBM on per-channel AE errors + window features.
- Limits: 3W channels differ from S3 (no load/amps in 3W), so transfer is through the univariate AE only; 3W faults are slow and many are subtle, which caps recall; baseline needs a warm-up (30 min for 3W, 24 h for S3; 2 h in quick mode).
"""
    return common.write_eval(d, ID, ev, card)
