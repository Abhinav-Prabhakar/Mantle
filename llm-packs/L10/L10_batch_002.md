# L10 steam_generator_log - batch 002 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00020 .. L10-00039 (each has an `item_id` you must echo).

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

### item_id: L10-00020
Write a daily steam-generator log for OTSG OTSG-2 on 2025-01-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 837.0, "rate_t_per_d": 59.786, "pressure_mpa": 9.085, "quality": 0.707}.

### item_id: L10-00021
Write a daily steam-generator log for OTSG OTSG-2 on 2023-06-02: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 736.0, "rate_t_per_d": 52.571, "pressure_mpa": 8.509, "quality": 0.7}.

### item_id: L10-00022
Write a daily steam-generator log for OTSG OTSG-3 on 2024-10-04: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1001.0, "rate_t_per_d": 71.5, "pressure_mpa": 10.921, "quality": 0.73}.

### item_id: L10-00023
Write a daily steam-generator log for OTSG OTSG-3 on 2023-01-01: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 717.0, "rate_t_per_d": 51.214, "pressure_mpa": 9.101, "quality": 0.68}.

### item_id: L10-00024
Write a daily steam-generator log for OTSG OTSG-2 on 2023-12-18: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 799.0, "rate_t_per_d": 57.071, "pressure_mpa": 9.1, "quality": 0.695}.

### item_id: L10-00025
Write a daily steam-generator log for OTSG OTSG-2 on 2024-01-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 685.0, "rate_t_per_d": 48.929, "pressure_mpa": 8.624, "quality": 0.791}.

### item_id: L10-00026
Write a daily steam-generator log for OTSG OTSG-3 on 2023-06-11: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1008.0, "rate_t_per_d": 72.0, "pressure_mpa": 10.838, "quality": 0.751}.

### item_id: L10-00027
Write a daily steam-generator log for OTSG OTSG-2 on 2023-03-28: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 765.0, "rate_t_per_d": 54.643, "pressure_mpa": 8.181, "quality": 0.746}.

### item_id: L10-00028
Write a daily steam-generator log for OTSG OTSG-2 on 2025-09-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 893.0, "rate_t_per_d": 63.786, "pressure_mpa": 10.099, "quality": 0.768}.

### item_id: L10-00029
Write a daily steam-generator log for OTSG OTSG-3 on 2022-08-21: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 595.0, "rate_t_per_d": 42.5, "pressure_mpa": 8.091, "quality": 0.654}.

### item_id: L10-00030
Write a daily steam-generator log for OTSG OTSG-1 on 2024-04-23: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 863.0, "rate_t_per_d": 61.643, "pressure_mpa": 9.472, "quality": 0.76}.

### item_id: L10-00031
Write a daily steam-generator log for OTSG OTSG-2 on 2023-10-19: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1017.0, "rate_t_per_d": 72.643, "pressure_mpa": 10.768, "quality": 0.773}.

### item_id: L10-00032
Write a daily steam-generator log for OTSG OTSG-2 on 2023-03-28: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1033.0, "rate_t_per_d": 73.786, "pressure_mpa": 11.045, "quality": 0.739}.

### item_id: L10-00033
Write a daily steam-generator log for OTSG OTSG-2 on 2024-02-05: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 811.0, "rate_t_per_d": 57.929, "pressure_mpa": 9.503, "quality": 0.7}.

### item_id: L10-00034
Write a daily steam-generator log for OTSG OTSG-2 on 2026-03-11: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 701.0, "rate_t_per_d": 50.071, "pressure_mpa": 8.521, "quality": 0.774}.

### item_id: L10-00035
Write a daily steam-generator log for OTSG OTSG-2 on 2024-05-29: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 795.0, "rate_t_per_d": 56.786, "pressure_mpa": 9.703, "quality": 0.645}.

### item_id: L10-00036
Write a daily steam-generator log for OTSG OTSG-1 on 2025-05-15: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 914.0, "rate_t_per_d": 65.286, "pressure_mpa": 9.146, "quality": 0.698}.

### item_id: L10-00037
Write a daily steam-generator log for OTSG OTSG-1 on 2025-07-31: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1014.0, "rate_t_per_d": 72.429, "pressure_mpa": 11.486, "quality": 0.702}.

### item_id: L10-00038
Write a daily steam-generator log for OTSG OTSG-1 on 2026-01-12: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 810.0, "rate_t_per_d": 57.857, "pressure_mpa": 9.526, "quality": 0.717}.

### item_id: L10-00039
Write a daily steam-generator log for OTSG OTSG-1 on 2026-05-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1000.0, "rate_t_per_d": 71.429, "pressure_mpa": 10.195, "quality": 0.776}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
