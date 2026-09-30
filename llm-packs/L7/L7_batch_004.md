# L7 alarm_narrative - batch 004 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_004.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00090 .. L7-00119 (each has an `item_id` you must echo).

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

### item_id: L7-00090
Explain alarm LOW_FLOWLINE_T raised on BGW-60 at 2026-04-28 05:15 IST with context {"load_kn": 47.7, "amps": 20.7, "thp_mpa": 0.6, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00091
Explain alarm HIGH_THP raised on BGW-58 at 2026-05-30 01:13 IST with context {"load_kn": 43.5, "amps": 28.0, "thp_mpa": 0.87, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00092
Explain alarm VFD_TRIP raised on BGW-38 at 2026-02-22 22:11 IST with context {"load_kn": 38.7, "amps": 27.2, "thp_mpa": 0.55, "spm": 6.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00093
Explain alarm LOW_FLOWLINE_T raised on BGW-46 at 2026-03-13 03:24 IST with context {"load_kn": 70.5, "amps": 17.6, "thp_mpa": 0.69, "spm": 4.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00094
Explain alarm ROD_FLOAT_RISK raised on BGW-50 at 2026-05-15 23:37 IST with context {"load_kn": 77.9, "amps": 10.0, "thp_mpa": 0.68, "spm": 6.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00095
Explain alarm HIGH_AMPS raised on BGW-48 at 2026-01-08 18:12 IST with context {"load_kn": 20.5, "amps": 26.8, "thp_mpa": 0.69, "spm": 4.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00096
Explain alarm GAS_LOCK raised on BGW-07 at 2026-06-09 12:00 IST with context {"load_kn": 102.0, "amps": 27.3, "thp_mpa": 0.69, "spm": 4.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00097
Explain alarm ROD_FLOAT_RISK raised on BGW-15 at 2026-03-03 23:42 IST with context {"load_kn": 65.6, "amps": 20.3, "thp_mpa": 1.04, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00098
Explain alarm GOODMAN_HIGH raised on BGW-35 at 2026-02-23 10:54 IST with context {"load_kn": 97.2, "amps": 23.4, "thp_mpa": 0.93, "spm": 6.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00099
Explain alarm LOW_FLOWLINE_T raised on BGW-18 at 2026-08-22 04:07 IST with context {"load_kn": 33.8, "amps": 18.0, "thp_mpa": 0.53, "spm": 6.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00100
Explain alarm GOODMAN_HIGH raised on BGW-08 at 2026-01-01 02:46 IST with context {"load_kn": 73.6, "amps": 31.2, "thp_mpa": 0.5, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00101
Explain alarm LOW_FLOWLINE_T raised on BGW-49 at 2026-09-05 01:29 IST with context {"load_kn": 37.0, "amps": 10.3, "thp_mpa": 0.48, "spm": 6.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00102
Explain alarm LOW_FLOWLINE_T raised on BGW-23 at 2026-08-10 04:53 IST with context {"load_kn": 60.5, "amps": 29.8, "thp_mpa": 1.14, "spm": 3.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00103
Explain alarm GAS_LOCK raised on BGW-02 at 2026-04-17 15:09 IST with context {"load_kn": 80.2, "amps": 22.2, "thp_mpa": 0.88, "spm": 5.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00104
Explain alarm LOW_FLOWLINE_T raised on BGW-14 at 2026-08-12 22:52 IST with context {"load_kn": 67.7, "amps": 11.1, "thp_mpa": 0.93, "spm": 7.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00105
Explain alarm VFD_TRIP raised on BGW-38 at 2026-01-20 17:29 IST with context {"load_kn": 34.9, "amps": 9.6, "thp_mpa": 0.6, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00106
Explain alarm GAS_LOCK raised on BGW-05 at 2026-04-09 11:57 IST with context {"load_kn": 28.6, "amps": 20.0, "thp_mpa": 0.75, "spm": 3.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00107
Explain alarm VFD_TRIP raised on BGW-34 at 2026-01-09 15:03 IST with context {"load_kn": 65.4, "amps": 22.0, "thp_mpa": 1.06, "spm": 3.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00108
Explain alarm GAS_LOCK raised on BGW-60 at 2026-06-20 16:24 IST with context {"load_kn": 36.1, "amps": 31.0, "thp_mpa": 0.88, "spm": 6.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00109
Explain alarm LOW_FLOWLINE_T raised on BGW-06 at 2026-04-17 14:07 IST with context {"load_kn": 72.9, "amps": 8.5, "thp_mpa": 0.8, "spm": 7.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00110
Explain alarm GAS_LOCK raised on BGW-58 at 2026-05-29 06:36 IST with context {"load_kn": 54.5, "amps": 22.9, "thp_mpa": 0.57, "spm": 7.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00111
Explain alarm HIGH_THP raised on BGW-01 at 2026-03-29 14:58 IST with context {"load_kn": 33.9, "amps": 26.7, "thp_mpa": 1.04, "spm": 5.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00112
Explain alarm ROD_FLOAT_RISK raised on BGW-49 at 2026-02-14 18:30 IST with context {"load_kn": 83.9, "amps": 30.2, "thp_mpa": 0.65, "spm": 6.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00113
Explain alarm VFD_TRIP raised on BGW-32 at 2026-03-28 18:23 IST with context {"load_kn": 62.4, "amps": 20.8, "thp_mpa": 1.09, "spm": 5.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00114
Explain alarm PUMP_OFF raised on BGW-13 at 2026-07-30 21:50 IST with context {"load_kn": 79.7, "amps": 30.1, "thp_mpa": 1.11, "spm": 7.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00115
Explain alarm GAS_LOCK raised on BGW-57 at 2026-06-23 16:18 IST with context {"load_kn": 67.0, "amps": 29.0, "thp_mpa": 0.8, "spm": 4.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00116
Explain alarm GAS_LOCK raised on BGW-50 at 2026-03-31 09:18 IST with context {"load_kn": 62.5, "amps": 28.3, "thp_mpa": 0.43, "spm": 6.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00117
Explain alarm VFD_TRIP raised on BGW-41 at 2026-02-11 14:15 IST with context {"load_kn": 62.1, "amps": 29.4, "thp_mpa": 0.51, "spm": 4.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00118
Explain alarm LOW_LOAD raised on BGW-49 at 2026-05-07 20:02 IST with context {"load_kn": 25.6, "amps": 27.5, "thp_mpa": 0.47, "spm": 5.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00119
Explain alarm LOW_FLOWLINE_T raised on BGW-09 at 2026-08-06 22:06 IST with context {"load_kn": 90.9, "amps": 8.7, "thp_mpa": 0.45, "spm": 5.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
