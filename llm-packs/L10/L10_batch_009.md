# L10 steam_generator_log - batch 009 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_009.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00160 .. L10-00179 (each has an `item_id` you must echo).

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

### item_id: L10-00160
Write a daily steam-generator log for OTSG OTSG-3 on 2025-01-16: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 870.0, "rate_t_per_d": 62.143, "pressure_mpa": 9.743, "quality": 0.681}.

### item_id: L10-00161
Write a daily steam-generator log for OTSG OTSG-3 on 2025-09-17: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 997.0, "rate_t_per_d": 71.214, "pressure_mpa": 10.537, "quality": 0.762}.

### item_id: L10-00162
Write a daily steam-generator log for OTSG OTSG-3 on 2025-04-03: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 987.0, "rate_t_per_d": 70.5, "pressure_mpa": 10.56, "quality": 0.679}.

### item_id: L10-00163
Write a daily steam-generator log for OTSG OTSG-2 on 2025-03-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 676.0, "rate_t_per_d": 48.286, "pressure_mpa": 9.136, "quality": 0.739}.

### item_id: L10-00164
Write a daily steam-generator log for OTSG OTSG-3 on 2024-12-10: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 758.0, "rate_t_per_d": 54.143, "pressure_mpa": 8.552, "quality": 0.674}.

### item_id: L10-00165
Write a daily steam-generator log for OTSG OTSG-2 on 2025-10-04: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 843.0, "rate_t_per_d": 60.214, "pressure_mpa": 9.027, "quality": 0.722}.

### item_id: L10-00166
Write a daily steam-generator log for OTSG OTSG-2 on 2024-12-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 758.0, "rate_t_per_d": 54.143, "pressure_mpa": 8.552, "quality": 0.674}.

### item_id: L10-00167
Write a daily steam-generator log for OTSG OTSG-1 on 2025-03-26: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 922.0, "rate_t_per_d": 65.857, "pressure_mpa": 9.844, "quality": 0.74}.

### item_id: L10-00168
Write a daily steam-generator log for OTSG OTSG-2 on 2026-07-30: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1033.0, "rate_t_per_d": 73.786, "pressure_mpa": 11.136, "quality": 0.772}.

### item_id: L10-00169
Write a daily steam-generator log for OTSG OTSG-1 on 2025-02-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 921.0, "rate_t_per_d": 65.786, "pressure_mpa": 10.182, "quality": 0.751}.

### item_id: L10-00170
Write a daily steam-generator log for OTSG OTSG-1 on 2024-11-25: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 974.0, "rate_t_per_d": 69.571, "pressure_mpa": 10.808, "quality": 0.621}.

### item_id: L10-00171
Write a daily steam-generator log for OTSG OTSG-3 on 2024-08-23: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 701.0, "rate_t_per_d": 50.071, "pressure_mpa": 7.775, "quality": 0.635}.

### item_id: L10-00172
Write a daily steam-generator log for OTSG OTSG-2 on 2026-03-02: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 751.0, "rate_t_per_d": 53.643, "pressure_mpa": 9.239, "quality": 0.703}.

### item_id: L10-00173
Write a daily steam-generator log for OTSG OTSG-3 on 2024-07-05: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 705.0, "rate_t_per_d": 50.357, "pressure_mpa": 8.234, "quality": 0.784}.

### item_id: L10-00174
Write a daily steam-generator log for OTSG OTSG-2 on 2025-06-29: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1070.0, "rate_t_per_d": 76.429, "pressure_mpa": 11.25, "quality": 0.662}.

### item_id: L10-00175
Write a daily steam-generator log for OTSG OTSG-1 on 2026-02-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 985.0, "rate_t_per_d": 70.357, "pressure_mpa": 10.366, "quality": 0.738}.

### item_id: L10-00176
Write a daily steam-generator log for OTSG OTSG-2 on 2026-08-07: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 855.0, "rate_t_per_d": 61.071, "pressure_mpa": 9.756, "quality": 0.677}.

### item_id: L10-00177
Write a daily steam-generator log for OTSG OTSG-2 on 2024-08-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 942.0, "rate_t_per_d": 67.286, "pressure_mpa": 9.819, "quality": 0.707}.

### item_id: L10-00178
Write a daily steam-generator log for OTSG OTSG-3 on 2025-09-26: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 801.0, "rate_t_per_d": 57.214, "pressure_mpa": 9.863, "quality": 0.668}.

### item_id: L10-00179
Write a daily steam-generator log for OTSG OTSG-1 on 2023-11-14: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 998.0, "rate_t_per_d": 71.286, "pressure_mpa": 9.999, "quality": 0.723}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
