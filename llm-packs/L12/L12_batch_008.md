# L12 copilot_qa - batch 008 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_008.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00175 .. L12-00199 (each has an `item_id` you must echo).

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

### item_id: L12-00175
Write a question an OIL production engineer might ask about SOR for BGW-33 and the ideal grounded answer using only {"well": "BGW-33", "api": 17.468, "asphaltene_wt_pct": 7.465, "latest_cycle": 8, "steam_t": 1074.0, "sor": 18.825, "cum_oil_bbl": 358.852, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00176
Write a question an OIL production engineer might ask about VFD profile for BGW-31 and the ideal grounded answer using only {"well": "BGW-31", "api": 17.565, "asphaltene_wt_pct": 7.32, "latest_cycle": 9, "steam_t": 741.0, "sor": 11.279, "cum_oil_bbl": 413.207, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00177
Write a question an OIL production engineer might ask about SOR for BGW-35 and the ideal grounded answer using only {"well": "BGW-35", "api": 18.034, "asphaltene_wt_pct": 8.047, "latest_cycle": 8, "steam_t": 947.0, "sor": 13.623, "cum_oil_bbl": 437.229, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00178
Write a question an OIL production engineer might ask about cut-off timing for BGW-03 and the ideal grounded answer using only {"well": "BGW-03", "api": 19.223, "asphaltene_wt_pct": 7.28, "latest_cycle": 8, "steam_t": 885.0, "sor": 99.0, "cum_oil_bbl": 7.913, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00179
Write a question an OIL production engineer might ask about SOR for BGW-59 and the ideal grounded answer using only {"well": "BGW-59", "api": 18.603, "asphaltene_wt_pct": 7.439, "latest_cycle": 9, "steam_t": 683.0, "sor": 3.26, "cum_oil_bbl": 1317.806, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00180
Write a question an OIL production engineer might ask about pump unseating for BGW-39 and the ideal grounded answer using only {"well": "BGW-39", "api": 17.782, "asphaltene_wt_pct": 7.693, "latest_cycle": 11, "steam_t": 986.0, "sor": 13.456, "cum_oil_bbl": 460.89, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00181
Write a question an OIL production engineer might ask about pump unseating for BGW-04 and the ideal grounded answer using only {"well": "BGW-04", "api": 17.637, "asphaltene_wt_pct": 9.561, "latest_cycle": 12, "steam_t": 721.0, "sor": 10.942, "cum_oil_bbl": 414.437, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00182
Write a question an OIL production engineer might ask about fluid pound for BGW-11 and the ideal grounded answer using only {"well": "BGW-11", "api": 19.26, "asphaltene_wt_pct": 8.28, "latest_cycle": 9, "steam_t": 1081.0, "sor": 8.694, "cum_oil_bbl": 782.105, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00183
Write a question an OIL production engineer might ask about fluid pound for BGW-36 and the ideal grounded answer using only {"well": "BGW-36", "api": 19.377, "asphaltene_wt_pct": 7.717, "latest_cycle": 12, "steam_t": 860.0, "sor": 10.567, "cum_oil_bbl": 511.913, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00184
Write a question an OIL production engineer might ask about fluid pound for BGW-04 and the ideal grounded answer using only {"well": "BGW-04", "api": 17.637, "asphaltene_wt_pct": 9.561, "latest_cycle": 12, "steam_t": 721.0, "sor": 10.942, "cum_oil_bbl": 414.437, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00185
Write a question an OIL production engineer might ask about SOR for BGW-32 and the ideal grounded answer using only {"well": "BGW-32", "api": 17.818, "asphaltene_wt_pct": 7.204, "latest_cycle": 12, "steam_t": 762.0, "sor": 15.74, "cum_oil_bbl": 304.49, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00186
Write a question an OIL production engineer might ask about pump unseating for BGW-06 and the ideal grounded answer using only {"well": "BGW-06", "api": 18.617, "asphaltene_wt_pct": 8.977, "latest_cycle": 10, "steam_t": 910.0, "sor": 32.106, "cum_oil_bbl": 178.277, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00187
Write a question an OIL production engineer might ask about fluid pound for BGW-29 and the ideal grounded answer using only {"well": "BGW-29", "api": 18.623, "asphaltene_wt_pct": 10.858, "latest_cycle": 9, "steam_t": 818.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00188
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-04 and the ideal grounded answer using only {"well": "BGW-04", "api": 17.637, "asphaltene_wt_pct": 9.561, "latest_cycle": 12, "steam_t": 721.0, "sor": 10.942, "cum_oil_bbl": 414.437, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00189
Write a question an OIL production engineer might ask about fluid pound for BGW-27 and the ideal grounded answer using only {"well": "BGW-27", "api": 18.998, "asphaltene_wt_pct": 10.959, "latest_cycle": 13, "steam_t": 768.0, "sor": 3.261, "cum_oil_bbl": 1481.358, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00190
Write a question an OIL production engineer might ask about rod float for BGW-33 and the ideal grounded answer using only {"well": "BGW-33", "api": 17.468, "asphaltene_wt_pct": 7.465, "latest_cycle": 8, "steam_t": 1074.0, "sor": 18.825, "cum_oil_bbl": 358.852, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00191
Write a question an OIL production engineer might ask about SOR for BGW-01 and the ideal grounded answer using only {"well": "BGW-01", "api": 19.123, "asphaltene_wt_pct": 10.261, "latest_cycle": 11, "steam_t": 875.0, "sor": 6.458, "cum_oil_bbl": 852.192, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00192
Write a question an OIL production engineer might ask about SOR for BGW-02 and the ideal grounded answer using only {"well": "BGW-02", "api": 17.704, "asphaltene_wt_pct": 11.955, "latest_cycle": 10, "steam_t": 1015.0, "sor": 44.034, "cum_oil_bbl": 144.983, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00193
Write a question an OIL production engineer might ask about fluid pound for BGW-54 and the ideal grounded answer using only {"well": "BGW-54", "api": 17.171, "asphaltene_wt_pct": 8.036, "latest_cycle": 13, "steam_t": 876.0, "sor": 77.783, "cum_oil_bbl": 70.837, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00194
Write a question an OIL production engineer might ask about VFD profile for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00195
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-23 and the ideal grounded answer using only {"well": "BGW-23", "api": 19.107, "asphaltene_wt_pct": 8.685, "latest_cycle": 13, "steam_t": 933.0, "sor": 81.264, "cum_oil_bbl": 72.213, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00196
Write a question an OIL production engineer might ask about pump unseating for BGW-21 and the ideal grounded answer using only {"well": "BGW-21", "api": 18.299, "asphaltene_wt_pct": 11.532, "latest_cycle": 11, "steam_t": 682.0, "sor": 3.491, "cum_oil_bbl": 1228.65, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00197
Write a question an OIL production engineer might ask about soak length for BGW-32 and the ideal grounded answer using only {"well": "BGW-32", "api": 17.818, "asphaltene_wt_pct": 7.204, "latest_cycle": 12, "steam_t": 762.0, "sor": 15.74, "cum_oil_bbl": 304.49, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00198
Write a question an OIL production engineer might ask about cut-off timing for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00199
Write a question an OIL production engineer might ask about fluid pound for BGW-11 and the ideal grounded answer using only {"well": "BGW-11", "api": 19.26, "asphaltene_wt_pct": 8.28, "latest_cycle": 9, "steam_t": 1081.0, "sor": 8.694, "cum_oil_bbl": 782.105, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
