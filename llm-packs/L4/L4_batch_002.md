# L4 pump_unseat_incident - batch 002 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L4/replies/L4_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L4-00020 .. L4-00039 (each has an `item_id` you must echo).

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

### item_id: L4-00020
Write a pump-unseating incident note for BGW-06 on 2026-07-28 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 3764 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00021
Write a pump-unseating incident note for BGW-03 on 2026-08-20 at cycle day 106: symptoms seen on the dyno card and in production, crude viscosity at the time 4635 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00022
Write a pump-unseating incident note for BGW-52 on 2026-01-03 at cycle day 64: symptoms seen on the dyno card and in production, crude viscosity at the time 580 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00023
Write a pump-unseating incident note for BGW-25 on 2025-08-03 at cycle day 92: symptoms seen on the dyno card and in production, crude viscosity at the time 3997 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00024
Write a pump-unseating incident note for BGW-56 on 2024-10-04 at cycle day 110: symptoms seen on the dyno card and in production, crude viscosity at the time 6010 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00025
Write a pump-unseating incident note for BGW-27 on 2025-01-12 at cycle day 76: symptoms seen on the dyno card and in production, crude viscosity at the time 1149 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00026
Write a pump-unseating incident note for BGW-40 on 2026-02-20 at cycle day 68: symptoms seen on the dyno card and in production, crude viscosity at the time 980 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00027
Write a pump-unseating incident note for BGW-42 on 2025-09-11 at cycle day 74: symptoms seen on the dyno card and in production, crude viscosity at the time 1427 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00028
Write a pump-unseating incident note for BGW-04 on 2025-09-14 at cycle day 77: symptoms seen on the dyno card and in production, crude viscosity at the time 1603 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00029
Write a pump-unseating incident note for BGW-25 on 2024-08-07 at cycle day 96: symptoms seen on the dyno card and in production, crude viscosity at the time 4593 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00030
Write a pump-unseating incident note for BGW-27 on 2025-01-12 at cycle day 76: symptoms seen on the dyno card and in production, crude viscosity at the time 1149 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00031
Write a pump-unseating incident note for BGW-10 on 2026-04-05 at cycle day 52: symptoms seen on the dyno card and in production, crude viscosity at the time 341 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00032
Write a pump-unseating incident note for BGW-41 on 2025-08-03 at cycle day 39: symptoms seen on the dyno card and in production, crude viscosity at the time 160 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00033
Write a pump-unseating incident note for BGW-06 on 2026-07-28 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 3764 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00034
Write a pump-unseating incident note for BGW-48 on 2025-12-20 at cycle day 67: symptoms seen on the dyno card and in production, crude viscosity at the time 799 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00035
Write a pump-unseating incident note for BGW-42 on 2025-09-11 at cycle day 74: symptoms seen on the dyno card and in production, crude viscosity at the time 1427 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00036
Write a pump-unseating incident note for BGW-40 on 2024-12-31 at cycle day 118: symptoms seen on the dyno card and in production, crude viscosity at the time 6296 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00037
Write a pump-unseating incident note for BGW-27 on 2026-08-21 at cycle day 51: symptoms seen on the dyno card and in production, crude viscosity at the time 314 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00038
Write a pump-unseating incident note for BGW-45 on 2026-05-03 at cycle day 39: symptoms seen on the dyno card and in production, crude viscosity at the time 144 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00039
Write a pump-unseating incident note for BGW-26 on 2024-03-23 at cycle day 118: symptoms seen on the dyno card and in production, crude viscosity at the time 6877 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
