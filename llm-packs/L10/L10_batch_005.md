# L10 steam_generator_log - batch 005 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_005.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00080 .. L10-00099 (each has an `item_id` you must echo).

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

### item_id: L10-00080
Write a daily steam-generator log for OTSG OTSG-3 on 2025-04-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 784.0, "rate_t_per_d": 56.0, "pressure_mpa": 8.166, "quality": 0.754}.

### item_id: L10-00081
Write a daily steam-generator log for OTSG OTSG-3 on 2026-07-21: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 721.0, "rate_t_per_d": 51.5, "pressure_mpa": 8.023, "quality": 0.689}.

### item_id: L10-00082
Write a daily steam-generator log for OTSG OTSG-1 on 2025-08-24: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 781.0, "rate_t_per_d": 55.786, "pressure_mpa": 9.029, "quality": 0.779}.

### item_id: L10-00083
Write a daily steam-generator log for OTSG OTSG-2 on 2024-06-07: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 790.0, "rate_t_per_d": 56.429, "pressure_mpa": 8.612, "quality": 0.78}.

### item_id: L10-00084
Write a daily steam-generator log for OTSG OTSG-1 on 2026-02-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 891.0, "rate_t_per_d": 63.643, "pressure_mpa": 10.061, "quality": 0.731}.

### item_id: L10-00085
Write a daily steam-generator log for OTSG OTSG-1 on 2023-12-30: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 884.0, "rate_t_per_d": 63.143, "pressure_mpa": 9.707, "quality": 0.645}.

### item_id: L10-00086
Write a daily steam-generator log for OTSG OTSG-1 on 2026-09-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 555.0, "rate_t_per_d": 39.643, "pressure_mpa": 7.19, "quality": 0.694}.

### item_id: L10-00087
Write a daily steam-generator log for OTSG OTSG-3 on 2026-04-06: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1017.0, "rate_t_per_d": 72.643, "pressure_mpa": 10.804, "quality": 0.654}.

### item_id: L10-00088
Write a daily steam-generator log for OTSG OTSG-2 on 2025-09-11: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 879.0, "rate_t_per_d": 62.786, "pressure_mpa": 9.271, "quality": 0.656}.

### item_id: L10-00089
Write a daily steam-generator log for OTSG OTSG-2 on 2025-03-18: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 914.0, "rate_t_per_d": 65.286, "pressure_mpa": 10.066, "quality": 0.62}.

### item_id: L10-00090
Write a daily steam-generator log for OTSG OTSG-3 on 2026-03-29: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 964.0, "rate_t_per_d": 68.857, "pressure_mpa": 9.812, "quality": 0.66}.

### item_id: L10-00091
Write a daily steam-generator log for OTSG OTSG-1 on 2023-11-22: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 874.0, "rate_t_per_d": 62.429, "pressure_mpa": 9.637, "quality": 0.674}.

### item_id: L10-00092
Write a daily steam-generator log for OTSG OTSG-2 on 2025-10-29: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1159.0, "rate_t_per_d": 82.786, "pressure_mpa": 11.778, "quality": 0.694}.

### item_id: L10-00093
Write a daily steam-generator log for OTSG OTSG-3 on 2025-02-16: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 705.0, "rate_t_per_d": 50.357, "pressure_mpa": 8.196, "quality": 0.685}.

### item_id: L10-00094
Write a daily steam-generator log for OTSG OTSG-2 on 2025-08-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 875.0, "rate_t_per_d": 62.5, "pressure_mpa": 9.955, "quality": 0.711}.

### item_id: L10-00095
Write a daily steam-generator log for OTSG OTSG-3 on 2026-04-15: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 813.0, "rate_t_per_d": 58.071, "pressure_mpa": 9.185, "quality": 0.722}.

### item_id: L10-00096
Write a daily steam-generator log for OTSG OTSG-1 on 2025-03-06: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 725.0, "rate_t_per_d": 51.786, "pressure_mpa": 9.045, "quality": 0.721}.

### item_id: L10-00097
Write a daily steam-generator log for OTSG OTSG-3 on 2026-01-04: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 917.0, "rate_t_per_d": 65.5, "pressure_mpa": 9.852, "quality": 0.727}.

### item_id: L10-00098
Write a daily steam-generator log for OTSG OTSG-2 on 2025-09-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 879.0, "rate_t_per_d": 62.786, "pressure_mpa": 9.271, "quality": 0.656}.

### item_id: L10-00099
Write a daily steam-generator log for OTSG OTSG-3 on 2026-04-25: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1013.0, "rate_t_per_d": 72.357, "pressure_mpa": 10.267, "quality": 0.662}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
