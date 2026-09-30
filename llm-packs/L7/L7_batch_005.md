# L7 alarm_narrative - batch 005 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_005.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00120 .. L7-00149 (each has an `item_id` you must echo).

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

### item_id: L7-00120
Explain alarm GOODMAN_HIGH raised on BGW-15 at 2026-05-14 14:38 IST with context {"load_kn": 76.0, "amps": 27.3, "thp_mpa": 0.85, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00121
Explain alarm VFD_TRIP raised on BGW-02 at 2026-06-14 04:00 IST with context {"load_kn": 82.2, "amps": 13.4, "thp_mpa": 0.79, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00122
Explain alarm HIGH_THP raised on BGW-02 at 2026-09-01 19:48 IST with context {"load_kn": 46.7, "amps": 8.4, "thp_mpa": 0.6, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00123
Explain alarm VFD_TRIP raised on BGW-18 at 2026-04-03 09:47 IST with context {"load_kn": 94.3, "amps": 16.5, "thp_mpa": 1.12, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00124
Explain alarm ROD_FLOAT_RISK raised on BGW-19 at 2026-09-17 07:35 IST with context {"load_kn": 103.7, "amps": 19.3, "thp_mpa": 0.6, "spm": 6.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00125
Explain alarm ROD_FLOAT_RISK raised on BGW-03 at 2026-05-11 05:25 IST with context {"load_kn": 52.6, "amps": 10.0, "thp_mpa": 0.57, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00126
Explain alarm ROD_FLOAT_RISK raised on BGW-50 at 2026-05-13 04:23 IST with context {"load_kn": 46.6, "amps": 26.9, "thp_mpa": 1.16, "spm": 3.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00127
Explain alarm VFD_TRIP raised on BGW-43 at 2026-07-11 02:10 IST with context {"load_kn": 60.1, "amps": 15.2, "thp_mpa": 0.75, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00128
Explain alarm ROD_FLOAT_RISK raised on BGW-09 at 2026-04-24 06:19 IST with context {"load_kn": 68.1, "amps": 23.9, "thp_mpa": 0.99, "spm": 5.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00129
Explain alarm HIGH_AMPS raised on BGW-03 at 2026-02-03 22:01 IST with context {"load_kn": 24.6, "amps": 30.3, "thp_mpa": 1.2, "spm": 4.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00130
Explain alarm ROD_FLOAT_RISK raised on BGW-03 at 2026-09-07 01:09 IST with context {"load_kn": 83.1, "amps": 15.7, "thp_mpa": 1.15, "spm": 5.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00131
Explain alarm LOW_FLOWLINE_T raised on BGW-57 at 2026-02-06 23:07 IST with context {"load_kn": 43.1, "amps": 22.6, "thp_mpa": 0.41, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00132
Explain alarm PUMP_OFF raised on BGW-29 at 2026-07-04 20:31 IST with context {"load_kn": 90.2, "amps": 28.3, "thp_mpa": 0.49, "spm": 5.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00133
Explain alarm PUMP_OFF raised on BGW-29 at 2026-03-22 08:37 IST with context {"load_kn": 78.2, "amps": 21.5, "thp_mpa": 0.75, "spm": 3.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00134
Explain alarm GOODMAN_HIGH raised on BGW-37 at 2026-09-01 10:22 IST with context {"load_kn": 43.5, "amps": 30.0, "thp_mpa": 1.17, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00135
Explain alarm VFD_TRIP raised on BGW-31 at 2026-02-11 10:34 IST with context {"load_kn": 67.6, "amps": 26.5, "thp_mpa": 0.7, "spm": 6.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00136
Explain alarm ROD_FLOAT_RISK raised on BGW-17 at 2026-05-04 01:46 IST with context {"load_kn": 30.1, "amps": 23.3, "thp_mpa": 1.19, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00137
Explain alarm LOAD_CELL_FAULT raised on BGW-16 at 2026-08-18 09:46 IST with context {"load_kn": 24.5, "amps": 22.2, "thp_mpa": 1.15, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00138
Explain alarm HIGH_THP raised on BGW-55 at 2026-05-16 16:17 IST with context {"load_kn": 40.7, "amps": 9.3, "thp_mpa": 0.62, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00139
Explain alarm LOW_FLOWLINE_T raised on BGW-15 at 2026-06-18 06:57 IST with context {"load_kn": 38.9, "amps": 9.0, "thp_mpa": 0.49, "spm": 5.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00140
Explain alarm ROD_FLOAT_RISK raised on BGW-27 at 2026-03-28 03:41 IST with context {"load_kn": 38.5, "amps": 11.4, "thp_mpa": 0.8, "spm": 3.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00141
Explain alarm PUMP_OFF raised on BGW-16 at 2026-04-04 05:43 IST with context {"load_kn": 29.2, "amps": 10.2, "thp_mpa": 0.9, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00142
Explain alarm VFD_TRIP raised on BGW-16 at 2026-04-04 22:40 IST with context {"load_kn": 24.8, "amps": 19.7, "thp_mpa": 1.13, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00143
Explain alarm LOW_LOAD raised on BGW-14 at 2026-01-30 13:00 IST with context {"load_kn": 44.7, "amps": 23.0, "thp_mpa": 0.45, "spm": 4.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00144
Explain alarm VFD_TRIP raised on BGW-02 at 2026-02-01 16:31 IST with context {"load_kn": 36.2, "amps": 20.3, "thp_mpa": 0.79, "spm": 6.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00145
Explain alarm LOAD_CELL_FAULT raised on BGW-19 at 2026-06-21 19:21 IST with context {"load_kn": 56.9, "amps": 21.9, "thp_mpa": 0.96, "spm": 5.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00146
Explain alarm HIGH_THP raised on BGW-42 at 2026-08-12 22:08 IST with context {"load_kn": 75.9, "amps": 22.5, "thp_mpa": 1.05, "spm": 7.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00147
Explain alarm LOAD_CELL_FAULT raised on BGW-44 at 2026-03-11 19:18 IST with context {"load_kn": 48.7, "amps": 26.5, "thp_mpa": 0.52, "spm": 3.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00148
Explain alarm LOW_FLOWLINE_T raised on BGW-28 at 2026-06-30 15:34 IST with context {"load_kn": 35.3, "amps": 12.3, "thp_mpa": 0.91, "spm": 4.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00149
Explain alarm HIGH_THP raised on BGW-04 at 2026-08-02 00:28 IST with context {"load_kn": 45.9, "amps": 28.4, "thp_mpa": 0.82, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
