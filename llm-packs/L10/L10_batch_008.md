# L10 steam_generator_log - batch 008 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_008.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00140 .. L10-00159 (each has an `item_id` you must echo).

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

### item_id: L10-00140
Write a daily steam-generator log for OTSG OTSG-3 on 2023-12-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 931.0, "rate_t_per_d": 66.5, "pressure_mpa": 9.972, "quality": 0.75}.

### item_id: L10-00141
Write a daily steam-generator log for OTSG OTSG-1 on 2026-08-10: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 855.0, "rate_t_per_d": 61.071, "pressure_mpa": 9.756, "quality": 0.677}.

### item_id: L10-00142
Write a daily steam-generator log for OTSG OTSG-1 on 2025-11-03: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 947.0, "rate_t_per_d": 67.643, "pressure_mpa": 10.623, "quality": 0.769}.

### item_id: L10-00143
Write a daily steam-generator log for OTSG OTSG-3 on 2025-03-30: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 993.0, "rate_t_per_d": 70.929, "pressure_mpa": 10.375, "quality": 0.745}.

### item_id: L10-00144
Write a daily steam-generator log for OTSG OTSG-1 on 2023-06-02: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 736.0, "rate_t_per_d": 52.571, "pressure_mpa": 8.509, "quality": 0.7}.

### item_id: L10-00145
Write a daily steam-generator log for OTSG OTSG-1 on 2026-07-02: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 979.0, "rate_t_per_d": 69.929, "pressure_mpa": 10.427, "quality": 0.798}.

### item_id: L10-00146
Write a daily steam-generator log for OTSG OTSG-2 on 2023-08-16: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 873.0, "rate_t_per_d": 62.357, "pressure_mpa": 8.822, "quality": 0.718}.

### item_id: L10-00147
Write a daily steam-generator log for OTSG OTSG-3 on 2025-06-05: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 860.0, "rate_t_per_d": 61.429, "pressure_mpa": 9.865, "quality": 0.758}.

### item_id: L10-00148
Write a daily steam-generator log for OTSG OTSG-3 on 2025-12-26: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1070.0, "rate_t_per_d": 76.429, "pressure_mpa": 10.739, "quality": 0.65}.

### item_id: L10-00149
Write a daily steam-generator log for OTSG OTSG-3 on 2026-09-14: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 873.0, "rate_t_per_d": 62.357, "pressure_mpa": 9.707, "quality": 0.658}.

### item_id: L10-00150
Write a daily steam-generator log for OTSG OTSG-3 on 2025-06-05: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 829.0, "rate_t_per_d": 59.214, "pressure_mpa": 9.687, "quality": 0.669}.

### item_id: L10-00151
Write a daily steam-generator log for OTSG OTSG-2 on 2024-08-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 789.0, "rate_t_per_d": 56.357, "pressure_mpa": 9.123, "quality": 0.772}.

### item_id: L10-00152
Write a daily steam-generator log for OTSG OTSG-2 on 2024-12-24: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1066.0, "rate_t_per_d": 76.143, "pressure_mpa": 10.794, "quality": 0.693}.

### item_id: L10-00153
Write a daily steam-generator log for OTSG OTSG-3 on 2026-02-27: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1020.0, "rate_t_per_d": 72.857, "pressure_mpa": 10.849, "quality": 0.767}.

### item_id: L10-00154
Write a daily steam-generator log for OTSG OTSG-2 on 2024-10-17: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 813.0, "rate_t_per_d": 58.071, "pressure_mpa": 9.766, "quality": 0.724}.

### item_id: L10-00155
Write a daily steam-generator log for OTSG OTSG-3 on 2024-12-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1115.0, "rate_t_per_d": 79.643, "pressure_mpa": 11.828, "quality": 0.622}.

### item_id: L10-00156
Write a daily steam-generator log for OTSG OTSG-1 on 2025-11-07: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 670.0, "rate_t_per_d": 47.857, "pressure_mpa": 8.817, "quality": 0.649}.

### item_id: L10-00157
Write a daily steam-generator log for OTSG OTSG-2 on 2024-03-15: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 599.0, "rate_t_per_d": 42.786, "pressure_mpa": 7.82, "quality": 0.692}.

### item_id: L10-00158
Write a daily steam-generator log for OTSG OTSG-2 on 2026-02-03: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 856.0, "rate_t_per_d": 61.143, "pressure_mpa": 9.027, "quality": 0.794}.

### item_id: L10-00159
Write a daily steam-generator log for OTSG OTSG-3 on 2026-09-10: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 963.0, "rate_t_per_d": 68.786, "pressure_mpa": 9.61, "quality": 0.67}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
