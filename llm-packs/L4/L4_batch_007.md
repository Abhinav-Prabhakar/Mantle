# L4 pump_unseat_incident - batch 007 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L4/replies/L4_batch_007.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L4-00120 .. L4-00139 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "well_id", "date", "cycle_day", "symptoms", "viscosity_cp", "hold_down_type", "actions_taken", "time_lost_hours", "lesson"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "well_id": {"type": "string"},
    "date": {"type": "string"},
    "cycle_day": {"type": "integer", "minimum": 0, "maximum": 140},
    "symptoms": {"type": "string"},
    "viscosity_cp": {"type": "number", "minimum": 0.3},
    "hold_down_type": {"type": "string"},
    "actions_taken": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "time_lost_hours": {"type": "number", "minimum": 0, "maximum": 300},
    "lesson": {"type": "string"}
  }
}
```

## Items (20)
Write one record per item, following the instruction under each item_id.

### item_id: L4-00120
Write a pump-unseating incident note for BGW-42 on 2025-05-23 at cycle day 89: symptoms seen on the dyno card and in production, crude viscosity at the time 2696 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00121
Write a pump-unseating incident note for BGW-54 on 2025-05-18 at cycle day 62: symptoms seen on the dyno card and in production, crude viscosity at the time 642 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00122
Write a pump-unseating incident note for BGW-58 on 2024-06-02 at cycle day 86: symptoms seen on the dyno card and in production, crude viscosity at the time 2086 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00123
Write a pump-unseating incident note for BGW-20 on 2026-08-23 at cycle day 59: symptoms seen on the dyno card and in production, crude viscosity at the time 655 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00124
Write a pump-unseating incident note for BGW-09 on 2025-12-24 at cycle day 113: symptoms seen on the dyno card and in production, crude viscosity at the time 6477 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00125
Write a pump-unseating incident note for BGW-21 on 2024-04-19 at cycle day 77: symptoms seen on the dyno card and in production, crude viscosity at the time 1767 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00126
Write a pump-unseating incident note for BGW-39 on 2025-12-11 at cycle day 43: symptoms seen on the dyno card and in production, crude viscosity at the time 161 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00127
Write a pump-unseating incident note for BGW-23 on 2024-11-26 at cycle day 64: symptoms seen on the dyno card and in production, crude viscosity at the time 931 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00128
Write a pump-unseating incident note for BGW-10 on 2024-09-03 at cycle day 108: symptoms seen on the dyno card and in production, crude viscosity at the time 5144 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00129
Write a pump-unseating incident note for BGW-54 on 2025-07-06 at cycle day 111: symptoms seen on the dyno card and in production, crude viscosity at the time 5181 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00130
Write a pump-unseating incident note for BGW-43 on 2026-06-15 at cycle day 103: symptoms seen on the dyno card and in production, crude viscosity at the time 4906 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00131
Write a pump-unseating incident note for BGW-25 on 2025-11-09 at cycle day 84: symptoms seen on the dyno card and in production, crude viscosity at the time 2505 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00132
Write a pump-unseating incident note for BGW-43 on 2026-06-15 at cycle day 103: symptoms seen on the dyno card and in production, crude viscosity at the time 4906 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00133
Write a pump-unseating incident note for BGW-27 on 2026-08-21 at cycle day 51: symptoms seen on the dyno card and in production, crude viscosity at the time 314 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00134
Write a pump-unseating incident note for BGW-32 on 2024-04-19 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 4238 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00135
Write a pump-unseating incident note for BGW-27 on 2024-04-29 at cycle day 76: symptoms seen on the dyno card and in production, crude viscosity at the time 1434 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00136
Write a pump-unseating incident note for BGW-17 on 2025-11-04 at cycle day 89: symptoms seen on the dyno card and in production, crude viscosity at the time 3011 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00137
Write a pump-unseating incident note for BGW-41 on 2025-08-03 at cycle day 39: symptoms seen on the dyno card and in production, crude viscosity at the time 160 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00138
Write a pump-unseating incident note for BGW-17 on 2026-02-21 at cycle day 78: symptoms seen on the dyno card and in production, crude viscosity at the time 1902 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00139
Write a pump-unseating incident note for BGW-25 on 2025-03-10 at cycle day 75: symptoms seen on the dyno card and in production, crude viscosity at the time 1751 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
