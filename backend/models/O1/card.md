# O1 SRP controller
Constrained optimisation of pump speed and stroke shape (kd) on the physics twin: maximise oil value - energy cost - risk cost subject to
float margin >= 0.15, fillage >= 0.8, Goodman <= 0.9, torque <= 1.0 (grid warm start + SLSQP; tabulated twin core, ~ms per call).
**Source: physics_synthetic** (the twin itself; no learned weights, so `train` = validation on 400 sampled states drawn like S2).
- Output: title, detail, spm, kd, hz, stroke, deltas{oil, float, energy, impacts}, confidence (+ constraints, impacts/day, objective).
- Metrics vs today's fixed SPM: {"impacts_reduction_all_states": 0.9461626095065859, "oil_change_all_states": -0.008639392747783914, "impacts_reduction_pounding_states": 0.951473883822178, "oil_change_pounding_states": -0.01392759019673484, "n_pounding_states": 384, "objective_gain_inr_per_day_mean": 475222.40329186886, "baseline_infeasible_share": 0.94, "recommended_infeasible_share": 0.0, "latency_ms_p50": 8.192020992282778, "latency_ms_p95": 12.893639883259304, "n_states": 400}. Target: >= 15 % fewer impacts at <= 2 % oil loss.
- Risk cost uses the physics hazard laws (same as S5/M4); stroke-hole selection is not modelled (the twin has one stroke length).
- Limits: optimum is for the current cycle day (myopic); fillage >= 0.8 makes the controller slow the unit whenever inflow is the bottleneck.
