# L1 well_master - batch 008 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L1/replies/L1_batch_008.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L1-00070 .. L1-00079 (each has an `item_id` you must echo).

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

### item_id: L1-00070
Write the well master record for BGW-32 drilled 2016-03-13: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1040.267 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1086.348-1123.35 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.818, "asphaltene_wt_pct": 7.204, "t_res_c": 47.746, "p_res_mpa": 2.785, "pump_bore_in": 1.75, "pump_depth_m": 1040.267, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 37.002, "porosity": 0.266, "perm_md": 1329.569}.

### item_id: L1-00071
Write the well master record for BGW-42 drilled 2021-02-28: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1085.252 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1121.972-1151.29 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.115, "asphaltene_wt_pct": 10.113, "t_res_c": 47.546, "p_res_mpa": 2.833, "pump_bore_in": 1.75, "pump_depth_m": 1085.252, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 29.318, "porosity": 0.25, "perm_md": 1982.822}.

### item_id: L1-00072
Write the well master record for BGW-07 drilled 2012-07-22: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1087.769 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1090.571-1130.256 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.131, "asphaltene_wt_pct": 11.233, "t_res_c": 47.814, "p_res_mpa": 3.197, "pump_bore_in": 1.0, "pump_depth_m": 1087.769, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 39.685, "porosity": 0.243, "perm_md": 1055.549}.

### item_id: L1-00073
Write the well master record for BGW-17 drilled 2024-02-14: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.0 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1100.0-1140.0 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.0, "asphaltene_wt_pct": 9.2, "t_res_c": 47.0, "p_res_mpa": 3.1, "pump_bore_in": 1.25, "pump_depth_m": 1068.0, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 40.0, "porosity": 0.27, "perm_md": 1800.0}.

### item_id: L1-00074
Write the well master record for BGW-17 drilled 2024-02-14: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.0 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1100.0-1140.0 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.0, "asphaltene_wt_pct": 9.2, "t_res_c": 47.0, "p_res_mpa": 3.1, "pump_bore_in": 1.25, "pump_depth_m": 1068.0, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 40.0, "porosity": 0.27, "perm_md": 1800.0}.

### item_id: L1-00075
Write the well master record for BGW-17 drilled 2024-02-14: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.0 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1100.0-1140.0 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.0, "asphaltene_wt_pct": 9.2, "t_res_c": 47.0, "p_res_mpa": 3.1, "pump_bore_in": 1.25, "pump_depth_m": 1068.0, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 40.0, "porosity": 0.27, "perm_md": 1800.0}.

### item_id: L1-00076
Write the well master record for BGW-53 drilled 2018-05-15: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1052.003 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1099.32-1137.94 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.345, "asphaltene_wt_pct": 8.99, "t_res_c": 47.731, "p_res_mpa": 3.137, "pump_bore_in": 1.25, "pump_depth_m": 1052.003, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 38.62, "porosity": 0.299, "perm_md": 1602.208}.

### item_id: L1-00077
Write the well master record for BGW-18 drilled 2015-10-06: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1051.677 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1114.697-1138.681 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.012, "asphaltene_wt_pct": 8.643, "t_res_c": 46.799, "p_res_mpa": 3.318, "pump_bore_in": 1.0, "pump_depth_m": 1051.677, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 23.984, "porosity": 0.286, "perm_md": 984.106}.

### item_id: L1-00078
Write the well master record for BGW-46 drilled 2014-08-31: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1069.939 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1102.753-1132.355 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.204, "asphaltene_wt_pct": 8.946, "t_res_c": 47.271, "p_res_mpa": 2.974, "pump_bore_in": 1.75, "pump_depth_m": 1069.939, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 29.602, "porosity": 0.265, "perm_md": 2974.298}.

### item_id: L1-00079
Write the well master record for BGW-23 drilled 2011-07-10: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1053.191 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1120.709-1143.683 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.107, "asphaltene_wt_pct": 8.685, "t_res_c": 47.152, "p_res_mpa": 2.776, "pump_bore_in": 1.0, "pump_depth_m": 1053.191, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 22.974, "porosity": 0.272, "perm_md": 1409.922}.

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
