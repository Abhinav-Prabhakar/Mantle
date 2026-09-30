# L3 rod_failure_report - batch 020 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_020.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00228 .. L3-00239 (each has an `item_id` you must echo).

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

### item_id: L3-00228
Write a rod-string failure report for BGW-06 on 2024-01-17: failed component sinker bar at 102.87 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.14, Goodman 0.976, impacts/day 208, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00229
Write a rod-string failure report for BGW-11 on 2025-03-13: failed component rod pin/coupling at 72.39 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.4, Goodman 1.058, impacts/day 3837, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00230
Write a rod-string failure report for BGW-06 on 2023-12-14: failed component sinker bar at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.21, Goodman 1.069, impacts/day 130, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00231
Write a rod-string failure report for BGW-38 on 2026-02-06: failed component rod body at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.02, Goodman 0.976, impacts/day 2661, corrosion index 0.62), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00232
Write a rod-string failure report for BGW-18 on 2024-11-08: failed component rod pin/coupling at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.1, Goodman 1.048, impacts/day 1264, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00233
Write a rod-string failure report for BGW-28 on 2025-01-25: failed component rod body at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.0, Goodman 1.105, impacts/day 2380, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00234
Write a rod-string failure report for BGW-28 on 2025-01-03: failed component rod pin/coupling at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.02, Goodman 1.164, impacts/day 889, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00235
Write a rod-string failure report for BGW-28 on 2025-01-03: failed component polished rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.08, Goodman 1.164, impacts/day 1332, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00236
Write a rod-string failure report for BGW-15 on 2026-09-18: failed component sinker bar at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.11, Goodman 1.036, impacts/day 3912, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00237
Write a rod-string failure report for BGW-06 on 2024-01-15: failed component pony rod at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.43, Goodman 1.095, impacts/day 3361, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00238
Write a rod-string failure report for BGW-18 on 2026-08-04: failed component polished rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.05, Goodman 1.219, impacts/day 437, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00239
Write a rod-string failure report for BGW-59 on 2026-09-17: failed component polished rod at 64.77 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.03, Goodman 0.878, impacts/day 2760, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
