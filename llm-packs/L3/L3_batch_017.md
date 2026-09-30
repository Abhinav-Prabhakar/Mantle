# L3 rod_failure_report - batch 017 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_017.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00192 .. L3-00203 (each has an `item_id` you must echo).

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

### item_id: L3-00192
Write a rod-string failure report for BGW-33 on 2024-08-09: failed component rod body at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.45, Goodman 1.06, impacts/day 3730, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00193
Write a rod-string failure report for BGW-18 on 2023-10-30: failed component sinker bar at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.0, Goodman 0.988, impacts/day 4119, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00194
Write a rod-string failure report for BGW-28 on 2024-12-24: failed component rod pin/coupling at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.08, Goodman 1.179, impacts/day 3543, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00195
Write a rod-string failure report for BGW-53 on 2026-05-09: failed component sinker bar at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.03, Goodman 1.074, impacts/day 1515, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00196
Write a rod-string failure report for BGW-11 on 2025-03-10: failed component polished rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.45, Goodman 1.18, impacts/day 153, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00197
Write a rod-string failure report for BGW-19 on 2023-09-18: failed component polished rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.35, Goodman 1.077, impacts/day 4384, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00198
Write a rod-string failure report for BGW-53 on 2025-04-21: failed component rod pin/coupling at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.4, Goodman 1.137, impacts/day 1949, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00199
Write a rod-string failure report for BGW-58 on 2024-04-27: failed component rod pin/coupling at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.06, Goodman 0.985, impacts/day 3669, corrosion index 0.79), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00200
Write a rod-string failure report for BGW-53 on 2025-05-11: failed component sinker bar at 95.25 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.05, Goodman 1.002, impacts/day 1787, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00201
Write a rod-string failure report for BGW-11 on 2025-12-10: failed component polished rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.01, Goodman 1.137, impacts/day 3929, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00202
Write a rod-string failure report for BGW-48 on 2024-08-06: failed component rod pin/coupling at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.49, Goodman 0.999, impacts/day 1499, corrosion index 0.38), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00203
Write a rod-string failure report for BGW-10 on 2023-08-28: failed component pony rod at 72.39 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.15, Goodman 0.858, impacts/day 969, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
