# L12 copilot_qa - batch 010 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_010.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00225 .. L12-00249 (each has an `item_id` you must echo).

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

### item_id: L12-00225
Write a question an OIL production engineer might ask about fluid pound for BGW-15 and the ideal grounded answer using only {"well": "BGW-15", "api": 18.179, "asphaltene_wt_pct": 8.151, "latest_cycle": 13, "steam_t": 960.0, "sor": 12.245, "cum_oil_bbl": 493.113, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00226
Write a question an OIL production engineer might ask about SOR for BGW-19 and the ideal grounded answer using only {"well": "BGW-19", "api": 17.44, "asphaltene_wt_pct": 7.906, "latest_cycle": 11, "steam_t": 952.0, "sor": 5.675, "cum_oil_bbl": 1055.081, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00227
Write a question an OIL production engineer might ask about SOR for BGW-21 and the ideal grounded answer using only {"well": "BGW-21", "api": 18.299, "asphaltene_wt_pct": 11.532, "latest_cycle": 11, "steam_t": 682.0, "sor": 3.491, "cum_oil_bbl": 1228.65, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00228
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-01 and the ideal grounded answer using only {"well": "BGW-01", "api": 19.123, "asphaltene_wt_pct": 10.261, "latest_cycle": 11, "steam_t": 875.0, "sor": 6.458, "cum_oil_bbl": 852.192, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00229
Write a question an OIL production engineer might ask about rod float for BGW-08 and the ideal grounded answer using only {"well": "BGW-08", "api": 18.197, "asphaltene_wt_pct": 10.749, "latest_cycle": 13, "steam_t": 1049.0, "sor": 11.817, "cum_oil_bbl": 558.353, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00230
Write a question an OIL production engineer might ask about soak length for BGW-19 and the ideal grounded answer using only {"well": "BGW-19", "api": 17.44, "asphaltene_wt_pct": 7.906, "latest_cycle": 11, "steam_t": 952.0, "sor": 5.675, "cum_oil_bbl": 1055.081, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00231
Write a question an OIL production engineer might ask about VFD profile for BGW-54 and the ideal grounded answer using only {"well": "BGW-54", "api": 17.171, "asphaltene_wt_pct": 8.036, "latest_cycle": 13, "steam_t": 876.0, "sor": 77.783, "cum_oil_bbl": 70.837, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00232
Write a question an OIL production engineer might ask about pump unseating for BGW-04 and the ideal grounded answer using only {"well": "BGW-04", "api": 17.637, "asphaltene_wt_pct": 9.561, "latest_cycle": 12, "steam_t": 721.0, "sor": 10.942, "cum_oil_bbl": 414.437, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00233
Write a question an OIL production engineer might ask about VFD profile for BGW-08 and the ideal grounded answer using only {"well": "BGW-08", "api": 18.197, "asphaltene_wt_pct": 10.749, "latest_cycle": 13, "steam_t": 1049.0, "sor": 11.817, "cum_oil_bbl": 558.353, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00234
Write a question an OIL production engineer might ask about pump unseating for BGW-59 and the ideal grounded answer using only {"well": "BGW-59", "api": 18.603, "asphaltene_wt_pct": 7.439, "latest_cycle": 9, "steam_t": 683.0, "sor": 3.26, "cum_oil_bbl": 1317.806, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00235
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-54 and the ideal grounded answer using only {"well": "BGW-54", "api": 17.171, "asphaltene_wt_pct": 8.036, "latest_cycle": 13, "steam_t": 876.0, "sor": 77.783, "cum_oil_bbl": 70.837, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00236
Write a question an OIL production engineer might ask about fluid pound for BGW-34 and the ideal grounded answer using only {"well": "BGW-34", "api": 17.392, "asphaltene_wt_pct": 11.811, "latest_cycle": 8, "steam_t": 1000.0, "sor": 16.899, "cum_oil_bbl": 372.2, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00237
Write a question an OIL production engineer might ask about VFD profile for BGW-18 and the ideal grounded answer using only {"well": "BGW-18", "api": 18.012, "asphaltene_wt_pct": 8.643, "latest_cycle": 12, "steam_t": 1077.0, "sor": 11.484, "cum_oil_bbl": 589.884, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00238
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-01 and the ideal grounded answer using only {"well": "BGW-01", "api": 19.123, "asphaltene_wt_pct": 10.261, "latest_cycle": 11, "steam_t": 875.0, "sor": 6.458, "cum_oil_bbl": 852.192, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00239
Write a question an OIL production engineer might ask about fluid pound for BGW-06 and the ideal grounded answer using only {"well": "BGW-06", "api": 18.617, "asphaltene_wt_pct": 8.977, "latest_cycle": 10, "steam_t": 910.0, "sor": 32.106, "cum_oil_bbl": 178.277, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00240
Write a question an OIL production engineer might ask about fluid pound for BGW-27 and the ideal grounded answer using only {"well": "BGW-27", "api": 18.998, "asphaltene_wt_pct": 10.959, "latest_cycle": 13, "steam_t": 768.0, "sor": 3.261, "cum_oil_bbl": 1481.358, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00241
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-38 and the ideal grounded answer using only {"well": "BGW-38", "api": 18.964, "asphaltene_wt_pct": 9.072, "latest_cycle": 11, "steam_t": 873.0, "sor": 3.647, "cum_oil_bbl": 1505.754, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00242
Write a question an OIL production engineer might ask about VFD profile for BGW-34 and the ideal grounded answer using only {"well": "BGW-34", "api": 17.392, "asphaltene_wt_pct": 11.811, "latest_cycle": 8, "steam_t": 1000.0, "sor": 16.899, "cum_oil_bbl": 372.2, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00243
Write a question an OIL production engineer might ask about rod float for BGW-09 and the ideal grounded answer using only {"well": "BGW-09", "api": 17.699, "asphaltene_wt_pct": 11.072, "latest_cycle": 10, "steam_t": 858.0, "sor": 80.402, "cum_oil_bbl": 67.121, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00244
Write a question an OIL production engineer might ask about rod float for BGW-44 and the ideal grounded answer using only {"well": "BGW-44", "api": 17.215, "asphaltene_wt_pct": 9.398, "latest_cycle": 13, "steam_t": 875.0, "sor": 16.715, "cum_oil_bbl": 329.26, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00245
Write a question an OIL production engineer might ask about fluid pound for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00246
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-58 and the ideal grounded answer using only {"well": "BGW-58", "api": 17.755, "asphaltene_wt_pct": 10.969, "latest_cycle": 12, "steam_t": 987.0, "sor": 14.054, "cum_oil_bbl": 441.729, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00247
Write a question an OIL production engineer might ask about cut-off timing for BGW-36 and the ideal grounded answer using only {"well": "BGW-36", "api": 19.377, "asphaltene_wt_pct": 7.717, "latest_cycle": 12, "steam_t": 860.0, "sor": 10.567, "cum_oil_bbl": 511.913, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00248
Write a question an OIL production engineer might ask about fluid pound for BGW-40 and the ideal grounded answer using only {"well": "BGW-40", "api": 17.037, "asphaltene_wt_pct": 11.206, "latest_cycle": 7, "steam_t": 817.0, "sor": 6.255, "cum_oil_bbl": 821.561, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00249
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-33 and the ideal grounded answer using only {"well": "BGW-33", "api": 17.468, "asphaltene_wt_pct": 7.465, "latest_cycle": 8, "steam_t": 1074.0, "sor": 18.825, "cum_oil_bbl": 358.852, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
