# L7 alarm_narrative - batch 008 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_008.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00210 .. L7-00239 (each has an `item_id` you must echo).

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

### item_id: L7-00210
Explain alarm ROD_FLOAT_RISK raised on BGW-37 at 2026-03-13 23:14 IST with context {"load_kn": 43.3, "amps": 8.7, "thp_mpa": 1.2, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00211
Explain alarm HIGH_THP raised on BGW-16 at 2026-07-23 05:12 IST with context {"load_kn": 51.9, "amps": 28.9, "thp_mpa": 1.16, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00212
Explain alarm GAS_LOCK raised on BGW-13 at 2026-06-01 02:10 IST with context {"load_kn": 79.1, "amps": 12.1, "thp_mpa": 1.12, "spm": 4.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00213
Explain alarm VFD_TRIP raised on BGW-55 at 2026-03-21 02:32 IST with context {"load_kn": 98.9, "amps": 15.9, "thp_mpa": 0.54, "spm": 5.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00214
Explain alarm GOODMAN_HIGH raised on BGW-14 at 2026-02-11 12:13 IST with context {"load_kn": 44.1, "amps": 31.9, "thp_mpa": 0.5, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00215
Explain alarm LOAD_CELL_FAULT raised on BGW-16 at 2026-03-21 10:27 IST with context {"load_kn": 22.9, "amps": 8.0, "thp_mpa": 0.82, "spm": 5.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00216
Explain alarm ROD_FLOAT_RISK raised on BGW-31 at 2026-05-25 16:32 IST with context {"load_kn": 102.1, "amps": 10.3, "thp_mpa": 0.89, "spm": 3.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00217
Explain alarm GOODMAN_HIGH raised on BGW-36 at 2026-04-11 16:57 IST with context {"load_kn": 24.0, "amps": 30.8, "thp_mpa": 0.82, "spm": 7.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00218
Explain alarm GAS_LOCK raised on BGW-15 at 2026-05-06 10:14 IST with context {"load_kn": 28.5, "amps": 14.2, "thp_mpa": 0.51, "spm": 5.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00219
Explain alarm HIGH_THP raised on BGW-43 at 2026-06-22 22:42 IST with context {"load_kn": 61.6, "amps": 9.3, "thp_mpa": 0.81, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00220
Explain alarm VFD_TRIP raised on BGW-11 at 2026-07-29 21:37 IST with context {"load_kn": 37.1, "amps": 11.6, "thp_mpa": 1.08, "spm": 5.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00221
Explain alarm GAS_LOCK raised on BGW-50 at 2026-04-04 22:53 IST with context {"load_kn": 75.8, "amps": 31.6, "thp_mpa": 1.16, "spm": 3.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00222
Explain alarm HIGH_THP raised on BGW-02 at 2026-05-04 06:03 IST with context {"load_kn": 32.9, "amps": 20.0, "thp_mpa": 0.89, "spm": 3.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00223
Explain alarm LOW_LOAD raised on BGW-59 at 2026-05-26 20:46 IST with context {"load_kn": 99.7, "amps": 31.3, "thp_mpa": 0.66, "spm": 7.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00224
Explain alarm VFD_TRIP raised on BGW-55 at 2026-03-04 15:04 IST with context {"load_kn": 41.7, "amps": 22.2, "thp_mpa": 0.69, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00225
Explain alarm HIGH_THP raised on BGW-48 at 2026-01-28 21:09 IST with context {"load_kn": 50.7, "amps": 31.9, "thp_mpa": 1.03, "spm": 7.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00226
Explain alarm HIGH_AMPS raised on BGW-52 at 2026-07-27 10:30 IST with context {"load_kn": 72.9, "amps": 13.4, "thp_mpa": 0.82, "spm": 4.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00227
Explain alarm LOAD_CELL_FAULT raised on BGW-01 at 2026-07-07 10:32 IST with context {"load_kn": 103.1, "amps": 24.8, "thp_mpa": 1.08, "spm": 5.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00228
Explain alarm LOW_LOAD raised on BGW-31 at 2026-09-03 08:09 IST with context {"load_kn": 29.3, "amps": 8.3, "thp_mpa": 0.92, "spm": 5.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00229
Explain alarm GAS_LOCK raised on BGW-07 at 2026-08-21 03:41 IST with context {"load_kn": 40.7, "amps": 24.8, "thp_mpa": 0.91, "spm": 6.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00230
Explain alarm GAS_LOCK raised on BGW-39 at 2026-06-09 01:15 IST with context {"load_kn": 31.2, "amps": 12.2, "thp_mpa": 0.4, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00231
Explain alarm LOW_LOAD raised on BGW-33 at 2026-07-03 00:02 IST with context {"load_kn": 83.8, "amps": 17.0, "thp_mpa": 0.44, "spm": 5.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00232
Explain alarm LOW_LOAD raised on BGW-19 at 2026-06-24 12:29 IST with context {"load_kn": 63.5, "amps": 24.2, "thp_mpa": 1.06, "spm": 7.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00233
Explain alarm GOODMAN_HIGH raised on BGW-38 at 2026-02-03 02:33 IST with context {"load_kn": 51.8, "amps": 25.0, "thp_mpa": 1.03, "spm": 4.3} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00234
Explain alarm VFD_TRIP raised on BGW-20 at 2026-02-06 05:25 IST with context {"load_kn": 86.7, "amps": 10.5, "thp_mpa": 0.48, "spm": 4.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00235
Explain alarm HIGH_AMPS raised on BGW-45 at 2026-09-10 22:45 IST with context {"load_kn": 40.0, "amps": 16.8, "thp_mpa": 0.47, "spm": 3.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00236
Explain alarm LOW_FLOWLINE_T raised on BGW-49 at 2026-03-15 12:59 IST with context {"load_kn": 103.6, "amps": 24.3, "thp_mpa": 0.54, "spm": 5.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00237
Explain alarm HIGH_THP raised on BGW-26 at 2026-03-31 10:26 IST with context {"load_kn": 30.2, "amps": 12.5, "thp_mpa": 0.55, "spm": 4.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00238
Explain alarm HIGH_THP raised on BGW-53 at 2026-01-26 04:28 IST with context {"load_kn": 21.0, "amps": 8.3, "thp_mpa": 1.05, "spm": 4.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00239
Explain alarm VFD_TRIP raised on BGW-17 at 2026-09-15 16:09 IST with context {"load_kn": 54.5, "amps": 21.0, "thp_mpa": 0.62, "spm": 4.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
