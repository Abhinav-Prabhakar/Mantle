# L2 css_cycle_design - batch 009 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_009.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00120 .. L2-00134 (each has an `item_id` you must echo).

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

### item_id: L2-00120
Write the CSS cycle design sheet for BGW-41 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 595.0, "soak_days": 9.0, "cum_oil_bbl": 1626.605, "sor": 2.301, "net_inr": 7981535.836}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 699.0, "soak_days": 5.0, "cutoff_day": 111, "cum_oil_bbl": 1425.398, "sor": 3.084}.

### item_id: L2-00121
Write the CSS cycle design sheet for BGW-05 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 736.0, "soak_days": 3.0, "cum_oil_bbl": 2139.416, "sor": 2.164, "net_inr": 10712226.485}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 740.0, "soak_days": 8.0, "cutoff_day": 80, "cum_oil_bbl": 1932.555, "sor": 2.408}.

### item_id: L2-00122
Write the CSS cycle design sheet for BGW-28 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1064.0, "soak_days": 6.0, "cum_oil_bbl": 2561.294, "sor": 2.613, "net_inr": 12322695.008}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 878.0, "soak_days": 10.0, "cutoff_day": 66, "cum_oil_bbl": 1942.082, "sor": 2.844}.

### item_id: L2-00123
Write the CSS cycle design sheet for BGW-33 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 917.0, "soak_days": 7.0, "cum_oil_bbl": 938.006, "sor": 6.149, "net_inr": 2942110.108}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 835.0, "soak_days": 4.0, "cutoff_day": 114, "cum_oil_bbl": 636.98, "sor": 8.245}.

### item_id: L2-00124
Write the CSS cycle design sheet for BGW-43 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 677.0, "soak_days": 6.0, "cum_oil_bbl": 2230.444, "sor": 1.909, "net_inr": 11316272.284}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 953.0, "soak_days": 6.0, "cutoff_day": 82, "cum_oil_bbl": 1867.349, "sor": 3.21}.

### item_id: L2-00125
Write the CSS cycle design sheet for BGW-21 cycle 9 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1150.0, "soak_days": 6.0, "cum_oil_bbl": 1710.589, "sor": 4.229, "net_inr": 6957009.178}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 884.0, "soak_days": 3.0, "cutoff_day": 59, "cum_oil_bbl": 1254.92, "sor": 4.431}.

### item_id: L2-00126
Write the CSS cycle design sheet for BGW-05 cycle 13 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 819.0, "soak_days": 8.0, "cum_oil_bbl": 523.762, "sor": 9.835, "net_inr": 801440.111}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1033.0, "soak_days": 4.0, "cutoff_day": 92, "cum_oil_bbl": 412.213, "sor": 15.762}.

### item_id: L2-00127
Write the CSS cycle design sheet for BGW-55 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 946.0, "soak_days": 7.0, "cum_oil_bbl": 2895.655, "sor": 2.055, "net_inr": 14653353.908}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1200.0, "soak_days": 10.0, "cutoff_day": 66, "cum_oil_bbl": 1743.63, "sor": 4.329}.

### item_id: L2-00128
Write the CSS cycle design sheet for BGW-39 cycle 9 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 715.0, "soak_days": 9.0, "cum_oil_bbl": 550.436, "sor": 8.17, "net_inr": 1265558.617}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 891.0, "soak_days": 8.0, "cutoff_day": 83, "cum_oil_bbl": 584.071, "sor": 9.595}.

### item_id: L2-00129
Write the CSS cycle design sheet for BGW-14 cycle 6 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 726.0, "soak_days": 3.0, "cum_oil_bbl": 1151.663, "sor": 3.965, "net_inr": 4830577.24}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 869.0, "soak_days": 8.0, "cutoff_day": 101, "cum_oil_bbl": 1431.36, "sor": 3.819}.

### item_id: L2-00130
Write the CSS cycle design sheet for BGW-18 cycle 9 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 777.0, "soak_days": 10.0, "cum_oil_bbl": 660.268, "sor": 7.402, "net_inr": 1742944.719}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 879.0, "soak_days": 3.0, "cutoff_day": 59, "cum_oil_bbl": 547.539, "sor": 10.097}.

### item_id: L2-00131
Write the CSS cycle design sheet for BGW-46 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 843.0, "soak_days": 5.0, "cum_oil_bbl": 886.562, "sor": 5.981, "net_inr": 2916400.214}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1021.0, "soak_days": 8.0, "cutoff_day": 70, "cum_oil_bbl": 959.005, "sor": 6.696}.

### item_id: L2-00132
Write the CSS cycle design sheet for BGW-56 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 854.0, "soak_days": 4.0, "cum_oil_bbl": 1968.917, "sor": 2.728, "net_inr": 9366477.185}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1037.0, "soak_days": 7.0, "cutoff_day": 99, "cum_oil_bbl": 1830.536, "sor": 3.563}.

### item_id: L2-00133
Write the CSS cycle design sheet for BGW-01 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 754.0, "soak_days": 9.0, "cum_oil_bbl": 1525.062, "sor": 3.11, "net_inr": 7000097.77}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 737.0, "soak_days": 8.0, "cutoff_day": 78, "cum_oil_bbl": 1557.07, "sor": 2.977}.

### item_id: L2-00134
Write the CSS cycle design sheet for BGW-04 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 864.0, "soak_days": 6.0, "cum_oil_bbl": 1255.652, "sor": 4.328, "net_inr": 5071438.155}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1033.0, "soak_days": 3.0, "cutoff_day": 119, "cum_oil_bbl": 1231.873, "sor": 5.274}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
