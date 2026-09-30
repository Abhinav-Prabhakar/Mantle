# L3 rod_failure_report - batch 006 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L3/replies/L3_batch_006.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L3-00060 .. L3-00071 (each has an `item_id` you must echo).

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

### item_id: L3-00060
Write a rod-string failure report for BGW-58 on 2024-04-27: failed component pony rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.4, Goodman 0.985, impacts/day 1464, corrosion index 0.79), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00061
Write a rod-string failure report for BGW-33 on 2024-09-02: failed component rod pin/coupling at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.04, Goodman 1.024, impacts/day 5053, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00062
Write a rod-string failure report for BGW-18 on 2026-01-12: failed component rod body at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.36, Goodman 1.08, impacts/day 3228, corrosion index 0.68), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00063
Write a rod-string failure report for BGW-30 on 2026-09-19: failed component rod pin/coupling at 528.283 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin 0.15, Goodman 0.8, impacts/day 406, corrosion index 0.33), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00064
Write a rod-string failure report for BGW-21 on 2026-06-12: failed component sinker bar at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.45, Goodman 1.032, impacts/day 706, corrosion index 0.25), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00065
Write a rod-string failure report for BGW-53 on 2025-03-30: failed component polished rod at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.44, Goodman 1.137, impacts/day 2525, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00066
Write a rod-string failure report for BGW-23 on 2025-10-12: failed component pony rod at 11.43 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin -0.01, Goodman 1.066, impacts/day 5442, corrosion index 0.28), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00067
Write a rod-string failure report for BGW-48 on 2025-08-11: failed component rod pin/coupling at 541.606 m, failure mode tubing leak at collar, visual inspection notes, suspected root cause (consistent with float margin 0.24, Goodman 0.8, impacts/day 978, corrosion index 0.38), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00068
Write a rod-string failure report for BGW-06 on 2024-01-17: failed component sinker bar at 110.49 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.39, Goodman 0.963, impacts/day 5087, corrosion index 0.71), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00069
Write a rod-string failure report for BGW-33 on 2024-08-24: failed component rod body at 19.05 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.46, Goodman 1.072, impacts/day 5480, corrosion index 0.78), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00070
Write a rod-string failure report for BGW-53 on 2026-04-27: failed component polished rod at 49.53 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.14, Goodman 1.013, impacts/day 5887, corrosion index 0.32), rods replaced, downtime hours, cost INR, recommendations.

### item_id: L3-00071
Write a rod-string failure report for BGW-49 on 2025-11-04: failed component sinker bar at 26.67 m, failure mode fatigue, visual inspection notes, suspected root cause (consistent with float margin 0.22, Goodman 1.097, impacts/day 4013, corrosion index 0.17), rods replaced, downtime hours, cost INR, recommendations.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
