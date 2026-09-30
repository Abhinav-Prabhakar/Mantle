# L1 well_master - batch 005 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L1/replies/L1_batch_005.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L1-00040 .. L1-00049 (each has an `item_id` you must echo).

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

### item_id: L1-00040
Write the well master record for BGW-01 drilled 2017-01-10: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1084.424 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1087.839-1128.76 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.123, "asphaltene_wt_pct": 10.261, "t_res_c": 47.522, "p_res_mpa": 3.19, "pump_bore_in": 1.75, "pump_depth_m": 1084.424, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 40.921, "porosity": 0.242, "perm_md": 1341.517}.

### item_id: L1-00041
Write the well master record for BGW-60 drilled 2015-03-26: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1054.859 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1110.47-1160.065 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.825, "asphaltene_wt_pct": 8.092, "t_res_c": 46.699, "p_res_mpa": 2.96, "pump_bore_in": 1.25, "pump_depth_m": 1054.859, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 49.594, "porosity": 0.283, "perm_md": 1605.689}.

### item_id: L1-00042
Write the well master record for BGW-40 drilled 2020-07-28: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1083.656 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1095.919-1133.621 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.037, "asphaltene_wt_pct": 11.206, "t_res_c": 46.349, "p_res_mpa": 2.694, "pump_bore_in": 1.75, "pump_depth_m": 1083.656, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 37.702, "porosity": 0.262, "perm_md": 917.628}.

### item_id: L1-00043
Write the well master record for BGW-45 drilled 2013-08-11: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1046.538 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1118.722-1142.441 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.049, "asphaltene_wt_pct": 7.775, "t_res_c": 47.865, "p_res_mpa": 2.638, "pump_bore_in": 1.75, "pump_depth_m": 1046.538, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 23.719, "porosity": 0.254, "perm_md": 1560.186}.

### item_id: L1-00044
Write the well master record for BGW-08 drilled 2015-03-26: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.974 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1096.312-1142.35 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.197, "asphaltene_wt_pct": 10.749, "t_res_c": 46.924, "p_res_mpa": 3.028, "pump_bore_in": 1.0, "pump_depth_m": 1068.974, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 46.038, "porosity": 0.256, "perm_md": 1930.528}.

### item_id: L1-00045
Write the well master record for BGW-02 drilled 2015-03-18: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1047.526 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1120.797-1160.559 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.704, "asphaltene_wt_pct": 11.955, "t_res_c": 46.753, "p_res_mpa": 2.718, "pump_bore_in": 1.5, "pump_depth_m": 1047.526, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 39.762, "porosity": 0.259, "perm_md": 1212.932}.

### item_id: L1-00046
Write the well master record for BGW-24 drilled 2011-07-11: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1068.035 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1107.236-1161.504 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.487, "asphaltene_wt_pct": 11.264, "t_res_c": 46.236, "p_res_mpa": 2.713, "pump_bore_in": 1.75, "pump_depth_m": 1068.035, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 54.267, "porosity": 0.279, "perm_md": 1130.544}.

### item_id: L1-00047
Write the well master record for BGW-41 drilled 2011-08-30: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1052.584 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1123.398-1146.413 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.921, "asphaltene_wt_pct": 11.897, "t_res_c": 46.125, "p_res_mpa": 3.052, "pump_bore_in": 1.25, "pump_depth_m": 1052.584, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 23.015, "porosity": 0.257, "perm_md": 1662.971}.

### item_id: L1-00048
Write the well master record for BGW-59 drilled 2013-03-09: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1081.444 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1094.31-1127.149 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.603, "asphaltene_wt_pct": 7.439, "t_res_c": 47.821, "p_res_mpa": 2.806, "pump_bore_in": 1.0, "pump_depth_m": 1081.444, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 32.839, "porosity": 0.275, "perm_md": 1672.968}.

### item_id: L1-00049
Write the well master record for BGW-02 drilled 2015-03-18: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1047.526 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1120.797-1160.559 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.704, "asphaltene_wt_pct": 11.955, "t_res_c": 46.753, "p_res_mpa": 2.718, "pump_bore_in": 1.5, "pump_depth_m": 1047.526, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 39.762, "porosity": 0.259, "perm_md": 1212.932}.

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
