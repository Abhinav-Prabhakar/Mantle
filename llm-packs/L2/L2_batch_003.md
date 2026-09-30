# L2 css_cycle_design - batch 003 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_003.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00030 .. L2-00044 (each has an `item_id` you must echo).

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

### item_id: L2-00030
Write the CSS cycle design sheet for BGW-20 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1116.0, "soak_days": 9.0, "cum_oil_bbl": 1135.655, "sor": 6.181, "net_inr": 3578432.722}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1119.0, "soak_days": 8.0, "cutoff_day": 77, "cum_oil_bbl": 911.948, "sor": 7.718}.

### item_id: L2-00031
Write the CSS cycle design sheet for BGW-43 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 755.0, "soak_days": 9.0, "cum_oil_bbl": 883.668, "sor": 5.374, "net_inr": 3079409.542}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 923.0, "soak_days": 7.0, "cutoff_day": 92, "cum_oil_bbl": 0.0, "sor": 0.0}.

### item_id: L2-00032
Write the CSS cycle design sheet for BGW-44 cycle 6 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 775.0, "soak_days": 10.0, "cum_oil_bbl": 1375.024, "sor": 3.545, "net_inr": 6019962.018}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 915.0, "soak_days": 8.0, "cutoff_day": 70, "cum_oil_bbl": 935.385, "sor": 6.153}.

### item_id: L2-00033
Write the CSS cycle design sheet for BGW-10 cycle 11 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 849.0, "soak_days": 6.0, "cum_oil_bbl": 472.772, "sor": 11.295, "net_inr": 418457.337}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 902.0, "soak_days": 9.0, "cutoff_day": 114, "cum_oil_bbl": 97.42, "sor": 58.236}.

### item_id: L2-00034
Write the CSS cycle design sheet for BGW-27 cycle 6 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 746.0, "soak_days": 5.0, "cum_oil_bbl": 3012.31, "sor": 1.558, "net_inr": 15912963.202}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 827.0, "soak_days": 9.0, "cutoff_day": 87, "cum_oil_bbl": 3513.544, "sor": 1.48}.

### item_id: L2-00035
Write the CSS cycle design sheet for BGW-39 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1022.0, "soak_days": 4.0, "cum_oil_bbl": 2203.581, "sor": 2.917, "net_inr": 10243097.925}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 885.0, "soak_days": 5.0, "cutoff_day": 93, "cum_oil_bbl": 2088.127, "sor": 2.666}.

### item_id: L2-00036
Write the CSS cycle design sheet for BGW-32 cycle 12 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 829.0, "soak_days": 7.0, "cum_oil_bbl": 495.155, "sor": 10.531, "net_inr": 598120.599}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 762.0, "soak_days": 9.0, "cutoff_day": 111, "cum_oil_bbl": 304.49, "sor": 15.74}.

### item_id: L2-00037
Write the CSS cycle design sheet for BGW-06 cycle 9 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 962.0, "soak_days": 5.0, "cum_oil_bbl": 624.538, "sor": 9.688, "net_inr": 907099.418}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 834.0, "soak_days": 6.0, "cutoff_day": 122, "cum_oil_bbl": 490.219, "sor": 10.701}.

### item_id: L2-00038
Write the CSS cycle design sheet for BGW-05 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 888.0, "soak_days": 3.0, "cum_oil_bbl": 1849.196, "sor": 3.02, "net_inr": 8516637.242}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 901.0, "soak_days": 3.0, "cutoff_day": 59, "cum_oil_bbl": 1265.248, "sor": 4.479}.

### item_id: L2-00039
Write the CSS cycle design sheet for BGW-17 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 800.0, "soak_days": 4.0, "cum_oil_bbl": 3900.0, "sor": 1.29, "net_inr": 20931977.608}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 800.0, "soak_days": 4.0, "cutoff_day": 104, "cum_oil_bbl": 3500.0, "sor": 1.438}.

### item_id: L2-00040
Write the CSS cycle design sheet for BGW-29 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 811.0, "soak_days": 8.0, "cum_oil_bbl": 2286.35, "sor": 2.231, "net_inr": 11398650.295}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 643.0, "soak_days": 7.0, "cutoff_day": 80, "cum_oil_bbl": 1917.722, "sor": 2.109}.

### item_id: L2-00041
Write the CSS cycle design sheet for BGW-60 cycle 9 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 854.0, "soak_days": 10.0, "cum_oil_bbl": 817.992, "sor": 6.567, "net_inr": 2469681.458}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 891.0, "soak_days": 5.0, "cutoff_day": 86, "cum_oil_bbl": 1085.726, "sor": 5.162}.

### item_id: L2-00042
Write the CSS cycle design sheet for BGW-07 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 873.0, "soak_days": 5.0, "cum_oil_bbl": 1237.228, "sor": 4.438, "net_inr": 4934510.725}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 596.0, "soak_days": 9.0, "cutoff_day": 94, "cum_oil_bbl": 957.642, "sor": 3.915}.

### item_id: L2-00043
Write the CSS cycle design sheet for BGW-41 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 595.0, "soak_days": 9.0, "cum_oil_bbl": 1626.605, "sor": 2.301, "net_inr": 7981535.836}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 699.0, "soak_days": 5.0, "cutoff_day": 111, "cum_oil_bbl": 1425.398, "sor": 3.084}.

### item_id: L2-00044
Write the CSS cycle design sheet for BGW-10 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 939.0, "soak_days": 7.0, "cum_oil_bbl": 638.941, "sor": 9.244, "net_inr": 1081292.973}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 849.0, "soak_days": 6.0, "cutoff_day": 90, "cum_oil_bbl": 472.772, "sor": 11.295}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
