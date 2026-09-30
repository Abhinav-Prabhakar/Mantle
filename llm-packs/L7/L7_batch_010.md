# L7 alarm_narrative - batch 010 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_010.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00270 .. L7-00299 (each has an `item_id` you must echo).

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

### item_id: L7-00270
Explain alarm HIGH_THP raised on BGW-41 at 2026-05-20 05:03 IST with context {"load_kn": 96.5, "amps": 15.1, "thp_mpa": 0.76, "spm": 3.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00271
Explain alarm HIGH_THP raised on BGW-10 at 2026-03-31 00:49 IST with context {"load_kn": 36.9, "amps": 9.6, "thp_mpa": 1.05, "spm": 3.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00272
Explain alarm LOW_FLOWLINE_T raised on BGW-15 at 2026-03-10 05:34 IST with context {"load_kn": 34.1, "amps": 19.3, "thp_mpa": 0.84, "spm": 3.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00273
Explain alarm GOODMAN_HIGH raised on BGW-45 at 2026-01-26 06:43 IST with context {"load_kn": 71.3, "amps": 22.8, "thp_mpa": 0.51, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00274
Explain alarm PUMP_OFF raised on BGW-59 at 2026-08-21 11:57 IST with context {"load_kn": 47.4, "amps": 15.7, "thp_mpa": 1.17, "spm": 7.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00275
Explain alarm LOW_FLOWLINE_T raised on BGW-34 at 2026-07-23 17:35 IST with context {"load_kn": 72.8, "amps": 9.5, "thp_mpa": 1.06, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00276
Explain alarm HIGH_THP raised on BGW-09 at 2026-06-21 17:44 IST with context {"load_kn": 68.0, "amps": 18.2, "thp_mpa": 0.92, "spm": 3.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00277
Explain alarm LOAD_CELL_FAULT raised on BGW-16 at 2026-05-22 23:52 IST with context {"load_kn": 72.4, "amps": 17.9, "thp_mpa": 1.08, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00278
Explain alarm LOAD_CELL_FAULT raised on BGW-12 at 2026-02-27 02:05 IST with context {"load_kn": 53.3, "amps": 17.6, "thp_mpa": 0.63, "spm": 6.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00279
Explain alarm VFD_TRIP raised on BGW-23 at 2026-08-04 18:45 IST with context {"load_kn": 36.9, "amps": 20.2, "thp_mpa": 0.79, "spm": 6.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00280
Explain alarm LOAD_CELL_FAULT raised on BGW-47 at 2026-01-29 20:28 IST with context {"load_kn": 27.5, "amps": 11.8, "thp_mpa": 1.08, "spm": 6.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00281
Explain alarm GAS_LOCK raised on BGW-26 at 2026-03-25 06:12 IST with context {"load_kn": 39.5, "amps": 15.6, "thp_mpa": 1.04, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00282
Explain alarm LOAD_CELL_FAULT raised on BGW-56 at 2026-01-20 19:28 IST with context {"load_kn": 39.2, "amps": 31.6, "thp_mpa": 1.03, "spm": 3.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00283
Explain alarm LOW_FLOWLINE_T raised on BGW-14 at 2026-08-18 19:22 IST with context {"load_kn": 47.3, "amps": 8.4, "thp_mpa": 0.58, "spm": 7.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00284
Explain alarm GOODMAN_HIGH raised on BGW-17 at 2026-05-20 23:34 IST with context {"load_kn": 68.4, "amps": 8.8, "thp_mpa": 0.82, "spm": 4.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00285
Explain alarm GOODMAN_HIGH raised on BGW-52 at 2026-06-16 11:36 IST with context {"load_kn": 29.1, "amps": 26.7, "thp_mpa": 1.01, "spm": 3.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00286
Explain alarm LOW_LOAD raised on BGW-31 at 2026-06-16 04:31 IST with context {"load_kn": 98.3, "amps": 23.5, "thp_mpa": 0.7, "spm": 5.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00287
Explain alarm HIGH_THP raised on BGW-18 at 2026-04-02 15:45 IST with context {"load_kn": 86.8, "amps": 15.7, "thp_mpa": 1.0, "spm": 5.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00288
Explain alarm LOW_FLOWLINE_T raised on BGW-19 at 2026-08-05 21:35 IST with context {"load_kn": 59.1, "amps": 24.5, "thp_mpa": 0.52, "spm": 4.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00289
Explain alarm HIGH_AMPS raised on BGW-03 at 2026-01-12 13:25 IST with context {"load_kn": 45.0, "amps": 25.3, "thp_mpa": 0.86, "spm": 4.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00290
Explain alarm LOAD_CELL_FAULT raised on BGW-21 at 2026-09-05 15:24 IST with context {"load_kn": 77.9, "amps": 21.1, "thp_mpa": 0.6, "spm": 3.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00291
Explain alarm PUMP_OFF raised on BGW-27 at 2026-09-11 02:00 IST with context {"load_kn": 34.3, "amps": 10.8, "thp_mpa": 0.7, "spm": 3.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00292
Explain alarm PUMP_OFF raised on BGW-11 at 2026-08-21 19:39 IST with context {"load_kn": 98.1, "amps": 22.2, "thp_mpa": 0.6, "spm": 5.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00293
Explain alarm LOW_LOAD raised on BGW-57 at 2026-09-16 12:52 IST with context {"load_kn": 77.6, "amps": 8.8, "thp_mpa": 0.89, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00294
Explain alarm GAS_LOCK raised on BGW-20 at 2026-08-07 21:52 IST with context {"load_kn": 95.3, "amps": 26.1, "thp_mpa": 0.54, "spm": 5.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00295
Explain alarm LOW_FLOWLINE_T raised on BGW-50 at 2026-09-16 07:25 IST with context {"load_kn": 21.2, "amps": 19.0, "thp_mpa": 1.01, "spm": 6.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00296
Explain alarm GAS_LOCK raised on BGW-35 at 2026-08-28 16:42 IST with context {"load_kn": 89.4, "amps": 19.8, "thp_mpa": 0.89, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00297
Explain alarm HIGH_THP raised on BGW-02 at 2026-01-02 06:22 IST with context {"load_kn": 45.5, "amps": 28.0, "thp_mpa": 1.09, "spm": 4.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00298
Explain alarm VFD_TRIP raised on BGW-54 at 2026-07-13 21:53 IST with context {"load_kn": 45.8, "amps": 12.0, "thp_mpa": 1.03, "spm": 3.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00299
Explain alarm PUMP_OFF raised on BGW-44 at 2026-07-13 06:12 IST with context {"load_kn": 92.5, "amps": 25.3, "thp_mpa": 0.92, "spm": 7.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
