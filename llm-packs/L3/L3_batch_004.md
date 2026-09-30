# L3 rod_failure_report - batch 004 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_004.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00036 .. L3-00047 (each has an `item_id` you must echo).

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

### item_id: L3-00036
Write a rod-string failure report for BGW-53 on 2026-07-17: failed component pony rod at 163.83 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.11, Goodman 0.806, impacts/day 4316, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00037
Write a rod-string failure report for BGW-15 on 2026-09-17: failed component sinker bar at 57.15 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.03, Goodman 1.001, impacts/day 165, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00038
Write a rod-string failure report for BGW-15 on 2026-04-03: failed component rod pin/coupling at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.1, Goodman 1.036, impacts/day 2949, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00039
Write a rod-string failure report for BGW-18 on 2026-08-29: failed component polished rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.25, Goodman 1.205, impacts/day 1636, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00040
Write a rod-string failure report for BGW-28 on 2025-08-01: failed component sinker bar at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.46, Goodman 0.994, impacts/day 4735, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00041
Write a rod-string failure report for BGW-57 on 2025-05-12: failed component polished rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.04, Goodman 0.959, impacts/day 1320, corrosion index 0.41), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00042
Write a rod-string failure report for BGW-28 on 2026-04-21: failed component sinker bar at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.06, Goodman 1.04, impacts/day 2, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00043
Write a rod-string failure report for BGW-28 on 2025-01-23: failed component rod body at 64.77 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.32, Goodman 1.076, impacts/day 774, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00044
Write a rod-string failure report for BGW-28 on 2026-04-18: failed component rod pin/coupling at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.07, Goodman 1.028, impacts/day 5543, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00045
Write a rod-string failure report for BGW-18 on 2025-12-28: failed component rod body at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.32, Goodman 1.103, impacts/day 5792, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00046
Write a rod-string failure report for BGW-28 on 2025-08-01: failed component rod pin/coupling at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.42, Goodman 0.994, impacts/day 5648, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00047
Write a rod-string failure report for BGW-18 on 2026-09-22: failed component pony rod at 34.29 m, failure mode float-buckling, visual inspection notes, suspected root cause (consistent with float margin 0.47, Goodman 1.176, impacts/day 155, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
