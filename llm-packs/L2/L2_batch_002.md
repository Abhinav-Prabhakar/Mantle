# L2 css_cycle_design - batch 002 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00015 .. L2-00029 (each has an `item_id` you must echo).

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

### item_id: L2-00015
Write the CSS cycle design sheet for BGW-05 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 759.0, "soak_days": 4.0, "cum_oil_bbl": 1214.607, "sor": 3.93, "net_inr": 5099487.54}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 809.0, "soak_days": 3.0, "cutoff_day": 104, "cum_oil_bbl": 1254.472, "sor": 4.056}.

### item_id: L2-00016
Write the CSS cycle design sheet for BGW-27 cycle 11 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 849.0, "soak_days": 4.0, "cum_oil_bbl": 2000.302, "sor": 2.67, "net_inr": 9565689.559}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 894.0, "soak_days": 3.0, "cutoff_day": 87, "cum_oil_bbl": 1972.149, "sor": 2.851}.

### item_id: L2-00017
Write the CSS cycle design sheet for BGW-24 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 916.0, "soak_days": 7.0, "cum_oil_bbl": 1283.494, "sor": 4.489, "net_inr": 5030534.335}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 555.0, "soak_days": 3.0, "cutoff_day": 69, "cum_oil_bbl": 289.133, "sor": 12.073}.

### item_id: L2-00018
Write the CSS cycle design sheet for BGW-08 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 673.0, "soak_days": 6.0, "cum_oil_bbl": 1056.042, "sor": 4.008, "net_inr": 4402965.387}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1007.0, "soak_days": 10.0, "cutoff_day": 66, "cum_oil_bbl": 978.509, "sor": 6.473}.

### item_id: L2-00019
Write the CSS cycle design sheet for BGW-41 cycle 11 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 877.0, "soak_days": 6.0, "cum_oil_bbl": 642.07, "sor": 8.591, "net_inr": 1345905.427}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1014.0, "soak_days": 3.0, "cutoff_day": 104, "cum_oil_bbl": 589.369, "sor": 10.821}.

### item_id: L2-00020
Write the CSS cycle design sheet for BGW-53 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 880.0, "soak_days": 6.0, "cum_oil_bbl": 1394.985, "sor": 3.968, "net_inr": 5776891.571}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 715.0, "soak_days": 4.0, "cutoff_day": 60, "cum_oil_bbl": 1172.256, "sor": 3.836}.

### item_id: L2-00021
Write the CSS cycle design sheet for BGW-32 cycle 1 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle none (first cycle)), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 659.0, "soak_days": 10.0, "cutoff_day": 76, "cum_oil_bbl": 1990.774, "sor": 2.082}.

### item_id: L2-00022
Write the CSS cycle design sheet for BGW-54 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 922.0, "soak_days": 7.0, "cum_oil_bbl": 515.022, "sor": 11.26, "net_inr": 457939.422}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 875.0, "soak_days": 7.0, "cutoff_day": 123, "cum_oil_bbl": 388.62, "sor": 14.162}.

### item_id: L2-00023
Write the CSS cycle design sheet for BGW-57 cycle 9 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 902.0, "soak_days": 9.0, "cum_oil_bbl": 808.586, "sor": 7.016, "net_inr": 2126646.204}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 829.0, "soak_days": 10.0, "cutoff_day": 100, "cum_oil_bbl": 541.673, "sor": 9.626}.

### item_id: L2-00024
Write the CSS cycle design sheet for BGW-01 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 849.0, "soak_days": 6.0, "cum_oil_bbl": 1488.777, "sor": 3.587, "net_inr": 6483079.667}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 811.0, "soak_days": 4.0, "cutoff_day": 76, "cum_oil_bbl": 962.072, "sor": 5.302}.

### item_id: L2-00025
Write the CSS cycle design sheet for BGW-30 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 595.0, "soak_days": 7.0, "cum_oil_bbl": 1941.312, "sor": 1.928, "net_inr": 9931748.941}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 789.0, "soak_days": 3.0, "cutoff_day": 66, "cum_oil_bbl": 1756.857, "sor": 2.825}.

### item_id: L2-00026
Write the CSS cycle design sheet for BGW-41 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 968.0, "soak_days": 6.0, "cum_oil_bbl": 1228.185, "sor": 4.957, "net_inr": 4606787.203}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 906.0, "soak_days": 10.0, "cutoff_day": 113, "cum_oil_bbl": 843.641, "sor": 6.755}.

### item_id: L2-00027
Write the CSS cycle design sheet for BGW-31 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 761.0, "soak_days": 5.0, "cum_oil_bbl": 622.359, "sor": 7.691, "net_inr": 1562206.302}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1012.0, "soak_days": 5.0, "cutoff_day": 115, "cum_oil_bbl": 621.024, "sor": 10.25}.

### item_id: L2-00028
Write the CSS cycle design sheet for BGW-19 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 707.0, "soak_days": 3.0, "cum_oil_bbl": 2010.244, "sor": 2.212, "net_inr": 9987371.679}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 884.0, "soak_days": 9.0, "cutoff_day": 79, "cum_oil_bbl": 1992.757, "sor": 2.79}.

### item_id: L2-00029
Write the CSS cycle design sheet for BGW-20 cycle 6 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 733.0, "soak_days": 8.0, "cum_oil_bbl": 1503.045, "sor": 3.067, "net_inr": 6901142.03}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 917.0, "soak_days": 8.0, "cutoff_day": 106, "cum_oil_bbl": 2030.437, "sor": 2.841}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
