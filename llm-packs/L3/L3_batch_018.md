# L3 rod_failure_report - batch 018 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_018.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00204 .. L3-00215 (each has an `item_id` you must echo).

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

### item_id: L3-00204
Write a rod-string failure report for BGW-06 on 2024-01-30: failed component rod pin/coupling at 102.87 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.04, Goodman 0.976, impacts/day 1703, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00205
Write a rod-string failure report for BGW-33 on 2024-09-09: failed component sinker bar at 87.63 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.48, Goodman 0.963, impacts/day 3118, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00206
Write a rod-string failure report for BGW-53 on 2025-05-01: failed component rod pin/coupling at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.06, Goodman 1.11, impacts/day 893, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00207
Write a rod-string failure report for BGW-18 on 2026-08-19: failed component rod pin/coupling at 57.15 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.07, Goodman 1.134, impacts/day 1265, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00208
Write a rod-string failure report for BGW-18 on 2024-11-09: failed component polished rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.09, Goodman 1.1, impacts/day 2450, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00209
Write a rod-string failure report for BGW-39 on 2026-06-23: failed component sinker bar at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.16, Goodman 1.059, impacts/day 1611, corrosion index 0.14), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00210
Write a rod-string failure report for BGW-28 on 2026-04-18: failed component rod body at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.22, Goodman 1.028, impacts/day 935, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00211
Write a rod-string failure report for BGW-48 on 2025-09-12: failed component pony rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.34, Goodman 0.968, impacts/day 839, corrosion index 0.38), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00212
Write a rod-string failure report for BGW-02 on 2024-02-04: failed component pony rod at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.04, Goodman 0.915, impacts/day 689, corrosion index 0.3), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00213
Write a rod-string failure report for BGW-11 on 2025-02-14: failed component polished rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.16, Goodman 1.18, impacts/day 5097, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00214
Write a rod-string failure report for BGW-06 on 2024-01-16: failed component rod body at 57.15 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.45, Goodman 1.055, impacts/day 65, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00215
Write a rod-string failure report for BGW-11 on 2025-12-15: failed component rod body at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.11, Goodman 1.164, impacts/day 472, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
