# L1 well_master - batch 006 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L1/replies/L1_batch_006.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L1-00050 .. L1-00059 (each has an `item_id` you must echo).

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

### item_id: L1-00050
Write the well master record for BGW-46 drilled 2014-08-31: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1069.939 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1102.753-1132.355 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.204, "asphaltene_wt_pct": 8.946, "t_res_c": 47.271, "p_res_mpa": 2.974, "pump_bore_in": 1.75, "pump_depth_m": 1069.939, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 29.602, "porosity": 0.265, "perm_md": 2974.298}.

### item_id: L1-00051
Write the well master record for BGW-16 drilled 2020-09-07: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1055.066 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1099.594-1152.476 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.381, "asphaltene_wt_pct": 8.983, "t_res_c": 46.023, "p_res_mpa": 3.021, "pump_bore_in": 1.5, "pump_depth_m": 1055.066, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 52.882, "porosity": 0.252, "perm_md": 986.013}.

### item_id: L1-00052
Write the well master record for BGW-03 drilled 2013-01-11: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1040.975 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1090.722-1117.122 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.223, "asphaltene_wt_pct": 7.28, "t_res_c": 47.653, "p_res_mpa": 2.708, "pump_bore_in": 1.75, "pump_depth_m": 1040.975, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 26.4, "porosity": 0.289, "perm_md": 2173.758}.

### item_id: L1-00053
Write the well master record for BGW-02 drilled 2015-03-18: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1047.526 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1120.797-1160.559 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.704, "asphaltene_wt_pct": 11.955, "t_res_c": 46.753, "p_res_mpa": 2.718, "pump_bore_in": 1.5, "pump_depth_m": 1047.526, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 39.762, "porosity": 0.259, "perm_md": 1212.932}.

### item_id: L1-00054
Write the well master record for BGW-47 drilled 2014-03-21: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1055.018 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1094.761-1147.087 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.914, "asphaltene_wt_pct": 7.827, "t_res_c": 46.251, "p_res_mpa": 2.887, "pump_bore_in": 1.75, "pump_depth_m": 1055.018, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 52.326, "porosity": 0.287, "perm_md": 1811.384}.

### item_id: L1-00055
Write the well master record for BGW-46 drilled 2014-08-31: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1069.939 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1102.753-1132.355 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.204, "asphaltene_wt_pct": 8.946, "t_res_c": 47.271, "p_res_mpa": 2.974, "pump_bore_in": 1.75, "pump_depth_m": 1069.939, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 29.602, "porosity": 0.265, "perm_md": 2974.298}.

### item_id: L1-00056
Write the well master record for BGW-39 drilled 2019-01-02: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1079.905 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1087.205-1119.181 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.782, "asphaltene_wt_pct": 7.693, "t_res_c": 46.649, "p_res_mpa": 2.965, "pump_bore_in": 1.25, "pump_depth_m": 1079.905, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 31.976, "porosity": 0.285, "perm_md": 1666.192}.

### item_id: L1-00057
Write the well master record for BGW-23 drilled 2011-07-10: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1053.191 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1120.709-1143.683 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.107, "asphaltene_wt_pct": 8.685, "t_res_c": 47.152, "p_res_mpa": 2.776, "pump_bore_in": 1.0, "pump_depth_m": 1053.191, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 22.974, "porosity": 0.272, "perm_md": 1409.922}.

### item_id: L1-00058
Write the well master record for BGW-18 drilled 2015-10-06: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1051.677 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1114.697-1138.681 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.012, "asphaltene_wt_pct": 8.643, "t_res_c": 46.799, "p_res_mpa": 3.318, "pump_bore_in": 1.0, "pump_depth_m": 1051.677, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 23.984, "porosity": 0.286, "perm_md": 984.106}.

### item_id: L1-00059
Write the well master record for BGW-22 drilled 2017-02-20: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1071.354 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1109.13-1148.23 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.273, "asphaltene_wt_pct": 9.486, "t_res_c": 47.238, "p_res_mpa": 2.898, "pump_bore_in": 1.0, "pump_depth_m": 1071.354, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 39.1, "porosity": 0.299, "perm_md": 4241.946}.

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
