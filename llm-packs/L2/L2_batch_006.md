# L2 css_cycle_design - batch 006 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_006.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00075 .. L2-00089 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "well_id", "cycle_no", "steam_volume_t", "injection_pressure_mpa", "injection_rate_t_per_d", "steam_quality", "soak_days", "expected_cutoff_day", "rationale", "approval_chain", "post_cycle_review"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "well_id": {"type": "string"},
    "cycle_no": {"type": "integer", "minimum": 1},
    "steam_volume_t": {"type": "number", "minimum": 200, "maximum": 1600},
    "injection_pressure_mpa": {"type": "number", "minimum": 3, "maximum": 15},
    "injection_rate_t_per_d": {"type": "number", "minimum": 15, "maximum": 120},
    "steam_quality": {"type": "number", "minimum": 0.3, "maximum": 1.0},
    "soak_days": {"type": "number", "minimum": 1, "maximum": 20},
    "expected_cutoff_day": {"type": "integer", "minimum": 30, "maximum": 140},
    "rationale": {"type": "string"},
    "approval_chain": {"type": "array", "items": {"type": "string"}, "minItems": 2},
    "post_cycle_review": {"type": "string"}
  }
}
```

## Items (15)
Write one record per item, following the instruction under each item_id.

### item_id: L2-00075
Write the CSS cycle design sheet for BGW-16 cycle 1 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle none (first cycle)), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 800.0, "soak_days": 10.0, "cutoff_day": 85, "cum_oil_bbl": 3101.065, "sor": 1.623}.

### item_id: L2-00076
Write the CSS cycle design sheet for BGW-14 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 769.0, "soak_days": 7.0, "cum_oil_bbl": 1786.104, "sor": 2.708, "net_inr": 8373009.709}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 998.0, "soak_days": 9.0, "cutoff_day": 65, "cum_oil_bbl": 1470.965, "sor": 4.267}.

### item_id: L2-00077
Write the CSS cycle design sheet for BGW-56 cycle 13 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 847.0, "soak_days": 6.0, "cum_oil_bbl": 378.16, "sor": 14.088, "net_inr": -139431.339}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 963.0, "soak_days": 6.0, "cutoff_day": 95, "cum_oil_bbl": 58.714, "sor": 99.0}.

### item_id: L2-00078
Write the CSS cycle design sheet for BGW-35 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 638.0, "soak_days": 4.0, "cum_oil_bbl": 1094.253, "sor": 3.667, "net_inr": 4735797.251}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 722.0, "soak_days": 6.0, "cutoff_day": 75, "cum_oil_bbl": 1326.551, "sor": 3.423}.

### item_id: L2-00079
Write the CSS cycle design sheet for BGW-28 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 789.0, "soak_days": 8.0, "cum_oil_bbl": 2134.888, "sor": 2.325, "net_inr": 10451202.319}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 962.0, "soak_days": 6.0, "cutoff_day": 78, "cum_oil_bbl": 1838.716, "sor": 3.291}.

### item_id: L2-00080
Write the CSS cycle design sheet for BGW-36 cycle 6 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 841.0, "soak_days": 10.0, "cum_oil_bbl": 981.293, "sor": 5.391, "net_inr": 3486225.505}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 897.0, "soak_days": 6.0, "cutoff_day": 77, "cum_oil_bbl": 1112.14, "sor": 5.073}.

### item_id: L2-00081
Write the CSS cycle design sheet for BGW-39 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 999.0, "soak_days": 6.0, "cum_oil_bbl": 811.514, "sor": 7.743, "net_inr": 2033607.963}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 715.0, "soak_days": 9.0, "cutoff_day": 78, "cum_oil_bbl": 550.436, "sor": 8.17}.

### item_id: L2-00082
Write the CSS cycle design sheet for BGW-08 cycle 12 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 857.0, "soak_days": 8.0, "cum_oil_bbl": 990.094, "sor": 5.444, "net_inr": 3420977.092}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 741.0, "soak_days": 9.0, "cutoff_day": 82, "cum_oil_bbl": 1137.971, "sor": 4.096}.

### item_id: L2-00083
Write the CSS cycle design sheet for BGW-44 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 825.0, "soak_days": 10.0, "cum_oil_bbl": 1926.647, "sor": 2.693, "net_inr": 9183645.152}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 896.0, "soak_days": 8.0, "cutoff_day": 75, "cum_oil_bbl": 1541.66, "sor": 3.656}.

### item_id: L2-00084
Write the CSS cycle design sheet for BGW-44 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 837.0, "soak_days": 3.0, "cum_oil_bbl": 973.679, "sor": 5.407, "net_inr": 3445859.144}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1002.0, "soak_days": 8.0, "cutoff_day": 79, "cum_oil_bbl": 834.22, "sor": 7.555}.

### item_id: L2-00085
Write the CSS cycle design sheet for BGW-18 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 775.0, "soak_days": 10.0, "cum_oil_bbl": 761.814, "sor": 6.399, "net_inr": 2273361.773}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 830.0, "soak_days": 7.0, "cutoff_day": 115, "cum_oil_bbl": 624.795, "sor": 8.356}.

### item_id: L2-00086
Write the CSS cycle design sheet for BGW-51 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 987.0, "soak_days": 10.0, "cum_oil_bbl": 2158.635, "sor": 2.876, "net_inr": 10044968.744}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 842.0, "soak_days": 3.0, "cutoff_day": 59, "cum_oil_bbl": 1491.098, "sor": 3.552}.

### item_id: L2-00087
Write the CSS cycle design sheet for BGW-60 cycle 13 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1002.0, "soak_days": 5.0, "cum_oil_bbl": 547.939, "sor": 11.502, "net_inr": 400233.143}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 873.0, "soak_days": 5.0, "cutoff_day": 86, "cum_oil_bbl": 0.0, "sor": 0.0}.

### item_id: L2-00088
Write the CSS cycle design sheet for BGW-58 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 968.0, "soak_days": 8.0, "cum_oil_bbl": 2938.308, "sor": 2.072, "net_inr": 14687116.509}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1198.0, "soak_days": 3.0, "cutoff_day": 69, "cum_oil_bbl": 2035.07, "sor": 3.703}.

### item_id: L2-00089
Write the CSS cycle design sheet for BGW-08 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 715.0, "soak_days": 10.0, "cum_oil_bbl": 1342.65, "sor": 3.349, "net_inr": 5966440.151}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1063.0, "soak_days": 3.0, "cutoff_day": 73, "cum_oil_bbl": 1298.422, "sor": 5.149}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
