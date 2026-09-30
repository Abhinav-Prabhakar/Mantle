# L10 steam_generator_log - batch 010 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_010.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00180 .. L10-00199 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "unit", "date", "steam_quality", "steam_rate_t_per_h", "feedwater_tds_ppm", "feedwater_hardness_ppm", "burner_hours", "fuel_gas_sm3", "trips", "remarks"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "unit": {"type": "string"},
    "date": {"type": "string"},
    "steam_quality": {"type": "number", "minimum": 0.3, "maximum": 1.0},
    "steam_rate_t_per_h": {"type": "number", "minimum": 0, "maximum": 40},
    "feedwater_tds_ppm": {"type": "number", "minimum": 0},
    "feedwater_hardness_ppm": {"type": "number", "minimum": 0},
    "burner_hours": {"type": "number", "minimum": 0, "maximum": 24},
    "fuel_gas_sm3": {"type": "number", "minimum": 0},
    "trips": {"type": "array", "items": {"type": "string"}},
    "remarks": {"type": "string"}
  }
}
```

## Items (20)
Write one record per item, following the instruction under each item_id.

### item_id: L10-00180
Write a daily steam-generator log for OTSG OTSG-1 on 2026-07-11: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 683.0, "rate_t_per_d": 48.786, "pressure_mpa": 8.142, "quality": 0.649}.

### item_id: L10-00181
Write a daily steam-generator log for OTSG OTSG-1 on 2025-03-16: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 914.0, "rate_t_per_d": 65.286, "pressure_mpa": 10.066, "quality": 0.62}.

### item_id: L10-00182
Write a daily steam-generator log for OTSG OTSG-3 on 2023-10-30: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 893.0, "rate_t_per_d": 63.786, "pressure_mpa": 9.892, "quality": 0.741}.

### item_id: L10-00183
Write a daily steam-generator log for OTSG OTSG-1 on 2026-01-03: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 852.0, "rate_t_per_d": 60.857, "pressure_mpa": 9.474, "quality": 0.738}.

### item_id: L10-00184
Write a daily steam-generator log for OTSG OTSG-2 on 2026-03-26: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 736.0, "rate_t_per_d": 52.571, "pressure_mpa": 8.777, "quality": 0.662}.

### item_id: L10-00185
Write a daily steam-generator log for OTSG OTSG-2 on 2024-02-11: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 769.0, "rate_t_per_d": 54.929, "pressure_mpa": 9.194, "quality": 0.637}.

### item_id: L10-00186
Write a daily steam-generator log for OTSG OTSG-1 on 2025-03-14: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 728.0, "rate_t_per_d": 52.0, "pressure_mpa": 9.065, "quality": 0.658}.

### item_id: L10-00187
Write a daily steam-generator log for OTSG OTSG-2 on 2025-08-16: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 875.0, "rate_t_per_d": 62.5, "pressure_mpa": 9.955, "quality": 0.711}.

### item_id: L10-00188
Write a daily steam-generator log for OTSG OTSG-2 on 2023-04-29: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 674.0, "rate_t_per_d": 48.143, "pressure_mpa": 9.07, "quality": 0.713}.

### item_id: L10-00189
Write a daily steam-generator log for OTSG OTSG-2 on 2025-10-16: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 832.0, "rate_t_per_d": 59.429, "pressure_mpa": 9.337, "quality": 0.713}.

### item_id: L10-00190
Write a daily steam-generator log for OTSG OTSG-2 on 2025-05-19: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 962.0, "rate_t_per_d": 68.714, "pressure_mpa": 10.34, "quality": 0.732}.

### item_id: L10-00191
Write a daily steam-generator log for OTSG OTSG-1 on 2024-12-23: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 802.0, "rate_t_per_d": 57.286, "pressure_mpa": 9.095, "quality": 0.796}.

### item_id: L10-00192
Write a daily steam-generator log for OTSG OTSG-1 on 2024-12-06: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 952.0, "rate_t_per_d": 68.0, "pressure_mpa": 10.554, "quality": 0.721}.

### item_id: L10-00193
Write a daily steam-generator log for OTSG OTSG-3 on 2024-03-15: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 968.0, "rate_t_per_d": 69.143, "pressure_mpa": 9.347, "quality": 0.763}.

### item_id: L10-00194
Write a daily steam-generator log for OTSG OTSG-1 on 2025-01-07: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 837.0, "rate_t_per_d": 59.786, "pressure_mpa": 9.085, "quality": 0.707}.

### item_id: L10-00195
Write a daily steam-generator log for OTSG OTSG-3 on 2025-03-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 728.0, "rate_t_per_d": 52.0, "pressure_mpa": 9.065, "quality": 0.658}.

### item_id: L10-00196
Write a daily steam-generator log for OTSG OTSG-1 on 2023-11-30: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 823.0, "rate_t_per_d": 58.786, "pressure_mpa": 9.054, "quality": 0.787}.

### item_id: L10-00197
Write a daily steam-generator log for OTSG OTSG-1 on 2026-01-28: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 955.0, "rate_t_per_d": 68.214, "pressure_mpa": 10.012, "quality": 0.732}.

### item_id: L10-00198
Write a daily steam-generator log for OTSG OTSG-2 on 2024-03-06: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 671.0, "rate_t_per_d": 47.929, "pressure_mpa": 7.894, "quality": 0.682}.

### item_id: L10-00199
Write a daily steam-generator log for OTSG OTSG-3 on 2026-03-25: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 996.0, "rate_t_per_d": 71.143, "pressure_mpa": 10.49, "quality": 0.659}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
