# L3 rod_failure_report - batch 002 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00012 .. L3-00023 (each has an `item_id` you must echo).

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

### item_id: L3-00012
Write a rod-string failure report for BGW-28 on 2024-12-26: failed component pony rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.48, Goodman 1.194, impacts/day 3803, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00013
Write a rod-string failure report for BGW-06 on 2024-02-01: failed component rod body at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.2, Goodman 1.095, impacts/day 423, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00014
Write a rod-string failure report for BGW-28 on 2024-12-23: failed component polished rod at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.47, Goodman 1.12, impacts/day 1812, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00015
Write a rod-string failure report for BGW-02 on 2025-03-04: failed component rod body at 507.783 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin 0.39, Goodman 0.8, impacts/day 2521, corrosion index 0.3), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00016
Write a rod-string failure report for BGW-27 on 2025-07-10: failed component polished rod at 538.945 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin 0.11, Goodman 0.8, impacts/day 2848, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00017
Write a rod-string failure report for BGW-38 on 2026-02-22: failed component rod pin/coupling at 57.15 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.36, Goodman 0.92, impacts/day 3270, corrosion index 0.62), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00018
Write a rod-string failure report for BGW-18 on 2026-08-11: failed component rod body at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.31, Goodman 1.191, impacts/day 2961, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00019
Write a rod-string failure report for BGW-06 on 2024-02-03: failed component pony rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.01, Goodman 1.134, impacts/day 2877, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00020
Write a rod-string failure report for BGW-11 on 2025-02-14: failed component polished rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.2, Goodman 1.153, impacts/day 788, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00021
Write a rod-string failure report for BGW-18 on 2026-09-08: failed component pony rod at 57.15 m, failure mode float-buckling, visual inspection notes, suspected root cause (consistent with float margin -0.05, Goodman 1.134, impacts/day 4740, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00022
Write a rod-string failure report for BGW-28 on 2025-01-30: failed component rod pin/coupling at 72.39 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.11, Goodman 1.061, impacts/day 586, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00023
Write a rod-string failure report for BGW-33 on 2024-09-24: failed component rod body at 57.15 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.07, Goodman 1.011, impacts/day 3411, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
