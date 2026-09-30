# L12 copilot_qa - batch 002 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00025 .. L12-00049 (each has an `item_id` you must echo).

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

### item_id: L12-00025
Write a question an OIL production engineer might ask about cut-off timing for BGW-12 and the ideal grounded answer using only {"well": "BGW-12", "api": 19.052, "asphaltene_wt_pct": 11.602, "latest_cycle": 11, "steam_t": 1200.0, "sor": 4.396, "cum_oil_bbl": 1716.802, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00026
Write a question an OIL production engineer might ask about pump unseating for BGW-13 and the ideal grounded answer using only {"well": "BGW-13", "api": 18.616, "asphaltene_wt_pct": 7.177, "latest_cycle": 9, "steam_t": 1038.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00027
Write a question an OIL production engineer might ask about pump unseating for BGW-21 and the ideal grounded answer using only {"well": "BGW-21", "api": 18.299, "asphaltene_wt_pct": 11.532, "latest_cycle": 11, "steam_t": 682.0, "sor": 3.491, "cum_oil_bbl": 1228.65, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00028
Write a question an OIL production engineer might ask about cut-off timing for BGW-21 and the ideal grounded answer using only {"well": "BGW-21", "api": 18.299, "asphaltene_wt_pct": 11.532, "latest_cycle": 11, "steam_t": 682.0, "sor": 3.491, "cum_oil_bbl": 1228.65, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00029
Write a question an OIL production engineer might ask about cut-off timing for BGW-05 and the ideal grounded answer using only {"well": "BGW-05", "api": 18.657, "asphaltene_wt_pct": 11.621, "latest_cycle": 13, "steam_t": 1033.0, "sor": 15.762, "cum_oil_bbl": 412.213, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00030
Write a question an OIL production engineer might ask about SOR for BGW-20 and the ideal grounded answer using only {"well": "BGW-20", "api": 17.004, "asphaltene_wt_pct": 7.221, "latest_cycle": 13, "steam_t": 954.0, "sor": 11.028, "cum_oil_bbl": 544.121, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00031
Write a question an OIL production engineer might ask about soak length for BGW-20 and the ideal grounded answer using only {"well": "BGW-20", "api": 17.004, "asphaltene_wt_pct": 7.221, "latest_cycle": 13, "steam_t": 954.0, "sor": 11.028, "cum_oil_bbl": 544.121, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00032
Write a question an OIL production engineer might ask about SOR for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00033
Write a question an OIL production engineer might ask about fluid pound for BGW-19 and the ideal grounded answer using only {"well": "BGW-19", "api": 17.44, "asphaltene_wt_pct": 7.906, "latest_cycle": 11, "steam_t": 952.0, "sor": 5.675, "cum_oil_bbl": 1055.081, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00034
Write a question an OIL production engineer might ask about rod float for BGW-54 and the ideal grounded answer using only {"well": "BGW-54", "api": 17.171, "asphaltene_wt_pct": 8.036, "latest_cycle": 13, "steam_t": 876.0, "sor": 77.783, "cum_oil_bbl": 70.837, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00035
Write a question an OIL production engineer might ask about rod float for BGW-26 and the ideal grounded answer using only {"well": "BGW-26", "api": 19.143, "asphaltene_wt_pct": 8.64, "latest_cycle": 10, "steam_t": 857.0, "sor": 6.357, "cum_oil_bbl": 847.913, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00036
Write a question an OIL production engineer might ask about pump unseating for BGW-22 and the ideal grounded answer using only {"well": "BGW-22", "api": 19.273, "asphaltene_wt_pct": 9.486, "latest_cycle": 12, "steam_t": 871.0, "sor": 7.051, "cum_oil_bbl": 776.94, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00037
Write a question an OIL production engineer might ask about SOR for BGW-44 and the ideal grounded answer using only {"well": "BGW-44", "api": 17.215, "asphaltene_wt_pct": 9.398, "latest_cycle": 13, "steam_t": 875.0, "sor": 16.715, "cum_oil_bbl": 329.26, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00038
Write a question an OIL production engineer might ask about soak length for BGW-48 and the ideal grounded answer using only {"well": "BGW-48", "api": 18.111, "asphaltene_wt_pct": 10.149, "latest_cycle": 13, "steam_t": 708.0, "sor": 9.913, "cum_oil_bbl": 449.232, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00039
Write a question an OIL production engineer might ask about VFD profile for BGW-35 and the ideal grounded answer using only {"well": "BGW-35", "api": 18.034, "asphaltene_wt_pct": 8.047, "latest_cycle": 8, "steam_t": 947.0, "sor": 13.623, "cum_oil_bbl": 437.229, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00040
Write a question an OIL production engineer might ask about cut-off timing for BGW-15 and the ideal grounded answer using only {"well": "BGW-15", "api": 18.179, "asphaltene_wt_pct": 8.151, "latest_cycle": 13, "steam_t": 960.0, "sor": 12.245, "cum_oil_bbl": 493.113, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00041
Write a question an OIL production engineer might ask about rod float for BGW-29 and the ideal grounded answer using only {"well": "BGW-29", "api": 18.623, "asphaltene_wt_pct": 10.858, "latest_cycle": 9, "steam_t": 818.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00042
Write a question an OIL production engineer might ask about soak length for BGW-25 and the ideal grounded answer using only {"well": "BGW-25", "api": 18.864, "asphaltene_wt_pct": 9.088, "latest_cycle": 11, "steam_t": 861.0, "sor": 16.88, "cum_oil_bbl": 320.818, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00043
Write a question an OIL production engineer might ask about rod float for BGW-03 and the ideal grounded answer using only {"well": "BGW-03", "api": 19.223, "asphaltene_wt_pct": 7.28, "latest_cycle": 8, "steam_t": 885.0, "sor": 99.0, "cum_oil_bbl": 7.913, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00044
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-31 and the ideal grounded answer using only {"well": "BGW-31", "api": 17.565, "asphaltene_wt_pct": 7.32, "latest_cycle": 9, "steam_t": 741.0, "sor": 11.279, "cum_oil_bbl": 413.207, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00045
Write a question an OIL production engineer might ask about SOR for BGW-31 and the ideal grounded answer using only {"well": "BGW-31", "api": 17.565, "asphaltene_wt_pct": 7.32, "latest_cycle": 9, "steam_t": 741.0, "sor": 11.279, "cum_oil_bbl": 413.207, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00046
Write a question an OIL production engineer might ask about pump unseating for BGW-29 and the ideal grounded answer using only {"well": "BGW-29", "api": 18.623, "asphaltene_wt_pct": 10.858, "latest_cycle": 9, "steam_t": 818.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00047
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-31 and the ideal grounded answer using only {"well": "BGW-31", "api": 17.565, "asphaltene_wt_pct": 7.32, "latest_cycle": 9, "steam_t": 741.0, "sor": 11.279, "cum_oil_bbl": 413.207, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00048
Write a question an OIL production engineer might ask about SOR for BGW-17 and the ideal grounded answer using only {"well": "BGW-17", "api": 18.0, "asphaltene_wt_pct": 9.2, "latest_cycle": 4, "steam_t": 800.0, "sor": 3.481, "cum_oil_bbl": 1445.611, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00049
Write a question an OIL production engineer might ask about rod float for BGW-49 and the ideal grounded answer using only {"well": "BGW-49", "api": 18.67, "asphaltene_wt_pct": 8.799, "latest_cycle": 8, "steam_t": 973.0, "sor": 4.009, "cum_oil_bbl": 1526.525, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
