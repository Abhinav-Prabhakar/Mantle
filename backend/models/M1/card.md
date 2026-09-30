# M1 thermal surrogate
Predicts sandface T, heated radius r_h and thermal battery over the cycle with quantiles 0.1/0.5/0.9.
**Source: physics_synthetic** (S2 daily rows from the twin, 51919 rows). The surrogate reproduces the twin's thermal law
(which S2 applies with per-well steam efficiency and soak-length time remapping), so accuracy shows how well the physics-feature
GBM absorbs those effects, not agreement with a real reservoir.
- Baseline: analytic thermal law at nominal steam and actual day. Features: steam_t, inj_pressure_mpa, steam_quality, soak_days, cycle_no, steam_eff, day, phase_i, dprod, an_T, an_rh, an_exc, an_Te, an_rhe, an_exce (analytic T/r_h/excess also at the well's effective steam).
- 5-fold grouped by well. Metrics: {"mae_T_ml": 0.19739593487635376, "mae_T_analytic": 3.8292679070279165, "cover80_T": 0.7665979699146748, "mae_rh_ml": 0.0045419929409438635, "mae_rh_analytic": 0.07454294716962971, "cover80_rh": 0.738380939540438, "mae_battery_ml": 0.0012924722128336195, "mae_battery_analytic": 0.025562302376031798, "cover80_battery": 0.8117259577418672}. Targets: MAE T <= 6 C, r_h <= 0.8 m.
- Limits: S2 is noiseless, so the 0.1/0.9 quantiles are narrow (coverage is reported, not tuned); no real steam-injection data used.
