# L3 rod_failure_report - batch 019 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_019.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00216 .. L3-00227 (each has an `item_id` you must echo).

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

### item_id: L3-00216
Write a rod-string failure report for BGW-33 on 2024-09-09: failed component rod pin/coupling at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.34, Goodman 1.06, impacts/day 2491, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00217
Write a rod-string failure report for BGW-53 on 2026-04-19: failed component polished rod at 64.77 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.13, Goodman 0.989, impacts/day 502, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00218
Write a rod-string failure report for BGW-11 on 2025-02-14: failed component sinker bar at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.05, Goodman 1.153, impacts/day 3796, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00219
Write a rod-string failure report for BGW-41 on 2022-10-13: failed component polished rod at 950.364 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin 0.34, Goodman 0.8, impacts/day 892, corrosion index 0.58), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00220
Write a rod-string failure report for BGW-11 on 2026-01-01: failed component rod body at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.29, Goodman 1.151, impacts/day 4607, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00221
Write a rod-string failure report for BGW-28 on 2024-12-24: failed component pony rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.24, Goodman 1.179, impacts/day 3672, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00222
Write a rod-string failure report for BGW-18 on 2026-09-22: failed component rod pin/coupling at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.2, Goodman 1.233, impacts/day 5173, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00223
Write a rod-string failure report for BGW-45 on 2024-04-23: failed component pony rod at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.11, Goodman 0.888, impacts/day 811, corrosion index 0.67), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00224
Write a rod-string failure report for BGW-19 on 2023-09-20: failed component pony rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.05, Goodman 1.064, impacts/day 660, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00225
Write a rod-string failure report for BGW-11 on 2026-01-03: failed component sinker bar at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.04, Goodman 1.137, impacts/day 214, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00226
Write a rod-string failure report for BGW-19 on 2023-09-19: failed component rod body at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.32, Goodman 1.038, impacts/day 3152, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00227
Write a rod-string failure report for BGW-39 on 2026-06-23: failed component pony rod at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.12, Goodman 1.008, impacts/day 5489, corrosion index 0.14), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
