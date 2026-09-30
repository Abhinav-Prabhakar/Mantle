# L3 rod_failure_report - batch 001 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00000 .. L3-00011 (each has an `item_id` you must echo).

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

### item_id: L3-00000
Write a rod-string failure report for BGW-04 on 2025-08-11: failed component sinker bar at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.23, Goodman 0.988, impacts/day 1815, corrosion index 0.6), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00001
Write a rod-string failure report for BGW-18 on 2026-09-09: failed component pony rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.29, Goodman 1.219, impacts/day 2419, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00002
Write a rod-string failure report for BGW-33 on 2025-04-09: failed component polished rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.22, Goodman 0.898, impacts/day 3227, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00003
Write a rod-string failure report for BGW-19 on 2023-09-18: failed component sinker bar at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.29, Goodman 1.077, impacts/day 4330, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00004
Write a rod-string failure report for BGW-53 on 2025-08-06: failed component rod pin/coupling at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.14, Goodman 1.104, impacts/day 5124, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00005
Write a rod-string failure report for BGW-39 on 2026-06-24: failed component rod body at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.27, Goodman 1.046, impacts/day 205, corrosion index 0.14), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00006
Write a rod-string failure report for BGW-58 on 2024-06-03: failed component pony rod at 64.77 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.34, Goodman 0.906, impacts/day 421, corrosion index 0.79), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00007
Write a rod-string failure report for BGW-18 on 2026-09-01: failed component rod body at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.4, Goodman 1.219, impacts/day 5946, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00008
Write a rod-string failure report for BGW-06 on 2023-12-21: failed component polished rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.06, Goodman 1.148, impacts/day 1942, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00009
Write a rod-string failure report for BGW-18 on 2024-11-09: failed component rod body at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.12, Goodman 1.1, impacts/day 5325, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00010
Write a rod-string failure report for BGW-28 on 2024-12-21: failed component rod pin/coupling at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.34, Goodman 1.164, impacts/day 4381, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00011
Write a rod-string failure report for BGW-28 on 2025-01-30: failed component sinker bar at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.11, Goodman 1.164, impacts/day 5656, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
