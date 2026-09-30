# L6 operator_shift_log - batch 003 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L6/replies/L6_batch_003.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L6-00040 .. L6-00059 (each has an `item_id` you must echo).

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

### item_id: L6-00040
Write 10 operator shift-log lines for BGW-44 over 2025-04-28 given telemetry highlights VFD trip 14:20; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00041
Write 10 operator shift-log lines for BGW-51 over 2025-04-02 given telemetry highlights none; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00042
Write 10 operator shift-log lines for BGW-41 over 2024-02-13 given telemetry highlights THP rise to 0.9 MPa; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00043
Write 10 operator shift-log lines for BGW-58 over 2024-08-09 given telemetry highlights VFD trip 14:20; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00044
Write 10 operator shift-log lines for BGW-59 over 2024-06-02 given telemetry highlights THP rise to 0.9 MPa; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00045
Write 10 operator shift-log lines for BGW-32 over 2025-08-05 given telemetry highlights none; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00046
Write 10 operator shift-log lines for BGW-15 over 2025-07-06 given telemetry highlights none; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00047
Write 10 operator shift-log lines for BGW-16 over 2026-06-04 given telemetry highlights THP rise to 0.9 MPa; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00048
Write 10 operator shift-log lines for BGW-01 over 2026-04-08 given telemetry highlights none; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00049
Write 10 operator shift-log lines for BGW-36 over 2026-05-10 given telemetry highlights load cell reading flat 09:00; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00050
Write 10 operator shift-log lines for BGW-13 over 2025-09-10 given telemetry highlights THP rise to 0.9 MPa; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00051
Write 10 operator shift-log lines for BGW-36 over 2025-06-09 given telemetry highlights THP rise to 0.9 MPa; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00052
Write 10 operator shift-log lines for BGW-12 over 2024-12-18 given telemetry highlights load cell reading flat 09:00; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00053
Write 10 operator shift-log lines for BGW-17 over 2025-08-10 given telemetry highlights pump-off 02:10-03:05; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00054
Write 10 operator shift-log lines for BGW-50 over 2026-05-18 given telemetry highlights none; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00055
Write 10 operator shift-log lines for BGW-19 over 2025-09-04 given telemetry highlights none; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00056
Write 10 operator shift-log lines for BGW-29 over 2025-08-14 given telemetry highlights none; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00057
Write 10 operator shift-log lines for BGW-10 over 2024-05-16 given telemetry highlights THP rise to 0.9 MPa; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00058
Write 10 operator shift-log lines for BGW-54 over 2025-11-29 given telemetry highlights load cell reading flat 09:00; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00059
Write 10 operator shift-log lines for BGW-54 over 2025-11-20 given telemetry highlights load cell reading flat 09:00; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
