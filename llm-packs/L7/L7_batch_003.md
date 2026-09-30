# L7 alarm_narrative - batch 003 (30 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 30 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L7/replies/L7_batch_003.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L7-00060 .. L7-00089 (each has an `item_id` you must echo).

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

### item_id: L7-00060
Explain alarm GOODMAN_HIGH raised on BGW-22 at 2026-08-29 04:30 IST with context {"load_kn": 102.0, "amps": 11.4, "thp_mpa": 1.04, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00061
Explain alarm VFD_TRIP raised on BGW-36 at 2026-05-17 02:06 IST with context {"load_kn": 84.0, "amps": 10.8, "thp_mpa": 0.68, "spm": 6.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00062
Explain alarm LOW_FLOWLINE_T raised on BGW-53 at 2026-02-26 18:41 IST with context {"load_kn": 92.4, "amps": 27.1, "thp_mpa": 0.79, "spm": 5.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00063
Explain alarm ROD_FLOAT_RISK raised on BGW-11 at 2026-08-21 05:04 IST with context {"load_kn": 70.5, "amps": 19.6, "thp_mpa": 1.01, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00064
Explain alarm LOW_LOAD raised on BGW-26 at 2026-07-05 22:41 IST with context {"load_kn": 60.7, "amps": 23.3, "thp_mpa": 0.75, "spm": 3.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00065
Explain alarm HIGH_THP raised on BGW-45 at 2026-06-06 01:21 IST with context {"load_kn": 72.8, "amps": 32.0, "thp_mpa": 0.41, "spm": 3.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00066
Explain alarm HIGH_THP raised on BGW-09 at 2026-04-24 07:26 IST with context {"load_kn": 55.4, "amps": 13.5, "thp_mpa": 0.95, "spm": 3.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00067
Explain alarm GAS_LOCK raised on BGW-14 at 2026-07-04 11:14 IST with context {"load_kn": 63.0, "amps": 22.0, "thp_mpa": 1.01, "spm": 7.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00068
Explain alarm GOODMAN_HIGH raised on BGW-21 at 2026-05-18 19:30 IST with context {"load_kn": 64.6, "amps": 22.9, "thp_mpa": 0.96, "spm": 6.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00069
Explain alarm LOW_FLOWLINE_T raised on BGW-12 at 2026-07-19 00:58 IST with context {"load_kn": 56.2, "amps": 27.2, "thp_mpa": 1.12, "spm": 6.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00070
Explain alarm GAS_LOCK raised on BGW-19 at 2026-04-02 20:46 IST with context {"load_kn": 63.3, "amps": 11.0, "thp_mpa": 0.85, "spm": 7.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00071
Explain alarm VFD_TRIP raised on BGW-51 at 2026-08-28 16:50 IST with context {"load_kn": 47.9, "amps": 20.1, "thp_mpa": 0.59, "spm": 4.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00072
Explain alarm LOAD_CELL_FAULT raised on BGW-18 at 2026-08-04 18:19 IST with context {"load_kn": 79.0, "amps": 30.8, "thp_mpa": 0.82, "spm": 5.0} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00073
Explain alarm LOW_FLOWLINE_T raised on BGW-30 at 2026-05-12 09:49 IST with context {"load_kn": 63.1, "amps": 10.7, "thp_mpa": 1.04, "spm": 4.2} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00074
Explain alarm LOW_FLOWLINE_T raised on BGW-05 at 2026-07-16 12:07 IST with context {"load_kn": 55.3, "amps": 27.2, "thp_mpa": 0.69, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00075
Explain alarm PUMP_OFF raised on BGW-07 at 2026-02-06 21:46 IST with context {"load_kn": 91.9, "amps": 9.0, "thp_mpa": 0.41, "spm": 6.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00076
Explain alarm HIGH_THP raised on BGW-20 at 2026-06-21 12:33 IST with context {"load_kn": 49.3, "amps": 8.3, "thp_mpa": 0.81, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00077
Explain alarm LOAD_CELL_FAULT raised on BGW-38 at 2026-07-06 15:19 IST with context {"load_kn": 77.1, "amps": 26.9, "thp_mpa": 1.04, "spm": 4.6} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00078
Explain alarm ROD_FLOAT_RISK raised on BGW-30 at 2026-03-31 03:17 IST with context {"load_kn": 20.8, "amps": 18.4, "thp_mpa": 1.08, "spm": 6.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00079
Explain alarm LOW_LOAD raised on BGW-14 at 2026-08-24 03:07 IST with context {"load_kn": 30.6, "amps": 25.3, "thp_mpa": 0.8, "spm": 6.1} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00080
Explain alarm PUMP_OFF raised on BGW-25 at 2026-02-10 19:11 IST with context {"load_kn": 28.8, "amps": 24.6, "thp_mpa": 0.75, "spm": 5.7} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00081
Explain alarm LOW_FLOWLINE_T raised on BGW-03 at 2026-04-16 02:34 IST with context {"load_kn": 39.2, "amps": 12.2, "thp_mpa": 1.07, "spm": 6.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00082
Explain alarm GOODMAN_HIGH raised on BGW-09 at 2026-01-03 20:09 IST with context {"load_kn": 74.3, "amps": 26.2, "thp_mpa": 0.81, "spm": 3.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00083
Explain alarm LOW_FLOWLINE_T raised on BGW-43 at 2026-06-04 20:22 IST with context {"load_kn": 62.2, "amps": 10.8, "thp_mpa": 0.94, "spm": 3.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00084
Explain alarm GOODMAN_HIGH raised on BGW-07 at 2026-07-17 19:18 IST with context {"load_kn": 28.6, "amps": 26.3, "thp_mpa": 1.03, "spm": 4.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00085
Explain alarm HIGH_AMPS raised on BGW-05 at 2026-01-22 04:02 IST with context {"load_kn": 58.0, "amps": 30.5, "thp_mpa": 0.9, "spm": 4.4} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00086
Explain alarm HIGH_AMPS raised on BGW-50 at 2026-05-14 07:33 IST with context {"load_kn": 64.1, "amps": 26.9, "thp_mpa": 0.65, "spm": 5.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00087
Explain alarm GOODMAN_HIGH raised on BGW-59 at 2026-05-15 06:40 IST with context {"load_kn": 92.5, "amps": 28.1, "thp_mpa": 0.63, "spm": 4.9} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00088
Explain alarm GOODMAN_HIGH raised on BGW-21 at 2026-01-16 17:44 IST with context {"load_kn": 101.0, "amps": 27.9, "thp_mpa": 0.77, "spm": 7.5} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

### item_id: L7-00089
Explain alarm PUMP_OFF raised on BGW-43 at 2026-01-03 02:40 IST with context {"load_kn": 21.3, "amps": 21.2, "thp_mpa": 1.11, "spm": 5.8} in the voice of a production engineer's triage note: probable cause, what to check, urgency (low/med/high).

## Output contract
Return a JSON array of exactly 30 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
