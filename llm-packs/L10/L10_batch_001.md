# L10 steam_generator_log - batch 001 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00000 .. L10-00019 (each has an `item_id` you must echo).

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

### item_id: L10-00000
Write a daily steam-generator log for OTSG OTSG-2 on 2023-12-15: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 848.0, "rate_t_per_d": 60.571, "pressure_mpa": 9.116, "quality": 0.694}.

### item_id: L10-00001
Write a daily steam-generator log for OTSG OTSG-1 on 2024-12-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1103.0, "rate_t_per_d": 78.786, "pressure_mpa": 11.475, "quality": 0.631}.

### item_id: L10-00002
Write a daily steam-generator log for OTSG OTSG-3 on 2025-02-23: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 676.0, "rate_t_per_d": 48.286, "pressure_mpa": 8.675, "quality": 0.654}.

### item_id: L10-00003
Write a daily steam-generator log for OTSG OTSG-3 on 2023-12-07: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 931.0, "rate_t_per_d": 66.5, "pressure_mpa": 9.972, "quality": 0.75}.

### item_id: L10-00004
Write a daily steam-generator log for OTSG OTSG-3 on 2026-08-10: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 986.0, "rate_t_per_d": 70.429, "pressure_mpa": 10.981, "quality": 0.679}.

### item_id: L10-00005
Write a daily steam-generator log for OTSG OTSG-1 on 2025-02-25: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 939.0, "rate_t_per_d": 67.071, "pressure_mpa": 9.683, "quality": 0.741}.

### item_id: L10-00006
Write a daily steam-generator log for OTSG OTSG-2 on 2024-12-11: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1200.0, "rate_t_per_d": 85.714, "pressure_mpa": 12.0, "quality": 0.687}.

### item_id: L10-00007
Write a daily steam-generator log for OTSG OTSG-2 on 2023-09-05: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 834.0, "rate_t_per_d": 59.571, "pressure_mpa": 9.61, "quality": 0.673}.

### item_id: L10-00008
Write a daily steam-generator log for OTSG OTSG-2 on 2026-02-01: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 891.0, "rate_t_per_d": 63.643, "pressure_mpa": 9.771, "quality": 0.742}.

### item_id: L10-00009
Write a daily steam-generator log for OTSG OTSG-2 on 2025-06-02: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 860.0, "rate_t_per_d": 61.429, "pressure_mpa": 9.865, "quality": 0.758}.

### item_id: L10-00010
Write a daily steam-generator log for OTSG OTSG-3 on 2025-08-06: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 822.0, "rate_t_per_d": 58.714, "pressure_mpa": 9.453, "quality": 0.73}.

### item_id: L10-00011
Write a daily steam-generator log for OTSG OTSG-2 on 2026-07-05: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 846.0, "rate_t_per_d": 60.429, "pressure_mpa": 9.662, "quality": 0.722}.

### item_id: L10-00012
Write a daily steam-generator log for OTSG OTSG-2 on 2026-01-30: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 891.0, "rate_t_per_d": 63.643, "pressure_mpa": 10.061, "quality": 0.731}.

### item_id: L10-00013
Write a daily steam-generator log for OTSG OTSG-2 on 2024-01-06: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 740.0, "rate_t_per_d": 52.857, "pressure_mpa": 8.435, "quality": 0.687}.

### item_id: L10-00014
Write a daily steam-generator log for OTSG OTSG-2 on 2026-07-10: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 683.0, "rate_t_per_d": 48.786, "pressure_mpa": 8.142, "quality": 0.649}.

### item_id: L10-00015
Write a daily steam-generator log for OTSG OTSG-2 on 2024-09-18: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 951.0, "rate_t_per_d": 67.929, "pressure_mpa": 9.543, "quality": 0.744}.

### item_id: L10-00016
Write a daily steam-generator log for OTSG OTSG-1 on 2024-05-05: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 595.0, "rate_t_per_d": 42.5, "pressure_mpa": 7.904, "quality": 0.768}.

### item_id: L10-00017
Write a daily steam-generator log for OTSG OTSG-3 on 2024-02-04: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 769.0, "rate_t_per_d": 54.929, "pressure_mpa": 9.194, "quality": 0.637}.

### item_id: L10-00018
Write a daily steam-generator log for OTSG OTSG-2 on 2025-08-02: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1023.0, "rate_t_per_d": 73.071, "pressure_mpa": 10.333, "quality": 0.67}.

### item_id: L10-00019
Write a daily steam-generator log for OTSG OTSG-3 on 2024-06-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 711.0, "rate_t_per_d": 50.786, "pressure_mpa": 8.829, "quality": 0.674}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
