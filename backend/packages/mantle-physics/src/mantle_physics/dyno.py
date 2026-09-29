"""Dynamometer cards: Gibbs wave-equation downhole card and a 12-class surface-card synthesiser.

Model
-----
The sucker-rod string is a damped, tapered 1-D elastic rod. With ``x`` measured downward from the polished
rod, ``p`` the rod position (up positive) and ``F`` the axial tension (``F = -EA * dp/dx``)::

    rho*A * p_tt = -dF/dx - c * p_t          (dynamic part; the static rod weight is handled separately)

For a periodic stroke the dynamic part is expanded in ``n_harm`` harmonics of the stroke frequency
(Gibbs 1963 truncates for stability). Each harmonic obeys a constant-coefficient ODE per rod section, so the
(position, load) pair at the top and bottom of a section are related by an exact 2x2 transfer matrix with
``gamma = sqrt((-rho*A*w^2 + i*w*c) / (E*A))``. Chaining sections handles the taper; ``c`` is the Gibbs
damping ``c = damping * rho*A * pi * a / L`` (``damping`` ~ 0.05..0.3).

``downhole_card`` inverts the chain (surface -> pump); ``surface_card_from_downhole`` runs it forward. A
finite-difference variant (``method="fd"``: Everitt-Jennings marching in depth with spectral time derivatives,
RK4) is provided as an independent check of the transfer-matrix implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from ._util import TAU
from .constants import G
from .rods import SECT

E_STEEL = 2.07e11

DYNO_CLASSES: tuple[str, ...] = (
    "normal",
    "fluid_pound",
    "gas_interference",
    "rod_float",
    "pump_off",
    "tubing_leak",
    "travelling_valve_leak",
    "standing_valve_leak",
    "unseated_pump",
    "parted_rods",
    "plunger_sticking",
    "excessive_friction",
)
CLASS_INDEX = {c: i for i, c in enumerate(DYNO_CLASSES)}


@dataclass(frozen=True)
class RodString:
    """Tapered rod string: per-section length (m), cross-section (m2) and weight in air (N/m)."""

    length: np.ndarray
    area: np.ndarray
    weight: np.ndarray
    E: float = E_STEEL
    _extra: dict = field(default_factory=dict, compare=False, repr=False)

    @classmethod
    def default(cls) -> RodString:
        return cls(
            np.array([s.bot - s.top for s in SECT], dtype=float),
            np.array([s.A * 1e-6 for s in SECT], dtype=float),
            np.array([s.w for s in SECT], dtype=float),
        )

    @property
    def total_length(self) -> float:
        return float(self.length.sum())

    @property
    def rho_a(self) -> np.ndarray:
        """Mass per unit length (kg/m)."""
        return self.weight / G

    @property
    def ea(self) -> np.ndarray:
        return self.E * self.area

    @property
    def wave_speed(self) -> np.ndarray:
        return np.sqrt(self.ea / self.rho_a)

    def air_weight(self) -> float:
        return float((self.weight * self.length).sum())

    def truncate(self, depth: float) -> RodString:
        """The part of the string above ``depth`` (m), e.g. above a parted rod."""
        cum = np.cumsum(self.length)
        keep, lens = [], []
        top = 0.0
        for i, bot in enumerate(cum):
            if depth <= top:
                break
            keep.append(i)
            lens.append(min(bot, depth) - top)
            top = bot
        idx = np.array(keep, dtype=int)
        return RodString(np.array(lens), self.area[idx], self.weight[idx], self.E)


def _transfer(omega: np.ndarray, rods: RodString, damping: float):
    """Top->bottom transfer entries (T11, T12, T21, T22) of the whole string, each shaped like ``omega``."""
    L_tot = rods.total_length
    damp = np.asarray(damping, dtype=float)
    if damp.ndim:
        damp = damp[:, None]
    T11 = np.ones_like(omega, dtype=complex)
    T12 = np.zeros_like(T11)
    T21 = np.zeros_like(T11)
    T22 = np.ones_like(T11)
    for L, ea, rho_a, a in zip(rods.length, rods.ea, rods.rho_a, rods.wave_speed, strict=True):
        c = damp * rho_a * np.pi * a / L_tot
        gamma = np.sqrt((-rho_a * omega**2 + 1j * omega * c) / ea)
        gl = gamma * L
        ch = np.cosh(gl)
        sh = np.sinh(gl)
        s12 = -sh / (gamma * ea)
        s21 = -ea * gamma * sh
        T11, T12, T21, T22 = (
            ch * T11 + s12 * T21,
            ch * T12 + s12 * T22,
            s21 * T11 + ch * T21,
            s21 * T12 + ch * T22,
        )
    return T11, T12, T21, T22


def _prep(pos, load, period, n_harm):
    pos = np.atleast_2d(np.asarray(pos, dtype=float))
    load = np.atleast_2d(np.asarray(load, dtype=float))
    n = pos.shape[-1]
    period = np.broadcast_to(np.asarray(period, dtype=float), pos.shape[:-1])
    K = min(int(n_harm), n // 2 - 1)
    k = np.arange(1, K + 1)
    omega = TAU * k[None, :] / period[:, None]
    return pos, load, n, K, omega


def _spec(x, K):
    return np.fft.rfft(x, axis=-1)[..., 1 : K + 1]


def _synth(spec, mean, n, K):
    full = np.zeros(spec.shape[:-1] + (n // 2 + 1,), dtype=complex)
    full[..., 1 : K + 1] = spec
    return np.fft.irfft(full, n=n, axis=-1) + mean[..., None]


def _buoyant_weight(rods: RodString, buoyancy: float) -> float:
    return rods.air_weight() * buoyancy


def downhole_card(
    surface_pos,
    surface_load,
    period_s,
    rods: RodString | None = None,
    damping: float = 0.1,
    n_harm: int = 24,
    buoyancy: float = 0.874,
    method: str = "spectral",
    fd_dx: float = 4.0,
):
    """Gibbs downhole (pump) card from a surface card sampled uniformly in time over one stroke.

    Parameters
    ----------
    surface_pos, surface_load : (..., n) polished-rod position (m) and load (N), one stroke, n samples.
    period_s : stroke period (s), scalar or (...,).
    Returns ``(pos, load)`` of the plunger with the same shape; position is shifted so its minimum is 0 and
    load is the absolute pump load (mean surface load minus the buoyant rod weight, plus the dynamics).
    """
    rods = rods or RodString.default()
    single = np.ndim(surface_pos) == 1
    pos, load, n, K, omega = _prep(surface_pos, surface_load, period_s, n_harm)
    P, F = _spec(pos, K), _spec(load, K)
    if method == "spectral":
        T11, T12, T21, T22 = _transfer(omega, rods, damping)
        Pb, Fb = T11 * P + T12 * F, T21 * P + T22 * F
    elif method == "fd":
        Pb, Fb = _march_fd(P, F, omega, rods, damping, fd_dx, n, K, down=True)
    else:
        raise ValueError(f"unknown method {method!r}")
    mean_load = load.mean(axis=-1) - _buoyant_weight(rods, buoyancy)
    dh_pos = _synth(Pb, np.zeros(pos.shape[:-1]), n, K)
    dh_pos -= dh_pos.min(axis=-1, keepdims=True)
    dh_load = _synth(Fb, mean_load, n, K)
    return (dh_pos[0], dh_load[0]) if single else (dh_pos, dh_load)


def surface_card_from_downhole(
    dh_pos,
    dh_load,
    period_s,
    rods: RodString | None = None,
    damping: float = 0.1,
    n_harm: int = 24,
    buoyancy: float = 0.874,
    method: str = "spectral",
    fd_dx: float = 4.0,
):
    """Forward wave-equation propagation: surface card produced by a known downhole card."""
    rods = rods or RodString.default()
    single = np.ndim(dh_pos) == 1
    pos, load, n, K, omega = _prep(dh_pos, dh_load, period_s, n_harm)
    P, F = _spec(pos, K), _spec(load, K)
    if method == "spectral":
        T11, T12, T21, T22 = _transfer(omega, rods, damping)
        Ps, Fs = T22 * P - T12 * F, -T21 * P + T11 * F      # inverse of a det-1 matrix
    elif method == "fd":
        Ps, Fs = _march_fd(P, F, omega, rods, damping, fd_dx, n, K, down=False)
    else:
        raise ValueError(f"unknown method {method!r}")
    mean_load = load.mean(axis=-1) + _buoyant_weight(rods, buoyancy)
    s_pos = _synth(Ps, np.zeros(pos.shape[:-1]), n, K)
    s_pos -= s_pos.min(axis=-1, keepdims=True)
    s_load = _synth(Fs, mean_load, n, K)
    return (s_pos[0], s_load[0]) if single else (s_pos, s_load)


def _march_fd(P, F, omega, rods, damping, dx, n, K, down):
    """Everitt-Jennings style marching in depth with RK4 and spectral (band-limited) time derivatives.

    d p/dx = -F/EA ;  dF/dx = -(rho*A p_tt + c p_t) ; harmonics k=1..K, so p_t = i w p, p_tt = -w^2 p.
    """
    L_tot = rods.total_length
    sign = 1.0 if down else -1.0
    Pk, Fk = P.copy(), F.copy()
    sections = list(zip(rods.length, rods.ea, rods.rho_a, rods.wave_speed, strict=True))
    if not down:
        sections = sections[::-1]
    for L, ea, rho_a, a in sections:
        c = damping * rho_a * np.pi * a / L_tot
        steps = max(1, int(np.ceil(L / dx)))
        h = sign * L / steps

        def rhs(p, f, ea=ea, rho_a=rho_a, c=c):
            return -f / ea, rho_a * omega**2 * p - 1j * omega * c * p

        for _ in range(steps):
            k1p, k1f = rhs(Pk, Fk)
            k2p, k2f = rhs(Pk + 0.5 * h * k1p, Fk + 0.5 * h * k1f)
            k3p, k3f = rhs(Pk + 0.5 * h * k2p, Fk + 0.5 * h * k2f)
            k4p, k4f = rhs(Pk + h * k3p, Fk + h * k3f)
            Pk = Pk + h / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
            Fk = Fk + h / 6 * (k1f + 2 * k2f + 2 * k3f + k4f)
    return Pk, Fk


# ---------------------------------------------------------------------------------------------- synthesiser


def _ss(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


@dataclass
class CardBatch:
    """Synthesised cards (time-uniform, one stroke, ``n_points`` samples) and their generating parameters."""

    labels: np.ndarray                 # (B,) int index into DYNO_CLASSES
    surface_pos: np.ndarray            # (B,n) m
    surface_load: np.ndarray           # (B,n) N
    dh_pos: np.ndarray                 # (B,n) m   true pump card (before band-limiting)
    dh_load: np.ndarray                # (B,n) N
    period_s: np.ndarray               # (B,)
    params: dict[str, np.ndarray]

    @property
    def class_names(self) -> list[str]:
        return [DYNO_CLASSES[i] for i in self.labels]


def sample_params(labels: np.ndarray, rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Draw physically plausible pump/fluid conditions for each requested class."""
    B = len(labels)
    u = lambda lo, hi: rng.uniform(lo, hi, B)  # noqa: E731
    plunger_in = u(1.0, 1.75)
    p = {
        "fluid_load": 7.8e3 * (plunger_in / 1.25) ** 2,
        "stroke": u(2.0, 3.2),
        "spm": u(2.0, 9.0),
        "kd": u(0.42, 0.68),
        "damping": u(0.06, 0.25),
        "stroke_ratio": u(0.86, 0.97),
        "edge_top": u(0.03, 0.07),
        "edge_bot": u(0.03, 0.07),
        "fillage": np.ones(B),
        "gas": np.zeros(B),
        "tubing_leak": np.zeros(B),
        "tv_leak": np.zeros(B),
        "sv_leak": np.zeros(B),
        "friction": u(0.0, 0.03),
        "float_ratio": np.ones(B),
        "unseated": np.zeros(B),
        "parted_depth": np.full(B, np.nan),
        "sand": np.zeros(B),
    }
    for cls, idx in CLASS_INDEX.items():
        m = labels == idx
        k = int(m.sum())
        if not k:
            continue
        r = lambda lo, hi, k=k: rng.uniform(lo, hi, k)  # noqa: E731
        if cls == "fluid_pound":
            p["fillage"][m] = r(0.5, 0.85)
        elif cls == "pump_off":
            p["fillage"][m] = r(0.08, 0.4)
        elif cls == "gas_interference":
            p["fillage"][m] = r(0.4, 0.75)
            p["gas"][m] = r(0.3, 0.55)
            p["edge_bot"][m] = r(0.15, 0.3)
        elif cls == "rod_float":
            p["float_ratio"][m] = r(0.55, 0.8)
            p["edge_bot"][m] = r(0.2, 0.3)
        elif cls == "tubing_leak":
            p["tubing_leak"][m] = r(0.3, 0.7)
        elif cls == "travelling_valve_leak":
            p["tv_leak"][m] = r(0.25, 0.6)
        elif cls == "standing_valve_leak":
            p["sv_leak"][m] = r(0.4, 0.8)
        elif cls == "unseated_pump":
            p["unseated"][m] = 1.0
        elif cls == "parted_rods":
            p["parted_depth"][m] = r(150.0, 950.0)
        elif cls == "plunger_sticking":
            p["sand"][m] = r(0.2, 0.5)
        elif cls == "excessive_friction":
            p["friction"][m] = r(0.15, 0.4)
    return p


