# L8 dyno_expert_annotation - batch 006 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_006.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00125 .. L8-00149 (each has an `item_id` you must echo).

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

### item_id: L8-00125
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.511, "load_range": 1.436, "roughness": 0.002, "up_mid": 5.615, "dn_mid": 4.56, "up_slope": -0.423, "dn_slope": 0.458, "drop_pos": 1.0, "drop_width": 0.125} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00126
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.257, "load_range": 2.939, "roughness": 0.023, "up_mid": 10.427, "dn_mid": 7.834, "up_slope": -0.803, "dn_slope": 0.395, "drop_pos": 0.95, "drop_width": 0.175} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00127
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.983, "load_range": 2.601, "roughness": 0.013, "up_mid": 9.961, "dn_mid": 7.658, "up_slope": -0.578, "dn_slope": 0.292, "drop_pos": 0.955, "drop_width": 0.105} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00128
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.459, "load_range": 3.903, "roughness": 0.022, "up_mid": 10.355, "dn_mid": 7.986, "up_slope": -2.263, "dn_slope": 0.813, "drop_pos": 1.0, "drop_width": 0.08} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00129
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.023, "load_range": 2.266, "roughness": 0.029, "up_mid": 7.565, "dn_mid": 5.619, "up_slope": -0.184, "dn_slope": 0.288, "drop_pos": 0.95, "drop_width": 0.405} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00130
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.071, "load_range": 3.507, "roughness": 0.033, "up_mid": 6.905, "dn_mid": 4.144, "up_slope": -0.8, "dn_slope": 0.698, "drop_pos": 0.97, "drop_width": 0.165} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00131
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.13, "load_range": 3.376, "roughness": 0.02, "up_mid": 8.187, "dn_mid": 5.588, "up_slope": -0.819, "dn_slope": 0.92, "drop_pos": 0.985, "drop_width": 0.135} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00132
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.178, "load_range": 1.627, "roughness": 0.009, "up_mid": 6.558, "dn_mid": 5.055, "up_slope": -0.104, "dn_slope": 0.154, "drop_pos": 0.955, "drop_width": 0.1} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00133
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.764, "load_range": 2.595, "roughness": 0.024, "up_mid": 7.679, "dn_mid": 5.307, "up_slope": -0.307, "dn_slope": 0.295, "drop_pos": 0.83, "drop_width": 0.255} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00134
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.973, "load_range": 4.723, "roughness": 0.009, "up_mid": 11.668, "dn_mid": 7.315, "up_slope": -1.078, "dn_slope": 0.406, "drop_pos": 0.89, "drop_width": 0.5} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00135
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.78, "load_range": 6.083, "roughness": 0.04, "up_mid": 10.581, "dn_mid": 5.417, "up_slope": -2.006, "dn_slope": 0.927, "drop_pos": 0.925, "drop_width": 0.18} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00136
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.238, "load_range": 2.639, "roughness": 0.005, "up_mid": 11.355, "dn_mid": 9.202, "up_slope": -0.602, "dn_slope": 0.681, "drop_pos": 0.99, "drop_width": 0.18} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00137
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.331, "load_range": 2.515, "roughness": 0.014, "up_mid": 5.501, "dn_mid": 3.244, "up_slope": -0.233, "dn_slope": 0.255, "drop_pos": 0.95, "drop_width": 0.2} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00138
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.189, "load_range": 3.894, "roughness": 0.019, "up_mid": 11.372, "dn_mid": 7.886, "up_slope": -0.477, "dn_slope": 0.639, "drop_pos": 0.955, "drop_width": 0.2} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00139
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.908, "load_range": 2.496, "roughness": 0.006, "up_mid": 10.189, "dn_mid": 8.551, "up_slope": -0.882, "dn_slope": 0.873, "drop_pos": 1.0, "drop_width": 0.07} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00140
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.438, "load_range": 3.671, "roughness": 0.021, "up_mid": 12.454, "dn_mid": 9.67, "up_slope": -1.935, "dn_slope": 0.663, "drop_pos": 1.0, "drop_width": 0.13} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00141
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.987, "load_range": 2.591, "roughness": 0.021, "up_mid": 11.26, "dn_mid": 9.057, "up_slope": -0.35, "dn_slope": 0.469, "drop_pos": 0.95, "drop_width": 0.17} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00142
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.906, "load_range": 5.33, "roughness": 0.017, "up_mid": 12.838, "dn_mid": 8.259, "up_slope": -1.456, "dn_slope": 0.964, "drop_pos": 0.97, "drop_width": 0.205} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00143
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.967, "load_range": 5.38, "roughness": 0.028, "up_mid": 8.69, "dn_mid": 4.027, "up_slope": -1.213, "dn_slope": 0.953, "drop_pos": 0.955, "drop_width": 0.2} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00144
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.854, "load_range": 1.611, "roughness": 0.006, "up_mid": 5.901, "dn_mid": 4.771, "up_slope": -0.409, "dn_slope": 0.58, "drop_pos": 0.995, "drop_width": 0.095} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00145
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.572, "load_range": 4.155, "roughness": 0.036, "up_mid": 8.32, "dn_mid": 4.97, "up_slope": -0.927, "dn_slope": 0.943, "drop_pos": 0.975, "drop_width": 0.14} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00146
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.179, "load_range": 3.117, "roughness": 0.05, "up_mid": 10.331, "dn_mid": 7.543, "up_slope": -0.674, "dn_slope": -0.4, "drop_pos": 0.845, "drop_width": 0.69} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00147
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.049, "load_range": 1.942, "roughness": 0.019, "up_mid": 5.062, "dn_mid": 3.311, "up_slope": -0.04, "dn_slope": 0.253, "drop_pos": 0.965, "drop_width": 0.14} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00148
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.718, "load_range": 3.724, "roughness": 0.017, "up_mid": 9.168, "dn_mid": 6.065, "up_slope": -0.995, "dn_slope": 0.638, "drop_pos": 0.955, "drop_width": 0.15} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00149
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.994, "load_range": 2.988, "roughness": 0.02, "up_mid": 8.879, "dn_mid": 6.187, "up_slope": -0.719, "dn_slope": 0.367, "drop_pos": 0.96, "drop_width": 0.205} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
