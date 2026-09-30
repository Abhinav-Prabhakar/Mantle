# L12 copilot_qa - batch 003 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_003.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00050 .. L12-00074 (each has an `item_id` you must echo).

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

### item_id: L12-00050
Write a question an OIL production engineer might ask about rod float for BGW-56 and the ideal grounded answer using only {"well": "BGW-56", "api": 19.25, "asphaltene_wt_pct": 9.106, "latest_cycle": 13, "steam_t": 963.0, "sor": 99.0, "cum_oil_bbl": 58.714, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00051
Write a question an OIL production engineer might ask about rod float for BGW-33 and the ideal grounded answer using only {"well": "BGW-33", "api": 17.468, "asphaltene_wt_pct": 7.465, "latest_cycle": 8, "steam_t": 1074.0, "sor": 18.825, "cum_oil_bbl": 358.852, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00052
Write a question an OIL production engineer might ask about soak length for BGW-04 and the ideal grounded answer using only {"well": "BGW-04", "api": 17.637, "asphaltene_wt_pct": 9.561, "latest_cycle": 12, "steam_t": 721.0, "sor": 10.942, "cum_oil_bbl": 414.437, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00053
Write a question an OIL production engineer might ask about soak length for BGW-05 and the ideal grounded answer using only {"well": "BGW-05", "api": 18.657, "asphaltene_wt_pct": 11.621, "latest_cycle": 13, "steam_t": 1033.0, "sor": 15.762, "cum_oil_bbl": 412.213, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00054
Write a question an OIL production engineer might ask about cut-off timing for BGW-46 and the ideal grounded answer using only {"well": "BGW-46", "api": 18.204, "asphaltene_wt_pct": 8.946, "latest_cycle": 10, "steam_t": 947.0, "sor": 7.168, "cum_oil_bbl": 831.012, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00055
Write a question an OIL production engineer might ask about soak length for BGW-40 and the ideal grounded answer using only {"well": "BGW-40", "api": 17.037, "asphaltene_wt_pct": 11.206, "latest_cycle": 7, "steam_t": 817.0, "sor": 6.255, "cum_oil_bbl": 821.561, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00056
Write a question an OIL production engineer might ask about SOR for BGW-12 and the ideal grounded answer using only {"well": "BGW-12", "api": 19.052, "asphaltene_wt_pct": 11.602, "latest_cycle": 11, "steam_t": 1200.0, "sor": 4.396, "cum_oil_bbl": 1716.802, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00057
Write a question an OIL production engineer might ask about SOR for BGW-55 and the ideal grounded answer using only {"well": "BGW-55", "api": 19.209, "asphaltene_wt_pct": 10.811, "latest_cycle": 9, "steam_t": 914.0, "sor": 7.658, "cum_oil_bbl": 750.704, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00058
Write a question an OIL production engineer might ask about SOR for BGW-44 and the ideal grounded answer using only {"well": "BGW-44", "api": 17.215, "asphaltene_wt_pct": 9.398, "latest_cycle": 13, "steam_t": 875.0, "sor": 16.715, "cum_oil_bbl": 329.26, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00059
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-33 and the ideal grounded answer using only {"well": "BGW-33", "api": 17.468, "asphaltene_wt_pct": 7.465, "latest_cycle": 8, "steam_t": 1074.0, "sor": 18.825, "cum_oil_bbl": 358.852, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00060
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-25 and the ideal grounded answer using only {"well": "BGW-25", "api": 18.864, "asphaltene_wt_pct": 9.088, "latest_cycle": 11, "steam_t": 861.0, "sor": 16.88, "cum_oil_bbl": 320.818, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00061
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-21 and the ideal grounded answer using only {"well": "BGW-21", "api": 18.299, "asphaltene_wt_pct": 11.532, "latest_cycle": 11, "steam_t": 682.0, "sor": 3.491, "cum_oil_bbl": 1228.65, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00062
Write a question an OIL production engineer might ask about SOR for BGW-42 and the ideal grounded answer using only {"well": "BGW-42", "api": 18.115, "asphaltene_wt_pct": 10.113, "latest_cycle": 12, "steam_t": 963.0, "sor": 46.099, "cum_oil_bbl": 131.393, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00063
Write a question an OIL production engineer might ask about pump unseating for BGW-14 and the ideal grounded answer using only {"well": "BGW-14", "api": 18.11, "asphaltene_wt_pct": 10.75, "latest_cycle": 12, "steam_t": 1099.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00064
Write a question an OIL production engineer might ask about pump unseating for BGW-22 and the ideal grounded answer using only {"well": "BGW-22", "api": 19.273, "asphaltene_wt_pct": 9.486, "latest_cycle": 12, "steam_t": 871.0, "sor": 7.051, "cum_oil_bbl": 776.94, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00065
Write a question an OIL production engineer might ask about rod float for BGW-06 and the ideal grounded answer using only {"well": "BGW-06", "api": 18.617, "asphaltene_wt_pct": 8.977, "latest_cycle": 10, "steam_t": 910.0, "sor": 32.106, "cum_oil_bbl": 178.277, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00066
Write a question an OIL production engineer might ask about rod float for BGW-35 and the ideal grounded answer using only {"well": "BGW-35", "api": 18.034, "asphaltene_wt_pct": 8.047, "latest_cycle": 8, "steam_t": 947.0, "sor": 13.623, "cum_oil_bbl": 437.229, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00067
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-33 and the ideal grounded answer using only {"well": "BGW-33", "api": 17.468, "asphaltene_wt_pct": 7.465, "latest_cycle": 8, "steam_t": 1074.0, "sor": 18.825, "cum_oil_bbl": 358.852, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00068
Write a question an OIL production engineer might ask about fluid pound for BGW-51 and the ideal grounded answer using only {"well": "BGW-51", "api": 19.384, "asphaltene_wt_pct": 7.974, "latest_cycle": 8, "steam_t": 830.0, "sor": 5.792, "cum_oil_bbl": 901.4, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00069
Write a question an OIL production engineer might ask about rod float for BGW-21 and the ideal grounded answer using only {"well": "BGW-21", "api": 18.299, "asphaltene_wt_pct": 11.532, "latest_cycle": 11, "steam_t": 682.0, "sor": 3.491, "cum_oil_bbl": 1228.65, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00070
Write a question an OIL production engineer might ask about pump unseating for BGW-59 and the ideal grounded answer using only {"well": "BGW-59", "api": 18.603, "asphaltene_wt_pct": 7.439, "latest_cycle": 9, "steam_t": 683.0, "sor": 3.26, "cum_oil_bbl": 1317.806, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00071
Write a question an OIL production engineer might ask about soak length for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00072
Write a question an OIL production engineer might ask about cut-off timing for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00073
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-59 and the ideal grounded answer using only {"well": "BGW-59", "api": 18.603, "asphaltene_wt_pct": 7.439, "latest_cycle": 9, "steam_t": 683.0, "sor": 3.26, "cum_oil_bbl": 1317.806, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00074
Write a question an OIL production engineer might ask about rod float for BGW-27 and the ideal grounded answer using only {"well": "BGW-27", "api": 18.998, "asphaltene_wt_pct": 10.959, "latest_cycle": 13, "steam_t": 768.0, "sor": 3.261, "cum_oil_bbl": 1481.358, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