def _time_shape(kd: np.ndarray, n: int):
    """Plunger normalised position s(t) in [0,1] (raised-cosine strokes) and the upstroke mask."""
    tau = np.arange(n)[None, :] / n
    up_share = (1 - kd)[:, None]
    up = tau < up_share
    u = np.where(up, tau / up_share, 0.0)
    v = np.where(up, 0.0, (tau - up_share) / (1 - up_share))
    s = np.where(up, 0.5 * (1 - np.cos(np.pi * u)), 0.5 * (1 + np.cos(np.pi * v)))
    return s, up


def _downhole_load(s: np.ndarray, up: np.ndarray, p: dict, rng: np.random.Generator, labels: np.ndarray):
    """Normalised pump load L = F/Fo as a function of plunger position s and stroke direction."""
    col = lambda k: p[k][:, None]  # noqa: E731
    eb, et = col("edge_bot"), col("edge_top")
    fr = col("friction")
    pick = _ss(s / eb)                                     # pickup of the fluid load on the upstroke
    drop_top = _ss((s - (1 - et)) / et)                    # transfer of the load off the rods at the top
    fill = col("fillage")
    width = 0.03 + 0.6 * col("gas")                        # gas compresses gradually
    x0 = np.clip(fill - 0.5 * width, 0.0, 1.0)
    drop_pound = _ss((s - x0) / width)                     # load falls when the plunger meets the fluid
    lo, hi = -fr, 1.0 + fr
    U = lo + (hi - lo) * pick
    D = lo + (hi - lo) * np.where(fill < 0.999, drop_pound, drop_top)
    # leaks
    U = U * (1 - col("tubing_leak")) * (1 - col("tv_leak") * s)
    D = D * (1 - col("tubing_leak")) * (1 - col("tv_leak") * s)
    D = D + col("sv_leak") * (1 - s) * (1 - drop_top) * (s < 1 - et)
    # unseated pump: no fluid load carried, only friction
    uns = col("unseated") > 0.5
    L = np.where(up, U, D)
    L = np.where(uns, 0.04 * (1 + 0.5 * np.sin(np.pi * s)) * np.where(up, 1.0, -1.0), L)
    # sticking / sand: localised load spikes on both strokes
    spikes = np.zeros_like(L)
    amp = col("sand")
    active = (amp[:, 0] > 0)
    if active.any():
        B = L.shape[0]
        for _ in range(4):
            c = rng.uniform(0.1, 0.9, (B, 1))
            a = amp * rng.choice([-1.0, 1.0], (B, 1)) * rng.uniform(0.5, 1.0, (B, 1))
            spikes += a * np.exp(-0.5 * ((s - c) / 0.012) ** 2)
        spikes += amp * 0.04 * rng.standard_normal(L.shape)
    return L + spikes


