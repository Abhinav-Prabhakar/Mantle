# L7 alarm_narrative - batch 009 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_009.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00240 .. L7-00269 (each has an `item_id` you must echo).

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

### item_id: L7-00240
Explain alarm GOODMAN_HIGH raised on BGW-08 at 2026-03-17 03:05 IST with context {"load_kn": 32.3, "amps": 26.9, "thp_mpa": 1.03, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00241
Explain alarm GOODMAN_HIGH raised on BGW-25 at 2026-04-05 05:23 IST with context {"load_kn": 34.8, "amps": 21.3, "thp_mpa": 0.81, "spm": 7.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00242
Explain alarm HIGH_THP raised on BGW-36 at 2026-02-24 04:10 IST with context {"load_kn": 91.1, "amps": 16.7, "thp_mpa": 0.62, "spm": 3.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00243
Explain alarm LOAD_CELL_FAULT raised on BGW-55 at 2026-02-02 13:44 IST with context {"load_kn": 39.5, "amps": 30.7, "thp_mpa": 0.81, "spm": 5.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00244
Explain alarm PUMP_OFF raised on BGW-09 at 2026-04-29 22:26 IST with context {"load_kn": 27.9, "amps": 22.6, "thp_mpa": 0.64, "spm": 4.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00245
Explain alarm HIGH_AMPS raised on BGW-51 at 2026-08-14 17:16 IST with context {"load_kn": 101.9, "amps": 22.2, "thp_mpa": 0.7, "spm": 4.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00246
Explain alarm HIGH_AMPS raised on BGW-43 at 2026-03-04 18:39 IST with context {"load_kn": 82.6, "amps": 16.6, "thp_mpa": 0.47, "spm": 7.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00247
Explain alarm LOW_LOAD raised on BGW-29 at 2026-09-04 07:14 IST with context {"load_kn": 76.0, "amps": 32.0, "thp_mpa": 0.67, "spm": 4.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00248
Explain alarm VFD_TRIP raised on BGW-27 at 2026-09-02 04:34 IST with context {"load_kn": 99.4, "amps": 28.7, "thp_mpa": 1.06, "spm": 5.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00249
Explain alarm PUMP_OFF raised on BGW-47 at 2026-05-20 21:07 IST with context {"load_kn": 68.2, "amps": 12.3, "thp_mpa": 0.72, "spm": 4.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00250
Explain alarm GAS_LOCK raised on BGW-60 at 2026-02-08 10:16 IST with context {"load_kn": 71.9, "amps": 8.5, "thp_mpa": 0.77, "spm": 6.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00251
Explain alarm HIGH_THP raised on BGW-56 at 2026-07-31 06:15 IST with context {"load_kn": 90.9, "amps": 10.5, "thp_mpa": 0.7, "spm": 7.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00252
Explain alarm PUMP_OFF raised on BGW-37 at 2026-09-14 21:41 IST with context {"load_kn": 54.4, "amps": 25.7, "thp_mpa": 0.5, "spm": 5.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00253
Explain alarm HIGH_AMPS raised on BGW-17 at 2026-03-21 15:26 IST with context {"load_kn": 87.3, "amps": 26.0, "thp_mpa": 0.95, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00254
Explain alarm ROD_FLOAT_RISK raised on BGW-09 at 2026-03-05 15:04 IST with context {"load_kn": 45.8, "amps": 15.5, "thp_mpa": 0.85, "spm": 5.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00255
Explain alarm ROD_FLOAT_RISK raised on BGW-45 at 2026-08-11 12:55 IST with context {"load_kn": 68.0, "amps": 22.4, "thp_mpa": 1.14, "spm": 4.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00256
Explain alarm HIGH_AMPS raised on BGW-04 at 2026-09-16 19:53 IST with context {"load_kn": 83.9, "amps": 16.9, "thp_mpa": 0.51, "spm": 3.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00257
Explain alarm PUMP_OFF raised on BGW-37 at 2026-04-20 14:56 IST with context {"load_kn": 67.4, "amps": 28.2, "thp_mpa": 0.69, "spm": 4.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00258
Explain alarm LOAD_CELL_FAULT raised on BGW-40 at 2026-08-31 22:38 IST with context {"load_kn": 69.1, "amps": 8.9, "thp_mpa": 0.75, "spm": 4.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00259
Explain alarm ROD_FLOAT_RISK raised on BGW-29 at 2026-07-28 11:19 IST with context {"load_kn": 59.6, "amps": 8.6, "thp_mpa": 0.8, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00260
Explain alarm LOW_LOAD raised on BGW-38 at 2026-01-28 14:27 IST with context {"load_kn": 48.0, "amps": 24.6, "thp_mpa": 0.7, "spm": 7.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00261
Explain alarm GOODMAN_HIGH raised on BGW-28 at 2026-01-28 00:40 IST with context {"load_kn": 68.5, "amps": 16.5, "thp_mpa": 0.59, "spm": 6.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00262
Explain alarm ROD_FLOAT_RISK raised on BGW-01 at 2026-01-02 22:14 IST with context {"load_kn": 22.0, "amps": 25.5, "thp_mpa": 0.45, "spm": 3.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00263
Explain alarm LOAD_CELL_FAULT raised on BGW-11 at 2026-06-26 12:57 IST with context {"load_kn": 88.6, "amps": 27.5, "thp_mpa": 0.59, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00264
Explain alarm LOW_FLOWLINE_T raised on BGW-53 at 2026-02-26 11:36 IST with context {"load_kn": 37.2, "amps": 20.0, "thp_mpa": 0.41, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00265
Explain alarm HIGH_THP raised on BGW-37 at 2026-03-31 04:48 IST with context {"load_kn": 74.4, "amps": 15.8, "thp_mpa": 0.55, "spm": 7.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00266
Explain alarm PUMP_OFF raised on BGW-02 at 2026-08-03 09:30 IST with context {"load_kn": 77.8, "amps": 23.2, "thp_mpa": 1.11, "spm": 6.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00267
Explain alarm LOW_FLOWLINE_T raised on BGW-30 at 2026-07-14 19:23 IST with context {"load_kn": 26.5, "amps": 15.5, "thp_mpa": 0.95, "spm": 6.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00268
Explain alarm PUMP_OFF raised on BGW-30 at 2026-06-03 08:55 IST with context {"load_kn": 96.1, "amps": 8.5, "thp_mpa": 0.96, "spm": 7.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00269
Explain alarm ROD_FLOAT_RISK raised on BGW-44 at 2026-04-01 16:34 IST with context {"load_kn": 61.0, "amps": 14.4, "thp_mpa": 0.86, "spm": 6.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
