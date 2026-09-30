# L2 css_cycle_design - batch 001 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00000 .. L2-00014 (each has an `item_id` you must echo).

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

### item_id: L2-00000
Write the CSS cycle design sheet for BGW-55 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 751.0, "soak_days": 6.0, "cum_oil_bbl": 2224.974, "sor": 2.123, "net_inr": 11142069.49}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 845.0, "soak_days": 10.0, "cutoff_day": 71, "cum_oil_bbl": 1366.951, "sor": 3.888}.

### item_id: L2-00001
Write the CSS cycle design sheet for BGW-31 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 966.0, "soak_days": 8.0, "cum_oil_bbl": 1238.211, "sor": 4.907, "net_inr": 4671196.797}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 914.0, "soak_days": 6.0, "cutoff_day": 62, "cum_oil_bbl": 967.287, "sor": 5.943}.

### item_id: L2-00002
Write the CSS cycle design sheet for BGW-44 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 896.0, "soak_days": 8.0, "cum_oil_bbl": 1541.66, "sor": 3.656, "net_inr": 6693034.789}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 775.0, "soak_days": 10.0, "cutoff_day": 83, "cum_oil_bbl": 1375.024, "sor": 3.545}.

### item_id: L2-00003
Write the CSS cycle design sheet for BGW-13 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 893.0, "soak_days": 9.0, "cum_oil_bbl": 3903.572, "sor": 1.439, "net_inr": 20854944.957}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 802.0, "soak_days": 9.0, "cutoff_day": 77, "cum_oil_bbl": 3619.404, "sor": 1.394}.

### item_id: L2-00004
Write the CSS cycle design sheet for BGW-12 cycle 9 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1161.0, "soak_days": 6.0, "cum_oil_bbl": 1945.523, "sor": 3.753, "net_inr": 8370003.092}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 669.0, "soak_days": 10.0, "cutoff_day": 87, "cum_oil_bbl": 1999.006, "sor": 2.105}.

### item_id: L2-00005
Write the CSS cycle design sheet for BGW-15 cycle 13 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 856.0, "soak_days": 5.0, "cum_oil_bbl": 434.795, "sor": 12.383, "net_inr": 103351.766}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 960.0, "soak_days": 7.0, "cutoff_day": 88, "cum_oil_bbl": 493.113, "sor": 12.245}.

### item_id: L2-00006
Write the CSS cycle design sheet for BGW-36 cycle 11 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1119.0, "soak_days": 8.0, "cum_oil_bbl": 763.459, "sor": 9.219, "net_inr": 1388241.72}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 893.0, "soak_days": 3.0, "cutoff_day": 119, "cum_oil_bbl": 554.435, "sor": 10.131}.

### item_id: L2-00007
Write the CSS cycle design sheet for BGW-56 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1037.0, "soak_days": 7.0, "cum_oil_bbl": 1830.536, "sor": 3.563, "net_inr": 8021086.595}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 953.0, "soak_days": 8.0, "cutoff_day": 83, "cum_oil_bbl": 1201.677, "sor": 4.988}.

### item_id: L2-00008
Write the CSS cycle design sheet for BGW-20 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 858.0, "soak_days": 6.0, "cum_oil_bbl": 1837.104, "sor": 2.938, "net_inr": 8548732.788}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 733.0, "soak_days": 8.0, "cutoff_day": 64, "cum_oil_bbl": 1503.045, "sor": 3.067}.

### item_id: L2-00009
Write the CSS cycle design sheet for BGW-51 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 842.0, "soak_days": 3.0, "cum_oil_bbl": 1491.098, "sor": 3.552, "net_inr": 6529040.189}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 801.0, "soak_days": 10.0, "cutoff_day": 79, "cum_oil_bbl": 1529.224, "sor": 3.295}.

### item_id: L2-00010
Write the CSS cycle design sheet for BGW-21 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 994.0, "soak_days": 10.0, "cum_oil_bbl": 1604.158, "sor": 3.897, "net_inr": 6791522.457}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 806.0, "soak_days": 3.0, "cutoff_day": 59, "cum_oil_bbl": 1462.863, "sor": 3.466}.

### item_id: L2-00011
Write the CSS cycle design sheet for BGW-11 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 820.0, "soak_days": 7.0, "cum_oil_bbl": 2437.919, "sor": 2.116, "net_inr": 12106392.367}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 877.0, "soak_days": 8.0, "cutoff_day": 68, "cum_oil_bbl": 1909.463, "sor": 2.889}.

### item_id: L2-00012
Write the CSS cycle design sheet for BGW-37 cycle 1 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle none (first cycle)), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 810.0, "soak_days": 8.0, "cutoff_day": 78, "cum_oil_bbl": 2381.075, "sor": 2.14}.

### item_id: L2-00013
Write the CSS cycle design sheet for BGW-24 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1011.0, "soak_days": 9.0, "cum_oil_bbl": 1717.2, "sor": 3.703, "net_inr": 7348460.234}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 716.0, "soak_days": 4.0, "cutoff_day": 69, "cum_oil_bbl": 1216.3, "sor": 3.703}.

### item_id: L2-00014
Write the CSS cycle design sheet for BGW-04 cycle 11 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 964.0, "soak_days": 3.0, "cum_oil_bbl": 419.221, "sor": 14.463, "net_inr": -232969.139}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 811.0, "soak_days": 9.0, "cutoff_day": 124, "cum_oil_bbl": 455.117, "sor": 11.208}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
