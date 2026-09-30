# L4 pump_unseat_incident - batch 006 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L4/replies/L4_batch_006.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L4-00100 .. L4-00119 (each has an `item_id` you must echo).

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

### item_id: L4-00100
Write a pump-unseating incident note for BGW-56 on 2026-02-16 at cycle day 110: symptoms seen on the dyno card and in production, crude viscosity at the time 5871 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00101
Write a pump-unseating incident note for BGW-56 on 2024-10-04 at cycle day 110: symptoms seen on the dyno card and in production, crude viscosity at the time 6010 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00102
Write a pump-unseating incident note for BGW-12 on 2025-02-27 at cycle day 83: symptoms seen on the dyno card and in production, crude viscosity at the time 1496 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00103
Write a pump-unseating incident note for BGW-25 on 2025-11-09 at cycle day 84: symptoms seen on the dyno card and in production, crude viscosity at the time 2505 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00104
Write a pump-unseating incident note for BGW-54 on 2025-05-18 at cycle day 62: symptoms seen on the dyno card and in production, crude viscosity at the time 642 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00105
Write a pump-unseating incident note for BGW-52 on 2026-01-03 at cycle day 64: symptoms seen on the dyno card and in production, crude viscosity at the time 580 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00106
Write a pump-unseating incident note for BGW-27 on 2026-08-21 at cycle day 51: symptoms seen on the dyno card and in production, crude viscosity at the time 314 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00107
Write a pump-unseating incident note for BGW-41 on 2023-07-03 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 5027 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00108
Write a pump-unseating incident note for BGW-43 on 2026-06-15 at cycle day 103: symptoms seen on the dyno card and in production, crude viscosity at the time 4906 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00109
Write a pump-unseating incident note for BGW-54 on 2025-11-03 at cycle day 88: symptoms seen on the dyno card and in production, crude viscosity at the time 2487 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00110
Write a pump-unseating incident note for BGW-06 on 2026-07-28 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 3764 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00111
Write a pump-unseating incident note for BGW-01 on 2025-09-05 at cycle day 95: symptoms seen on the dyno card and in production, crude viscosity at the time 3267 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00112
Write a pump-unseating incident note for BGW-23 on 2023-03-24 at cycle day 100: symptoms seen on the dyno card and in production, crude viscosity at the time 4219 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00113
Write a pump-unseating incident note for BGW-02 on 2024-02-12 at cycle day 58: symptoms seen on the dyno card and in production, crude viscosity at the time 416 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00114
Write a pump-unseating incident note for BGW-12 on 2025-02-27 at cycle day 83: symptoms seen on the dyno card and in production, crude viscosity at the time 1496 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00115
Write a pump-unseating incident note for BGW-30 on 2025-05-15 at cycle day 79: symptoms seen on the dyno card and in production, crude viscosity at the time 1419 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00116
Write a pump-unseating incident note for BGW-56 on 2024-12-24 at cycle day 62: symptoms seen on the dyno card and in production, crude viscosity at the time 618 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00117
Write a pump-unseating incident note for BGW-40 on 2025-06-22 at cycle day 84: symptoms seen on the dyno card and in production, crude viscosity at the time 2093 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00118
Write a pump-unseating incident note for BGW-09 on 2025-12-24 at cycle day 113: symptoms seen on the dyno card and in production, crude viscosity at the time 6477 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00119
Write a pump-unseating incident note for BGW-43 on 2026-06-15 at cycle day 103: symptoms seen on the dyno card and in production, crude viscosity at the time 4906 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
