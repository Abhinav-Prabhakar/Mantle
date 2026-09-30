# L1 well_master - batch 010 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L1/replies/L1_batch_010.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L1-00090 .. L1-00099 (each has an `item_id` you must echo).

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

### item_id: L1-00090
Write the well master record for BGW-20 drilled 2014-07-05: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1048.051 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1097.198-1135.755 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.004, "asphaltene_wt_pct": 7.221, "t_res_c": 47.623, "p_res_mpa": 3.365, "pump_bore_in": 1.25, "pump_depth_m": 1048.051, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 38.557, "porosity": 0.283, "perm_md": 2108.11}.

### item_id: L1-00091
Write the well master record for BGW-02 drilled 2015-03-18: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1047.526 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1120.797-1160.559 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.704, "asphaltene_wt_pct": 11.955, "t_res_c": 46.753, "p_res_mpa": 2.718, "pump_bore_in": 1.5, "pump_depth_m": 1047.526, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 39.762, "porosity": 0.259, "perm_md": 1212.932}.

### item_id: L1-00092
Write the well master record for BGW-53 drilled 2018-05-15: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1052.003 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1099.32-1137.94 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.345, "asphaltene_wt_pct": 8.99, "t_res_c": 47.731, "p_res_mpa": 3.137, "pump_bore_in": 1.25, "pump_depth_m": 1052.003, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 38.62, "porosity": 0.299, "perm_md": 1602.208}.

### item_id: L1-00093
Write the well master record for BGW-35 drilled 2012-08-04: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1051.008 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1098.889-1125.912 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.034, "asphaltene_wt_pct": 8.047, "t_res_c": 46.797, "p_res_mpa": 3.158, "pump_bore_in": 1.0, "pump_depth_m": 1051.008, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 27.023, "porosity": 0.263, "perm_md": 858.894}.

### item_id: L1-00094
Write the well master record for BGW-52 drilled 2020-01-04: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1064.402 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1107.197-1145.594 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.22, "asphaltene_wt_pct": 8.888, "t_res_c": 46.212, "p_res_mpa": 2.735, "pump_bore_in": 1.75, "pump_depth_m": 1064.402, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 38.398, "porosity": 0.243, "perm_md": 1402.021}.

### item_id: L1-00095
Write the well master record for BGW-19 drilled 2021-03-01: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1075.96 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1116.916-1160.322 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.44, "asphaltene_wt_pct": 7.906, "t_res_c": 46.707, "p_res_mpa": 3.011, "pump_bore_in": 1.0, "pump_depth_m": 1075.96, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 43.406, "porosity": 0.261, "perm_md": 1635.693}.

### item_id: L1-00096
Write the well master record for BGW-48 drilled 2020-06-13: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1061.514 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1123.613-1156.821 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.111, "asphaltene_wt_pct": 10.149, "t_res_c": 46.518, "p_res_mpa": 3.231, "pump_bore_in": 1.25, "pump_depth_m": 1061.514, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 33.208, "porosity": 0.271, "perm_md": 3354.568}.

### item_id: L1-00097
Write the well master record for BGW-46 drilled 2014-08-31: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1069.939 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1102.753-1132.355 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.204, "asphaltene_wt_pct": 8.946, "t_res_c": 47.271, "p_res_mpa": 2.974, "pump_bore_in": 1.75, "pump_depth_m": 1069.939, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 29.602, "porosity": 0.265, "perm_md": 2974.298}.

### item_id: L1-00098
Write the well master record for BGW-09 drilled 2012-06-19: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.663 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1089.776-1116.065 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.699, "asphaltene_wt_pct": 11.072, "t_res_c": 46.327, "p_res_mpa": 3.24, "pump_bore_in": 1.0, "pump_depth_m": 1068.663, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 26.289, "porosity": 0.259, "perm_md": 1502.326}.

### item_id: L1-00099
Write the well master record for BGW-49 drilled 2012-07-31: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1082.879 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1086.913-1130.797 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.67, "asphaltene_wt_pct": 8.799, "t_res_c": 46.153, "p_res_mpa": 3.309, "pump_bore_in": 1.0, "pump_depth_m": 1082.879, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 43.884, "porosity": 0.257, "perm_md": 1769.971}.

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
