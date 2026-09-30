# L2 css_cycle_design - batch 008 (15 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 15 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L2/replies/L2_batch_008.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L2-00105 .. L2-00119 (each has an `item_id` you must echo).

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

### item_id: L2-00105
Write the CSS cycle design sheet for BGW-45 cycle 6 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 920.0, "soak_days": 4.0, "cum_oil_bbl": 969.458, "sor": 5.969, "net_inr": 3116020.882}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 842.0, "soak_days": 3.0, "cutoff_day": 61, "cum_oil_bbl": 659.068, "sor": 8.036}.

### item_id: L2-00106
Write the CSS cycle design sheet for BGW-14 cycle 6 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 726.0, "soak_days": 3.0, "cum_oil_bbl": 1151.663, "sor": 3.965, "net_inr": 4830577.24}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 869.0, "soak_days": 8.0, "cutoff_day": 101, "cum_oil_bbl": 1431.36, "sor": 3.819}.

### item_id: L2-00107
Write the CSS cycle design sheet for BGW-37 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 878.0, "soak_days": 8.0, "cum_oil_bbl": 1012.447, "sor": 5.455, "net_inr": 3576533.037}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 736.0, "soak_days": 7.0, "cutoff_day": 79, "cum_oil_bbl": 1145.476, "sor": 4.041}.

### item_id: L2-00108
Write the CSS cycle design sheet for BGW-45 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 944.0, "soak_days": 7.0, "cum_oil_bbl": 562.138, "sor": 10.562, "net_inr": 678890.631}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 961.0, "soak_days": 6.0, "cutoff_day": 65, "cum_oil_bbl": 564.556, "sor": 10.707}.

### item_id: L2-00109
Write the CSS cycle design sheet for BGW-49 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 804.0, "soak_days": 10.0, "cum_oil_bbl": 1624.505, "sor": 3.113, "net_inr": 7427586.991}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 997.0, "soak_days": 10.0, "cutoff_day": 82, "cum_oil_bbl": 1565.651, "sor": 4.005}.

### item_id: L2-00110
Write the CSS cycle design sheet for BGW-20 cycle 5 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 858.0, "soak_days": 6.0, "cum_oil_bbl": 1837.104, "sor": 2.938, "net_inr": 8548732.788}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 733.0, "soak_days": 8.0, "cutoff_day": 64, "cum_oil_bbl": 1503.045, "sor": 3.067}.

### item_id: L2-00111
Write the CSS cycle design sheet for BGW-45 cycle 9 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 961.0, "soak_days": 6.0, "cum_oil_bbl": 564.556, "sor": 10.707, "net_inr": 614446.21}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 987.0, "soak_days": 4.0, "cutoff_day": 120, "cum_oil_bbl": 418.126, "sor": 14.847}.

### item_id: L2-00112
Write the CSS cycle design sheet for BGW-19 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 707.0, "soak_days": 3.0, "cum_oil_bbl": 2010.244, "sor": 2.212, "net_inr": 9987371.679}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 884.0, "soak_days": 9.0, "cutoff_day": 79, "cum_oil_bbl": 1992.757, "sor": 2.79}.

### item_id: L2-00113
Write the CSS cycle design sheet for BGW-25 cycle 4 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 884.0, "soak_days": 9.0, "cum_oil_bbl": 1247.277, "sor": 4.458, "net_inr": 4962617.518}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 826.0, "soak_days": 4.0, "cutoff_day": 112, "cum_oil_bbl": 952.097, "sor": 5.457}.

### item_id: L2-00114
Write the CSS cycle design sheet for BGW-38 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 932.0, "soak_days": 4.0, "cum_oil_bbl": 2169.486, "sor": 2.702, "net_inr": 10166489.953}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 917.0, "soak_days": 5.0, "cutoff_day": 77, "cum_oil_bbl": 1966.819, "sor": 2.933}.

### item_id: L2-00115
Write the CSS cycle design sheet for BGW-35 cycle 7 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 670.0, "soak_days": 4.0, "cum_oil_bbl": 640.095, "sor": 6.584, "net_inr": 1924268.607}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 889.0, "soak_days": 9.0, "cutoff_day": 120, "cum_oil_bbl": 665.501, "sor": 8.402}.

### item_id: L2-00116
Write the CSS cycle design sheet for BGW-20 cycle 8 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 971.0, "soak_days": 9.0, "cum_oil_bbl": 1377.039, "sor": 4.435, "net_inr": 5435236.97}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 757.0, "soak_days": 3.0, "cutoff_day": 60, "cum_oil_bbl": 1059.024, "sor": 4.496}.

### item_id: L2-00117
Write the CSS cycle design sheet for BGW-55 cycle 3 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 946.0, "soak_days": 7.0, "cum_oil_bbl": 2895.655, "sor": 2.055, "net_inr": 14653353.908}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 1200.0, "soak_days": 10.0, "cutoff_day": 66, "cum_oil_bbl": 1743.63, "sor": 4.329}.

### item_id: L2-00118
Write the CSS cycle design sheet for BGW-23 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 857.0, "soak_days": 10.0, "cum_oil_bbl": 451.662, "sor": 11.934, "net_inr": 183874.328}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 882.0, "soak_days": 8.0, "cutoff_day": 78, "cum_oil_bbl": 422.906, "sor": 13.118}.

### item_id: L2-00119
Write the CSS cycle design sheet for BGW-30 cycle 10 as planned by the reservoir team: steam volume, injection pressure/rate/quality, soak days, expected cut-off, rationale (2-4 sentences referring to previous cycle {"steam_t": 850.0, "soak_days": 6.0, "cum_oil_bbl": 871.612, "sor": 6.134, "net_inr": 2773483.378}), approval chain, and a post-cycle review note comparing plan vs actual {"steam_t": 979.0, "soak_days": 5.0, "cutoff_day": 65, "cum_oil_bbl": 723.662, "sor": 8.509}.

## Output contract
Return a JSON array of exactly 15 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
