# L9 lab_fluid_report - batch 001 (12 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 12 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L9/replies/L9_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L9-00000 .. L9-00011 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "well_id", "sample_date", "api_15_6c", "asphaltene_pct", "resin_pct", "saturate_pct", "aromatic_pct", "wax_appearance_temp_c", "viscosity_50c_cp", "viscosity_80c_cp", "viscosity_120c_cp", "viscosity_160c_cp", "water_cut_pct", "bsw_pct", "emulsion_notes"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "well_id": {"type": "string"},
    "sample_date": {"type": "string"},
    "api_15_6c": {"type": "number", "minimum": 10, "maximum": 25},
    "asphaltene_pct": {"type": "number", "minimum": 0, "maximum": 30},
    "resin_pct": {"type": "number", "minimum": 0, "maximum": 50},
    "saturate_pct": {"type": "number", "minimum": 0, "maximum": 80},
    "aromatic_pct": {"type": "number", "minimum": 0, "maximum": 80},
    "wax_appearance_temp_c": {"type": "number", "minimum": 0, "maximum": 80},
    "viscosity_50c_cp": {"type": "number", "minimum": 0.3},
    "viscosity_80c_cp": {"type": "number", "minimum": 0.3},
    "viscosity_120c_cp": {"type": "number", "minimum": 0.3},
    "viscosity_160c_cp": {"type": "number", "minimum": 0.3},
    "water_cut_pct": {"type": "number", "minimum": 0, "maximum": 100},
    "bsw_pct": {"type": "number", "minimum": 0, "maximum": 100},
    "emulsion_notes": {"type": "string"}
  }
}
```
Extra constraints:
- viscosity_50c_cp >= viscosity_80c_cp >= viscosity_120c_cp >= viscosity_160c_cp

## Items (12)
Write one record per item, following the instruction under each item_id.

### item_id: L9-00000
Write a lab report for a crude sample from BGW-41 taken 2024-12-27: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.648,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00001
Write a lab report for a crude sample from BGW-09 taken 2025-12-31: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.644,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00002
Write a lab report for a crude sample from BGW-59 taken 2025-11-14: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.642,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00003
Write a lab report for a crude sample from BGW-50 taken 2025-06-10: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.644,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00004
Write a lab report for a crude sample from BGW-43 taken 2026-04-19: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.649,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00005
Write a lab report for a crude sample from BGW-46 taken 2024-03-21: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.637,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00006
Write a lab report for a crude sample from BGW-34 taken 2024-10-25: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.632,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00007
Write a lab report for a crude sample from BGW-35 taken 2025-10-05: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.65,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00008
Write a lab report for a crude sample from BGW-05 taken 2024-07-03: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.636,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00009
Write a lab report for a crude sample from BGW-20 taken 2025-09-03: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.645,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00010
Write a lab report for a crude sample from BGW-18 taken 2025-04-20: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.646,2.803, water cut, BS&W, emulsion notes.

### item_id: L9-00011
Write a lab report for a crude sample from BGW-54 taken 2024-03-24: API at 15.6 C, asphaltene/resin/saturate/aromatic %, wax appearance temperature, viscosity at 50/80/120/160 C consistent with Walther parameters 7.646,2.803, water cut, BS&W, emulsion notes.

## Output contract
Return a JSON array of exactly 12 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
