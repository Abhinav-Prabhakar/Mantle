# L10 steam_generator_log - batch 007 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_007.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00120 .. L10-00139 (each has an `item_id` you must echo).

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

### item_id: L10-00120
Write a daily steam-generator log for OTSG OTSG-1 on 2026-02-01: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 872.0, "rate_t_per_d": 62.286, "pressure_mpa": 10.304, "quality": 0.764}.

### item_id: L10-00121
Write a daily steam-generator log for OTSG OTSG-1 on 2026-03-26: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 711.0, "rate_t_per_d": 50.786, "pressure_mpa": 8.51, "quality": 0.733}.

### item_id: L10-00122
Write a daily steam-generator log for OTSG OTSG-1 on 2025-06-16: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 889.0, "rate_t_per_d": 63.5, "pressure_mpa": 9.167, "quality": 0.694}.

### item_id: L10-00123
Write a daily steam-generator log for OTSG OTSG-3 on 2026-04-07: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 711.0, "rate_t_per_d": 50.786, "pressure_mpa": 8.51, "quality": 0.733}.

### item_id: L10-00124
Write a daily steam-generator log for OTSG OTSG-2 on 2025-03-18: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 676.0, "rate_t_per_d": 48.286, "pressure_mpa": 9.136, "quality": 0.739}.

### item_id: L10-00125
Write a daily steam-generator log for OTSG OTSG-3 on 2025-01-29: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1012.0, "rate_t_per_d": 72.286, "pressure_mpa": 10.413, "quality": 0.785}.

### item_id: L10-00126
Write a daily steam-generator log for OTSG OTSG-1 on 2026-09-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 947.0, "rate_t_per_d": 67.643, "pressure_mpa": 10.254, "quality": 0.745}.

### item_id: L10-00127
Write a daily steam-generator log for OTSG OTSG-3 on 2024-09-17: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 951.0, "rate_t_per_d": 67.929, "pressure_mpa": 9.543, "quality": 0.744}.

### item_id: L10-00128
Write a daily steam-generator log for OTSG OTSG-2 on 2025-06-13: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 922.0, "rate_t_per_d": 65.857, "pressure_mpa": 10.489, "quality": 0.735}.

### item_id: L10-00129
Write a daily steam-generator log for OTSG OTSG-1 on 2026-06-28: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 979.0, "rate_t_per_d": 69.929, "pressure_mpa": 10.427, "quality": 0.798}.

### item_id: L10-00130
Write a daily steam-generator log for OTSG OTSG-1 on 2025-10-13: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 874.0, "rate_t_per_d": 62.429, "pressure_mpa": 9.738, "quality": 0.715}.

### item_id: L10-00131
Write a daily steam-generator log for OTSG OTSG-2 on 2025-12-11: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1011.0, "rate_t_per_d": 72.214, "pressure_mpa": 10.032, "quality": 0.793}.

### item_id: L10-00132
Write a daily steam-generator log for OTSG OTSG-2 on 2026-04-10: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1038.0, "rate_t_per_d": 74.143, "pressure_mpa": 10.813, "quality": 0.771}.

### item_id: L10-00133
Write a daily steam-generator log for OTSG OTSG-1 on 2026-02-13: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 884.0, "rate_t_per_d": 63.143, "pressure_mpa": 10.118, "quality": 0.622}.

### item_id: L10-00134
Write a daily steam-generator log for OTSG OTSG-2 on 2024-03-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 953.0, "rate_t_per_d": 68.071, "pressure_mpa": 10.147, "quality": 0.711}.

### item_id: L10-00135
Write a daily steam-generator log for OTSG OTSG-2 on 2026-03-01: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1010.0, "rate_t_per_d": 72.143, "pressure_mpa": 10.01, "quality": 0.714}.

### item_id: L10-00136
Write a daily steam-generator log for OTSG OTSG-3 on 2026-09-25: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1038.0, "rate_t_per_d": 74.143, "pressure_mpa": 11.03, "quality": 0.711}.

### item_id: L10-00137
Write a daily steam-generator log for OTSG OTSG-3 on 2023-06-13: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1008.0, "rate_t_per_d": 72.0, "pressure_mpa": 10.838, "quality": 0.751}.

### item_id: L10-00138
Write a daily steam-generator log for OTSG OTSG-3 on 2024-02-25: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 885.0, "rate_t_per_d": 63.214, "pressure_mpa": 9.885, "quality": 0.664}.

### item_id: L10-00139
Write a daily steam-generator log for OTSG OTSG-3 on 2025-07-15: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 975.0, "rate_t_per_d": 69.643, "pressure_mpa": 10.005, "quality": 0.622}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
