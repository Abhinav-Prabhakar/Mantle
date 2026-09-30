# L4 pump_unseat_incident - batch 009 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L4/replies/L4_batch_009.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L4-00160 .. L4-00179 (each has an `item_id` you must echo).

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

### item_id: L4-00160
Write a pump-unseating incident note for BGW-17 on 2026-02-21 at cycle day 78: symptoms seen on the dyno card and in production, crude viscosity at the time 1902 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00161
Write a pump-unseating incident note for BGW-52 on 2026-01-03 at cycle day 64: symptoms seen on the dyno card and in production, crude viscosity at the time 580 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00162
Write a pump-unseating incident note for BGW-41 on 2025-05-16 at cycle day 66: symptoms seen on the dyno card and in production, crude viscosity at the time 987 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00163
Write a pump-unseating incident note for BGW-45 on 2026-05-03 at cycle day 39: symptoms seen on the dyno card and in production, crude viscosity at the time 144 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00164
Write a pump-unseating incident note for BGW-54 on 2025-07-06 at cycle day 111: symptoms seen on the dyno card and in production, crude viscosity at the time 5181 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00165
Write a pump-unseating incident note for BGW-25 on 2023-11-20 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 4600 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00166
Write a pump-unseating incident note for BGW-19 on 2026-06-07 at cycle day 82: symptoms seen on the dyno card and in production, crude viscosity at the time 1926 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00167
Write a pump-unseating incident note for BGW-01 on 2025-09-05 at cycle day 95: symptoms seen on the dyno card and in production, crude viscosity at the time 3267 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00168
Write a pump-unseating incident note for BGW-02 on 2024-02-12 at cycle day 58: symptoms seen on the dyno card and in production, crude viscosity at the time 416 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00169
Write a pump-unseating incident note for BGW-20 on 2025-04-26 at cycle day 33: symptoms seen on the dyno card and in production, crude viscosity at the time 121 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00170
Write a pump-unseating incident note for BGW-10 on 2026-07-27 at cycle day 90: symptoms seen on the dyno card and in production, crude viscosity at the time 2890 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00171
Write a pump-unseating incident note for BGW-35 on 2026-06-19 at cycle day 112: symptoms seen on the dyno card and in production, crude viscosity at the time 5682 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00172
Write a pump-unseating incident note for BGW-32 on 2026-04-18 at cycle day 57: symptoms seen on the dyno card and in production, crude viscosity at the time 516 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00173
Write a pump-unseating incident note for BGW-17 on 2026-07-01 at cycle day 82: symptoms seen on the dyno card and in production, crude viscosity at the time 2272 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00174
Write a pump-unseating incident note for BGW-40 on 2026-02-20 at cycle day 68: symptoms seen on the dyno card and in production, crude viscosity at the time 980 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00175
Write a pump-unseating incident note for BGW-39 on 2025-12-11 at cycle day 43: symptoms seen on the dyno card and in production, crude viscosity at the time 161 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00176
Write a pump-unseating incident note for BGW-04 on 2025-09-14 at cycle day 77: symptoms seen on the dyno card and in production, crude viscosity at the time 1603 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00177
Write a pump-unseating incident note for BGW-56 on 2024-12-24 at cycle day 62: symptoms seen on the dyno card and in production, crude viscosity at the time 618 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00178
Write a pump-unseating incident note for BGW-41 on 2025-05-16 at cycle day 66: symptoms seen on the dyno card and in production, crude viscosity at the time 987 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00179
Write a pump-unseating incident note for BGW-07 on 2025-03-09 at cycle day 98: symptoms seen on the dyno card and in production, crude viscosity at the time 3555 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
