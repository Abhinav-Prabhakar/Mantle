# L2 css_cycle_design - batch 007 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_007.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00090 .. L2-00104 (each has an `item_id` you must echo).

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

### item_id: L2-00090
Write the CSS cycle design sheet for BGW-59 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 909.0, "soak_days": 9.0, "cum_oil_bbl": 1785.741, "sor": 3.202, "net_inr": 8114858.037}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 716.0, "soak_days": 3.0, "cutoff_day": 101, "cum_oil_bbl": 1559.757, "sor": 2.887}.

### item_id: L2-00091
Write the CSS cycle design sheet for BGW-23 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 727.0, "soak_days": 8.0, "cum_oil_bbl": 754.548, "sor": 6.06, "net_inr": 2440039.495}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 811.0, "soak_days": 3.0, "cutoff_day": 77, "cum_oil_bbl": 784.429, "sor": 6.503}.

### item_id: L2-00092
Write the CSS cycle design sheet for BGW-44 cycle 12 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 810.0, "soak_days": 5.0, "cum_oil_bbl": 483.044, "sor": 10.547, "net_inr": 573445.87}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1051.0, "soak_days": 8.0, "cutoff_day": 82, "cum_oil_bbl": 472.729, "sor": 13.984}.

### item_id: L2-00093
Write the CSS cycle design sheet for BGW-33 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 835.0, "soak_days": 4.0, "cum_oil_bbl": 636.98, "sor": 8.245, "net_inr": 1436564.077}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1074.0, "soak_days": 8.0, "cutoff_day": 124, "cum_oil_bbl": 358.852, "sor": 18.825}.

### item_id: L2-00094
Write the CSS cycle design sheet for BGW-55 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 751.0, "soak_days": 6.0, "cum_oil_bbl": 2224.974, "sor": 2.123, "net_inr": 11142069.49}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 845.0, "soak_days": 10.0, "cutoff_day": 71, "cum_oil_bbl": 1366.951, "sor": 3.888}.

### item_id: L2-00095
Write the CSS cycle design sheet for BGW-05 cycle 1 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle none (first cycle)), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 736.0, "soak_days": 3.0, "cutoff_day": 96, "cum_oil_bbl": 2139.416, "sor": 2.164}.

### item_id: L2-00096
Write the CSS cycle design sheet for BGW-29 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 974.0, "soak_days": 3.0, "cum_oil_bbl": 2712.571, "sor": 2.258, "net_inr": 13459114.818}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 811.0, "soak_days": 8.0, "cutoff_day": 70, "cum_oil_bbl": 2286.35, "sor": 2.231}.

### item_id: L2-00097
Write the CSS cycle design sheet for BGW-60 cycle 13 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1002.0, "soak_days": 5.0, "cum_oil_bbl": 547.939, "sor": 11.502, "net_inr": 400233.143}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 873.0, "soak_days": 5.0, "cutoff_day": 86, "cum_oil_bbl": 0.0, "sor": 0.0}.

### item_id: L2-00098
Write the CSS cycle design sheet for BGW-33 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 835.0, "soak_days": 4.0, "cum_oil_bbl": 636.98, "sor": 8.245, "net_inr": 1436564.077}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1074.0, "soak_days": 8.0, "cutoff_day": 124, "cum_oil_bbl": 358.852, "sor": 18.825}.

### item_id: L2-00099
Write the CSS cycle design sheet for BGW-51 cycle 1 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle none (first cycle)), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 921.0, "soak_days": 10.0, "cutoff_day": 75, "cum_oil_bbl": 3005.27, "sor": 1.928}.

### item_id: L2-00100
Write the CSS cycle design sheet for BGW-23 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 843.0, "soak_days": 5.0, "cum_oil_bbl": 871.476, "sor": 6.084, "net_inr": 2823471.551}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 752.0, "soak_days": 9.0, "cutoff_day": 125, "cum_oil_bbl": 825.183, "sor": 5.732}.

### item_id: L2-00101
Write the CSS cycle design sheet for BGW-44 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 896.0, "soak_days": 8.0, "cum_oil_bbl": 1541.66, "sor": 3.656, "net_inr": 6693034.789}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 775.0, "soak_days": 10.0, "cutoff_day": 83, "cum_oil_bbl": 1375.024, "sor": 3.545}.

### item_id: L2-00102
Write the CSS cycle design sheet for BGW-37 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 810.0, "soak_days": 8.0, "cum_oil_bbl": 2381.075, "sor": 2.14, "net_inr": 11938256.493}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 940.0, "soak_days": 9.0, "cutoff_day": 116, "cum_oil_bbl": 2202.017, "sor": 2.685}.

### item_id: L2-00103
Write the CSS cycle design sheet for BGW-29 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 932.0, "soak_days": 9.0, "cum_oil_bbl": 1629.124, "sor": 3.598, "net_inr": 7073822.702}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1010.0, "soak_days": 8.0, "cutoff_day": 75, "cum_oil_bbl": 1525.124, "sor": 4.165}.

### item_id: L2-00104
Write the CSS cycle design sheet for BGW-16 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 800.0, "soak_days": 10.0, "cum_oil_bbl": 3101.065, "sor": 1.623, "net_inr": 16194840.523}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 906.0, "soak_days": 6.0, "cutoff_day": 65, "cum_oil_bbl": 2179.172, "sor": 2.615}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
