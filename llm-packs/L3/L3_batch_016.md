# L3 rod_failure_report - batch 016 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_016.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00180 .. L3-00191 (each has an `item_id` you must echo).

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

### item_id: L3-00180
Write a rod-string failure report for BGW-28 on 2025-07-14: failed component rod pin/coupling at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.12, Goodman 1.005, impacts/day 124, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00181
Write a rod-string failure report for BGW-19 on 2023-09-13: failed component rod body at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.47, Goodman 1.051, impacts/day 656, corrosion index 0.47), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00182
Write a rod-string failure report for BGW-06 on 2024-01-25: failed component pony rod at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.05, Goodman 1.148, impacts/day 1052, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00183
Write a rod-string failure report for BGW-28 on 2024-12-29: failed component sinker bar at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.45, Goodman 1.135, impacts/day 4826, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00184
Write a rod-string failure report for BGW-28 on 2025-01-25: failed component pony rod at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.39, Goodman 1.105, impacts/day 3280, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00185
Write a rod-string failure report for BGW-18 on 2026-08-08: failed component pony rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.1, Goodman 1.205, impacts/day 3151, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00186
Write a rod-string failure report for BGW-28 on 2025-01-13: failed component sinker bar at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.42, Goodman 1.194, impacts/day 5, corrosion index 0.56), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00187
Write a rod-string failure report for BGW-58 on 2024-05-14: failed component polished rod at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.01, Goodman 0.963, impacts/day 5743, corrosion index 0.79), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00188
Write a rod-string failure report for BGW-23 on 2025-11-05: failed component polished rod at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.08, Goodman 1.03, impacts/day 1696, corrosion index 0.28), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00189
Write a rod-string failure report for BGW-11 on 2026-01-08: failed component polished rod at 125.73 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.22, Goodman 0.951, impacts/day 3080, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00190
Write a rod-string failure report for BGW-06 on 2023-12-14: failed component rod body at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.38, Goodman 1.082, impacts/day 1178, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00191
Write a rod-string failure report for BGW-58 on 2024-04-22: failed component pony rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.39, Goodman 0.974, impacts/day 39, corrosion index 0.79), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
