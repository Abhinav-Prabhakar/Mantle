# L1 well_master - batch 001 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L1/replies/L1_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L1-00000 .. L1-00009 (each has an `item_id` you must echo).

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

### item_id: L1-00000
Write the well master record for BGW-05 drilled 2013-07-04: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1081.278 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1100.197-1128.915 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.657, "asphaltene_wt_pct": 11.621, "t_res_c": 47.008, "p_res_mpa": 3.073, "pump_bore_in": 1.5, "pump_depth_m": 1081.278, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 28.718, "porosity": 0.247, "perm_md": 1235.473}.

### item_id: L1-00001
Write the well master record for BGW-42 drilled 2021-02-28: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1085.252 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1121.972-1151.29 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.115, "asphaltene_wt_pct": 10.113, "t_res_c": 47.546, "p_res_mpa": 2.833, "pump_bore_in": 1.75, "pump_depth_m": 1085.252, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 29.318, "porosity": 0.25, "perm_md": 1982.822}.

### item_id: L1-00002
Write the well master record for BGW-29 drilled 2016-06-27: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1065.086 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1116.113-1166.378 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.623, "asphaltene_wt_pct": 10.858, "t_res_c": 46.878, "p_res_mpa": 2.805, "pump_bore_in": 1.5, "pump_depth_m": 1065.086, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 50.265, "porosity": 0.263, "perm_md": 2870.667}.

### item_id: L1-00003
Write the well master record for BGW-46 drilled 2014-08-31: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1069.939 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1102.753-1132.355 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.204, "asphaltene_wt_pct": 8.946, "t_res_c": 47.271, "p_res_mpa": 2.974, "pump_bore_in": 1.75, "pump_depth_m": 1069.939, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 29.602, "porosity": 0.265, "perm_md": 2974.298}.

### item_id: L1-00004
Write the well master record for BGW-09 drilled 2012-06-19: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.663 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1089.776-1116.065 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.699, "asphaltene_wt_pct": 11.072, "t_res_c": 46.327, "p_res_mpa": 3.24, "pump_bore_in": 1.0, "pump_depth_m": 1068.663, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 26.289, "porosity": 0.259, "perm_md": 1502.326}.

### item_id: L1-00005
Write the well master record for BGW-33 drilled 2011-07-03: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.397 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1090.391-1116.042 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.468, "asphaltene_wt_pct": 7.465, "t_res_c": 46.553, "p_res_mpa": 2.88, "pump_bore_in": 1.25, "pump_depth_m": 1068.397, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 25.651, "porosity": 0.245, "perm_md": 1983.857}.

### item_id: L1-00006
Write the well master record for BGW-30 drilled 2020-12-22: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1076.962 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1123.039-1157.137 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.157, "asphaltene_wt_pct": 11.204, "t_res_c": 46.346, "p_res_mpa": 2.897, "pump_bore_in": 1.0, "pump_depth_m": 1076.962, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 34.098, "porosity": 0.283, "perm_md": 2875.938}.

### item_id: L1-00007
Write the well master record for BGW-41 drilled 2011-08-30: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1052.584 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1123.398-1146.413 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.921, "asphaltene_wt_pct": 11.897, "t_res_c": 46.125, "p_res_mpa": 3.052, "pump_bore_in": 1.25, "pump_depth_m": 1052.584, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 23.015, "porosity": 0.257, "perm_md": 1662.971}.

### item_id: L1-00008
Write the well master record for BGW-54 drilled 2019-10-26: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1045.253 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1096.235-1136.485 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.171, "asphaltene_wt_pct": 8.036, "t_res_c": 47.861, "p_res_mpa": 2.796, "pump_bore_in": 1.25, "pump_depth_m": 1045.253, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 40.251, "porosity": 0.264, "perm_md": 766.389}.

### item_id: L1-00009
Write the well master record for BGW-57 drilled 2017-04-14: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1075.995 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1086.971-1118.572 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.074, "asphaltene_wt_pct": 11.426, "t_res_c": 47.7, "p_res_mpa": 3.005, "pump_bore_in": 1.0, "pump_depth_m": 1075.995, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 31.601, "porosity": 0.275, "perm_md": 2206.616}.

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