def synthesize_cards(
    labels: Any,
    rng: np.random.Generator | None = None,
    n_points: int = 128,
    rods: RodString | None = None,
    n_harm: int = 24,
    noise: float = 0.0,
    params: dict[str, np.ndarray] | None = None,
    buoyancy: float = 0.874,
) -> CardBatch:
    """Synthesise surface and downhole cards for the 12 dyno classes.

    ``labels`` is an int (number of cards, classes cycled evenly) or an array of class indices/names.
    Downhole cards are built from valve-state models and propagated up the rod string with the wave
    equation (band-limited to ``n_harm`` harmonics) to give the surface card. Parted rods use the string
    truncated at the break with a free end. ``noise`` adds relative Gaussian load-cell noise to the surface.
    """
    rng = rng or np.random.default_rng(0)
    rods = rods or RodString.default()
    if isinstance(labels, int):
        labels = np.arange(labels) % len(DYNO_CLASSES)
    labels = np.asarray([CLASS_INDEX[x] if isinstance(x, str) else int(x) for x in labels])
    p = params if params is not None else sample_params(labels, rng)
    period = 60.0 / p["spm"]
    s, up = _time_shape(p["kd"], n_points)
    L = _downhole_load(s, up, p, rng, labels)
    dh_pos = p["stroke"][:, None] * p["stroke_ratio"][:, None] * p["float_ratio"][:, None] * s
    dh_load = p["fluid_load"][:, None] * L
    surf_pos = np.empty_like(dh_pos)
    surf_load = np.empty_like(dh_load)

    parted = labels == CLASS_INDEX["parted_rods"]
    norm = ~parted
    if norm.any():
        sp, sl = surface_card_from_downhole(
            dh_pos[norm], dh_load[norm], period[norm], rods, p["damping"][norm], n_harm, buoyancy
        )
        surf_pos[norm], surf_load[norm] = sp, sl
    if parted.any():
        idx = np.flatnonzero(parted)
        for i in idx:
            top = rods.truncate(float(p["parted_depth"][i]))
            sp = p["stroke"][i] * s[i]
            surf_pos[i] = sp
            surf_load[i] = _free_end_load(sp, period[i], top, float(p["damping"][i]), n_harm, buoyancy)
        # the pump is stationary and carries no rod load
        dh_pos[parted] = 0.0
        dh_load[parted] = 0.0
    if noise > 0:
        scale = np.ptp(surf_load, axis=-1, keepdims=True)
        surf_load = surf_load + noise * scale * rng.standard_normal(surf_load.shape)
    return CardBatch(labels, surf_pos, surf_load, dh_pos, dh_load, period, p)


