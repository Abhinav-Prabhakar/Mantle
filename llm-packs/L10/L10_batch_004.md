# L10 steam_generator_log - batch 004 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L10/replies/L10_batch_004.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L10-00060 .. L10-00079 (each has an `item_id` you must echo).

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

### item_id: L10-00060
Write a daily steam-generator log for OTSG OTSG-1 on 2022-12-27: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 717.0, "rate_t_per_d": 51.214, "pressure_mpa": 9.101, "quality": 0.68}.

### item_id: L10-00061
Write a daily steam-generator log for OTSG OTSG-3 on 2025-12-07: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 675.0, "rate_t_per_d": 48.214, "pressure_mpa": 8.512, "quality": 0.798}.

### item_id: L10-00062
Write a daily steam-generator log for OTSG OTSG-1 on 2023-12-17: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 848.0, "rate_t_per_d": 60.571, "pressure_mpa": 9.116, "quality": 0.694}.

### item_id: L10-00063
Write a daily steam-generator log for OTSG OTSG-2 on 2024-12-14: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 766.0, "rate_t_per_d": 54.714, "pressure_mpa": 8.443, "quality": 0.68}.

### item_id: L10-00064
Write a daily steam-generator log for OTSG OTSG-2 on 2024-09-06: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 871.0, "rate_t_per_d": 62.214, "pressure_mpa": 9.249, "quality": 0.74}.

### item_id: L10-00065
Write a daily steam-generator log for OTSG OTSG-2 on 2026-05-07: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 849.0, "rate_t_per_d": 60.643, "pressure_mpa": 9.502, "quality": 0.633}.

### item_id: L10-00066
Write a daily steam-generator log for OTSG OTSG-1 on 2026-04-08: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1038.0, "rate_t_per_d": 74.143, "pressure_mpa": 10.813, "quality": 0.771}.

### item_id: L10-00067
Write a daily steam-generator log for OTSG OTSG-1 on 2026-07-23: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1081.0, "rate_t_per_d": 77.214, "pressure_mpa": 10.779, "quality": 0.722}.

### item_id: L10-00068
Write a daily steam-generator log for OTSG OTSG-3 on 2024-08-31: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 735.0, "rate_t_per_d": 52.5, "pressure_mpa": 8.494, "quality": 0.707}.

### item_id: L10-00069
Write a daily steam-generator log for OTSG OTSG-1 on 2026-08-26: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 910.0, "rate_t_per_d": 65.0, "pressure_mpa": 10.174, "quality": 0.739}.

### item_id: L10-00070
Write a daily steam-generator log for OTSG OTSG-3 on 2024-06-21: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 797.0, "rate_t_per_d": 56.929, "pressure_mpa": 9.409, "quality": 0.794}.

### item_id: L10-00071
Write a daily steam-generator log for OTSG OTSG-1 on 2026-01-06: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1021.0, "rate_t_per_d": 72.929, "pressure_mpa": 11.883, "quality": 0.673}.

### item_id: L10-00072
Write a daily steam-generator log for OTSG OTSG-1 on 2023-11-09: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 875.0, "rate_t_per_d": 62.5, "pressure_mpa": 9.512, "quality": 0.794}.

### item_id: L10-00073
Write a daily steam-generator log for OTSG OTSG-3 on 2024-10-28: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 905.0, "rate_t_per_d": 64.643, "pressure_mpa": 9.13, "quality": 0.664}.

### item_id: L10-00074
Write a daily steam-generator log for OTSG OTSG-1 on 2026-07-17: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 741.0, "rate_t_per_d": 52.929, "pressure_mpa": 8.74, "quality": 0.656}.

### item_id: L10-00075
Write a daily steam-generator log for OTSG OTSG-1 on 2025-08-21: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 596.0, "rate_t_per_d": 42.571, "pressure_mpa": 7.862, "quality": 0.711}.

### item_id: L10-00076
Write a daily steam-generator log for OTSG OTSG-1 on 2025-11-01: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 778.0, "rate_t_per_d": 55.571, "pressure_mpa": 8.949, "quality": 0.648}.

### item_id: L10-00077
Write a daily steam-generator log for OTSG OTSG-1 on 2025-08-22: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 885.0, "rate_t_per_d": 63.214, "pressure_mpa": 9.92, "quality": 0.675}.

### item_id: L10-00078
Write a daily steam-generator log for OTSG OTSG-3 on 2024-12-17: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 1200.0, "rate_t_per_d": 85.714, "pressure_mpa": 12.0, "quality": 0.687}.

### item_id: L10-00079
Write a daily steam-generator log for OTSG OTSG-3 on 2026-04-11: steam quality, rate t/h, feedwater TDS/hardness, burner hours, fuel gas Sm3, trips and causes, consistent with injection plan {"steam_t": 953.0, "rate_t_per_d": 68.071, "pressure_mpa": 10.068, "quality": 0.671}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
