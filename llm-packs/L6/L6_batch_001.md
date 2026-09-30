# L6 operator_shift_log - batch 001 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L6/replies/L6_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L6-00000 .. L6-00019 (each has an `item_id` you must echo).

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

### item_id: L6-00000
Write 10 operator shift-log lines for BGW-16 over 2026-02-04 given telemetry highlights VFD trip 14:20; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00001
Write 10 operator shift-log lines for BGW-07 over 2024-11-20 given telemetry highlights VFD trip 14:20; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00002
Write 10 operator shift-log lines for BGW-15 over 2025-03-19 given telemetry highlights none; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00003
Write 10 operator shift-log lines for BGW-22 over 2025-05-17 given telemetry highlights VFD trip 14:20; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00004
Write 10 operator shift-log lines for BGW-41 over 2025-07-29 given telemetry highlights pump-off 02:10-03:05; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00005
Write 10 operator shift-log lines for BGW-30 over 2025-11-14 given telemetry highlights VFD trip 14:20; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00006
Write 10 operator shift-log lines for BGW-32 over 2024-02-16 given telemetry highlights none; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00007
Write 10 operator shift-log lines for BGW-57 over 2025-07-26 given telemetry highlights VFD trip 14:20; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00008
Write 10 operator shift-log lines for BGW-31 over 2024-03-31 given telemetry highlights THP rise to 0.9 MPa; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00009
Write 10 operator shift-log lines for BGW-54 over 2025-09-14 given telemetry highlights VFD trip 14:20; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00010
Write 10 operator shift-log lines for BGW-04 over 2026-04-27 given telemetry highlights load cell reading flat 09:00; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00011
Write 10 operator shift-log lines for BGW-19 over 2025-03-14 given telemetry highlights none; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00012
Write 10 operator shift-log lines for BGW-28 over 2024-05-21 given telemetry highlights pump-off 02:10-03:05; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00013
Write 10 operator shift-log lines for BGW-58 over 2025-06-18 given telemetry highlights none; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00014
Write 10 operator shift-log lines for BGW-55 over 2024-10-24 given telemetry highlights none; pump-off 02:10-03:05: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00015
Write 10 operator shift-log lines for BGW-38 over 2025-08-30 given telemetry highlights VFD trip 14:20; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00016
Write 10 operator shift-log lines for BGW-03 over 2024-06-11 given telemetry highlights pump-off 02:10-03:05; load cell reading flat 09:00: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00017
Write 10 operator shift-log lines for BGW-34 over 2024-02-15 given telemetry highlights VFD trip 14:20; none: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00018
Write 10 operator shift-log lines for BGW-41 over 2025-06-15 given telemetry highlights load cell reading flat 09:00; THP rise to 0.9 MPa: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

### item_id: L6-00019
Write 10 operator shift-log lines for BGW-20 over 2026-05-10 given telemetry highlights pump-off 02:10-03:05; VFD trip 14:20: terse, timestamped, abbreviations operators use (SPM, THP, CHP, POC, fluid pound), occasional typos.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
