# L4 pump_unseat_incident - batch 008 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L4/replies/L4_batch_008.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L4-00140 .. L4-00159 (each has an `item_id` you must echo).

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

### item_id: L4-00140
Write a pump-unseating incident note for BGW-21 on 2024-10-11 at cycle day 53: symptoms seen on the dyno card and in production, crude viscosity at the time 403 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00141
Write a pump-unseating incident note for BGW-10 on 2024-04-17 at cycle day 101: symptoms seen on the dyno card and in production, crude viscosity at the time 4753 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00142
Write a pump-unseating incident note for BGW-56 on 2024-02-07 at cycle day 92: symptoms seen on the dyno card and in production, crude viscosity at the time 3060 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00143
Write a pump-unseating incident note for BGW-04 on 2025-09-14 at cycle day 77: symptoms seen on the dyno card and in production, crude viscosity at the time 1603 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00144
Write a pump-unseating incident note for BGW-17 on 2025-11-04 at cycle day 89: symptoms seen on the dyno card and in production, crude viscosity at the time 3011 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00145
Write a pump-unseating incident note for BGW-43 on 2026-06-15 at cycle day 103: symptoms seen on the dyno card and in production, crude viscosity at the time 4906 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00146
Write a pump-unseating incident note for BGW-53 on 2024-11-04 at cycle day 63: symptoms seen on the dyno card and in production, crude viscosity at the time 865 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00147
Write a pump-unseating incident note for BGW-56 on 2024-05-25 at cycle day 83: symptoms seen on the dyno card and in production, crude viscosity at the time 2119 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00148
Write a pump-unseating incident note for BGW-01 on 2025-09-05 at cycle day 95: symptoms seen on the dyno card and in production, crude viscosity at the time 3267 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00149
Write a pump-unseating incident note for BGW-56 on 2024-02-07 at cycle day 92: symptoms seen on the dyno card and in production, crude viscosity at the time 3060 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00150
Write a pump-unseating incident note for BGW-06 on 2024-01-30 at cycle day 90: symptoms seen on the dyno card and in production, crude viscosity at the time 2425 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00151
Write a pump-unseating incident note for BGW-10 on 2024-04-17 at cycle day 101: symptoms seen on the dyno card and in production, crude viscosity at the time 4753 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00152
Write a pump-unseating incident note for BGW-32 on 2025-09-13 at cycle day 109: symptoms seen on the dyno card and in production, crude viscosity at the time 5147 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00153
Write a pump-unseating incident note for BGW-17 on 2026-07-01 at cycle day 82: symptoms seen on the dyno card and in production, crude viscosity at the time 2272 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00154
Write a pump-unseating incident note for BGW-17 on 2025-11-04 at cycle day 89: symptoms seen on the dyno card and in production, crude viscosity at the time 3011 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00155
Write a pump-unseating incident note for BGW-10 on 2026-04-05 at cycle day 52: symptoms seen on the dyno card and in production, crude viscosity at the time 341 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00156
Write a pump-unseating incident note for BGW-42 on 2025-05-23 at cycle day 89: symptoms seen on the dyno card and in production, crude viscosity at the time 2696 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00157
Write a pump-unseating incident note for BGW-32 on 2024-08-21 at cycle day 77: symptoms seen on the dyno card and in production, crude viscosity at the time 1693 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00158
Write a pump-unseating incident note for BGW-56 on 2024-12-24 at cycle day 62: symptoms seen on the dyno card and in production, crude viscosity at the time 618 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00159
Write a pump-unseating incident note for BGW-01 on 2025-09-05 at cycle day 95: symptoms seen on the dyno card and in production, crude viscosity at the time 3267 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
