# L13 strategy_playbook - batch 009 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L13/replies/L13_batch_009.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L13-00120 .. L13-00134 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "decision", "conditions", "guidance", "rules_of_thumb", "typical_numbers", "risks"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "decision": {"type": "string"},
    "conditions": {"type": "string"},
    "guidance": {"type": "string"},
    "rules_of_thumb": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "typical_numbers": {"type": "string"},
    "risks": {"type": "string"}
  }
}
```

## Items (15)
Write one record per item, following the instruction under each item_id.

### item_id: L13-00120
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding VFD speed profile under summer ambient above 45 C, as a senior operator would today without a digital twin.

### item_id: L13-00121
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding when to re-steam under late cycle with falling fillage, as a senior operator would today without a digital twin.

### item_id: L13-00122
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding when to pull rods under cycle 1-3, viscosity above 1000 cP, as a senior operator would today without a digital twin.

### item_id: L13-00123
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding production cut-off day under cycle 1-3, viscosity above 1000 cP, as a senior operator would today without a digital twin.

### item_id: L13-00124
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding production cut-off day under late cycle with falling fillage, as a senior operator would today without a digital twin.

### item_id: L13-00125
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding soak length under summer ambient above 45 C, as a senior operator would today without a digital twin.

### item_id: L13-00126
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding pump speed (SPM) setting under late cycle with falling fillage, as a senior operator would today without a digital twin.

### item_id: L13-00127
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding soak length under asphaltene deposition in tubing, as a senior operator would today without a digital twin.

### item_id: L13-00128
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding when to re-steam under high water cut after cycle 6, as a senior operator would today without a digital twin.

### item_id: L13-00129
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding production cut-off day under rod float alarms in the last week, as a senior operator would today without a digital twin.

### item_id: L13-00130
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding hold-down selection under steam generator derated, as a senior operator would today without a digital twin.

### item_id: L13-00131
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding cycle steam volume under summer ambient above 45 C, as a senior operator would today without a digital twin.

### item_id: L13-00132
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding hold-down selection under low reservoir pressure, as a senior operator would today without a digital twin.

### item_id: L13-00133
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding VFD speed profile under rod float alarms in the last week, as a senior operator would today without a digital twin.

### item_id: L13-00134
Write a field-practice playbook entry (the 'historical experience' baseline) for deciding pump speed (SPM) setting under summer ambient above 45 C, as a senior operator would today without a digital twin.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
