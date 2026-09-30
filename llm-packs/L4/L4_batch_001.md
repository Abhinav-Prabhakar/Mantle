# L4 pump_unseat_incident - batch 001 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L4/replies/L4_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L4-00000 .. L4-00019 (each has an `item_id` you must echo).

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

### item_id: L4-00000
Write a pump-unseating incident note for BGW-48 on 2025-12-20 at cycle day 67: symptoms seen on the dyno card and in production, crude viscosity at the time 799 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00001
Write a pump-unseating incident note for BGW-02 on 2026-02-05 at cycle day 117: symptoms seen on the dyno card and in production, crude viscosity at the time 5392 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00002
Write a pump-unseating incident note for BGW-40 on 2025-06-22 at cycle day 84: symptoms seen on the dyno card and in production, crude viscosity at the time 2093 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00003
Write a pump-unseating incident note for BGW-56 on 2024-10-04 at cycle day 110: symptoms seen on the dyno card and in production, crude viscosity at the time 6010 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00004
Write a pump-unseating incident note for BGW-06 on 2026-07-28 at cycle day 102: symptoms seen on the dyno card and in production, crude viscosity at the time 3764 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00005
Write a pump-unseating incident note for BGW-06 on 2024-01-30 at cycle day 90: symptoms seen on the dyno card and in production, crude viscosity at the time 2425 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00006
Write a pump-unseating incident note for BGW-25 on 2025-03-10 at cycle day 75: symptoms seen on the dyno card and in production, crude viscosity at the time 1751 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00007
Write a pump-unseating incident note for BGW-28 on 2025-04-23 at cycle day 68: symptoms seen on the dyno card and in production, crude viscosity at the time 1177 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00008
Write a pump-unseating incident note for BGW-03 on 2026-08-20 at cycle day 106: symptoms seen on the dyno card and in production, crude viscosity at the time 4635 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00009
Write a pump-unseating incident note for BGW-26 on 2025-07-17 at cycle day 107: symptoms seen on the dyno card and in production, crude viscosity at the time 4508 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00010
Write a pump-unseating incident note for BGW-28 on 2025-04-23 at cycle day 68: symptoms seen on the dyno card and in production, crude viscosity at the time 1177 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00011
Write a pump-unseating incident note for BGW-48 on 2025-12-20 at cycle day 67: symptoms seen on the dyno card and in production, crude viscosity at the time 799 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00012
Write a pump-unseating incident note for BGW-26 on 2025-07-17 at cycle day 107: symptoms seen on the dyno card and in production, crude viscosity at the time 4508 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00013
Write a pump-unseating incident note for BGW-23 on 2026-07-26 at cycle day 119: symptoms seen on the dyno card and in production, crude viscosity at the time 6148 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00014
Write a pump-unseating incident note for BGW-32 on 2025-09-13 at cycle day 109: symptoms seen on the dyno card and in production, crude viscosity at the time 5147 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00015
Write a pump-unseating incident note for BGW-56 on 2024-02-07 at cycle day 92: symptoms seen on the dyno card and in production, crude viscosity at the time 3060 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00016
Write a pump-unseating incident note for BGW-17 on 2026-02-21 at cycle day 78: symptoms seen on the dyno card and in production, crude viscosity at the time 1902 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00017
Write a pump-unseating incident note for BGW-03 on 2026-08-20 at cycle day 106: symptoms seen on the dyno card and in production, crude viscosity at the time 4635 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00018
Write a pump-unseating incident note for BGW-02 on 2024-02-12 at cycle day 58: symptoms seen on the dyno card and in production, crude viscosity at the time 416 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

### item_id: L4-00019
Write a pump-unseating incident note for BGW-10 on 2024-04-17 at cycle day 101: symptoms seen on the dyno card and in production, crude viscosity at the time 4753 cP, hold-down type, actions taken (rod pull, reseat, hold-down change), time lost, and a one-line lesson.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
