# L3 rod_failure_report - batch 014 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_014.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00156 .. L3-00167 (each has an `item_id` you must echo).

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

### item_id: L3-00156
Write a rod-string failure report for BGW-18 on 2026-08-09: failed component rod pin/coupling at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.48, Goodman 1.176, impacts/day 5940, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00157
Write a rod-string failure report for BGW-15 on 2026-09-24: failed component pony rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.4, Goodman 1.059, impacts/day 5189, corrosion index 0.48), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00158
Write a rod-string failure report for BGW-49 on 2025-10-12: failed component rod body at 3.81 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.03, Goodman 1.141, impacts/day 4593, corrosion index 0.17), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00159
Write a rod-string failure report for BGW-38 on 2026-02-26: failed component pony rod at 72.39 m, failure mode float-buckling, visual inspection notes, suspected root cause (consistent with float margin 0.24, Goodman 0.898, impacts/day 90, corrosion index 0.62), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00160
Write a rod-string failure report for BGW-11 on 2025-03-13: failed component rod pin/coupling at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.1, Goodman 1.153, impacts/day 4107, corrosion index 0.49), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00161
Write a rod-string failure report for BGW-06 on 2024-01-16: failed component polished rod at 57.15 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.08, Goodman 1.055, impacts/day 2451, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00162
Write a rod-string failure report for BGW-48 on 2024-07-10: failed component rod body at 41.91 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.18, Goodman 0.988, impacts/day 5314, corrosion index 0.38), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00163
Write a rod-string failure report for BGW-06 on 2023-12-05: failed component pony rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.09, Goodman 1.134, impacts/day 394, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00164
Write a rod-string failure report for BGW-51 on 2025-05-30: failed component pony rod at 34.29 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.24, Goodman 0.958, impacts/day 552, corrosion index 0.67), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00165
Write a rod-string failure report for BGW-14 on 2024-04-15: failed component polished rod at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.02, Goodman 0.964, impacts/day 2055, corrosion index 0.13), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00166
Write a rod-string failure report for BGW-06 on 2024-01-05: failed component polished rod at 95.25 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.01, Goodman 0.99, impacts/day 4243, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00167
Write a rod-string failure report for BGW-18 on 2026-09-04: failed component sinker bar at 95.25 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.07, Goodman 1.063, impacts/day 5709, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
