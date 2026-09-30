# L7 alarm_narrative - batch 006 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_006.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00150 .. L7-00179 (each has an `item_id` you must echo).

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

### item_id: L7-00150
Explain alarm LOAD_CELL_FAULT raised on BGW-34 at 2026-05-26 15:19 IST with context {"load_kn": 84.5, "amps": 29.3, "thp_mpa": 1.08, "spm": 4.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00151
Explain alarm GOODMAN_HIGH raised on BGW-10 at 2026-06-14 13:03 IST with context {"load_kn": 29.6, "amps": 25.7, "thp_mpa": 0.56, "spm": 4.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00152
Explain alarm GOODMAN_HIGH raised on BGW-49 at 2026-03-14 08:21 IST with context {"load_kn": 85.9, "amps": 9.4, "thp_mpa": 0.82, "spm": 6.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00153
Explain alarm LOW_LOAD raised on BGW-26 at 2026-05-13 21:27 IST with context {"load_kn": 92.7, "amps": 19.8, "thp_mpa": 0.87, "spm": 4.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00154
Explain alarm LOW_FLOWLINE_T raised on BGW-18 at 2026-06-02 13:00 IST with context {"load_kn": 50.9, "amps": 29.8, "thp_mpa": 1.12, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00155
Explain alarm LOW_FLOWLINE_T raised on BGW-04 at 2026-06-27 14:39 IST with context {"load_kn": 58.5, "amps": 31.1, "thp_mpa": 0.58, "spm": 6.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00156
Explain alarm GOODMAN_HIGH raised on BGW-26 at 2026-08-16 17:41 IST with context {"load_kn": 90.7, "amps": 18.9, "thp_mpa": 1.01, "spm": 6.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00157
Explain alarm LOW_LOAD raised on BGW-22 at 2026-02-23 01:49 IST with context {"load_kn": 70.3, "amps": 28.5, "thp_mpa": 0.46, "spm": 5.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00158
Explain alarm GAS_LOCK raised on BGW-30 at 2026-06-04 05:14 IST with context {"load_kn": 91.1, "amps": 13.5, "thp_mpa": 0.64, "spm": 6.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00159
Explain alarm PUMP_OFF raised on BGW-54 at 2026-09-03 05:26 IST with context {"load_kn": 31.2, "amps": 17.3, "thp_mpa": 1.2, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00160
Explain alarm VFD_TRIP raised on BGW-32 at 2026-05-27 10:33 IST with context {"load_kn": 36.3, "amps": 24.8, "thp_mpa": 1.14, "spm": 5.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00161
Explain alarm LOW_FLOWLINE_T raised on BGW-28 at 2026-03-01 18:29 IST with context {"load_kn": 35.6, "amps": 17.2, "thp_mpa": 0.87, "spm": 4.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00162
Explain alarm GOODMAN_HIGH raised on BGW-32 at 2026-02-22 14:54 IST with context {"load_kn": 66.8, "amps": 21.1, "thp_mpa": 0.58, "spm": 6.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00163
Explain alarm GAS_LOCK raised on BGW-44 at 2026-08-22 23:06 IST with context {"load_kn": 38.8, "amps": 22.1, "thp_mpa": 0.75, "spm": 6.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00164
Explain alarm GAS_LOCK raised on BGW-04 at 2026-05-14 22:38 IST with context {"load_kn": 53.1, "amps": 18.1, "thp_mpa": 1.04, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00165
Explain alarm HIGH_THP raised on BGW-09 at 2026-08-26 23:37 IST with context {"load_kn": 79.8, "amps": 19.0, "thp_mpa": 0.78, "spm": 4.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00166
Explain alarm LOW_FLOWLINE_T raised on BGW-22 at 2026-01-29 02:39 IST with context {"load_kn": 58.9, "amps": 19.8, "thp_mpa": 0.94, "spm": 3.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00167
Explain alarm LOW_LOAD raised on BGW-06 at 2026-04-29 18:41 IST with context {"load_kn": 93.0, "amps": 18.4, "thp_mpa": 0.9, "spm": 5.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00168
Explain alarm PUMP_OFF raised on BGW-44 at 2026-06-25 16:39 IST with context {"load_kn": 51.1, "amps": 16.8, "thp_mpa": 0.8, "spm": 3.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00169
Explain alarm GAS_LOCK raised on BGW-35 at 2026-04-12 14:57 IST with context {"load_kn": 31.7, "amps": 31.3, "thp_mpa": 0.46, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00170
Explain alarm ROD_FLOAT_RISK raised on BGW-12 at 2026-03-27 18:59 IST with context {"load_kn": 84.2, "amps": 28.8, "thp_mpa": 0.81, "spm": 6.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00171
Explain alarm HIGH_THP raised on BGW-49 at 2026-03-31 09:49 IST with context {"load_kn": 93.7, "amps": 23.1, "thp_mpa": 0.48, "spm": 6.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00172
Explain alarm PUMP_OFF raised on BGW-52 at 2026-01-14 13:49 IST with context {"load_kn": 54.3, "amps": 14.1, "thp_mpa": 0.54, "spm": 3.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00173
Explain alarm PUMP_OFF raised on BGW-52 at 2026-07-31 19:12 IST with context {"load_kn": 72.3, "amps": 17.6, "thp_mpa": 0.64, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00174
Explain alarm LOAD_CELL_FAULT raised on BGW-04 at 2026-06-02 16:12 IST with context {"load_kn": 20.6, "amps": 26.3, "thp_mpa": 0.99, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00175
Explain alarm ROD_FLOAT_RISK raised on BGW-54 at 2026-05-13 09:00 IST with context {"load_kn": 65.7, "amps": 8.6, "thp_mpa": 0.78, "spm": 5.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00176
Explain alarm GAS_LOCK raised on BGW-59 at 2026-01-03 21:45 IST with context {"load_kn": 44.1, "amps": 23.3, "thp_mpa": 0.62, "spm": 3.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00177
Explain alarm GAS_LOCK raised on BGW-19 at 2026-04-22 13:55 IST with context {"load_kn": 82.8, "amps": 12.2, "thp_mpa": 0.48, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00178
Explain alarm VFD_TRIP raised on BGW-39 at 2026-01-12 06:02 IST with context {"load_kn": 52.9, "amps": 29.6, "thp_mpa": 0.71, "spm": 6.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00179
Explain alarm GAS_LOCK raised on BGW-14 at 2026-01-20 16:41 IST with context {"load_kn": 47.2, "amps": 21.0, "thp_mpa": 1.03, "spm": 5.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