def _free_end_load(pos, period, rods: RodString, damping: float, n_harm: int, buoyancy: float):
    """Surface load of a string with a free lower end (tension 0) driven by a prescribed surface motion."""
    n = pos.shape[-1]
    K = min(int(n_harm), n // 2 - 1)
    omega = TAU * np.arange(1, K + 1) / period
    T11, T12, T21, T22 = _transfer(omega[None, :], rods, damping)
    Fs = -(T21 / T22) * _spec(pos[None, :], K)
    return _synth(Fs, np.array([_buoyant_weight(rods, buoyancy)]), n, K)[0]


# ---------------------------------------------------------------------------------------------- features


def card_features(pos, load, fluid_load: float, stroke: float | None = None) -> dict[str, float]:
    """Shape features of a (downhole) card sampled uniformly in time over one stroke.

    Loads are normalised by ``fluid_load``; positions by the card's own stroke (``s`` in [0, 1]).
    Keys: ``stroke_ratio`` (card stroke / nominal ``stroke``), ``up_mid`` / ``dn_mid`` (mean load mid-stroke),
    ``up_slope`` (load change upstroke s=0.3 -> 0.85), ``dn_slope`` (downstroke s=0.5 -> 0.1),
    ``drop_pos`` / ``drop_width`` (where and how fast the downstroke load falls), ``load_range`` and
    ``roughness`` (RMS second difference of the load).
    """
    pos = np.asarray(pos, dtype=float)
    f = np.asarray(load, dtype=float) / fluid_load
    n = len(pos)
    span = float(pos.max() - pos.min())
    feats = {
        "stroke_ratio": span / stroke if stroke else span,
        "load_range": float(f.max() - f.min()),
        "roughness": float(np.sqrt(np.mean((np.roll(f, -1) - 2 * f + np.roll(f, 1)) ** 2))),
    }
    if span < 1e-9:
        feats.update(up_mid=0.0, dn_mid=0.0, up_slope=0.0, dn_slope=0.0, drop_pos=0.0, drop_width=0.0)
        return feats
    s = (pos - pos.min()) / span
    i0, i1 = int(np.argmin(pos)), int(np.argmax(pos))
    up_idx = (np.arange(i0, i0 + ((i1 - i0) % n) + 1)) % n
    dn_idx = (np.arange(i1, i1 + ((i0 - i1) % n) + 1)) % n
    grid = np.linspace(0, 1, 201)

    def curve(idx):
        x, y = s[idx], f[idx]
        order = np.argsort(x)
        return np.interp(grid, x[order], y[order])

    U, D = curve(up_idx), curve(dn_idx)
    at = lambda c, v: float(np.interp(v, grid, c))  # noqa: E731
    feats["up_mid"] = float(U[(grid >= 0.25) & (grid <= 0.75)].mean())
    feats["dn_mid"] = float(D[(grid >= 0.1) & (grid <= 0.35)].mean())
    feats["up_slope"] = at(U, 0.85) - at(U, 0.3)
    feats["dn_slope"] = at(D, 0.1) - at(D, 0.5)
    hi, lo = float(D.max()), float(D.min())
    half = 0.5 * (hi + lo)
    feats["drop_pos"] = _walk_down(D, grid, half)
    hi_l, lo_l = lo + 0.9 * (hi - lo), lo + 0.1 * (hi - lo)
    feats["drop_width"] = _walk_down(D, grid, hi_l) - _walk_down(D, grid, lo_l)
    return feats


def _walk_down(D: np.ndarray, grid: np.ndarray, level: float) -> float:
    """Position where the downstroke load, walking from the top of the stroke down, first falls below ``level``."""
    below = np.flatnonzero(D[::-1] < level)
    return float(grid[::-1][below[0]]) if len(below) else 0.0
