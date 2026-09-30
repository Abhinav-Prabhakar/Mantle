# L3 rod_failure_report - batch 008 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_008.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00084 .. L3-00095 (each has an `item_id` you must echo).

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

### item_id: L3-00084
Write a rod-string failure report for BGW-53 on 2026-05-08: failed component rod pin/coupling at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.47, Goodman 1.062, impacts/day 4110, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00085
Write a rod-string failure report for BGW-18 on 2024-11-08: failed component rod pin/coupling at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.01, Goodman 1.048, impacts/day 2230, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00086
Write a rod-string failure report for BGW-28 on 2025-01-31: failed component sinker bar at 140.97 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.33, Goodman 0.937, impacts/day 817, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00087
Write a rod-string failure report for BGW-28 on 2024-12-22: failed component pony rod at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.33, Goodman 1.15, impacts/day 4214, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00088
Write a rod-string failure report for BGW-33 on 2024-09-20: failed component rod pin/coupling at 102.87 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.01, Goodman 0.939, impacts/day 5372, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00089
Write a rod-string failure report for BGW-11 on 2025-12-31: failed component rod pin/coupling at 57.15 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.08, Goodman 1.071, impacts/day 5616, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00090
Write a rod-string failure report for BGW-28 on 2025-08-01: failed component sinker bar at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.03, Goodman 0.994, impacts/day 29, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00091
Write a rod-string failure report for BGW-48 on 2024-07-19: failed component pony rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.34, Goodman 1.022, impacts/day 4744, corrosion index 0.38), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00092
Write a rod-string failure report for BGW-39 on 2026-06-23: failed component polished rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.48, Goodman 1.059, impacts/day 163, corrosion index 0.14), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00093
Write a rod-string failure report for BGW-11 on 2025-03-26: failed component polished rod at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.05, Goodman 1.112, impacts/day 1395, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00094
Write a rod-string failure report for BGW-53 on 2026-01-20: failed component polished rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.23, Goodman 1.072, impacts/day 5044, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00095
Write a rod-string failure report for BGW-19 on 2023-09-20: failed component rod body at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.37, Goodman 1.025, impacts/day 3257, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
