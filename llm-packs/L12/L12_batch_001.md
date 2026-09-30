# L12 copilot_qa - batch 001 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00000 .. L12-00024 (each has an `item_id` you must echo).

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

### item_id: L12-00000
Write a question an OIL production engineer might ask about VFD profile for BGW-07 and the ideal grounded answer using only {"well": "BGW-07", "api": 18.131, "asphaltene_wt_pct": 11.233, "latest_cycle": 7, "steam_t": 866.0, "sor": 25.808, "cum_oil_bbl": 211.06, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00001
Write a question an OIL production engineer might ask about cut-off timing for BGW-40 and the ideal grounded answer using only {"well": "BGW-40", "api": 17.037, "asphaltene_wt_pct": 11.206, "latest_cycle": 7, "steam_t": 817.0, "sor": 6.255, "cum_oil_bbl": 821.561, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00002
Write a question an OIL production engineer might ask about cut-off timing for BGW-31 and the ideal grounded answer using only {"well": "BGW-31", "api": 17.565, "asphaltene_wt_pct": 7.32, "latest_cycle": 9, "steam_t": 741.0, "sor": 11.279, "cum_oil_bbl": 413.207, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00003
Write a question an OIL production engineer might ask about soak length for BGW-46 and the ideal grounded answer using only {"well": "BGW-46", "api": 18.204, "asphaltene_wt_pct": 8.946, "latest_cycle": 10, "steam_t": 947.0, "sor": 7.168, "cum_oil_bbl": 831.012, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00004
Write a question an OIL production engineer might ask about SOR for BGW-60 and the ideal grounded answer using only {"well": "BGW-60", "api": 17.825, "asphaltene_wt_pct": 8.092, "latest_cycle": 13, "steam_t": 873.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00005
Write a question an OIL production engineer might ask about soak length for BGW-11 and the ideal grounded answer using only {"well": "BGW-11", "api": 19.26, "asphaltene_wt_pct": 8.28, "latest_cycle": 9, "steam_t": 1081.0, "sor": 8.694, "cum_oil_bbl": 782.105, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00006
Write a question an OIL production engineer might ask about pump unseating for BGW-29 and the ideal grounded answer using only {"well": "BGW-29", "api": 18.623, "asphaltene_wt_pct": 10.858, "latest_cycle": 9, "steam_t": 818.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00007
Write a question an OIL production engineer might ask about pump unseating for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00008
Write a question an OIL production engineer might ask about soak length for BGW-49 and the ideal grounded answer using only {"well": "BGW-49", "api": 18.67, "asphaltene_wt_pct": 8.799, "latest_cycle": 8, "steam_t": 973.0, "sor": 4.009, "cum_oil_bbl": 1526.525, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00009
Write a question an OIL production engineer might ask about cut-off timing for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00010
Write a question an OIL production engineer might ask about pump unseating for BGW-12 and the ideal grounded answer using only {"well": "BGW-12", "api": 19.052, "asphaltene_wt_pct": 11.602, "latest_cycle": 11, "steam_t": 1200.0, "sor": 4.396, "cum_oil_bbl": 1716.802, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00011
Write a question an OIL production engineer might ask about pump unseating for BGW-48 and the ideal grounded answer using only {"well": "BGW-48", "api": 18.111, "asphaltene_wt_pct": 10.149, "latest_cycle": 13, "steam_t": 708.0, "sor": 9.913, "cum_oil_bbl": 449.232, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00012
Write a question an OIL production engineer might ask about rod float for BGW-06 and the ideal grounded answer using only {"well": "BGW-06", "api": 18.617, "asphaltene_wt_pct": 8.977, "latest_cycle": 10, "steam_t": 910.0, "sor": 32.106, "cum_oil_bbl": 178.277, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00013
Write a question an OIL production engineer might ask about VFD profile for BGW-26 and the ideal grounded answer using only {"well": "BGW-26", "api": 19.143, "asphaltene_wt_pct": 8.64, "latest_cycle": 10, "steam_t": 857.0, "sor": 6.357, "cum_oil_bbl": 847.913, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00014
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-43 and the ideal grounded answer using only {"well": "BGW-43", "api": 19.306, "asphaltene_wt_pct": 7.141, "latest_cycle": 10, "steam_t": 923.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00015
Write a question an OIL production engineer might ask about soak length for BGW-13 and the ideal grounded answer using only {"well": "BGW-13", "api": 18.616, "asphaltene_wt_pct": 7.177, "latest_cycle": 9, "steam_t": 1038.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00016
Write a question an OIL production engineer might ask about fluid pound for BGW-14 and the ideal grounded answer using only {"well": "BGW-14", "api": 18.11, "asphaltene_wt_pct": 10.75, "latest_cycle": 12, "steam_t": 1099.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00017
Write a question an OIL production engineer might ask about rod float for BGW-10 and the ideal grounded answer using only {"well": "BGW-10", "api": 17.681, "asphaltene_wt_pct": 9.229, "latest_cycle": 11, "steam_t": 902.0, "sor": 58.236, "cum_oil_bbl": 97.42, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00018
Write a question an OIL production engineer might ask about fluid pound for BGW-03 and the ideal grounded answer using only {"well": "BGW-03", "api": 19.223, "asphaltene_wt_pct": 7.28, "latest_cycle": 8, "steam_t": 885.0, "sor": 99.0, "cum_oil_bbl": 7.913, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00019
Write a question an OIL production engineer might ask about fluid pound for BGW-35 and the ideal grounded answer using only {"well": "BGW-35", "api": 18.034, "asphaltene_wt_pct": 8.047, "latest_cycle": 8, "steam_t": 947.0, "sor": 13.623, "cum_oil_bbl": 437.229, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00020
Write a question an OIL production engineer might ask about VFD profile for BGW-26 and the ideal grounded answer using only {"well": "BGW-26", "api": 19.143, "asphaltene_wt_pct": 8.64, "latest_cycle": 10, "steam_t": 857.0, "sor": 6.357, "cum_oil_bbl": 847.913, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00021
Write a question an OIL production engineer might ask about VFD profile for BGW-43 and the ideal grounded answer using only {"well": "BGW-43", "api": 19.306, "asphaltene_wt_pct": 7.141, "latest_cycle": 10, "steam_t": 923.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00022
Write a question an OIL production engineer might ask about soak length for BGW-08 and the ideal grounded answer using only {"well": "BGW-08", "api": 18.197, "asphaltene_wt_pct": 10.749, "latest_cycle": 13, "steam_t": 1049.0, "sor": 11.817, "cum_oil_bbl": 558.353, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00023
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-13 and the ideal grounded answer using only {"well": "BGW-13", "api": 18.616, "asphaltene_wt_pct": 7.177, "latest_cycle": 9, "steam_t": 1038.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00024
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-10 and the ideal grounded answer using only {"well": "BGW-10", "api": 17.681, "asphaltene_wt_pct": 9.229, "latest_cycle": 11, "steam_t": 902.0, "sor": 58.236, "cum_oil_bbl": 97.42, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
