# L2 css_cycle_design - batch 004 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_004.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00045 .. L2-00059 (each has an `item_id` you must echo).

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

### item_id: L2-00045
Write the CSS cycle design sheet for BGW-34 cycle 1 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle none (first cycle)), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 816.0, "soak_days": 9.0, "cutoff_day": 66, "cum_oil_bbl": 1979.459, "sor": 2.593}.

### item_id: L2-00046
Write the CSS cycle design sheet for BGW-07 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 773.0, "soak_days": 3.0, "cum_oil_bbl": 1320.466, "sor": 3.682, "net_inr": 5717173.188}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 873.0, "soak_days": 5.0, "cutoff_day": 110, "cum_oil_bbl": 1237.228, "sor": 4.438}.

### item_id: L2-00047
Write the CSS cycle design sheet for BGW-37 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 940.0, "soak_days": 9.0, "cum_oil_bbl": 2202.017, "sor": 2.685, "net_inr": 10503116.179}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 787.0, "soak_days": 8.0, "cutoff_day": 93, "cum_oil_bbl": 1534.318, "sor": 3.226}.

### item_id: L2-00048
Write the CSS cycle design sheet for BGW-56 cycle 6 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 735.0, "soak_days": 10.0, "cum_oil_bbl": 1119.667, "sor": 4.129, "net_inr": 4604384.544}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1029.0, "soak_days": 9.0, "cutoff_day": 73, "cum_oil_bbl": 1041.99, "sor": 6.211}.

### item_id: L2-00049
Write the CSS cycle design sheet for BGW-60 cycle 6 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 871.0, "soak_days": 4.0, "cum_oil_bbl": 1511.117, "sor": 3.625, "net_inr": 6571930.219}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 980.0, "soak_days": 8.0, "cutoff_day": 87, "cum_oil_bbl": 1440.541, "sor": 4.279}.

### item_id: L2-00050
Write the CSS cycle design sheet for BGW-22 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 736.0, "soak_days": 6.0, "cum_oil_bbl": 2570.661, "sor": 1.801, "net_inr": 13301458.685}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 950.0, "soak_days": 5.0, "cutoff_day": 80, "cum_oil_bbl": 2391.797, "sor": 2.498}.

### item_id: L2-00051
Write the CSS cycle design sheet for BGW-24 cycle 9 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 716.0, "soak_days": 4.0, "cum_oil_bbl": 1216.3, "sor": 3.703, "net_inr": 5241864.616}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 916.0, "soak_days": 7.0, "cutoff_day": 69, "cum_oil_bbl": 1283.494, "sor": 4.489}.

### item_id: L2-00052
Write the CSS cycle design sheet for BGW-25 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 826.0, "soak_days": 4.0, "cum_oil_bbl": 952.097, "sor": 5.457, "net_inr": 3353499.814}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1001.0, "soak_days": 9.0, "cutoff_day": 76, "cum_oil_bbl": 1291.651, "sor": 4.874}.

### item_id: L2-00053
Write the CSS cycle design sheet for BGW-12 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 889.0, "soak_days": 6.0, "cum_oil_bbl": 2560.069, "sor": 2.184, "net_inr": 12726132.792}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1161.0, "soak_days": 6.0, "cutoff_day": 62, "cum_oil_bbl": 1945.523, "sor": 3.753}.

### item_id: L2-00054
Write the CSS cycle design sheet for BGW-53 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 583.0, "soak_days": 3.0, "cum_oil_bbl": 1274.63, "sor": 2.877, "net_inr": 5982487.115}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 725.0, "soak_days": 9.0, "cutoff_day": 77, "cum_oil_bbl": 1722.51, "sor": 2.647}.

### item_id: L2-00055
Write the CSS cycle design sheet for BGW-05 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 852.0, "soak_days": 9.0, "cum_oil_bbl": 1579.514, "sor": 3.393, "net_inr": 7054343.881}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 888.0, "soak_days": 3.0, "cutoff_day": 59, "cum_oil_bbl": 1849.196, "sor": 3.02}.

### item_id: L2-00056
Write the CSS cycle design sheet for BGW-04 cycle 11 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 964.0, "soak_days": 3.0, "cum_oil_bbl": 419.221, "sor": 14.463, "net_inr": -232969.139}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 811.0, "soak_days": 9.0, "cutoff_day": 124, "cum_oil_bbl": 455.117, "sor": 11.208}.

### item_id: L2-00057
Write the CSS cycle design sheet for BGW-34 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 737.0, "soak_days": 9.0, "cum_oil_bbl": 1939.127, "sor": 2.391, "net_inr": 9511980.034}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 602.0, "soak_days": 10.0, "cutoff_day": 93, "cum_oil_bbl": 1429.71, "sor": 2.648}.

### item_id: L2-00058
Write the CSS cycle design sheet for BGW-40 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 817.0, "soak_days": 4.0, "cum_oil_bbl": 1161.31, "sor": 4.425, "net_inr": 4627489.211}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 649.0, "soak_days": 10.0, "cutoff_day": 80, "cum_oil_bbl": 1122.515, "sor": 3.637}.

### item_id: L2-00059
Write the CSS cycle design sheet for BGW-54 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 932.0, "soak_days": 10.0, "cum_oil_bbl": 933.235, "sor": 6.281, "net_inr": 2938745.073}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1017.0, "soak_days": 10.0, "cutoff_day": 126, "cum_oil_bbl": 949.82, "sor": 6.735}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
