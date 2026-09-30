# L1 well_master - batch 002 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L1/replies/L1_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L1-00010 .. L1-00019 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "well_id", "spud_date", "completion_summary", "casing_design", "tubing_design", "rod_taper_sections", "pump_type", "pump_bore_in", "pump_setting_depth_m", "pumping_unit_model", "stroke_settings", "vfd_rating_kw", "perforation_top_m", "perforation_bottom_m", "last_workovers"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "well_id": {"type": "string"},
    "spud_date": {"type": "string"},
    "completion_summary": {"type": "string"},
    "casing_design": {"type": "string"},
    "tubing_design": {"type": "string"},
    "rod_taper_sections": {"type": "array", "items": {"type": "string"}, "minItems": 2},
    "pump_type": {"type": "string"},
    "pump_bore_in": {"type": "number", "minimum": 0.75, "maximum": 2.5},
    "pump_setting_depth_m": {"type": "number", "minimum": 500, "maximum": 1300},
    "pumping_unit_model": {"type": "string"},
    "stroke_settings": {"type": "string"},
    "vfd_rating_kw": {"type": "number", "minimum": 5, "maximum": 75},
    "perforation_top_m": {"type": "number", "minimum": 1000, "maximum": 1200},
    "perforation_bottom_m": {"type": "number", "minimum": 1000, "maximum": 1250},
    "last_workovers": {"type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 3}
  }
}
```
Extra constraints:
- perforation_top_m <= perforation_bottom_m

## Items (10)
Write one record per item, following the instruction under each item_id.

### item_id: L1-00010
Write the well master record for BGW-30 drilled 2020-12-22: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1076.962 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1123.039-1157.137 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.157, "asphaltene_wt_pct": 11.204, "t_res_c": 46.346, "p_res_mpa": 2.897, "pump_bore_in": 1.0, "pump_depth_m": 1076.962, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 34.098, "porosity": 0.283, "perm_md": 2875.938}.

### item_id: L1-00011
Write the well master record for BGW-54 drilled 2019-10-26: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1045.253 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1096.235-1136.485 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.171, "asphaltene_wt_pct": 8.036, "t_res_c": 47.861, "p_res_mpa": 2.796, "pump_bore_in": 1.25, "pump_depth_m": 1045.253, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 40.251, "porosity": 0.264, "perm_md": 766.389}.

### item_id: L1-00012
Write the well master record for BGW-13 drilled 2020-08-21: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1044.516 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1094.065-1139.628 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.616, "asphaltene_wt_pct": 7.177, "t_res_c": 47.52, "p_res_mpa": 2.843, "pump_bore_in": 1.75, "pump_depth_m": 1044.516, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 45.563, "porosity": 0.248, "perm_md": 2769.387}.

### item_id: L1-00013
Write the well master record for BGW-28 drilled 2012-08-06: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.367 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1100.961-1145.384 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.019, "asphaltene_wt_pct": 11.024, "t_res_c": 46.747, "p_res_mpa": 3.354, "pump_bore_in": 1.5, "pump_depth_m": 1068.367, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 44.423, "porosity": 0.276, "perm_md": 946.699}.

### item_id: L1-00014
Write the well master record for BGW-18 drilled 2015-10-06: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1051.677 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1114.697-1138.681 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.012, "asphaltene_wt_pct": 8.643, "t_res_c": 46.799, "p_res_mpa": 3.318, "pump_bore_in": 1.0, "pump_depth_m": 1051.677, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 23.984, "porosity": 0.286, "perm_md": 984.106}.

### item_id: L1-00015
Write the well master record for BGW-46 drilled 2014-08-31: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1069.939 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1102.753-1132.355 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.204, "asphaltene_wt_pct": 8.946, "t_res_c": 47.271, "p_res_mpa": 2.974, "pump_bore_in": 1.75, "pump_depth_m": 1069.939, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 29.602, "porosity": 0.265, "perm_md": 2974.298}.

### item_id: L1-00016
Write the well master record for BGW-15 drilled 2012-07-30: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1069.487 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1099.566-1131.932 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.179, "asphaltene_wt_pct": 8.151, "t_res_c": 46.934, "p_res_mpa": 3.32, "pump_bore_in": 1.0, "pump_depth_m": 1069.487, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 32.366, "porosity": 0.253, "perm_md": 2515.126}.

### item_id: L1-00017
Write the well master record for BGW-07 drilled 2012-07-22: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1087.769 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1090.571-1130.256 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.131, "asphaltene_wt_pct": 11.233, "t_res_c": 47.814, "p_res_mpa": 3.197, "pump_bore_in": 1.0, "pump_depth_m": 1087.769, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 39.685, "porosity": 0.243, "perm_md": 1055.549}.

### item_id: L1-00018
Write the well master record for BGW-57 drilled 2017-04-14: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1075.995 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1086.971-1118.572 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.074, "asphaltene_wt_pct": 11.426, "t_res_c": 47.7, "p_res_mpa": 3.005, "pump_bore_in": 1.0, "pump_depth_m": 1075.995, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 31.601, "porosity": 0.275, "perm_md": 2206.616}.

### item_id: L1-00019
Write the well master record for BGW-24 drilled 2011-07-11: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.035 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1107.236-1161.504 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.487, "asphaltene_wt_pct": 11.264, "t_res_c": 46.236, "p_res_mpa": 2.713, "pump_bore_in": 1.75, "pump_depth_m": 1068.035, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 54.267, "porosity": 0.279, "perm_md": 1130.544}.

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
