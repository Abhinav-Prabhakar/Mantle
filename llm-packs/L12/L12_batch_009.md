# L12 copilot_qa - batch 009 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_009.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00200 .. L12-00224 (each has an `item_id` you must echo).

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

### item_id: L12-00200
Write a question an OIL production engineer might ask about fluid pound for BGW-15 and the ideal grounded answer using only {"well": "BGW-15", "api": 18.179, "asphaltene_wt_pct": 8.151, "latest_cycle": 13, "steam_t": 960.0, "sor": 12.245, "cum_oil_bbl": 493.113, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00201
Write a question an OIL production engineer might ask about fluid pound for BGW-02 and the ideal grounded answer using only {"well": "BGW-02", "api": 17.704, "asphaltene_wt_pct": 11.955, "latest_cycle": 10, "steam_t": 1015.0, "sor": 44.034, "cum_oil_bbl": 144.983, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00202
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-48 and the ideal grounded answer using only {"well": "BGW-48", "api": 18.111, "asphaltene_wt_pct": 10.149, "latest_cycle": 13, "steam_t": 708.0, "sor": 9.913, "cum_oil_bbl": 449.232, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00203
Write a question an OIL production engineer might ask about pump unseating for BGW-46 and the ideal grounded answer using only {"well": "BGW-46", "api": 18.204, "asphaltene_wt_pct": 8.946, "latest_cycle": 10, "steam_t": 947.0, "sor": 7.168, "cum_oil_bbl": 831.012, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00204
Write a question an OIL production engineer might ask about soak length for BGW-04 and the ideal grounded answer using only {"well": "BGW-04", "api": 17.637, "asphaltene_wt_pct": 9.561, "latest_cycle": 12, "steam_t": 721.0, "sor": 10.942, "cum_oil_bbl": 414.437, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00205
Write a question an OIL production engineer might ask about soak length for BGW-56 and the ideal grounded answer using only {"well": "BGW-56", "api": 19.25, "asphaltene_wt_pct": 9.106, "latest_cycle": 13, "steam_t": 963.0, "sor": 99.0, "cum_oil_bbl": 58.714, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00206
Write a question an OIL production engineer might ask about fluid pound for BGW-05 and the ideal grounded answer using only {"well": "BGW-05", "api": 18.657, "asphaltene_wt_pct": 11.621, "latest_cycle": 13, "steam_t": 1033.0, "sor": 15.762, "cum_oil_bbl": 412.213, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00207
Write a question an OIL production engineer might ask about VFD profile for BGW-06 and the ideal grounded answer using only {"well": "BGW-06", "api": 18.617, "asphaltene_wt_pct": 8.977, "latest_cycle": 10, "steam_t": 910.0, "sor": 32.106, "cum_oil_bbl": 178.277, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00208
Write a question an OIL production engineer might ask about pump unseating for BGW-07 and the ideal grounded answer using only {"well": "BGW-07", "api": 18.131, "asphaltene_wt_pct": 11.233, "latest_cycle": 7, "steam_t": 866.0, "sor": 25.808, "cum_oil_bbl": 211.06, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00209
Write a question an OIL production engineer might ask about VFD profile for BGW-39 and the ideal grounded answer using only {"well": "BGW-39", "api": 17.782, "asphaltene_wt_pct": 7.693, "latest_cycle": 11, "steam_t": 986.0, "sor": 13.456, "cum_oil_bbl": 460.89, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00210
Write a question an OIL production engineer might ask about soak length for BGW-55 and the ideal grounded answer using only {"well": "BGW-55", "api": 19.209, "asphaltene_wt_pct": 10.811, "latest_cycle": 9, "steam_t": 914.0, "sor": 7.658, "cum_oil_bbl": 750.704, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00211
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-31 and the ideal grounded answer using only {"well": "BGW-31", "api": 17.565, "asphaltene_wt_pct": 7.32, "latest_cycle": 9, "steam_t": 741.0, "sor": 11.279, "cum_oil_bbl": 413.207, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00212
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-52 and the ideal grounded answer using only {"well": "BGW-52", "api": 17.22, "asphaltene_wt_pct": 8.888, "latest_cycle": 8, "steam_t": 807.0, "sor": 43.678, "cum_oil_bbl": 116.212, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00213
Write a question an OIL production engineer might ask about cut-off timing for BGW-47 and the ideal grounded answer using only {"well": "BGW-47", "api": 17.914, "asphaltene_wt_pct": 7.827, "latest_cycle": 8, "steam_t": 801.0, "sor": 57.396, "cum_oil_bbl": 87.778, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00214
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00215
Write a question an OIL production engineer might ask about fluid pound for BGW-09 and the ideal grounded answer using only {"well": "BGW-09", "api": 17.699, "asphaltene_wt_pct": 11.072, "latest_cycle": 10, "steam_t": 858.0, "sor": 80.402, "cum_oil_bbl": 67.121, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00216
Write a question an OIL production engineer might ask about cut-off timing for BGW-37 and the ideal grounded answer using only {"well": "BGW-37", "api": 17.504, "asphaltene_wt_pct": 8.662, "latest_cycle": 8, "steam_t": 954.0, "sor": 6.946, "cum_oil_bbl": 863.932, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00217
Write a question an OIL production engineer might ask about soak length for BGW-55 and the ideal grounded answer using only {"well": "BGW-55", "api": 19.209, "asphaltene_wt_pct": 10.811, "latest_cycle": 9, "steam_t": 914.0, "sor": 7.658, "cum_oil_bbl": 750.704, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00218
Write a question an OIL production engineer might ask about SOR for BGW-42 and the ideal grounded answer using only {"well": "BGW-42", "api": 18.115, "asphaltene_wt_pct": 10.113, "latest_cycle": 12, "steam_t": 963.0, "sor": 46.099, "cum_oil_bbl": 131.393, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00219
Write a question an OIL production engineer might ask about fluid pound for BGW-13 and the ideal grounded answer using only {"well": "BGW-13", "api": 18.616, "asphaltene_wt_pct": 7.177, "latest_cycle": 9, "steam_t": 1038.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00220
Write a question an OIL production engineer might ask about rod float for BGW-56 and the ideal grounded answer using only {"well": "BGW-56", "api": 19.25, "asphaltene_wt_pct": 9.106, "latest_cycle": 13, "steam_t": 963.0, "sor": 99.0, "cum_oil_bbl": 58.714, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00221
Write a question an OIL production engineer might ask about VFD profile for BGW-28 and the ideal grounded answer using only {"well": "BGW-28", "api": 18.019, "asphaltene_wt_pct": 11.024, "latest_cycle": 10, "steam_t": 1054.0, "sor": 25.776, "cum_oil_bbl": 257.197, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00222
Write a question an OIL production engineer might ask about cut-off timing for BGW-16 and the ideal grounded answer using only {"well": "BGW-16", "api": 18.381, "asphaltene_wt_pct": 8.983, "latest_cycle": 7, "steam_t": 867.0, "sor": 20.459, "cum_oil_bbl": 266.542, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00223
Write a question an OIL production engineer might ask about cut-off timing for BGW-26 and the ideal grounded answer using only {"well": "BGW-26", "api": 19.143, "asphaltene_wt_pct": 8.64, "latest_cycle": 10, "steam_t": 857.0, "sor": 6.357, "cum_oil_bbl": 847.913, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00224
Write a question an OIL production engineer might ask about soak length for BGW-19 and the ideal grounded answer using only {"well": "BGW-19", "api": 17.44, "asphaltene_wt_pct": 7.906, "latest_cycle": 11, "steam_t": 952.0, "sor": 5.675, "cum_oil_bbl": 1055.081, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
