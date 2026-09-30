# L3 rod_failure_report - batch 010 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_010.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00108 .. L3-00119 (each has an `item_id` you must echo).

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

### item_id: L3-00108
Write a rod-string failure report for BGW-18 on 2026-09-12: failed component sinker bar at 80.01 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.39, Goodman 1.091, impacts/day 1533, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00109
Write a rod-string failure report for BGW-18 on 2026-08-13: failed component rod pin/coupling at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.02, Goodman 1.233, impacts/day 1155, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00110
Write a rod-string failure report for BGW-23 on 2025-09-29: failed component pony rod at 26.67 m, failure mode float-buckling, visual inspection notes, suspected root cause (consistent with float margin 0.48, Goodman 1.042, impacts/day 5462, corrosion index 0.28), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00111
Write a rod-string failure report for BGW-15 on 2026-09-22: failed component polished rod at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.22, Goodman 1.013, impacts/day 362, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00112
Write a rod-string failure report for BGW-21 on 2024-04-10: failed component pony rod at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.46, Goodman 1.07, impacts/day 5348, corrosion index 0.25), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00113
Write a rod-string failure report for BGW-33 on 2024-09-17: failed component polished rod at 125.73 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.31, Goodman 0.902, impacts/day 3521, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00114
Write a rod-string failure report for BGW-19 on 2026-06-07: failed component pony rod at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.29, Goodman 0.924, impacts/day 4576, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00115
Write a rod-string failure report for BGW-18 on 2026-08-11: failed component polished rod at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.01, Goodman 1.191, impacts/day 5710, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00116
Write a rod-string failure report for BGW-06 on 2023-12-20: failed component pony rod at 72.39 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.46, Goodman 1.029, impacts/day 2295, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00117
Write a rod-string failure report for BGW-18 on 2026-09-08: failed component polished rod at 57.15 m, failure mode float-buckling, visual inspection notes, suspected root cause (consistent with float margin 0.21, Goodman 1.134, impacts/day 4085, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00118
Write a rod-string failure report for BGW-15 on 2026-09-22: failed component rod pin/coupling at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.49, Goodman 1.013, impacts/day 4665, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00119
Write a rod-string failure report for BGW-04 on 2025-08-11: failed component rod pin/coupling at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.17, Goodman 0.988, impacts/day 5420, corrosion index 0.6), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
