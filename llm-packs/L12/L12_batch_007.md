# L12 copilot_qa - batch 007 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_007.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00150 .. L12-00174 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "topic", "well_id", "question", "answer", "cited_facts"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "topic": {"type": "string"},
    "well_id": {"type": "string"},
    "question": {"type": "string"},
    "answer": {"type": "string"},
    "cited_facts": {"type": "array", "items": {"type": "string"}, "minItems": 1}
  }
}
```

## Items (25)
Write one record per item, following the instruction under each item_id.

### item_id: L12-00150
Write a question an OIL production engineer might ask about soak length for BGW-29 and the ideal grounded answer using only {"well": "BGW-29", "api": 18.623, "asphaltene_wt_pct": 10.858, "latest_cycle": 9, "steam_t": 818.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00151
Write a question an OIL production engineer might ask about SOR for BGW-32 and the ideal grounded answer using only {"well": "BGW-32", "api": 17.818, "asphaltene_wt_pct": 7.204, "latest_cycle": 12, "steam_t": 762.0, "sor": 15.74, "cum_oil_bbl": 304.49, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00152
Write a question an OIL production engineer might ask about soak length for BGW-49 and the ideal grounded answer using only {"well": "BGW-49", "api": 18.67, "asphaltene_wt_pct": 8.799, "latest_cycle": 8, "steam_t": 973.0, "sor": 4.009, "cum_oil_bbl": 1526.525, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00153
Write a question an OIL production engineer might ask about soak length for BGW-12 and the ideal grounded answer using only {"well": "BGW-12", "api": 19.052, "asphaltene_wt_pct": 11.602, "latest_cycle": 11, "steam_t": 1200.0, "sor": 4.396, "cum_oil_bbl": 1716.802, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00154
Write a question an OIL production engineer might ask about rod float for BGW-60 and the ideal grounded answer using only {"well": "BGW-60", "api": 17.825, "asphaltene_wt_pct": 8.092, "latest_cycle": 13, "steam_t": 873.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00155
Write a question an OIL production engineer might ask about pump unseating for BGW-58 and the ideal grounded answer using only {"well": "BGW-58", "api": 17.755, "asphaltene_wt_pct": 10.969, "latest_cycle": 12, "steam_t": 987.0, "sor": 14.054, "cum_oil_bbl": 441.729, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00156
Write a question an OIL production engineer might ask about fluid pound for BGW-20 and the ideal grounded answer using only {"well": "BGW-20", "api": 17.004, "asphaltene_wt_pct": 7.221, "latest_cycle": 13, "steam_t": 954.0, "sor": 11.028, "cum_oil_bbl": 544.121, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00157
Write a question an OIL production engineer might ask about rod float for BGW-13 and the ideal grounded answer using only {"well": "BGW-13", "api": 18.616, "asphaltene_wt_pct": 7.177, "latest_cycle": 9, "steam_t": 1038.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00158
Write a question an OIL production engineer might ask about fluid pound for BGW-18 and the ideal grounded answer using only {"well": "BGW-18", "api": 18.012, "asphaltene_wt_pct": 8.643, "latest_cycle": 12, "steam_t": 1077.0, "sor": 11.484, "cum_oil_bbl": 589.884, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00159
Write a question an OIL production engineer might ask about rod float for BGW-23 and the ideal grounded answer using only {"well": "BGW-23", "api": 19.107, "asphaltene_wt_pct": 8.685, "latest_cycle": 13, "steam_t": 933.0, "sor": 81.264, "cum_oil_bbl": 72.213, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00160
Write a question an OIL production engineer might ask about VFD profile for BGW-54 and the ideal grounded answer using only {"well": "BGW-54", "api": 17.171, "asphaltene_wt_pct": 8.036, "latest_cycle": 13, "steam_t": 876.0, "sor": 77.783, "cum_oil_bbl": 70.837, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00161
Write a question an OIL production engineer might ask about soak length for BGW-36 and the ideal grounded answer using only {"well": "BGW-36", "api": 19.377, "asphaltene_wt_pct": 7.717, "latest_cycle": 12, "steam_t": 860.0, "sor": 10.567, "cum_oil_bbl": 511.913, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00162
Write a question an OIL production engineer might ask about soak length for BGW-39 and the ideal grounded answer using only {"well": "BGW-39", "api": 17.782, "asphaltene_wt_pct": 7.693, "latest_cycle": 11, "steam_t": 986.0, "sor": 13.456, "cum_oil_bbl": 460.89, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00163
Write a question an OIL production engineer might ask about VFD profile for BGW-08 and the ideal grounded answer using only {"well": "BGW-08", "api": 18.197, "asphaltene_wt_pct": 10.749, "latest_cycle": 13, "steam_t": 1049.0, "sor": 11.817, "cum_oil_bbl": 558.353, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00164
Write a question an OIL production engineer might ask about SOR for BGW-10 and the ideal grounded answer using only {"well": "BGW-10", "api": 17.681, "asphaltene_wt_pct": 9.229, "latest_cycle": 11, "steam_t": 902.0, "sor": 58.236, "cum_oil_bbl": 97.42, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00165
Write a question an OIL production engineer might ask about rod float for BGW-60 and the ideal grounded answer using only {"well": "BGW-60", "api": 17.825, "asphaltene_wt_pct": 8.092, "latest_cycle": 13, "steam_t": 873.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00166
Write a question an OIL production engineer might ask about fluid pound for BGW-48 and the ideal grounded answer using only {"well": "BGW-48", "api": 18.111, "asphaltene_wt_pct": 10.149, "latest_cycle": 13, "steam_t": 708.0, "sor": 9.913, "cum_oil_bbl": 449.232, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00167
Write a question an OIL production engineer might ask about SOR for BGW-12 and the ideal grounded answer using only {"well": "BGW-12", "api": 19.052, "asphaltene_wt_pct": 11.602, "latest_cycle": 11, "steam_t": 1200.0, "sor": 4.396, "cum_oil_bbl": 1716.802, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00168
Write a question an OIL production engineer might ask about SOR for BGW-03 and the ideal grounded answer using only {"well": "BGW-03", "api": 19.223, "asphaltene_wt_pct": 7.28, "latest_cycle": 8, "steam_t": 885.0, "sor": 99.0, "cum_oil_bbl": 7.913, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00169
Write a question an OIL production engineer might ask about VFD profile for BGW-43 and the ideal grounded answer using only {"well": "BGW-43", "api": 19.306, "asphaltene_wt_pct": 7.141, "latest_cycle": 10, "steam_t": 923.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00170
Write a question an OIL production engineer might ask about fluid pound for BGW-35 and the ideal grounded answer using only {"well": "BGW-35", "api": 18.034, "asphaltene_wt_pct": 8.047, "latest_cycle": 8, "steam_t": 947.0, "sor": 13.623, "cum_oil_bbl": 437.229, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00171
Write a question an OIL production engineer might ask about cut-off timing for BGW-32 and the ideal grounded answer using only {"well": "BGW-32", "api": 17.818, "asphaltene_wt_pct": 7.204, "latest_cycle": 12, "steam_t": 762.0, "sor": 15.74, "cum_oil_bbl": 304.49, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00172
Write a question an OIL production engineer might ask about SOR for BGW-53 and the ideal grounded answer using only {"well": "BGW-53", "api": 19.345, "asphaltene_wt_pct": 8.99, "latest_cycle": 9, "steam_t": 890.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00173
Write a question an OIL production engineer might ask about pump unseating for BGW-53 and the ideal grounded answer using only {"well": "BGW-53", "api": 19.345, "asphaltene_wt_pct": 8.99, "latest_cycle": 9, "steam_t": 890.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00174
Write a question an OIL production engineer might ask about SOR for BGW-56 and the ideal grounded answer using only {"well": "BGW-56", "api": 19.25, "asphaltene_wt_pct": 9.106, "latest_cycle": 13, "steam_t": 963.0, "sor": 99.0, "cum_oil_bbl": 58.714, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
