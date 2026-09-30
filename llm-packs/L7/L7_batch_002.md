# L7 alarm_narrative - batch 002 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00030 .. L7-00059 (each has an `item_id` you must echo).

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

### item_id: L7-00030
Explain alarm LOW_FLOWLINE_T raised on BGW-17 at 2026-06-10 03:47 IST with context {"load_kn": 35.5, "amps": 16.1, "thp_mpa": 0.76, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00031
Explain alarm GOODMAN_HIGH raised on BGW-55 at 2026-06-05 09:03 IST with context {"load_kn": 33.4, "amps": 12.9, "thp_mpa": 1.2, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00032
Explain alarm LOAD_CELL_FAULT raised on BGW-06 at 2026-07-01 12:36 IST with context {"load_kn": 85.1, "amps": 12.0, "thp_mpa": 0.43, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00033
Explain alarm HIGH_AMPS raised on BGW-21 at 2026-03-06 08:11 IST with context {"load_kn": 62.4, "amps": 8.6, "thp_mpa": 0.98, "spm": 5.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00034
Explain alarm LOW_LOAD raised on BGW-06 at 2026-03-16 21:15 IST with context {"load_kn": 39.5, "amps": 19.1, "thp_mpa": 0.9, "spm": 6.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00035
Explain alarm HIGH_AMPS raised on BGW-44 at 2026-07-11 17:13 IST with context {"load_kn": 81.1, "amps": 31.2, "thp_mpa": 0.43, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00036
Explain alarm GOODMAN_HIGH raised on BGW-25 at 2026-03-29 21:07 IST with context {"load_kn": 76.1, "amps": 21.1, "thp_mpa": 0.63, "spm": 4.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00037
Explain alarm LOAD_CELL_FAULT raised on BGW-33 at 2026-04-07 06:37 IST with context {"load_kn": 25.0, "amps": 25.9, "thp_mpa": 1.0, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00038
Explain alarm GOODMAN_HIGH raised on BGW-12 at 2026-05-15 11:20 IST with context {"load_kn": 89.6, "amps": 19.3, "thp_mpa": 1.19, "spm": 4.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00039
Explain alarm HIGH_THP raised on BGW-47 at 2026-09-06 12:34 IST with context {"load_kn": 23.2, "amps": 20.7, "thp_mpa": 0.67, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00040
Explain alarm PUMP_OFF raised on BGW-06 at 2026-02-22 02:02 IST with context {"load_kn": 84.3, "amps": 15.0, "thp_mpa": 0.71, "spm": 7.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00041
Explain alarm LOW_LOAD raised on BGW-18 at 2026-05-02 13:46 IST with context {"load_kn": 34.3, "amps": 15.9, "thp_mpa": 0.6, "spm": 4.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00042
Explain alarm HIGH_AMPS raised on BGW-52 at 2026-03-15 04:09 IST with context {"load_kn": 90.9, "amps": 17.3, "thp_mpa": 1.0, "spm": 5.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00043
Explain alarm LOW_LOAD raised on BGW-42 at 2026-07-28 17:57 IST with context {"load_kn": 91.1, "amps": 18.7, "thp_mpa": 0.8, "spm": 6.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00044
Explain alarm HIGH_AMPS raised on BGW-23 at 2026-01-16 14:23 IST with context {"load_kn": 72.4, "amps": 28.9, "thp_mpa": 0.5, "spm": 6.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00045
Explain alarm LOW_LOAD raised on BGW-24 at 2026-08-22 17:22 IST with context {"load_kn": 46.6, "amps": 27.0, "thp_mpa": 0.95, "spm": 7.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00046
Explain alarm LOW_FLOWLINE_T raised on BGW-43 at 2026-04-13 13:42 IST with context {"load_kn": 64.8, "amps": 29.4, "thp_mpa": 0.78, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00047
Explain alarm HIGH_THP raised on BGW-41 at 2026-09-17 21:18 IST with context {"load_kn": 57.7, "amps": 13.2, "thp_mpa": 0.68, "spm": 3.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00048
Explain alarm LOW_LOAD raised on BGW-45 at 2026-03-27 09:25 IST with context {"load_kn": 21.9, "amps": 9.3, "thp_mpa": 0.5, "spm": 6.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00049
Explain alarm LOW_FLOWLINE_T raised on BGW-30 at 2026-07-01 08:11 IST with context {"load_kn": 96.2, "amps": 15.9, "thp_mpa": 0.65, "spm": 4.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00050
Explain alarm HIGH_THP raised on BGW-43 at 2026-03-03 10:42 IST with context {"load_kn": 57.1, "amps": 16.4, "thp_mpa": 1.14, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00051
Explain alarm VFD_TRIP raised on BGW-53 at 2026-08-20 16:36 IST with context {"load_kn": 88.4, "amps": 15.9, "thp_mpa": 0.9, "spm": 3.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00052
Explain alarm GAS_LOCK raised on BGW-51 at 2026-02-11 06:05 IST with context {"load_kn": 91.7, "amps": 27.2, "thp_mpa": 0.96, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00053
Explain alarm GOODMAN_HIGH raised on BGW-09 at 2026-08-22 11:00 IST with context {"load_kn": 86.9, "amps": 27.8, "thp_mpa": 0.53, "spm": 4.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00054
Explain alarm ROD_FLOAT_RISK raised on BGW-52 at 2026-03-14 14:52 IST with context {"load_kn": 61.1, "amps": 11.3, "thp_mpa": 1.01, "spm": 3.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00055
Explain alarm ROD_FLOAT_RISK raised on BGW-38 at 2026-02-05 00:30 IST with context {"load_kn": 40.2, "amps": 30.0, "thp_mpa": 0.87, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00056
Explain alarm GOODMAN_HIGH raised on BGW-54 at 2026-04-28 15:06 IST with context {"load_kn": 103.5, "amps": 10.9, "thp_mpa": 0.93, "spm": 4.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00057
Explain alarm VFD_TRIP raised on BGW-33 at 2026-08-22 11:15 IST with context {"load_kn": 78.2, "amps": 19.6, "thp_mpa": 1.03, "spm": 6.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00058
Explain alarm PUMP_OFF raised on BGW-45 at 2026-04-03 06:32 IST with context {"load_kn": 35.1, "amps": 15.4, "thp_mpa": 0.45, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00059
Explain alarm GOODMAN_HIGH raised on BGW-44 at 2026-07-02 13:06 IST with context {"load_kn": 72.1, "amps": 29.7, "thp_mpa": 1.08, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
