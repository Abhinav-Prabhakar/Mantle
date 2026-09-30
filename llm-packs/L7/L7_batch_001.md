# L7 alarm_narrative - batch 001 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00000 .. L7-00029 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "alarm_code", "well_id", "timestamp", "probable_cause", "checks", "urgency"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "alarm_code": {"type": "string"},
    "well_id": {"type": "string"},
    "timestamp": {"type": "string"},
    "probable_cause": {"type": "string"},
    "checks": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "urgency": {"type": "string", "enum": ["low", "med", "high"]}
  }
}
```

## Items (30)
Write one record per item, following the instruction under each item_id.

### item_id: L7-00000
Explain alarm PUMP_OFF raised on BGW-45 at 2026-02-20 14:38 IST with context {"load_kn": 89.9, "amps": 25.6, "thp_mpa": 0.65, "spm": 7.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00001
Explain alarm HIGH_AMPS raised on BGW-05 at 2026-05-23 23:32 IST with context {"load_kn": 49.8, "amps": 28.9, "thp_mpa": 1.07, "spm": 4.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00002
Explain alarm VFD_TRIP raised on BGW-17 at 2026-01-03 02:12 IST with context {"load_kn": 21.7, "amps": 15.2, "thp_mpa": 0.44, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00003
Explain alarm LOW_FLOWLINE_T raised on BGW-10 at 2026-04-03 06:25 IST with context {"load_kn": 50.3, "amps": 20.8, "thp_mpa": 0.9, "spm": 6.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00004
Explain alarm GAS_LOCK raised on BGW-23 at 2026-04-04 16:20 IST with context {"load_kn": 93.1, "amps": 19.8, "thp_mpa": 0.83, "spm": 7.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00005
Explain alarm GOODMAN_HIGH raised on BGW-37 at 2026-03-20 19:44 IST with context {"load_kn": 95.8, "amps": 19.6, "thp_mpa": 0.76, "spm": 3.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00006
Explain alarm HIGH_THP raised on BGW-35 at 2026-09-02 00:31 IST with context {"load_kn": 45.8, "amps": 26.1, "thp_mpa": 0.55, "spm": 4.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00007
Explain alarm HIGH_THP raised on BGW-15 at 2026-08-03 23:56 IST with context {"load_kn": 33.7, "amps": 28.1, "thp_mpa": 0.81, "spm": 6.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00008
Explain alarm GOODMAN_HIGH raised on BGW-14 at 2026-01-23 00:02 IST with context {"load_kn": 37.0, "amps": 21.9, "thp_mpa": 0.99, "spm": 6.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00009
Explain alarm GOODMAN_HIGH raised on BGW-51 at 2026-08-30 00:57 IST with context {"load_kn": 35.0, "amps": 28.4, "thp_mpa": 0.58, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00010
Explain alarm HIGH_AMPS raised on BGW-37 at 2026-07-09 22:59 IST with context {"load_kn": 28.7, "amps": 23.8, "thp_mpa": 0.56, "spm": 7.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00011
Explain alarm GAS_LOCK raised on BGW-25 at 2026-07-07 16:03 IST with context {"load_kn": 81.6, "amps": 18.0, "thp_mpa": 0.67, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00012
Explain alarm LOW_LOAD raised on BGW-42 at 2026-08-05 01:33 IST with context {"load_kn": 31.8, "amps": 23.2, "thp_mpa": 0.95, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00013
Explain alarm HIGH_AMPS raised on BGW-30 at 2026-06-19 13:19 IST with context {"load_kn": 21.2, "amps": 16.5, "thp_mpa": 0.77, "spm": 7.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00014
Explain alarm HIGH_THP raised on BGW-06 at 2026-01-29 15:33 IST with context {"load_kn": 55.9, "amps": 20.4, "thp_mpa": 0.69, "spm": 6.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00015
Explain alarm VFD_TRIP raised on BGW-01 at 2026-04-17 00:14 IST with context {"load_kn": 47.3, "amps": 18.9, "thp_mpa": 0.74, "spm": 4.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00016
Explain alarm GOODMAN_HIGH raised on BGW-30 at 2026-01-19 17:09 IST with context {"load_kn": 104.3, "amps": 12.8, "thp_mpa": 0.89, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00017
Explain alarm LOW_LOAD raised on BGW-41 at 2026-08-12 16:30 IST with context {"load_kn": 72.0, "amps": 20.4, "thp_mpa": 0.91, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00018
Explain alarm HIGH_THP raised on BGW-46 at 2026-07-04 18:52 IST with context {"load_kn": 51.3, "amps": 23.3, "thp_mpa": 0.45, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00019
Explain alarm ROD_FLOAT_RISK raised on BGW-04 at 2026-04-13 15:30 IST with context {"load_kn": 28.8, "amps": 27.7, "thp_mpa": 0.44, "spm": 6.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00020
Explain alarm HIGH_THP raised on BGW-44 at 2026-03-26 17:01 IST with context {"load_kn": 84.8, "amps": 16.1, "thp_mpa": 0.64, "spm": 6.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00021
Explain alarm ROD_FLOAT_RISK raised on BGW-60 at 2026-01-29 23:06 IST with context {"load_kn": 70.6, "amps": 18.2, "thp_mpa": 0.59, "spm": 3.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00022
Explain alarm VFD_TRIP raised on BGW-16 at 2026-07-25 11:47 IST with context {"load_kn": 77.9, "amps": 27.7, "thp_mpa": 0.93, "spm": 4.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00023
Explain alarm GAS_LOCK raised on BGW-43 at 2026-01-28 06:18 IST with context {"load_kn": 51.6, "amps": 16.4, "thp_mpa": 0.47, "spm": 6.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00024
Explain alarm PUMP_OFF raised on BGW-39 at 2026-05-29 18:20 IST with context {"load_kn": 58.7, "amps": 12.1, "thp_mpa": 0.55, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00025
Explain alarm LOAD_CELL_FAULT raised on BGW-35 at 2026-07-20 01:41 IST with context {"load_kn": 40.9, "amps": 9.7, "thp_mpa": 1.12, "spm": 5.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00026
Explain alarm HIGH_AMPS raised on BGW-49 at 2026-08-03 23:01 IST with context {"load_kn": 40.7, "amps": 10.5, "thp_mpa": 0.84, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00027
Explain alarm PUMP_OFF raised on BGW-34 at 2026-02-20 00:36 IST with context {"load_kn": 79.2, "amps": 15.0, "thp_mpa": 0.46, "spm": 3.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00028
Explain alarm GAS_LOCK raised on BGW-49 at 2026-05-11 16:45 IST with context {"load_kn": 78.1, "amps": 12.0, "thp_mpa": 0.44, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00029
Explain alarm LOAD_CELL_FAULT raised on BGW-37 at 2026-04-17 20:17 IST with context {"load_kn": 92.0, "amps": 25.4, "thp_mpa": 0.58, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
