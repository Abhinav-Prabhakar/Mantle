# L2 css_cycle_design - batch 005 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_005.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00060 .. L2-00074 (each has an `item_id` you must echo).

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

### item_id: L2-00060
Write the CSS cycle design sheet for BGW-07 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 913.0, "soak_days": 3.0, "cum_oil_bbl": 1013.639, "sor": 5.665, "net_inr": 3478077.62}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 866.0, "soak_days": 6.0, "cutoff_day": 122, "cum_oil_bbl": 211.06, "sor": 25.808}.

### item_id: L2-00061
Write the CSS cycle design sheet for BGW-20 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 917.0, "soak_days": 8.0, "cum_oil_bbl": 2030.437, "sor": 2.841, "net_inr": 9505212.627}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 971.0, "soak_days": 9.0, "cutoff_day": 75, "cum_oil_bbl": 1377.039, "sor": 4.435}.

### item_id: L2-00062
Write the CSS cycle design sheet for BGW-34 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1000.0, "soak_days": 7.0, "cum_oil_bbl": 1675.063, "sor": 3.755, "net_inr": 7137888.932}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1000.0, "soak_days": 4.0, "cutoff_day": 86, "cum_oil_bbl": 372.2, "sor": 16.899}.

### item_id: L2-00063
Write the CSS cycle design sheet for BGW-12 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1025.0, "soak_days": 6.0, "cum_oil_bbl": 3704.825, "sor": 1.74, "net_inr": 19255957.729}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 855.0, "soak_days": 4.0, "cutoff_day": 63, "cum_oil_bbl": 3054.509, "sor": 1.761}.

### item_id: L2-00064
Write the CSS cycle design sheet for BGW-36 cycle 1 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle none (first cycle)), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 717.0, "soak_days": 3.0, "cutoff_day": 59, "cum_oil_bbl": 1608.244, "sor": 2.804}.

### item_id: L2-00065
Write the CSS cycle design sheet for BGW-48 cycle 1 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle none (first cycle)), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 675.0, "soak_days": 9.0, "cutoff_day": 70, "cum_oil_bbl": 2337.879, "sor": 1.816}.

### item_id: L2-00066
Write the CSS cycle design sheet for BGW-26 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 944.0, "soak_days": 7.0, "cum_oil_bbl": 1391.024, "sor": 4.268, "net_inr": 5537706.442}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 812.0, "soak_days": 10.0, "cutoff_day": 111, "cum_oil_bbl": 792.53, "sor": 6.444}.

### item_id: L2-00067
Write the CSS cycle design sheet for BGW-22 cycle 11 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 923.0, "soak_days": 8.0, "cum_oil_bbl": 999.519, "sor": 5.808, "net_inr": 3359263.636}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 873.0, "soak_days": 7.0, "cutoff_day": 74, "cum_oil_bbl": 841.588, "sor": 6.525}.

### item_id: L2-00068
Write the CSS cycle design sheet for BGW-51 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 846.0, "soak_days": 6.0, "cum_oil_bbl": 2507.753, "sor": 2.122, "net_inr": 12552042.312}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 987.0, "soak_days": 10.0, "cutoff_day": 70, "cum_oil_bbl": 2158.635, "sor": 2.876}.

### item_id: L2-00069
Write the CSS cycle design sheet for BGW-20 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 917.0, "soak_days": 8.0, "cum_oil_bbl": 2030.437, "sor": 2.841, "net_inr": 9505212.627}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 971.0, "soak_days": 9.0, "cutoff_day": 75, "cum_oil_bbl": 1377.039, "sor": 4.435}.

### item_id: L2-00070
Write the CSS cycle design sheet for BGW-30 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 972.0, "soak_days": 10.0, "cum_oil_bbl": 1043.079, "sor": 5.861, "net_inr": 3478906.945}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 862.0, "soak_days": 4.0, "cutoff_day": 62, "cum_oil_bbl": 741.378, "sor": 7.313}.

### item_id: L2-00071
Write the CSS cycle design sheet for BGW-32 cycle 12 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 829.0, "soak_days": 7.0, "cum_oil_bbl": 495.155, "sor": 10.531, "net_inr": 598120.599}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 762.0, "soak_days": 9.0, "cutoff_day": 111, "cum_oil_bbl": 304.49, "sor": 15.74}.

### item_id: L2-00072
Write the CSS cycle design sheet for BGW-29 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 932.0, "soak_days": 9.0, "cum_oil_bbl": 1629.124, "sor": 3.598, "net_inr": 7073822.702}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1010.0, "soak_days": 8.0, "cutoff_day": 75, "cum_oil_bbl": 1525.124, "sor": 4.165}.

### item_id: L2-00073
Write the CSS cycle design sheet for BGW-44 cycle 2 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 1008.0, "soak_days": 10.0, "cum_oil_bbl": 2214.542, "sor": 2.863, "net_inr": 10415900.701}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 729.0, "soak_days": 4.0, "cutoff_day": 66, "cum_oil_bbl": 2364.656, "sor": 1.939}.

### item_id: L2-00074
Write the CSS cycle design sheet for BGW-46 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 741.0, "soak_days": 8.0, "cum_oil_bbl": 858.449, "sor": 5.429, "net_inr": 2971995.615}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 947.0, "soak_days": 3.0, "cutoff_day": 78, "cum_oil_bbl": 831.012, "sor": 7.168}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
