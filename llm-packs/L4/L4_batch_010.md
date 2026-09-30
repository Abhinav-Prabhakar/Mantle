# L4 pump_unseat_incident - batch 010 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L4/replies/L4_batch_010.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L4-00180 .. L4-00199 (each has an `item_id` you must echo).

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

### item_id: L4-00180
Write a pump-unseating incident note for BGW-48 on 2025-12-20 at cycle day 67: symptoms seen on the dyno card and in production, crude viscosity at the time 799 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00181
Write a pump-unseating incident note for BGW-40 on 2026-02-20 at cycle day 68: symptoms seen on the dyno card and in production, crude viscosity at the time 980 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00182
Write a pump-unseating incident note for BGW-10 on 2024-09-03 at cycle day 108: symptoms seen on the dyno card and in production, crude viscosity at the time 5144 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00183
Write a pump-unseating incident note for BGW-18 on 2026-08-08 at cycle day 31: symptoms seen on the dyno card and in production, crude viscosity at the time 73 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00184
Write a pump-unseating incident note for BGW-31 on 2025-10-18 at cycle day 68: symptoms seen on the dyno card and in production, crude viscosity at the time 1138 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00185
Write a pump-unseating incident note for BGW-43 on 2026-06-15 at cycle day 103: symptoms seen on the dyno card and in production, crude viscosity at the time 4906 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00186
Write a pump-unseating incident note for BGW-17 on 2026-07-01 at cycle day 82: symptoms seen on the dyno card and in production, crude viscosity at the time 2272 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00187
Write a pump-unseating incident note for BGW-26 on 2024-03-23 at cycle day 118: symptoms seen on the dyno card and in production, crude viscosity at the time 6877 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00188
Write a pump-unseating incident note for BGW-33 on 2024-08-21 at cycle day 56: symptoms seen on the dyno card and in production, crude viscosity at the time 325 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00189
Write a pump-unseating incident note for BGW-53 on 2024-11-04 at cycle day 63: symptoms seen on the dyno card and in production, crude viscosity at the time 865 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00190
Write a pump-unseating incident note for BGW-32 on 2024-04-19 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 4238 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00191
Write a pump-unseating incident note for BGW-17 on 2026-02-21 at cycle day 78: symptoms seen on the dyno card and in production, crude viscosity at the time 1902 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00192
Write a pump-unseating incident note for BGW-21 on 2024-10-11 at cycle day 53: symptoms seen on the dyno card and in production, crude viscosity at the time 403 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00193
Write a pump-unseating incident note for BGW-32 on 2026-04-18 at cycle day 57: symptoms seen on the dyno card and in production, crude viscosity at the time 516 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00194
Write a pump-unseating incident note for BGW-39 on 2025-12-11 at cycle day 43: symptoms seen on the dyno card and in production, crude viscosity at the time 161 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00195
Write a pump-unseating incident note for BGW-32 on 2026-04-18 at cycle day 57: symptoms seen on the dyno card and in production, crude viscosity at the time 516 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00196
Write a pump-unseating incident note for BGW-41 on 2025-05-16 at cycle day 66: symptoms seen on the dyno card and in production, crude viscosity at the time 987 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00197
Write a pump-unseating incident note for BGW-56 on 2024-05-25 at cycle day 83: symptoms seen on the dyno card and in production, crude viscosity at the time 2119 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00198
Write a pump-unseating incident note for BGW-05 on 2025-03-02 at cycle day 98: symptoms seen on the dyno card and in production, crude viscosity at the time 3586 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00199
Write a pump-unseating incident note for BGW-23 on 2023-07-08 at cycle day 84: symptoms seen on the dyno card and in production, crude viscosity at the time 2131 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
