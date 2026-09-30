# L4 pump_unseat_incident - batch 003 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L4/replies/L4_batch_003.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L4-00040 .. L4-00059 (each has an `item_id` you must echo).

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

### item_id: L4-00040
Write a pump-unseating incident note for BGW-17 on 2026-02-21 at cycle day 78: symptoms seen on the dyno card and in production, crude viscosity at the time 1902 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00041
Write a pump-unseating incident note for BGW-23 on 2026-07-26 at cycle day 119: symptoms seen on the dyno card and in production, crude viscosity at the time 6148 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00042
Write a pump-unseating incident note for BGW-31 on 2025-10-18 at cycle day 68: symptoms seen on the dyno card and in production, crude viscosity at the time 1138 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00043
Write a pump-unseating incident note for BGW-03 on 2026-04-10 at cycle day 71: symptoms seen on the dyno card and in production, crude viscosity at the time 1271 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00044
Write a pump-unseating incident note for BGW-18 on 2026-08-08 at cycle day 31: symptoms seen on the dyno card and in production, crude viscosity at the time 73 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00045
Write a pump-unseating incident note for BGW-06 on 2024-12-21 at cycle day 38: symptoms seen on the dyno card and in production, crude viscosity at the time 91 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00046
Write a pump-unseating incident note for BGW-54 on 2025-05-18 at cycle day 62: symptoms seen on the dyno card and in production, crude viscosity at the time 642 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00047
Write a pump-unseating incident note for BGW-04 on 2025-09-14 at cycle day 77: symptoms seen on the dyno card and in production, crude viscosity at the time 1603 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00048
Write a pump-unseating incident note for BGW-41 on 2023-07-03 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 5027 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00049
Write a pump-unseating incident note for BGW-33 on 2024-08-21 at cycle day 56: symptoms seen on the dyno card and in production, crude viscosity at the time 325 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00050
Write a pump-unseating incident note for BGW-52 on 2026-01-03 at cycle day 64: symptoms seen on the dyno card and in production, crude viscosity at the time 580 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00051
Write a pump-unseating incident note for BGW-53 on 2025-12-13 at cycle day 24: symptoms seen on the dyno card and in production, crude viscosity at the time 40 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00052
Write a pump-unseating incident note for BGW-03 on 2026-08-20 at cycle day 106: symptoms seen on the dyno card and in production, crude viscosity at the time 4635 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00053
Write a pump-unseating incident note for BGW-01 on 2025-09-05 at cycle day 95: symptoms seen on the dyno card and in production, crude viscosity at the time 3267 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00054
Write a pump-unseating incident note for BGW-31 on 2025-10-18 at cycle day 68: symptoms seen on the dyno card and in production, crude viscosity at the time 1138 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00055
Write a pump-unseating incident note for BGW-32 on 2025-09-13 at cycle day 109: symptoms seen on the dyno card and in production, crude viscosity at the time 5147 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00056
Write a pump-unseating incident note for BGW-52 on 2026-01-03 at cycle day 64: symptoms seen on the dyno card and in production, crude viscosity at the time 580 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00057
Write a pump-unseating incident note for BGW-41 on 2026-02-02 at cycle day 96: symptoms seen on the dyno card and in production, crude viscosity at the time 3926 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00058
Write a pump-unseating incident note for BGW-35 on 2026-06-19 at cycle day 112: symptoms seen on the dyno card and in production, crude viscosity at the time 5682 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00059
Write a pump-unseating incident note for BGW-56 on 2024-05-25 at cycle day 83: symptoms seen on the dyno card and in production, crude viscosity at the time 2119 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
