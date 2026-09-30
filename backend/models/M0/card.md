# M0 viscosity (Walther + monotone LightGBM residual)
**Source of training data: physics_synthetic** (NOT real lab data). Real sample-level literature data was unavailable
(the reference CSV has column statistics only), so wells' lab-like points come from the twin's Walther law with
per-well multipliers, an asphaltene/resin/WAT deviation (decreasing in T) that Walther cannot express, and 4 %
lognormal noise. The GBM therefore learns *the generator's* deviation; the MAPE below is not evidence about real crude.

- Features: T, api, asph, resin, wat, wA, wB (wA/wB from a 2-point fit at 50/150 C). Target: log10(mu/mu_walther); LightGBM with monotone
  constraint decreasing in T, so the total curve is strictly decreasing.
- Metrics (5-fold, grouped by fluid): {"mape_gbm_pct": 4.337736042162992, "mape_walther_2pt_pct": 4.621458214534785, "mape_beggs_robinson_pct": 98.49000414674859, "mape_gbm_ge50C_pct": 3.8811616263644115, "mape_walther_ge50C_pct": 4.017765234090797}
- Baselines: Beggs-Robinson dead oil (98 % MAPE: it is not built for 12,000 cP oils), plain 2-point Walther.
- Envelope check vs literature statistics: {"available": true, "lit_min_cp": 1.7, "lit_max_cp": 11900.0, "pred_80_120_160C": [1484.6101435654878, 219.2052084684569, 59.56292529839182], "inside": true}
- Limits: inference at temperatures outside 20-160 C or API outside 17-19.5 extrapolates; no pressure/gas effects.
