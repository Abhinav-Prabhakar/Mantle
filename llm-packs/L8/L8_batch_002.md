# L8 dyno_expert_annotation - batch 002 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00025 .. L8-00049 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "card_class", "visual_cues", "diagnosis", "confidence", "corrective_action"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "card_class": {"type": "string"},
    "visual_cues": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "diagnosis": {"type": "string"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "corrective_action": {"type": "string"}
  }
}
```

## Items (25)
Write one record per item, following the instruction under each item_id.

### item_id: L8-00025
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.489, "load_range": 3.257, "roughness": 0.018, "up_mid": 9.985, "dn_mid": 7.207, "up_slope": -0.393, "dn_slope": 0.711, "drop_pos": 0.965, "drop_width": 0.165} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00026
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.02, "load_range": 4.633, "roughness": 0.041, "up_mid": 11.269, "dn_mid": 7.583, "up_slope": -1.611, "dn_slope": 0.921, "drop_pos": 0.805, "drop_width": 0.26} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00027
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.047, "load_range": 2.099, "roughness": 0.021, "up_mid": 6.406, "dn_mid": 4.484, "up_slope": -0.082, "dn_slope": 0.222, "drop_pos": 0.945, "drop_width": 0.185} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00028
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.817, "load_range": 1.758, "roughness": 0.02, "up_mid": 6.053, "dn_mid": 4.453, "up_slope": -0.208, "dn_slope": 0.059, "drop_pos": 0.615, "drop_width": 0.36} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00029
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.943, "load_range": 3.488, "roughness": 0.014, "up_mid": 6.072, "dn_mid": 3.144, "up_slope": -0.696, "dn_slope": 0.796, "drop_pos": 0.97, "drop_width": 0.19} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00030
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.01, "load_range": 1.77, "roughness": 0.004, "up_mid": 6.069, "dn_mid": 4.561, "up_slope": -0.275, "dn_slope": 0.424, "drop_pos": 0.97, "drop_width": 0.225} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00031
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.002, "load_range": 7.933, "roughness": 0.048, "up_mid": 12.107, "dn_mid": 5.608, "up_slope": -1.963, "dn_slope": 1.883, "drop_pos": 0.975, "drop_width": 0.175} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00032
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.171, "load_range": 5.473, "roughness": 0.033, "up_mid": 12.915, "dn_mid": 8.116, "up_slope": -1.323, "dn_slope": 0.866, "drop_pos": 0.94, "drop_width": 0.205} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00033
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.512, "load_range": 1.41, "roughness": 0.02, "up_mid": 6.069, "dn_mid": 4.721, "up_slope": -0.072, "dn_slope": -0.253, "drop_pos": 0.535, "drop_width": 0.435} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00034
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.088, "load_range": 3.264, "roughness": 0.031, "up_mid": 6.297, "dn_mid": 3.436, "up_slope": -0.462, "dn_slope": 0.601, "drop_pos": 0.97, "drop_width": 0.19} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00035
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.397, "load_range": 3.608, "roughness": 0.006, "up_mid": 9.146, "dn_mid": 6.118, "up_slope": -0.586, "dn_slope": 0.923, "drop_pos": 0.975, "drop_width": 0.215} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00036
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.3, "load_range": 2.174, "roughness": 0.044, "up_mid": 8.67, "dn_mid": 7.014, "up_slope": -0.324, "dn_slope": 0.342, "drop_pos": 0.95, "drop_width": 0.18} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00037
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.556, "load_range": 3.662, "roughness": 0.006, "up_mid": 6.602, "dn_mid": 3.302, "up_slope": -0.585, "dn_slope": 0.614, "drop_pos": 0.84, "drop_width": 0.39} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00038
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.006, "load_range": 3.718, "roughness": 0.021, "up_mid": 7.183, "dn_mid": 4.096, "up_slope": -0.742, "dn_slope": 0.905, "drop_pos": 0.965, "drop_width": 0.195} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00039
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.66, "load_range": 2.826, "roughness": 0.025, "up_mid": 8.467, "dn_mid": 6.059, "up_slope": -0.231, "dn_slope": 0.596, "drop_pos": 0.975, "drop_width": 0.16} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00040
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.582, "load_range": 3.126, "roughness": 0.045, "up_mid": 11.668, "dn_mid": 8.888, "up_slope": -0.534, "dn_slope": -0.098, "drop_pos": 0.9, "drop_width": 0.56} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00041
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.158, "load_range": 3.091, "roughness": 0.046, "up_mid": 9.457, "dn_mid": 6.636, "up_slope": -0.541, "dn_slope": -0.413, "drop_pos": 0.82, "drop_width": 0.675} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00042
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.493, "load_range": 3.064, "roughness": 0.026, "up_mid": 5.877, "dn_mid": 3.261, "up_slope": -0.676, "dn_slope": 0.586, "drop_pos": 0.96, "drop_width": 0.19} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00043
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.61, "load_range": 1.648, "roughness": 0.046, "up_mid": 8.146, "dn_mid": 7.127, "up_slope": -0.635, "dn_slope": 0.359, "drop_pos": 1.0, "drop_width": 0.0} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00044
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.879, "load_range": 2.42, "roughness": 0.034, "up_mid": 6.379, "dn_mid": 4.56, "up_slope": -0.31, "dn_slope": -0.359, "drop_pos": 0.75, "drop_width": 0.915} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00045
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.154, "load_range": 4.572, "roughness": 0.046, "up_mid": 10.774, "dn_mid": 7.088, "up_slope": -0.685, "dn_slope": 1.198, "drop_pos": 0.97, "drop_width": 0.195} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00046
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.843, "load_range": 2.101, "roughness": 0.006, "up_mid": 6.651, "dn_mid": 4.696, "up_slope": -0.175, "dn_slope": -0.06, "drop_pos": 0.61, "drop_width": 0.545} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00047
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.218, "load_range": 1.266, "roughness": 0.003, "up_mid": 6.003, "dn_mid": 4.888, "up_slope": -0.202, "dn_slope": 0.235, "drop_pos": 0.95, "drop_width": 0.255} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00048
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.743, "load_range": 5.563, "roughness": 0.011, "up_mid": 9.139, "dn_mid": 4.684, "up_slope": -1.851, "dn_slope": 1.299, "drop_pos": 1.0, "drop_width": 0.155} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00049
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.48, "load_range": 1.547, "roughness": 0.033, "up_mid": 4.736, "dn_mid": 3.365, "up_slope": -0.181, "dn_slope": 0.055, "drop_pos": 0.955, "drop_width": 0.115} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
