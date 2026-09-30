# L3 rod_failure_report - batch 011 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_011.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00120 .. L3-00131 (each has an `item_id` you must echo).

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

### item_id: L3-00120
Write a rod-string failure report for BGW-16 on 2025-04-13: failed component polished rod at 11.43 m, failure mode float-buckling, visual inspection notes, suspected root cause (consistent with float margin 0.42, Goodman 0.992, impacts/day 2797, corrosion index 0.6), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00121
Write a rod-string failure report for BGW-06 on 2024-01-04: failed component pony rod at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.27, Goodman 1.108, impacts/day 3731, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00122
Write a rod-string failure report for BGW-11 on 2025-12-24: failed component polished rod at 64.77 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.07, Goodman 1.057, impacts/day 5777, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00123
Write a rod-string failure report for BGW-57 on 2025-05-12: failed component rod body at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.26, Goodman 0.959, impacts/day 5521, corrosion index 0.41), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00124
Write a rod-string failure report for BGW-38 on 2026-02-04: failed component rod pin/coupling at 11.43 m, failure mode float-buckling, visual inspection notes, suspected root cause (consistent with float margin 0.11, Goodman 0.987, impacts/day 5306, corrosion index 0.62), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00125
Write a rod-string failure report for BGW-18 on 2024-11-08: failed component sinker bar at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.05, Goodman 1.048, impacts/day 2070, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00126
Write a rod-string failure report for BGW-15 on 2026-09-21: failed component sinker bar at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.42, Goodman 1.083, impacts/day 5507, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00127
Write a rod-string failure report for BGW-18 on 2026-09-29: failed component rod pin/coupling at 156.21 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.36, Goodman 0.952, impacts/day 5677, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00128
Write a rod-string failure report for BGW-18 on 2026-08-29: failed component pony rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.04, Goodman 1.205, impacts/day 2221, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00129
Write a rod-string failure report for BGW-33 on 2024-09-24: failed component rod pin/coupling at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.09, Goodman 1.024, impacts/day 5337, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00130
Write a rod-string failure report for BGW-33 on 2024-08-28: failed component polished rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.04, Goodman 1.084, impacts/day 971, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00131
Write a rod-string failure report for BGW-11 on 2025-02-11: failed component polished rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.22, Goodman 1.166, impacts/day 972, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
