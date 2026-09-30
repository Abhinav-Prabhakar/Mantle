# L12 copilot_qa - batch 006 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_006.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00125 .. L12-00149 (each has an `item_id` you must echo).

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

### item_id: L12-00125
Write a question an OIL production engineer might ask about VFD profile for BGW-23 and the ideal grounded answer using only {"well": "BGW-23", "api": 19.107, "asphaltene_wt_pct": 8.685, "latest_cycle": 13, "steam_t": 933.0, "sor": 81.264, "cum_oil_bbl": 72.213, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00126
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-50 and the ideal grounded answer using only {"well": "BGW-50", "api": 17.287, "asphaltene_wt_pct": 11.817, "latest_cycle": 11, "steam_t": 855.0, "sor": 5.708, "cum_oil_bbl": 942.228, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00127
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-52 and the ideal grounded answer using only {"well": "BGW-52", "api": 17.22, "asphaltene_wt_pct": 8.888, "latest_cycle": 8, "steam_t": 807.0, "sor": 43.678, "cum_oil_bbl": 116.212, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00128
Write a question an OIL production engineer might ask about soak length for BGW-40 and the ideal grounded answer using only {"well": "BGW-40", "api": 17.037, "asphaltene_wt_pct": 11.206, "latest_cycle": 7, "steam_t": 817.0, "sor": 6.255, "cum_oil_bbl": 821.561, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00129
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-05 and the ideal grounded answer using only {"well": "BGW-05", "api": 18.657, "asphaltene_wt_pct": 11.621, "latest_cycle": 13, "steam_t": 1033.0, "sor": 15.762, "cum_oil_bbl": 412.213, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00130
Write a question an OIL production engineer might ask about fluid pound for BGW-42 and the ideal grounded answer using only {"well": "BGW-42", "api": 18.115, "asphaltene_wt_pct": 10.113, "latest_cycle": 12, "steam_t": 963.0, "sor": 46.099, "cum_oil_bbl": 131.393, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00131
Write a question an OIL production engineer might ask about VFD profile for BGW-17 and the ideal grounded answer using only {"well": "BGW-17", "api": 18.0, "asphaltene_wt_pct": 9.2, "latest_cycle": 4, "steam_t": 800.0, "sor": 3.481, "cum_oil_bbl": 1445.611, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00132
Write a question an OIL production engineer might ask about soak length for BGW-41 and the ideal grounded answer using only {"well": "BGW-41", "api": 17.921, "asphaltene_wt_pct": 11.897, "latest_cycle": 13, "steam_t": 751.0, "sor": 12.296, "cum_oil_bbl": 384.151, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00133
Write a question an OIL production engineer might ask about soak length for BGW-25 and the ideal grounded answer using only {"well": "BGW-25", "api": 18.864, "asphaltene_wt_pct": 9.088, "latest_cycle": 11, "steam_t": 861.0, "sor": 16.88, "cum_oil_bbl": 320.818, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00134
Write a question an OIL production engineer might ask about fluid pound for BGW-04 and the ideal grounded answer using only {"well": "BGW-04", "api": 17.637, "asphaltene_wt_pct": 9.561, "latest_cycle": 12, "steam_t": 721.0, "sor": 10.942, "cum_oil_bbl": 414.437, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00135
Write a question an OIL production engineer might ask about pump unseating for BGW-26 and the ideal grounded answer using only {"well": "BGW-26", "api": 19.143, "asphaltene_wt_pct": 8.64, "latest_cycle": 10, "steam_t": 857.0, "sor": 6.357, "cum_oil_bbl": 847.913, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00136
Write a question an OIL production engineer might ask about rod float for BGW-05 and the ideal grounded answer using only {"well": "BGW-05", "api": 18.657, "asphaltene_wt_pct": 11.621, "latest_cycle": 13, "steam_t": 1033.0, "sor": 15.762, "cum_oil_bbl": 412.213, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00137
Write a question an OIL production engineer might ask about cut-off timing for BGW-21 and the ideal grounded answer using only {"well": "BGW-21", "api": 18.299, "asphaltene_wt_pct": 11.532, "latest_cycle": 11, "steam_t": 682.0, "sor": 3.491, "cum_oil_bbl": 1228.65, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00138
Write a question an OIL production engineer might ask about SOR for BGW-56 and the ideal grounded answer using only {"well": "BGW-56", "api": 19.25, "asphaltene_wt_pct": 9.106, "latest_cycle": 13, "steam_t": 963.0, "sor": 99.0, "cum_oil_bbl": 58.714, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00139
Write a question an OIL production engineer might ask about soak length for BGW-36 and the ideal grounded answer using only {"well": "BGW-36", "api": 19.377, "asphaltene_wt_pct": 7.717, "latest_cycle": 12, "steam_t": 860.0, "sor": 10.567, "cum_oil_bbl": 511.913, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00140
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-43 and the ideal grounded answer using only {"well": "BGW-43", "api": 19.306, "asphaltene_wt_pct": 7.141, "latest_cycle": 10, "steam_t": 923.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00141
Write a question an OIL production engineer might ask about SOR for BGW-46 and the ideal grounded answer using only {"well": "BGW-46", "api": 18.204, "asphaltene_wt_pct": 8.946, "latest_cycle": 10, "steam_t": 947.0, "sor": 7.168, "cum_oil_bbl": 831.012, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00142
Write a question an OIL production engineer might ask about fluid pound for BGW-55 and the ideal grounded answer using only {"well": "BGW-55", "api": 19.209, "asphaltene_wt_pct": 10.811, "latest_cycle": 9, "steam_t": 914.0, "sor": 7.658, "cum_oil_bbl": 750.704, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00143
Write a question an OIL production engineer might ask about rod float for BGW-13 and the ideal grounded answer using only {"well": "BGW-13", "api": 18.616, "asphaltene_wt_pct": 7.177, "latest_cycle": 9, "steam_t": 1038.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00144
Write a question an OIL production engineer might ask about pump unseating for BGW-46 and the ideal grounded answer using only {"well": "BGW-46", "api": 18.204, "asphaltene_wt_pct": 8.946, "latest_cycle": 10, "steam_t": 947.0, "sor": 7.168, "cum_oil_bbl": 831.012, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00145
Write a question an OIL production engineer might ask about pump unseating for BGW-05 and the ideal grounded answer using only {"well": "BGW-05", "api": 18.657, "asphaltene_wt_pct": 11.621, "latest_cycle": 13, "steam_t": 1033.0, "sor": 15.762, "cum_oil_bbl": 412.213, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00146
Write a question an OIL production engineer might ask about SOR for BGW-45 and the ideal grounded answer using only {"well": "BGW-45", "api": 19.049, "asphaltene_wt_pct": 7.775, "latest_cycle": 10, "steam_t": 961.0, "sor": 45.979, "cum_oil_bbl": 131.462, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00147
Write a question an OIL production engineer might ask about soak length for BGW-22 and the ideal grounded answer using only {"well": "BGW-22", "api": 19.273, "asphaltene_wt_pct": 9.486, "latest_cycle": 12, "steam_t": 871.0, "sor": 7.051, "cum_oil_bbl": 776.94, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00148
Write a question an OIL production engineer might ask about cut-off timing for BGW-07 and the ideal grounded answer using only {"well": "BGW-07", "api": 18.131, "asphaltene_wt_pct": 11.233, "latest_cycle": 7, "steam_t": 866.0, "sor": 25.808, "cum_oil_bbl": 211.06, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00149
Write a question an OIL production engineer might ask about rod float for BGW-07 and the ideal grounded answer using only {"well": "BGW-07", "api": 18.131, "asphaltene_wt_pct": 11.233, "latest_cycle": 7, "steam_t": 866.0, "sor": 25.808, "cum_oil_bbl": 211.06, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
