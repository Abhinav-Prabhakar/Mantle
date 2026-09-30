# L3 rod_failure_report - batch 007 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_007.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00072 .. L3-00083 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "well_id", "date", "failed_component", "depth_m", "failure_mode", "inspection_notes", "root_cause", "rods_replaced", "downtime_hours", "cost_inr", "recommendations"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "well_id": {"type": "string"},
    "date": {"type": "string"},
    "failed_component": {"type": "string"},
    "depth_m": {"type": "number", "minimum": 0, "maximum": 1300},
    "failure_mode": {"type": "string"},
    "inspection_notes": {"type": "string"},
    "root_cause": {"type": "string"},
    "rods_replaced": {"type": "integer", "minimum": 0, "maximum": 60},
    "downtime_hours": {"type": "number", "minimum": 0, "maximum": 400},
    "cost_inr": {"type": "number", "minimum": 0},
    "recommendations": {"type": "array", "items": {"type": "string"}, "minItems": 1}
  }
}
```

## Items (12)
Write one record per item, following the instruction under each item_id.

### item_id: L3-00072
Write a rod-string failure report for BGW-58 on 2024-05-05: failed component pony rod at 87.63 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.28, Goodman 0.872, impacts/day 202, corrosion index 0.79), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00073
Write a rod-string failure report for BGW-18 on 2026-02-09: failed component pony rod at 133.35 m, failure mode float-buckling, visual inspection notes, suspected root cause (consistent with float margin 0.14, Goodman 0.916, impacts/day 5017, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00074
Write a rod-string failure report for BGW-53 on 2026-01-20: failed component sinker bar at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.03, Goodman 1.072, impacts/day 5122, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00075
Write a rod-string failure report for BGW-09 on 2025-04-22: failed component rod body at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.01, Goodman 0.929, impacts/day 1845, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00076
Write a rod-string failure report for BGW-11 on 2026-01-03: failed component pony rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.02, Goodman 1.137, impacts/day 1221, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00077
Write a rod-string failure report for BGW-53 on 2025-04-21: failed component rod pin/coupling at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.33, Goodman 1.137, impacts/day 2023, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00078
Write a rod-string failure report for BGW-10 on 2023-08-16: failed component rod body at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.09, Goodman 0.958, impacts/day 3403, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00079
Write a rod-string failure report for BGW-11 on 2025-02-14: failed component rod pin/coupling at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.15, Goodman 1.153, impacts/day 812, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00080
Write a rod-string failure report for BGW-18 on 2026-09-04: failed component sinker bar at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.22, Goodman 1.162, impacts/day 1693, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00081
Write a rod-string failure report for BGW-38 on 2025-02-09: failed component pony rod at 740.151 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin 0.41, Goodman 0.8, impacts/day 5970, corrosion index 0.62), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00082
Write a rod-string failure report for BGW-02 on 2026-04-14: failed component sinker bar at 876.694 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin 0.33, Goodman 0.8, impacts/day 907, corrosion index 0.3), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00083
Write a rod-string failure report for BGW-28 on 2024-12-08: failed component rod pin/coupling at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.07, Goodman 1.179, impacts/day 2716, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
