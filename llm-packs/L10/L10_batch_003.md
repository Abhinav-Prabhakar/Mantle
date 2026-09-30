# L10 steam_generator_log - batch 003 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_003.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00040 .. L10-00059 (each has an `item_id` you must echo).

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

### item_id: L10-00040
Write a daily steam-generator log for OTSG OTSG-2 on 2025-03-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 970.0, "rate_t_per_d": 69.286, "pressure_mpa": 10.442, "quality": 0.765}.

### item_id: L10-00041
Write a daily steam-generator log for OTSG OTSG-3 on 2024-04-18: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 863.0, "rate_t_per_d": 61.643, "pressure_mpa": 9.472, "quality": 0.76}.

### item_id: L10-00042
Write a daily steam-generator log for OTSG OTSG-2 on 2026-07-14: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 762.0, "rate_t_per_d": 54.429, "pressure_mpa": 8.545, "quality": 0.734}.

### item_id: L10-00043
Write a daily steam-generator log for OTSG OTSG-2 on 2024-03-31: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 805.0, "rate_t_per_d": 57.5, "pressure_mpa": 9.107, "quality": 0.716}.

### item_id: L10-00044
Write a daily steam-generator log for OTSG OTSG-1 on 2024-04-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 947.0, "rate_t_per_d": 67.643, "pressure_mpa": 10.367, "quality": 0.751}.

### item_id: L10-00045
Write a daily steam-generator log for OTSG OTSG-2 on 2024-07-17: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 726.0, "rate_t_per_d": 51.857, "pressure_mpa": 8.623, "quality": 0.799}.

### item_id: L10-00046
Write a daily steam-generator log for OTSG OTSG-1 on 2025-02-28: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 902.0, "rate_t_per_d": 64.429, "pressure_mpa": 10.546, "quality": 0.722}.

### item_id: L10-00047
Write a daily steam-generator log for OTSG OTSG-1 on 2025-09-26: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 770.0, "rate_t_per_d": 55.0, "pressure_mpa": 9.055, "quality": 0.629}.

### item_id: L10-00048
Write a daily steam-generator log for OTSG OTSG-2 on 2026-09-03: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 963.0, "rate_t_per_d": 68.786, "pressure_mpa": 10.357, "quality": 0.691}.

### item_id: L10-00049
Write a daily steam-generator log for OTSG OTSG-2 on 2025-01-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 837.0, "rate_t_per_d": 59.786, "pressure_mpa": 9.085, "quality": 0.707}.

### item_id: L10-00050
Write a daily steam-generator log for OTSG OTSG-2 on 2026-06-03: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 778.0, "rate_t_per_d": 55.571, "pressure_mpa": 9.3, "quality": 0.767}.

### item_id: L10-00051
Write a daily steam-generator log for OTSG OTSG-3 on 2024-10-16: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 838.0, "rate_t_per_d": 59.857, "pressure_mpa": 9.046, "quality": 0.751}.

### item_id: L10-00052
Write a daily steam-generator log for OTSG OTSG-1 on 2024-05-26: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 699.0, "rate_t_per_d": 49.929, "pressure_mpa": 8.359, "quality": 0.728}.

### item_id: L10-00053
Write a daily steam-generator log for OTSG OTSG-2 on 2024-12-05: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 952.0, "rate_t_per_d": 68.0, "pressure_mpa": 10.554, "quality": 0.721}.

### item_id: L10-00054
Write a daily steam-generator log for OTSG OTSG-2 on 2023-07-25: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 919.0, "rate_t_per_d": 65.643, "pressure_mpa": 10.548, "quality": 0.74}.

### item_id: L10-00055
Write a daily steam-generator log for OTSG OTSG-2 on 2024-12-24: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 830.0, "rate_t_per_d": 59.286, "pressure_mpa": 9.821, "quality": 0.674}.

### item_id: L10-00056
Write a daily steam-generator log for OTSG OTSG-2 on 2025-02-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 714.0, "rate_t_per_d": 51.0, "pressure_mpa": 8.605, "quality": 0.699}.

### item_id: L10-00057
Write a daily steam-generator log for OTSG OTSG-1 on 2024-10-27: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 942.0, "rate_t_per_d": 67.286, "pressure_mpa": 10.111, "quality": 0.767}.

### item_id: L10-00058
Write a daily steam-generator log for OTSG OTSG-1 on 2022-11-15: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 699.0, "rate_t_per_d": 49.929, "pressure_mpa": 8.801, "quality": 0.659}.

### item_id: L10-00059
Write a daily steam-generator log for OTSG OTSG-2 on 2025-02-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 714.0, "rate_t_per_d": 51.0, "pressure_mpa": 8.605, "quality": 0.699}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
