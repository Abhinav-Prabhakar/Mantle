# M5 VFD / impact estimator
From one stroke (96 time-uniform samples of polished-rod load + position, spm) predicts fillage, impacts/day, impact velocity and mean motor amps.
**Source: physics_synthetic** (5000 training strokes drawn from the twin across steam 500-1200 t, cycle days 19-120, spm 2-9, kd 0.42-0.68, with load/position noise; targets are the twin's own fillage and `derive` impact/amps laws).
- Physics features: card area, up/down mean loads, steepest downstroke drop (position, kN, severity), drop-position fillage estimate. LightGBM calibrates each target.
- Metrics (held-out 1500 strokes): {"mae_fillage_ml": 0.7192666220846237, "mae_fillage_threshold": 35.96627385558603, "mae_impacts_day_ml": 55.27761455937726, "mae_impacts_day_threshold": 2814.2662049986693, "mae_impact_vel_ml": 0.010258898345183858, "mae_impact_vel_threshold": 0.5638830898135148, "mae_amps_ml": 0.37731684049636005, "mae_amps_threshold": 25.215804304172092, "mae_fillage_phys_raw": 37.06387862775699}
- Baseline: fixed thresholds on the drop position (fillage buckets, pound if < 85 %, constant amps).
- Limits: the twin sets the truth, so the model calibrates the estimator against the twin, not against measured pump-off events. The fixed 4 Hz-like stroke length assumed is 96 points.
