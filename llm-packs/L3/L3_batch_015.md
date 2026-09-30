# L3 rod_failure_report - batch 015 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_015.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00168 .. L3-00179 (each has an `item_id` you must echo).

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

### item_id: L3-00168
Write a rod-string failure report for BGW-33 on 2024-09-09: failed component sinker bar at 87.63 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.12, Goodman 0.963, impacts/day 5588, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00169
Write a rod-string failure report for BGW-38 on 2026-02-09: failed component sinker bar at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.26, Goodman 0.965, impacts/day 95, corrosion index 0.62), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00170
Write a rod-string failure report for BGW-38 on 2025-02-09: failed component rod pin/coupling at 740.151 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin -0.02, Goodman 0.8, impacts/day 0, corrosion index 0.62), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00171
Write a rod-string failure report for BGW-60 on 2025-12-09: failed component rod body at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.41, Goodman 0.932, impacts/day 4116, corrosion index 0.55), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00172
Write a rod-string failure report for BGW-57 on 2025-05-18: failed component rod body at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.31, Goodman 0.948, impacts/day 5973, corrosion index 0.41), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00173
Write a rod-string failure report for BGW-33 on 2024-09-02: failed component polished rod at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.05, Goodman 1.024, impacts/day 2627, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00174
Write a rod-string failure report for BGW-60 on 2025-12-09: failed component pony rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.38, Goodman 0.932, impacts/day 4749, corrosion index 0.55), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00175
Write a rod-string failure report for BGW-15 on 2026-09-21: failed component sinker bar at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.45, Goodman 1.083, impacts/day 3452, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00176
Write a rod-string failure report for BGW-11 on 2025-02-26: failed component pony rod at 41.91 m, failure mode float-buckling, visual inspection notes, suspected root cause (consistent with float margin 0.15, Goodman 1.112, impacts/day 1537, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00177
Write a rod-string failure report for BGW-35 on 2025-03-16: failed component rod pin/coupling at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.04, Goodman 1.017, impacts/day 2214, corrosion index 0.11), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00178
Write a rod-string failure report for BGW-18 on 2026-01-16: failed component pony rod at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.18, Goodman 1.068, impacts/day 213, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00179
Write a rod-string failure report for BGW-18 on 2026-08-21: failed component polished rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.43, Goodman 1.219, impacts/day 5126, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
