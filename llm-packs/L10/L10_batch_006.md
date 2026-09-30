# L10 steam_generator_log - batch 006 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_006.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00100 .. L10-00119 (each has an `item_id` you must echo).

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

### item_id: L10-00100
Write a daily steam-generator log for OTSG OTSG-2 on 2026-04-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1038.0, "rate_t_per_d": 74.143, "pressure_mpa": 10.813, "quality": 0.771}.

### item_id: L10-00101
Write a daily steam-generator log for OTSG OTSG-2 on 2025-06-23: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1130.0, "rate_t_per_d": 80.714, "pressure_mpa": 11.496, "quality": 0.726}.

### item_id: L10-00102
Write a daily steam-generator log for OTSG OTSG-3 on 2025-07-01: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 845.0, "rate_t_per_d": 60.357, "pressure_mpa": 10.33, "quality": 0.717}.

### item_id: L10-00103
Write a daily steam-generator log for OTSG OTSG-2 on 2025-03-13: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 751.0, "rate_t_per_d": 53.643, "pressure_mpa": 9.035, "quality": 0.755}.

### item_id: L10-00104
Write a daily steam-generator log for OTSG OTSG-1 on 2026-01-02: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 763.0, "rate_t_per_d": 54.5, "pressure_mpa": 9.166, "quality": 0.72}.

### item_id: L10-00105
Write a daily steam-generator log for OTSG OTSG-3 on 2026-01-29: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 891.0, "rate_t_per_d": 63.643, "pressure_mpa": 10.061, "quality": 0.731}.

### item_id: L10-00106
Write a daily steam-generator log for OTSG OTSG-1 on 2026-09-07: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1000.0, "rate_t_per_d": 71.429, "pressure_mpa": 11.111, "quality": 0.644}.

### item_id: L10-00107
Write a daily steam-generator log for OTSG OTSG-3 on 2024-08-04: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 969.0, "rate_t_per_d": 69.214, "pressure_mpa": 10.252, "quality": 0.689}.

### item_id: L10-00108
Write a daily steam-generator log for OTSG OTSG-2 on 2025-10-10: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 832.0, "rate_t_per_d": 59.429, "pressure_mpa": 9.337, "quality": 0.713}.

### item_id: L10-00109
Write a daily steam-generator log for OTSG OTSG-2 on 2026-02-22: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 829.0, "rate_t_per_d": 59.214, "pressure_mpa": 8.561, "quality": 0.677}.

### item_id: L10-00110
Write a daily steam-generator log for OTSG OTSG-2 on 2023-04-17: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 752.0, "rate_t_per_d": 53.714, "pressure_mpa": 9.282, "quality": 0.658}.

### item_id: L10-00111
Write a daily steam-generator log for OTSG OTSG-1 on 2023-11-25: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 874.0, "rate_t_per_d": 62.429, "pressure_mpa": 9.637, "quality": 0.674}.

### item_id: L10-00112
Write a daily steam-generator log for OTSG OTSG-3 on 2025-09-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 908.0, "rate_t_per_d": 64.857, "pressure_mpa": 9.618, "quality": 0.764}.

### item_id: L10-00113
Write a daily steam-generator log for OTSG OTSG-3 on 2025-08-20: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 868.0, "rate_t_per_d": 62.0, "pressure_mpa": 10.315, "quality": 0.738}.

### item_id: L10-00114
Write a daily steam-generator log for OTSG OTSG-3 on 2025-01-05: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 823.0, "rate_t_per_d": 58.786, "pressure_mpa": 8.818, "quality": 0.663}.

### item_id: L10-00115
Write a daily steam-generator log for OTSG OTSG-2 on 2023-08-28: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 834.0, "rate_t_per_d": 59.571, "pressure_mpa": 9.61, "quality": 0.673}.

### item_id: L10-00116
Write a daily steam-generator log for OTSG OTSG-3 on 2024-08-20: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 896.0, "rate_t_per_d": 64.0, "pressure_mpa": 9.736, "quality": 0.641}.

### item_id: L10-00117
Write a daily steam-generator log for OTSG OTSG-3 on 2026-03-11: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 701.0, "rate_t_per_d": 50.071, "pressure_mpa": 8.521, "quality": 0.774}.

### item_id: L10-00118
Write a daily steam-generator log for OTSG OTSG-3 on 2025-03-03: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 926.0, "rate_t_per_d": 66.143, "pressure_mpa": 10.295, "quality": 0.748}.

### item_id: L10-00119
Write a daily steam-generator log for OTSG OTSG-1 on 2026-05-06: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 814.0, "rate_t_per_d": 58.143, "pressure_mpa": 8.716, "quality": 0.724}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
