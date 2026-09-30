# L1 well_master - batch 009 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L1/replies/L1_batch_009.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L1-00080 .. L1-00089 (each has an `item_id` you must echo).

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

### item_id: L1-00080
Write the well master record for BGW-41 drilled 2011-08-30: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1052.584 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1123.398-1146.413 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.921, "asphaltene_wt_pct": 11.897, "t_res_c": 46.125, "p_res_mpa": 3.052, "pump_bore_in": 1.25, "pump_depth_m": 1052.584, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 23.015, "porosity": 0.257, "perm_md": 1662.971}.

### item_id: L1-00081
Write the well master record for BGW-54 drilled 2019-10-26: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1045.253 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1096.235-1136.485 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.171, "asphaltene_wt_pct": 8.036, "t_res_c": 47.861, "p_res_mpa": 2.796, "pump_bore_in": 1.25, "pump_depth_m": 1045.253, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 40.251, "porosity": 0.264, "perm_md": 766.389}.

### item_id: L1-00082
Write the well master record for BGW-55 drilled 2020-08-17: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1076.779 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1118.427-1166.187 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.209, "asphaltene_wt_pct": 10.811, "t_res_c": 47.811, "p_res_mpa": 2.889, "pump_bore_in": 1.0, "pump_depth_m": 1076.779, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 47.76, "porosity": 0.246, "perm_md": 2647.295}.

### item_id: L1-00083
Write the well master record for BGW-54 drilled 2019-10-26: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1045.253 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1096.235-1136.485 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.171, "asphaltene_wt_pct": 8.036, "t_res_c": 47.861, "p_res_mpa": 2.796, "pump_bore_in": 1.25, "pump_depth_m": 1045.253, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 40.251, "porosity": 0.264, "perm_md": 766.389}.

### item_id: L1-00084
Write the well master record for BGW-47 drilled 2014-03-21: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1055.018 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1094.761-1147.087 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.914, "asphaltene_wt_pct": 7.827, "t_res_c": 46.251, "p_res_mpa": 2.887, "pump_bore_in": 1.75, "pump_depth_m": 1055.018, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 52.326, "porosity": 0.287, "perm_md": 1811.384}.

### item_id: L1-00085
Write the well master record for BGW-57 drilled 2017-04-14: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1075.995 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1086.971-1118.572 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.074, "asphaltene_wt_pct": 11.426, "t_res_c": 47.7, "p_res_mpa": 3.005, "pump_bore_in": 1.0, "pump_depth_m": 1075.995, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 31.601, "porosity": 0.275, "perm_md": 2206.616}.

### item_id: L1-00086
Write the well master record for BGW-03 drilled 2013-01-11: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1040.975 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1090.722-1117.122 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.223, "asphaltene_wt_pct": 7.28, "t_res_c": 47.653, "p_res_mpa": 2.708, "pump_bore_in": 1.75, "pump_depth_m": 1040.975, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 26.4, "porosity": 0.289, "perm_md": 2173.758}.

### item_id: L1-00087
Write the well master record for BGW-23 drilled 2011-07-10: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1053.191 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1120.709-1143.683 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.107, "asphaltene_wt_pct": 8.685, "t_res_c": 47.152, "p_res_mpa": 2.776, "pump_bore_in": 1.0, "pump_depth_m": 1053.191, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 22.974, "porosity": 0.272, "perm_md": 1409.922}.

### item_id: L1-00088
Write the well master record for BGW-23 drilled 2011-07-10: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1053.191 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1120.709-1143.683 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.107, "asphaltene_wt_pct": 8.685, "t_res_c": 47.152, "p_res_mpa": 2.776, "pump_bore_in": 1.0, "pump_depth_m": 1053.191, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 22.974, "porosity": 0.272, "perm_md": 1409.922}.

### item_id: L1-00089
Write the well master record for BGW-29 drilled 2016-06-27: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1065.086 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1116.113-1166.378 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.623, "asphaltene_wt_pct": 10.858, "t_res_c": 46.878, "p_res_mpa": 2.805, "pump_bore_in": 1.5, "pump_depth_m": 1065.086, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 18.5, "net_pay_m": 50.265, "porosity": 0.263, "perm_md": 2870.667}.

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
