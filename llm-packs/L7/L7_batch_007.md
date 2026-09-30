# L7 alarm_narrative - batch 007 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_007.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00180 .. L7-00209 (each has an `item_id` you must echo).

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

### item_id: L7-00180
Explain alarm LOW_FLOWLINE_T raised on BGW-19 at 2026-07-26 14:44 IST with context {"load_kn": 51.1, "amps": 14.8, "thp_mpa": 0.6, "spm": 3.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00181
Explain alarm LOW_FLOWLINE_T raised on BGW-16 at 2026-03-02 00:43 IST with context {"load_kn": 34.0, "amps": 18.1, "thp_mpa": 0.79, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00182
Explain alarm LOW_LOAD raised on BGW-32 at 2026-07-15 03:31 IST with context {"load_kn": 24.2, "amps": 26.6, "thp_mpa": 0.56, "spm": 4.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00183
Explain alarm LOAD_CELL_FAULT raised on BGW-24 at 2026-04-03 00:35 IST with context {"load_kn": 74.9, "amps": 25.1, "thp_mpa": 0.79, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00184
Explain alarm HIGH_AMPS raised on BGW-28 at 2026-06-16 05:04 IST with context {"load_kn": 42.0, "amps": 17.7, "thp_mpa": 0.51, "spm": 4.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00185
Explain alarm PUMP_OFF raised on BGW-37 at 2026-02-10 15:30 IST with context {"load_kn": 27.2, "amps": 16.8, "thp_mpa": 0.71, "spm": 7.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00186
Explain alarm GAS_LOCK raised on BGW-46 at 2026-02-08 03:37 IST with context {"load_kn": 35.6, "amps": 25.9, "thp_mpa": 0.84, "spm": 7.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00187
Explain alarm HIGH_AMPS raised on BGW-05 at 2026-06-20 02:58 IST with context {"load_kn": 79.5, "amps": 19.9, "thp_mpa": 0.43, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00188
Explain alarm HIGH_THP raised on BGW-52 at 2026-09-16 23:36 IST with context {"load_kn": 98.7, "amps": 15.5, "thp_mpa": 0.68, "spm": 3.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00189
Explain alarm VFD_TRIP raised on BGW-28 at 2026-07-17 04:59 IST with context {"load_kn": 75.1, "amps": 26.7, "thp_mpa": 0.75, "spm": 6.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00190
Explain alarm PUMP_OFF raised on BGW-48 at 2026-06-26 09:11 IST with context {"load_kn": 61.1, "amps": 16.7, "thp_mpa": 0.87, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00191
Explain alarm LOAD_CELL_FAULT raised on BGW-01 at 2026-02-17 20:41 IST with context {"load_kn": 91.8, "amps": 12.0, "thp_mpa": 0.75, "spm": 4.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00192
Explain alarm HIGH_THP raised on BGW-28 at 2026-06-26 06:15 IST with context {"load_kn": 68.3, "amps": 14.0, "thp_mpa": 1.04, "spm": 6.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00193
Explain alarm LOW_FLOWLINE_T raised on BGW-53 at 2026-06-29 04:14 IST with context {"load_kn": 67.4, "amps": 20.5, "thp_mpa": 1.05, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00194
Explain alarm VFD_TRIP raised on BGW-05 at 2026-02-19 08:54 IST with context {"load_kn": 91.3, "amps": 13.2, "thp_mpa": 0.67, "spm": 5.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00195
Explain alarm HIGH_AMPS raised on BGW-04 at 2026-05-24 00:03 IST with context {"load_kn": 58.9, "amps": 26.4, "thp_mpa": 0.94, "spm": 6.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00196
Explain alarm ROD_FLOAT_RISK raised on BGW-29 at 2026-03-14 06:06 IST with context {"load_kn": 98.9, "amps": 16.7, "thp_mpa": 0.76, "spm": 4.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00197
Explain alarm ROD_FLOAT_RISK raised on BGW-52 at 2026-05-25 11:48 IST with context {"load_kn": 20.6, "amps": 29.4, "thp_mpa": 0.53, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00198
Explain alarm ROD_FLOAT_RISK raised on BGW-57 at 2026-03-29 12:28 IST with context {"load_kn": 49.4, "amps": 15.8, "thp_mpa": 0.41, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00199
Explain alarm LOW_LOAD raised on BGW-38 at 2026-09-15 16:19 IST with context {"load_kn": 66.0, "amps": 29.7, "thp_mpa": 0.52, "spm": 4.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00200
Explain alarm HIGH_AMPS raised on BGW-37 at 2026-04-08 03:44 IST with context {"load_kn": 96.6, "amps": 24.5, "thp_mpa": 0.7, "spm": 4.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00201
Explain alarm VFD_TRIP raised on BGW-59 at 2026-02-03 05:05 IST with context {"load_kn": 41.3, "amps": 18.6, "thp_mpa": 0.65, "spm": 6.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00202
Explain alarm GOODMAN_HIGH raised on BGW-10 at 2026-05-24 22:25 IST with context {"load_kn": 54.5, "amps": 11.4, "thp_mpa": 1.08, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00203
Explain alarm ROD_FLOAT_RISK raised on BGW-58 at 2026-03-03 01:12 IST with context {"load_kn": 57.6, "amps": 31.9, "thp_mpa": 0.93, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00204
Explain alarm HIGH_THP raised on BGW-39 at 2026-04-23 05:55 IST with context {"load_kn": 26.4, "amps": 29.7, "thp_mpa": 0.85, "spm": 6.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00205
Explain alarm GAS_LOCK raised on BGW-19 at 2026-01-03 04:53 IST with context {"load_kn": 77.2, "amps": 16.4, "thp_mpa": 0.64, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00206
Explain alarm LOAD_CELL_FAULT raised on BGW-11 at 2026-08-25 12:33 IST with context {"load_kn": 45.9, "amps": 15.9, "thp_mpa": 0.79, "spm": 5.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00207
Explain alarm GAS_LOCK raised on BGW-14 at 2026-02-21 19:24 IST with context {"load_kn": 25.4, "amps": 31.1, "thp_mpa": 0.92, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00208
Explain alarm LOW_FLOWLINE_T raised on BGW-50 at 2026-05-30 23:47 IST with context {"load_kn": 57.9, "amps": 18.7, "thp_mpa": 0.92, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00209
Explain alarm HIGH_THP raised on BGW-03 at 2026-03-25 13:51 IST with context {"load_kn": 79.3, "amps": 28.8, "thp_mpa": 0.53, "spm": 4.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
