# L6 operator_shift_log - batch 008 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L6/replies/L6_batch_008.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L6-00140 .. L6-00159 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "well_id", "date", "lines"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "well_id": {"type": "string"},
    "date": {"type": "string"},
    "lines": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 40}
  }
}
```

## Items (20)
Write one record per item, following the instruction under each item_id.

### item_id: L6-00140
Write 10 operator shift-log lines for BGW-12 over 2024-09-14 given telemetry highlights THP rise to 0.9 MPa; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00141
Write 10 operator shift-log lines for BGW-39 over 2024-01-08 given telemetry highlights load cell reading flat 09:00; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00142
Write 10 operator shift-log lines for BGW-40 over 2024-07-15 given telemetry highlights VFD trip 14:20; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00143
Write 10 operator shift-log lines for BGW-56 over 2025-07-09 given telemetry highlights none; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00144
Write 10 operator shift-log lines for BGW-41 over 2024-03-04 given telemetry highlights none; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00145
Write 10 operator shift-log lines for BGW-23 over 2025-07-26 given telemetry highlights THP rise to 0.9 MPa; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00146
Write 10 operator shift-log lines for BGW-29 over 2025-11-04 given telemetry highlights none; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00147
Write 10 operator shift-log lines for BGW-08 over 2026-02-04 given telemetry highlights load cell reading flat 09:00; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00148
Write 10 operator shift-log lines for BGW-27 over 2024-12-27 given telemetry highlights THP rise to 0.9 MPa; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00149
Write 10 operator shift-log lines for BGW-45 over 2024-03-26 given telemetry highlights pump-off 02:10-03:05; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00150
Write 10 operator shift-log lines for BGW-13 over 2025-10-10 given telemetry highlights none; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00151
Write 10 operator shift-log lines for BGW-43 over 2025-01-13 given telemetry highlights load cell reading flat 09:00; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00152
Write 10 operator shift-log lines for BGW-09 over 2026-05-19 given telemetry highlights load cell reading flat 09:00; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00153
Write 10 operator shift-log lines for BGW-18 over 2024-02-04 given telemetry highlights THP rise to 0.9 MPa; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00154
Write 10 operator shift-log lines for BGW-29 over 2024-12-06 given telemetry highlights pump-off 02:10-03:05; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00155
Write 10 operator shift-log lines for BGW-05 over 2026-02-02 given telemetry highlights THP rise to 0.9 MPa; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00156
Write 10 operator shift-log lines for BGW-34 over 2024-07-23 given telemetry highlights VFD trip 14:20; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00157
Write 10 operator shift-log lines for BGW-13 over 2025-09-05 given telemetry highlights pump-off 02:10-03:05; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00158
Write 10 operator shift-log lines for BGW-33 over 2024-05-19 given telemetry highlights pump-off 02:10-03:05; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00159
Write 10 operator shift-log lines for BGW-07 over 2025-09-01 given telemetry highlights load cell reading flat 09:00; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
