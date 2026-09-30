# L2 css_cycle_design - batch 010 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_010.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00135 .. L2-00149 (each has an `item_id` you must echo).

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

### item_id: L2-00135
Write the CSS cycle design sheet for BGW-16 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 906.0, "soak_days": 6.0, "cum_oil_bbl": 2179.172, "sor": 2.615, "net_inr": 10451991.776}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 822.0, "soak_days": 9.0, "cutoff_day": 94, "cum_oil_bbl": 2187.786, "sor": 2.363}.

### item_id: L2-00136
Write the CSS cycle design sheet for BGW-29 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 932.0, "soak_days": 9.0, "cum_oil_bbl": 1629.124, "sor": 3.598, "net_inr": 7073822.702}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1010.0, "soak_days": 8.0, "cutoff_day": 75, "cum_oil_bbl": 1525.124, "sor": 4.165}.

### item_id: L2-00137
Write the CSS cycle design sheet for BGW-56 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 854.0, "soak_days": 4.0, "cum_oil_bbl": 1968.917, "sor": 2.728, "net_inr": 9366477.185}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1037.0, "soak_days": 7.0, "cutoff_day": 99, "cum_oil_bbl": 1830.536, "sor": 3.563}.

### item_id: L2-00138
Write the CSS cycle design sheet for BGW-14 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1026.0, "soak_days": 8.0, "cum_oil_bbl": 1081.696, "sor": 5.966, "net_inr": 3556021.366}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 811.0, "soak_days": 8.0, "cutoff_day": 75, "cum_oil_bbl": 994.865, "sor": 5.127}.

### item_id: L2-00139
Write the CSS cycle design sheet for BGW-54 cycle 12 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 810.0, "soak_days": 7.0, "cum_oil_bbl": 409.264, "sor": 12.449, "net_inr": 46912.555}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1038.0, "soak_days": 6.0, "cutoff_day": 115, "cum_oil_bbl": 257.275, "sor": 25.377}.

### item_id: L2-00140
Write the CSS cycle design sheet for BGW-07 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 913.0, "soak_days": 3.0, "cum_oil_bbl": 1013.639, "sor": 5.665, "net_inr": 3478077.62}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 866.0, "soak_days": 6.0, "cutoff_day": 122, "cum_oil_bbl": 211.06, "sor": 25.808}.

### item_id: L2-00141
Write the CSS cycle design sheet for BGW-47 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 751.0, "soak_days": 3.0, "cum_oil_bbl": 1584.247, "sor": 2.982, "net_inr": 7266996.744}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 926.0, "soak_days": 3.0, "cutoff_day": 78, "cum_oil_bbl": 1498.387, "sor": 3.887}.

### item_id: L2-00142
Write the CSS cycle design sheet for BGW-19 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1009.0, "soak_days": 4.0, "cum_oil_bbl": 998.137, "sor": 6.358, "net_inr": 3110345.406}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 996.0, "soak_days": 5.0, "cutoff_day": 84, "cum_oil_bbl": 1311.956, "sor": 4.775}.

### item_id: L2-00143
Write the CSS cycle design sheet for BGW-54 cycle 13 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1038.0, "soak_days": 6.0, "cum_oil_bbl": 257.275, "sor": 25.377, "net_inr": -1408723.135}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 876.0, "soak_days": 3.0, "cutoff_day": 109, "cum_oil_bbl": 70.837, "sor": 77.783}.

### item_id: L2-00144
Write the CSS cycle design sheet for BGW-35 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 889.0, "soak_days": 9.0, "cum_oil_bbl": 665.501, "sor": 8.402, "net_inr": 1455496.967}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 947.0, "soak_days": 6.0, "cutoff_day": 122, "cum_oil_bbl": 437.229, "sor": 13.623}.

### item_id: L2-00145
Write the CSS cycle design sheet for BGW-59 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 685.0, "soak_days": 5.0, "cum_oil_bbl": 1800.471, "sor": 2.393, "net_inr": 8840118.989}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 909.0, "soak_days": 9.0, "cutoff_day": 100, "cum_oil_bbl": 1785.741, "sor": 3.202}.

### item_id: L2-00146
Write the CSS cycle design sheet for BGW-44 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 837.0, "soak_days": 3.0, "cum_oil_bbl": 973.679, "sor": 5.407, "net_inr": 3445859.144}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1002.0, "soak_days": 8.0, "cutoff_day": 79, "cum_oil_bbl": 834.22, "sor": 7.555}.

### item_id: L2-00147
Write the CSS cycle design sheet for BGW-44 cycle 12 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 810.0, "soak_days": 5.0, "cum_oil_bbl": 483.044, "sor": 10.547, "net_inr": 573445.87}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1051.0, "soak_days": 8.0, "cutoff_day": 82, "cum_oil_bbl": 472.729, "sor": 13.984}.

### item_id: L2-00148
Write the CSS cycle design sheet for BGW-18 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 775.0, "soak_days": 10.0, "cum_oil_bbl": 761.814, "sor": 6.399, "net_inr": 2273361.773}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 830.0, "soak_days": 7.0, "cutoff_day": 115, "cum_oil_bbl": 624.795, "sor": 8.356}.

### item_id: L2-00149
Write the CSS cycle design sheet for BGW-19 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1009.0, "soak_days": 4.0, "cum_oil_bbl": 998.137, "sor": 6.358, "net_inr": 3110345.406}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 996.0, "soak_days": 5.0, "cutoff_day": 84, "cum_oil_bbl": 1311.956, "sor": 4.775}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
