# L12 copilot_qa - batch 005 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L12/replies/L12_batch_005.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L12-00100 .. L12-00124 (each has an `item_id` you must echo).

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

### item_id: L12-00100
Write a question an OIL production engineer might ask about soak length for BGW-03 and the ideal grounded answer using only {"well": "BGW-03", "api": 19.223, "asphaltene_wt_pct": 7.28, "latest_cycle": 8, "steam_t": 885.0, "sor": 99.0, "cum_oil_bbl": 7.913, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00101
Write a question an OIL production engineer might ask about SOR for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00102
Write a question an OIL production engineer might ask about soak length for BGW-35 and the ideal grounded answer using only {"well": "BGW-35", "api": 18.034, "asphaltene_wt_pct": 8.047, "latest_cycle": 8, "steam_t": 947.0, "sor": 13.623, "cum_oil_bbl": 437.229, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00103
Write a question an OIL production engineer might ask about pump unseating for BGW-56 and the ideal grounded answer using only {"well": "BGW-56", "api": 19.25, "asphaltene_wt_pct": 9.106, "latest_cycle": 13, "steam_t": 963.0, "sor": 99.0, "cum_oil_bbl": 58.714, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00104
Write a question an OIL production engineer might ask about SOR for BGW-52 and the ideal grounded answer using only {"well": "BGW-52", "api": 17.22, "asphaltene_wt_pct": 8.888, "latest_cycle": 8, "steam_t": 807.0, "sor": 43.678, "cum_oil_bbl": 116.212, "soak_days": 9.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00105
Write a question an OIL production engineer might ask about cut-off timing for BGW-23 and the ideal grounded answer using only {"well": "BGW-23", "api": 19.107, "asphaltene_wt_pct": 8.685, "latest_cycle": 13, "steam_t": 933.0, "sor": 81.264, "cum_oil_bbl": 72.213, "soak_days": 10.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00106
Write a question an OIL production engineer might ask about SOR for BGW-12 and the ideal grounded answer using only {"well": "BGW-12", "api": 19.052, "asphaltene_wt_pct": 11.602, "latest_cycle": 11, "steam_t": 1200.0, "sor": 4.396, "cum_oil_bbl": 1716.802, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00107
Write a question an OIL production engineer might ask about fluid pound for BGW-14 and the ideal grounded answer using only {"well": "BGW-14", "api": 18.11, "asphaltene_wt_pct": 10.75, "latest_cycle": 12, "steam_t": 1099.0, "sor": 0.0, "cum_oil_bbl": 0.0, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00108
Write a question an OIL production engineer might ask about soak length for BGW-46 and the ideal grounded answer using only {"well": "BGW-46", "api": 18.204, "asphaltene_wt_pct": 8.946, "latest_cycle": 10, "steam_t": 947.0, "sor": 7.168, "cum_oil_bbl": 831.012, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00109
Write a question an OIL production engineer might ask about rod float for BGW-03 and the ideal grounded answer using only {"well": "BGW-03", "api": 19.223, "asphaltene_wt_pct": 7.28, "latest_cycle": 8, "steam_t": 885.0, "sor": 99.0, "cum_oil_bbl": 7.913, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00110
Write a question an OIL production engineer might ask about soak length for BGW-08 and the ideal grounded answer using only {"well": "BGW-08", "api": 18.197, "asphaltene_wt_pct": 10.749, "latest_cycle": 13, "steam_t": 1049.0, "sor": 11.817, "cum_oil_bbl": 558.353, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00111
Write a question an OIL production engineer might ask about SOR for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00112
Write a question an OIL production engineer might ask about rod float for BGW-24 and the ideal grounded answer using only {"well": "BGW-24", "api": 18.487, "asphaltene_wt_pct": 11.264, "latest_cycle": 10, "steam_t": 555.0, "sor": 12.073, "cum_oil_bbl": 289.133, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00113
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-12 and the ideal grounded answer using only {"well": "BGW-12", "api": 19.052, "asphaltene_wt_pct": 11.602, "latest_cycle": 11, "steam_t": 1200.0, "sor": 4.396, "cum_oil_bbl": 1716.802, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00114
Write a question an OIL production engineer might ask about cut-off timing for BGW-07 and the ideal grounded answer using only {"well": "BGW-07", "api": 18.131, "asphaltene_wt_pct": 11.233, "latest_cycle": 7, "steam_t": 866.0, "sor": 25.808, "cum_oil_bbl": 211.06, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00115
Write a question an OIL production engineer might ask about fluid pound for BGW-50 and the ideal grounded answer using only {"well": "BGW-50", "api": 17.287, "asphaltene_wt_pct": 11.817, "latest_cycle": 11, "steam_t": 855.0, "sor": 5.708, "cum_oil_bbl": 942.228, "soak_days": 8.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00116
Write a question an OIL production engineer might ask about cut-off timing for BGW-35 and the ideal grounded answer using only {"well": "BGW-35", "api": 18.034, "asphaltene_wt_pct": 8.047, "latest_cycle": 8, "steam_t": 947.0, "sor": 13.623, "cum_oil_bbl": 437.229, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00117
Write a question an OIL production engineer might ask about fluid pound for BGW-12 and the ideal grounded answer using only {"well": "BGW-12", "api": 19.052, "asphaltene_wt_pct": 11.602, "latest_cycle": 11, "steam_t": 1200.0, "sor": 4.396, "cum_oil_bbl": 1716.802, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00118
Write a question an OIL production engineer might ask about pump unseating for BGW-39 and the ideal grounded answer using only {"well": "BGW-39", "api": 17.782, "asphaltene_wt_pct": 7.693, "latest_cycle": 11, "steam_t": 986.0, "sor": 13.456, "cum_oil_bbl": 460.89, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00119
Write a question an OIL production engineer might ask about fluid pound for BGW-28 and the ideal grounded answer using only {"well": "BGW-28", "api": 18.019, "asphaltene_wt_pct": 11.024, "latest_cycle": 10, "steam_t": 1054.0, "sor": 25.776, "cum_oil_bbl": 257.197, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00120
Write a question an OIL production engineer might ask about SOR for BGW-31 and the ideal grounded answer using only {"well": "BGW-31", "api": 17.565, "asphaltene_wt_pct": 7.32, "latest_cycle": 9, "steam_t": 741.0, "sor": 11.279, "cum_oil_bbl": 413.207, "soak_days": 5.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00121
Write a question an OIL production engineer might ask about SOR for BGW-35 and the ideal grounded answer using only {"well": "BGW-35", "api": 18.034, "asphaltene_wt_pct": 8.047, "latest_cycle": 8, "steam_t": 947.0, "sor": 13.623, "cum_oil_bbl": 437.229, "soak_days": 6.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00122
Write a question an OIL production engineer might ask about VFD profile for BGW-59 and the ideal grounded answer using only {"well": "BGW-59", "api": 18.603, "asphaltene_wt_pct": 7.439, "latest_cycle": 9, "steam_t": 683.0, "sor": 3.26, "cum_oil_bbl": 1317.806, "soak_days": 4.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00123
Write a question an OIL production engineer might ask about asphaltene deposition for BGW-54 and the ideal grounded answer using only {"well": "BGW-54", "api": 17.171, "asphaltene_wt_pct": 8.036, "latest_cycle": 13, "steam_t": 876.0, "sor": 77.783, "cum_oil_bbl": 70.837, "soak_days": 3.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

### item_id: L12-00124
Write a question an OIL production engineer might ask about soak length for BGW-15 and the ideal grounded answer using only {"well": "BGW-15", "api": 18.179, "asphaltene_wt_pct": 8.151, "latest_cycle": 13, "steam_t": 960.0, "sor": 12.245, "cum_oil_bbl": 493.113, "soak_days": 7.0} (cite the numbers). Topics: rod float, fluid pound, SOR, cut-off timing, soak length, VFD profile, asphaltene deposition, pump unseating.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
