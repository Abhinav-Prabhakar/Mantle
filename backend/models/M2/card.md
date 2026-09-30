# M2 cycle production forecaster
Daily oil = physics prior (twin Boberg-Lantz rate x PI) x exp(LightGBM residual); P10/P90 from CQR (daily) and split-conformal
(cycle cum oil). **Source: physics_synthetic** (S2). S2 cycles carry a 6 % lognormal cycle-to-cycle noise that no model can
predict, so about 5 % MAPE is the floor on this data.
- 5-fold grouped by well; M1 inputs out-of-fold. Metrics: {"cycle_mape_ml_pct": 6.450035252441596, "cycle_mape_ml_with_well_scaling_pct": 6.624872378044613, "cycle_mape_arps_pct": 26.62141901564677, "cycle_mape_ml_same_subset_pct": 6.473569355315119, "daily_mape_ml_pct": 6.85462722286035, "n_cycles": 565, "n_cycles_with_prev": 505, "daily_cover80": 0.8057090239410681, "cycle_cover80_mean": 0.7920690748421052, "cycle_cover80_std": 0.030062006113288922}
- Baseline: Arps hyperbolic on the previous cycle (blind to steam/soak/pump changes). Targets: cycle cum-oil MAPE <= 10 %, 80 % interval coverage 0.78-0.82.
- Per-well Bayesian scaling (prior strength 2) is applied at inference via ``scale=well_scale(history)``.
- Limits: trained on the 60-well roster; production-days only; requires M0 and M1 artifacts at inference.
