# L11 energy_tariff_note - batch 002 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L11/replies/L11_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L11-00010 .. L11-00019 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "period", "energy_slabs", "demand_charge_inr_per_kva_month", "fuel_gas_inr_per_sm3", "note"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "period": {"type": "string"},
    "energy_slabs": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "demand_charge_inr_per_kva_month": {"type": "number", "minimum": 0},
    "fuel_gas_inr_per_sm3": {"type": "number", "minimum": 0},
    "note": {"type": "string"}
  }
}
```

## Items (10)
Write one record per item, following the instruction under each item_id.

### item_id: L11-00010
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2019-20 Q1 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

### item_id: L11-00011
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2020-21 Q4 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

### item_id: L11-00012
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2021-22 Q1 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

### item_id: L11-00013
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2022-23 Q4 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

### item_id: L11-00014
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2023-24 Q1 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

### item_id: L11-00015
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2024-25 Q2 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

### item_id: L11-00016
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2025-26 Q4 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

### item_id: L11-00017
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2026-27 Q3 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

### item_id: L11-00018
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2018-19 Q1 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

### item_id: L11-00019
Write a short note on the electricity tariff and fuel-gas price applicable to FY 2019-20 Q3 for a Rajasthan upstream site, as would appear in an internal cost memo (INR/kWh slabs, demand charge, gas INR/Sm3).

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
