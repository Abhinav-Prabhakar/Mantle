# L1 well_master - batch 004 (10 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 10 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L1/replies/L1_batch_004.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L1-00030 .. L1-00039 (each has an `item_id` you must echo).

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

### item_id: L1-00030
Write the well master record for BGW-18 drilled 2015-10-06: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1051.677 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1114.697-1138.681 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.012, "asphaltene_wt_pct": 8.643, "t_res_c": 46.799, "p_res_mpa": 3.318, "pump_bore_in": 1.0, "pump_depth_m": 1051.677, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 23.984, "porosity": 0.286, "perm_md": 984.106}.

### item_id: L1-00031
Write the well master record for BGW-35 drilled 2012-08-04: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1051.008 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1098.889-1125.912 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.034, "asphaltene_wt_pct": 8.047, "t_res_c": 46.797, "p_res_mpa": 3.158, "pump_bore_in": 1.0, "pump_depth_m": 1051.008, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 27.023, "porosity": 0.263, "perm_md": 858.894}.

### item_id: L1-00032
Write the well master record for BGW-50 drilled 2013-04-10: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1079.53 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1091.918-1137.385 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.287, "asphaltene_wt_pct": 11.817, "t_res_c": 47.494, "p_res_mpa": 2.625, "pump_bore_in": 1.75, "pump_depth_m": 1079.53, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 45.467, "porosity": 0.28, "perm_md": 1439.446}.

### item_id: L1-00033
Write the well master record for BGW-05 drilled 2013-07-04: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1081.278 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1100.197-1128.915 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.657, "asphaltene_wt_pct": 11.621, "t_res_c": 47.008, "p_res_mpa": 3.073, "pump_bore_in": 1.5, "pump_depth_m": 1081.278, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 28.718, "porosity": 0.247, "perm_md": 1235.473}.

### item_id: L1-00034
Write the well master record for BGW-15 drilled 2012-07-30: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1069.487 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1099.566-1131.932 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.179, "asphaltene_wt_pct": 8.151, "t_res_c": 46.934, "p_res_mpa": 3.32, "pump_bore_in": 1.0, "pump_depth_m": 1069.487, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 32.366, "porosity": 0.253, "perm_md": 2515.126}.

### item_id: L1-00035
Write the well master record for BGW-26 drilled 2017-09-10: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1071.59 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1106.743-1140.483 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.143, "asphaltene_wt_pct": 8.64, "t_res_c": 47.214, "p_res_mpa": 3.143, "pump_bore_in": 1.75, "pump_depth_m": 1071.59, "unit_class": "C-160D-173-64", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 33.74, "porosity": 0.298, "perm_md": 895.661}.

### item_id: L1-00036
Write the well master record for BGW-20 drilled 2014-07-05: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1048.051 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1097.198-1135.755 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 17.004, "asphaltene_wt_pct": 7.221, "t_res_c": 47.623, "p_res_mpa": 3.365, "pump_bore_in": 1.25, "pump_depth_m": 1048.051, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 38.557, "porosity": 0.283, "perm_md": 2108.11}.

### item_id: L1-00037
Write the well master record for BGW-55 drilled 2020-08-17: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1076.779 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1118.427-1166.187 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.209, "asphaltene_wt_pct": 10.811, "t_res_c": 47.811, "p_res_mpa": 2.889, "pump_bore_in": 1.0, "pump_depth_m": 1076.779, "unit_class": "C-320D-256-100", "stroke_m": 3.026, "vfd_kw": 37.0, "net_pay_m": 47.76, "porosity": 0.246, "perm_md": 2647.295}.

### item_id: L1-00038
Write the well master record for BGW-11 drilled 2014-05-11: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1041.094 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1091.809-1142.544 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 19.26, "asphaltene_wt_pct": 8.28, "t_res_c": 47.171, "p_res_mpa": 3.23, "pump_bore_in": 1.5, "pump_depth_m": 1041.094, "unit_class": "C-228D-213-86", "stroke_m": 3.026, "vfd_kw": 22.0, "net_pay_m": 50.735, "porosity": 0.254, "perm_md": 1854.191}.

### item_id: L1-00039
Write the well master record for BGW-49 drilled 2012-07-31: completion summary, casing/tubing/rod taper design (grades, sizes, lengths), pump (type, bore, setting depth 1082.879 m), pumping unit model class and stroke settings, VFD rating, perforation interval 1086.913-1130.797 m, last 3 workovers with reasons. Keep numbers consistent with: {"api": 18.67, "asphaltene_wt_pct": 8.799, "t_res_c": 46.153, "p_res_mpa": 3.309, "pump_bore_in": 1.0, "pump_depth_m": 1082.879, "unit_class": "C-456D-256-120", "stroke_m": 3.026, "vfd_kw": 30.0, "net_pay_m": 43.884, "porosity": 0.257, "perm_md": 1769.971}.

## Output contract
Return a JSON array of exactly 10 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
