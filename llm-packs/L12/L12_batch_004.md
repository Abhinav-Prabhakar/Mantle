# L12 copilot_qa - batch 004 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_004.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00075 .. L12-00099 (each has an `item_id` you must echo).

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

### item_id: L12-00075
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-18 and the ideal grounded answer using only {"well": "BGW-18", "api": 18.012, "asphaltene_wt_pct": 8.643, "latest_cycle": 12, "steam_t": 1077.0, "sor": 11.484, "cum_oil_bbl": 589.884, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00076
Write a question an OIL production engineer might ask about VFD profile for BGW-16 and the ideal grounded answer using only {"well": "BGW-16", "api": 18.381, "asphaltene_wt_pct": 8.983, "latest_cycle": 7, "steam_t": 867.0, "sor": 20.459, "cum_oil_bbl": 266.542, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00077
Write a question an OIL production engineer might ask about soak length for BGW-39 and the ideal grounded answer using only {"well": "BGW-39", "api": 17.782, "asphaltene_wt_pct": 7.693, "latest_cycle": 11, "steam_t": 986.0, "sor": 13.456, "cum_oil_bbl": 460.89, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00078
Write a question an OIL production engineer might ask about VFD profile for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00079
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-60 and the ideal grounded answer using only {"well": "BGW-60", "api": 17.825, "asphaltene_wt_pct": 8.092, "latest_cycle": 13, "steam_t": 873.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00080
Write a question an OIL production engineer might ask about pump unseating for BGW-06 and the ideal grounded answer using only {"well": "BGW-06", "api": 18.617, "asphaltene_wt_pct": 8.977, "latest_cycle": 10, "steam_t": 910.0, "sor": 32.106, "cum_oil_bbl": 178.277, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00081
Write a question an OIL production engineer might ask about soak length for BGW-16 and the ideal grounded answer using only {"well": "BGW-16", "api": 18.381, "asphaltene_wt_pct": 8.983, "latest_cycle": 7, "steam_t": 867.0, "sor": 20.459, "cum_oil_bbl": 266.542, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00082
Write a question an OIL production engineer might ask about cut-off timing for BGW-55 and the ideal grounded answer using only {"well": "BGW-55", "api": 19.209, "asphaltene_wt_pct": 10.811, "latest_cycle": 9, "steam_t": 914.0, "sor": 7.658, "cum_oil_bbl": 750.704, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00083
Write a question an OIL production engineer might ask about fluid pound for BGW-27 and the ideal grounded answer using only {"well": "BGW-27", "api": 18.998, "asphaltene_wt_pct": 10.959, "latest_cycle": 13, "steam_t": 768.0, "sor": 3.261, "cum_oil_bbl": 1481.358, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00084
Write a question an OIL production engineer might ask about cut-off timing for BGW-33 and the ideal grounded answer using only {"well": "BGW-33", "api": 17.468, "asphaltene_wt_pct": 7.465, "latest_cycle": 8, "steam_t": 1074.0, "sor": 18.825, "cum_oil_bbl": 358.852, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00085
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-05 and the ideal grounded answer using only {"well": "BGW-05", "api": 18.657, "asphaltene_wt_pct": 11.621, "latest_cycle": 13, "steam_t": 1033.0, "sor": 15.762, "cum_oil_bbl": 412.213, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00086
Write a question an OIL production engineer might ask about VFD profile for BGW-41 and the ideal grounded answer using only {"well": "BGW-41", "api": 17.921, "asphaltene_wt_pct": 11.897, "latest_cycle": 13, "steam_t": 751.0, "sor": 12.296, "cum_oil_bbl": 384.151, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00087
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-56 and the ideal grounded answer using only {"well": "BGW-56", "api": 19.25, "asphaltene_wt_pct": 9.106, "latest_cycle": 13, "steam_t": 963.0, "sor": 99.0, "cum_oil_bbl": 58.714, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00088
Write a question an OIL production engineer might ask about fluid pound for BGW-60 and the ideal grounded answer using only {"well": "BGW-60", "api": 17.825, "asphaltene_wt_pct": 8.092, "latest_cycle": 13, "steam_t": 873.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00089
Write a question an OIL production engineer might ask about fluid pound for BGW-25 and the ideal grounded answer using only {"well": "BGW-25", "api": 18.864, "asphaltene_wt_pct": 9.088, "latest_cycle": 11, "steam_t": 861.0, "sor": 16.88, "cum_oil_bbl": 320.818, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00090
Write a question an OIL production engineer might ask about rod float for BGW-18 and the ideal grounded answer using only {"well": "BGW-18", "api": 18.012, "asphaltene_wt_pct": 8.643, "latest_cycle": 12, "steam_t": 1077.0, "sor": 11.484, "cum_oil_bbl": 589.884, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00091
Write a question an OIL production engineer might ask about fluid pound for BGW-01 and the ideal grounded answer using only {"well": "BGW-01", "api": 19.123, "asphaltene_wt_pct": 10.261, "latest_cycle": 11, "steam_t": 875.0, "sor": 6.458, "cum_oil_bbl": 852.192, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00092
Write a question an OIL production engineer might ask about VFD profile for BGW-50 and the ideal grounded answer using only {"well": "BGW-50", "api": 17.287, "asphaltene_wt_pct": 11.817, "latest_cycle": 11, "steam_t": 855.0, "sor": 5.708, "cum_oil_bbl": 942.228, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00093
Write a question an OIL production engineer might ask about VFD profile for BGW-13 and the ideal grounded answer using only {"well": "BGW-13", "api": 18.616, "asphaltene_wt_pct": 7.177, "latest_cycle": 9, "steam_t": 1038.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00094
Write a question an OIL production engineer might ask about fluid pound for BGW-26 and the ideal grounded answer using only {"well": "BGW-26", "api": 19.143, "asphaltene_wt_pct": 8.64, "latest_cycle": 10, "steam_t": 857.0, "sor": 6.357, "cum_oil_bbl": 847.913, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00095
Write a question an OIL production engineer might ask about cut-off timing for BGW-14 and the ideal grounded answer using only {"well": "BGW-14", "api": 18.11, "asphaltene_wt_pct": 10.75, "latest_cycle": 12, "steam_t": 1099.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00096
Write a question an OIL production engineer might ask about soak length for BGW-44 and the ideal grounded answer using only {"well": "BGW-44", "api": 17.215, "asphaltene_wt_pct": 9.398, "latest_cycle": 13, "steam_t": 875.0, "sor": 16.715, "cum_oil_bbl": 329.26, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00097
Write a question an OIL production engineer might ask about cut-off timing for BGW-20 and the ideal grounded answer using only {"well": "BGW-20", "api": 17.004, "asphaltene_wt_pct": 7.221, "latest_cycle": 13, "steam_t": 954.0, "sor": 11.028, "cum_oil_bbl": 544.121, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00098
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-25 and the ideal grounded answer using only {"well": "BGW-25", "api": 18.864, "asphaltene_wt_pct": 9.088, "latest_cycle": 11, "steam_t": 861.0, "sor": 16.88, "cum_oil_bbl": 320.818, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00099
Write a question an OIL production engineer might ask about soak length for BGW-02 and the ideal grounded answer using only {"well": "BGW-02", "api": 17.704, "asphaltene_wt_pct": 11.955, "latest_cycle": 10, "steam_t": 1015.0, "sor": 44.034, "cum_oil_bbl": 144.983, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
