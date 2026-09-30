# L4 pump_unseat_incident - batch 004 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L4/replies/L4_batch_004.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L4-00060 .. L4-00079 (each has an `item_id` you must echo).

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

### item_id: L4-00060
Write a pump-unseating incident note for BGW-32 on 2024-08-21 at cycle day 77: symptoms seen on the dyno card and in production, crude viscosity at the time 1693 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00061
Write a pump-unseating incident note for BGW-30 on 2025-05-15 at cycle day 79: symptoms seen on the dyno card and in production, crude viscosity at the time 1419 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00062
Write a pump-unseating incident note for BGW-12 on 2025-02-27 at cycle day 83: symptoms seen on the dyno card and in production, crude viscosity at the time 1496 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00063
Write a pump-unseating incident note for BGW-41 on 2023-07-03 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 5027 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00064
Write a pump-unseating incident note for BGW-03 on 2026-08-20 at cycle day 106: symptoms seen on the dyno card and in production, crude viscosity at the time 4635 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00065
Write a pump-unseating incident note for BGW-23 on 2024-11-26 at cycle day 64: symptoms seen on the dyno card and in production, crude viscosity at the time 931 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00066
Write a pump-unseating incident note for BGW-25 on 2023-11-20 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 4600 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00067
Write a pump-unseating incident note for BGW-48 on 2024-01-18 at cycle day 72: symptoms seen on the dyno card and in production, crude viscosity at the time 966 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00068
Write a pump-unseating incident note for BGW-45 on 2026-05-03 at cycle day 39: symptoms seen on the dyno card and in production, crude viscosity at the time 144 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00069
Write a pump-unseating incident note for BGW-56 on 2025-09-25 at cycle day 40: symptoms seen on the dyno card and in production, crude viscosity at the time 226 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00070
Write a pump-unseating incident note for BGW-32 on 2024-08-21 at cycle day 77: symptoms seen on the dyno card and in production, crude viscosity at the time 1693 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00071
Write a pump-unseating incident note for BGW-41 on 2025-08-03 at cycle day 39: symptoms seen on the dyno card and in production, crude viscosity at the time 160 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00072
Write a pump-unseating incident note for BGW-05 on 2026-06-28 at cycle day 75: symptoms seen on the dyno card and in production, crude viscosity at the time 1139 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00073
Write a pump-unseating incident note for BGW-01 on 2025-09-05 at cycle day 95: symptoms seen on the dyno card and in production, crude viscosity at the time 3267 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00074
Write a pump-unseating incident note for BGW-17 on 2026-02-21 at cycle day 78: symptoms seen on the dyno card and in production, crude viscosity at the time 1902 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00075
Write a pump-unseating incident note for BGW-54 on 2025-07-06 at cycle day 111: symptoms seen on the dyno card and in production, crude viscosity at the time 5181 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00076
Write a pump-unseating incident note for BGW-29 on 2025-01-18 at cycle day 86: symptoms seen on the dyno card and in production, crude viscosity at the time 3311 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00077
Write a pump-unseating incident note for BGW-21 on 2024-04-19 at cycle day 77: symptoms seen on the dyno card and in production, crude viscosity at the time 1767 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00078
Write a pump-unseating incident note for BGW-56 on 2024-02-07 at cycle day 92: symptoms seen on the dyno card and in production, crude viscosity at the time 3060 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00079
Write a pump-unseating incident note for BGW-53 on 2024-11-04 at cycle day 63: symptoms seen on the dyno card and in production, crude viscosity at the time 865 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
