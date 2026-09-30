# L3 rod_failure_report - batch 003 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_003.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00024 .. L3-00035 (each has an `item_id` you must echo).

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

### item_id: L3-00024
Write a rod-string failure report for BGW-11 on 2025-12-10: failed component sinker bar at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.3, Goodman 1.137, impacts/day 3732, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00025
Write a rod-string failure report for BGW-06 on 2024-01-08: failed component rod body at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.21, Goodman 1.148, impacts/day 3598, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00026
Write a rod-string failure report for BGW-18 on 2026-08-08: failed component rod pin/coupling at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.12, Goodman 1.205, impacts/day 2586, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00027
Write a rod-string failure report for BGW-06 on 2024-01-08: failed component sinker bar at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.23, Goodman 1.148, impacts/day 4353, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00028
Write a rod-string failure report for BGW-28 on 2024-12-28: failed component rod body at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.23, Goodman 1.164, impacts/day 909, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00029
Write a rod-string failure report for BGW-06 on 2024-01-08: failed component sinker bar at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.07, Goodman 1.148, impacts/day 3260, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00030
Write a rod-string failure report for BGW-31 on 2025-02-10: failed component rod pin/coupling at 742.475 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin 0.35, Goodman 0.8, impacts/day 1309, corrosion index 0.74), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00031
Write a rod-string failure report for BGW-18 on 2026-09-20: failed component pony rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.05, Goodman 1.219, impacts/day 3066, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00032
Write a rod-string failure report for BGW-06 on 2024-01-10: failed component pony rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.25, Goodman 1.121, impacts/day 2116, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00033
Write a rod-string failure report for BGW-11 on 2025-02-10: failed component pony rod at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.42, Goodman 1.112, impacts/day 5384, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00034
Write a rod-string failure report for BGW-53 on 2026-04-27: failed component pony rod at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.2, Goodman 1.013, impacts/day 4358, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00035
Write a rod-string failure report for BGW-19 on 2023-09-18: failed component rod body at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.04, Goodman 1.077, impacts/day 345, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
