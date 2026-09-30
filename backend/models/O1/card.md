# O1 SRP controller
Constrained optimisation of pump speed and stroke shape (kd) on the physics twin: maximise oil value - energy cost - risk cost subject to
float margin >= 0.15, fillage >= 0.8, Goodman <= 0.9, torque <= 1.0 (grid warm start + SLSQP; tabulated twin core, ~ms per call).
**Source: physics_synthetic** (the twin itself; no learned weights, so `train` = validation on 400 sampled states drawn like S2).
- Output: title, detail, spm, kd, hz, stroke, deltas{oil, float, energy, impacts}, confidence (+ constraints, impacts/day, objective).
- Metrics vs today's fixed SPM: {"impacts_reduction_all_states": 0.9455781657141136, "oil_change_all_states": -0.008655366977713297, "impacts_reduction_pounding_states": 0.950889261238514, "oil_change_pounding_states": -0.013944884462928853, "n_pounding_states": 384, "objective_gain_inr_per_day_mean": 447494.1850590107, "baseline_infeasible_share": 0.94, "recommended_infeasible_share": 0.0, "latency_ms_p50": 7.702979492023587, "latency_ms_p95": 11.970156256575136, "n_states": 400}. Target: >= 15 % fewer impacts at <= 2 % oil loss.
- Risk cost uses the physics hazard laws (same as S5/M4); stroke-hole selection is not modelled (the twin has one stroke length).
- Limits: optimum is for the current cycle day (myopic); fillage >= 0.8 makes the controller slow the unit whenever inflow is the bottleneck.
