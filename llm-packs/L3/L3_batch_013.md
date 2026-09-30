# L3 rod_failure_report - batch 013 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_013.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00144 .. L3-00155 (each has an `item_id` you must echo).

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

### item_id: L3-00144
Write a rod-string failure report for BGW-11 on 2025-03-27: failed component polished rod at 57.15 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.07, Goodman 1.085, impacts/day 4945, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00145
Write a rod-string failure report for BGW-49 on 2025-11-05: failed component rod pin/coupling at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.01, Goodman 1.141, impacts/day 286, corrosion index 0.17), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00146
Write a rod-string failure report for BGW-14 on 2024-04-15: failed component sinker bar at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.38, Goodman 0.964, impacts/day 1933, corrosion index 0.13), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00147
Write a rod-string failure report for BGW-53 on 2025-05-11: failed component polished rod at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.43, Goodman 1.11, impacts/day 624, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00148
Write a rod-string failure report for BGW-53 on 2025-04-23: failed component polished rod at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.24, Goodman 1.123, impacts/day 2107, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00149
Write a rod-string failure report for BGW-03 on 2026-03-26: failed component rod pin/coupling at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.39, Goodman 0.986, impacts/day 3543, corrosion index 0.27), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00150
Write a rod-string failure report for BGW-15 on 2026-09-16: failed component rod body at 95.25 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.1, Goodman 0.943, impacts/day 4060, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00151
Write a rod-string failure report for BGW-53 on 2026-01-22: failed component sinker bar at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.27, Goodman 1.01, impacts/day 5911, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00152
Write a rod-string failure report for BGW-18 on 2026-09-25: failed component polished rod at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.05, Goodman 1.162, impacts/day 3870, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00153
Write a rod-string failure report for BGW-19 on 2023-09-20: failed component rod body at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.39, Goodman 1.064, impacts/day 1500, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00154
Write a rod-string failure report for BGW-15 on 2026-09-28: failed component rod body at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.03, Goodman 1.083, impacts/day 581, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00155
Write a rod-string failure report for BGW-11 on 2025-03-13: failed component rod body at 72.39 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.48, Goodman 1.058, impacts/day 1969, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
