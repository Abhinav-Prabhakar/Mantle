# L1 well_master - batch 007 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L1/replies/L1_batch_007.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L1-00060 .. L1-00069 (each has an `item_id` you must echo).

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

### item_id: L1-00060
Write the well master record for BGW-35 drilled 2012-08-04: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1051.008 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1098.889-1125.912 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.034, "asphaltene_wt_pct": 8.047, "t_res_c": 46.797, "p_res_mpa": 3.158, "pump_bore_in": 1.0, "pump_depth_m": 1051.008, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 27.023, "porosity": 0.263, "perm_md": 858.894}.

### item_id: L1-00061
Write the well master record for BGW-05 drilled 2013-07-04: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1081.278 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1100.197-1128.915 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.657, "asphaltene_wt_pct": 11.621, "t_res_c": 47.008, "p_res_mpa": 3.073, "pump_bore_in": 1.5, "pump_depth_m": 1081.278, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 28.718, "porosity": 0.247, "perm_md": 1235.473}.

### item_id: L1-00062
Write the well master record for BGW-04 drilled 2016-11-20: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1040.067 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1102.594-1143.55 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.637, "asphaltene_wt_pct": 9.561, "t_res_c": 47.643, "p_res_mpa": 3.379, "pump_bore_in": 1.5, "pump_depth_m": 1040.067, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 40.957, "porosity": 0.275, "perm_md": 750.229}.

### item_id: L1-00063
Write the well master record for BGW-01 drilled 2017-01-10: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1084.424 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1087.839-1128.76 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.123, "asphaltene_wt_pct": 10.261, "t_res_c": 47.522, "p_res_mpa": 3.19, "pump_bore_in": 1.75, "pump_depth_m": 1084.424, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 40.921, "porosity": 0.242, "perm_md": 1341.517}.

### item_id: L1-00064
Write the well master record for BGW-32 drilled 2016-03-13: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1040.267 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1086.348-1123.35 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.818, "asphaltene_wt_pct": 7.204, "t_res_c": 47.746, "p_res_mpa": 2.785, "pump_bore_in": 1.75, "pump_depth_m": 1040.267, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 37.002, "porosity": 0.266, "perm_md": 1329.569}.

### item_id: L1-00065
Write the well master record for BGW-38 drilled 2019-06-27: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1057.676 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1123.207-1177.002 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.964, "asphaltene_wt_pct": 9.072, "t_res_c": 47.221, "p_res_mpa": 3.062, "pump_bore_in": 1.75, "pump_depth_m": 1057.676, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 53.796, "porosity": 0.281, "perm_md": 1077.873}.

### item_id: L1-00066
Write the well master record for BGW-25 drilled 2019-04-24: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1071.319 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1085.724-1122.97 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.864, "asphaltene_wt_pct": 9.088, "t_res_c": 46.021, "p_res_mpa": 3.264, "pump_bore_in": 1.25, "pump_depth_m": 1071.319, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 37.246, "porosity": 0.291, "perm_md": 981.47}.

### item_id: L1-00067
Write the well master record for BGW-56 drilled 2011-02-19: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1065.279 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1101.693-1144.919 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.25, "asphaltene_wt_pct": 9.106, "t_res_c": 47.033, "p_res_mpa": 2.932, "pump_bore_in": 1.0, "pump_depth_m": 1065.279, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 43.225, "porosity": 0.272, "perm_md": 2228.106}.

### item_id: L1-00068
Write the well master record for BGW-37 drilled 2011-01-07: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1054.582 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1103.938-1149.855 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.504, "asphaltene_wt_pct": 8.662, "t_res_c": 47.272, "p_res_mpa": 2.887, "pump_bore_in": 1.75, "pump_depth_m": 1054.582, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 45.918, "porosity": 0.249, "perm_md": 675.498}.

### item_id: L1-00069
Write the well master record for BGW-25 drilled 2019-04-24: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1071.319 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1085.724-1122.97 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.864, "asphaltene_wt_pct": 9.088, "t_res_c": 46.021, "p_res_mpa": 3.264, "pump_bore_in": 1.25, "pump_depth_m": 1071.319, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 37.246, "porosity": 0.291, "perm_md": 981.47}.

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
