# L6 operator_shift_log - batch 007 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L6/replies/L6_batch_007.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L6-00120 .. L6-00139 (each has an `item_id` you must echo).

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

### item_id: L6-00120
Write 10 operator shift-log lines for BGW-04 over 2025-06-09 given telemetry highlights THP rise to 0.9 MPa; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00121
Write 10 operator shift-log lines for BGW-47 over 2024-08-13 given telemetry highlights VFD trip 14:20; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00122
Write 10 operator shift-log lines for BGW-36 over 2024-06-20 given telemetry highlights VFD trip 14:20; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00123
Write 10 operator shift-log lines for BGW-39 over 2024-11-13 given telemetry highlights load cell reading flat 09:00; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00124
Write 10 operator shift-log lines for BGW-50 over 2025-10-31 given telemetry highlights none; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00125
Write 10 operator shift-log lines for BGW-43 over 2024-04-06 given telemetry highlights load cell reading flat 09:00; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00126
Write 10 operator shift-log lines for BGW-54 over 2025-02-05 given telemetry highlights none; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00127
Write 10 operator shift-log lines for BGW-30 over 2025-10-25 given telemetry highlights pump-off 02:10-03:05; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00128
Write 10 operator shift-log lines for BGW-36 over 2025-03-17 given telemetry highlights VFD trip 14:20; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00129
Write 10 operator shift-log lines for BGW-53 over 2025-09-21 given telemetry highlights none; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00130
Write 10 operator shift-log lines for BGW-21 over 2025-02-16 given telemetry highlights load cell reading flat 09:00; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00131
Write 10 operator shift-log lines for BGW-51 over 2025-09-23 given telemetry highlights VFD trip 14:20; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00132
Write 10 operator shift-log lines for BGW-45 over 2024-03-12 given telemetry highlights VFD trip 14:20; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00133
Write 10 operator shift-log lines for BGW-48 over 2024-01-20 given telemetry highlights THP rise to 0.9 MPa; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00134
Write 10 operator shift-log lines for BGW-49 over 2025-09-13 given telemetry highlights none; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00135
Write 10 operator shift-log lines for BGW-51 over 2024-01-20 given telemetry highlights THP rise to 0.9 MPa; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00136
Write 10 operator shift-log lines for BGW-39 over 2024-02-20 given telemetry highlights THP rise to 0.9 MPa; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00137
Write 10 operator shift-log lines for BGW-02 over 2024-12-13 given telemetry highlights pump-off 02:10-03:05; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00138
Write 10 operator shift-log lines for BGW-26 over 2025-06-07 given telemetry highlights VFD trip 14:20; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00139
Write 10 operator shift-log lines for BGW-56 over 2026-05-28 given telemetry highlights THP rise to 0.9 MPa; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
