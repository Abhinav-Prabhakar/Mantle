# L3 rod_failure_report - batch 012 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_012.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00132 .. L3-00143 (each has an `item_id` you must echo).

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

### item_id: L3-00132
Write a rod-string failure report for BGW-27 on 2025-07-10: failed component sinker bar at 538.945 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin 0.13, Goodman 0.8, impacts/day 4527, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00133
Write a rod-string failure report for BGW-53 on 2025-05-14: failed component sinker bar at 87.63 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.16, Goodman 1.015, impacts/day 5379, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00134
Write a rod-string failure report for BGW-33 on 2024-08-12: failed component rod body at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.04, Goodman 1.084, impacts/day 4479, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00135
Write a rod-string failure report for BGW-53 on 2026-01-22: failed component sinker bar at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.15, Goodman 1.01, impacts/day 517, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00136
Write a rod-string failure report for BGW-23 on 2025-10-13: failed component polished rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.42, Goodman 1.054, impacts/day 4880, corrosion index 0.28), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00137
Write a rod-string failure report for BGW-41 on 2025-01-18: failed component sinker bar at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.37, Goodman 0.925, impacts/day 248, corrosion index 0.58), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00138
Write a rod-string failure report for BGW-18 on 2026-08-18: failed component rod pin/coupling at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.25, Goodman 1.148, impacts/day 2049, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00139
Write a rod-string failure report for BGW-05 on 2025-06-01: failed component rod body at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.45, Goodman 0.924, impacts/day 4332, corrosion index 0.46), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00140
Write a rod-string failure report for BGW-28 on 2026-05-04: failed component polished rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.25, Goodman 1.078, impacts/day 806, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00141
Write a rod-string failure report for BGW-58 on 2024-05-29: failed component rod body at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.09, Goodman 0.929, impacts/day 188, corrosion index 0.79), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00142
Write a rod-string failure report for BGW-23 on 2025-10-12: failed component sinker bar at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.03, Goodman 1.066, impacts/day 5718, corrosion index 0.28), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00143
Write a rod-string failure report for BGW-28 on 2025-01-15: failed component pony rod at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.24, Goodman 1.12, impacts/day 495, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
