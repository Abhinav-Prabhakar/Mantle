# L8 dyno_expert_annotation - batch 004 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_004.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00075 .. L8-00099 (each has an `item_id` you must echo).

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

### item_id: L8-00075
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.375, "load_range": 1.518, "roughness": 0.01, "up_mid": 5.883, "dn_mid": 4.51, "up_slope": -0.058, "dn_slope": 0.092, "drop_pos": 0.94, "drop_width": 0.13} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00076
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.735, "load_range": 3.502, "roughness": 0.029, "up_mid": 12.49, "dn_mid": 9.866, "up_slope": -0.816, "dn_slope": 0.766, "drop_pos": 0.965, "drop_width": 0.11} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00077
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.026, "load_range": 2.802, "roughness": 0.006, "up_mid": 10.327, "dn_mid": 7.797, "up_slope": -0.532, "dn_slope": 0.189, "drop_pos": 0.655, "drop_width": 0.51} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00078
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.884, "load_range": 1.448, "roughness": 0.018, "up_mid": 6.578, "dn_mid": 5.496, "up_slope": -0.142, "dn_slope": -0.828, "drop_pos": 0.28, "drop_width": 0.785} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00079
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.466, "load_range": 3.465, "roughness": 0.015, "up_mid": 9.483, "dn_mid": 6.922, "up_slope": -1.755, "dn_slope": 0.727, "drop_pos": 1.0, "drop_width": 0.11} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00080
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.579, "load_range": 1.182, "roughness": 0.008, "up_mid": 5.125, "dn_mid": 4.086, "up_slope": -0.286, "dn_slope": 0.186, "drop_pos": 0.97, "drop_width": 0.23} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00081
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.944, "load_range": 4.442, "roughness": 0.053, "up_mid": 11.492, "dn_mid": 7.607, "up_slope": -1.499, "dn_slope": -0.313, "drop_pos": 0.815, "drop_width": 0.695} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00082
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.274, "load_range": 2.448, "roughness": 0.046, "up_mid": 6.72, "dn_mid": 4.714, "up_slope": -0.741, "dn_slope": 0.344, "drop_pos": 0.855, "drop_width": 0.23} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00083
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.162, "load_range": 3.43, "roughness": 0.011, "up_mid": 5.78, "dn_mid": 2.907, "up_slope": -1.253, "dn_slope": 0.601, "drop_pos": 0.99, "drop_width": 0.185} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00084
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.791, "load_range": 2.818, "roughness": 0.027, "up_mid": 6.367, "dn_mid": 4.804, "up_slope": -0.56, "dn_slope": 1.155, "drop_pos": 0.99, "drop_width": 0.13} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00085
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.393, "load_range": 2.314, "roughness": 0.029, "up_mid": 5.49, "dn_mid": 3.784, "up_slope": -0.211, "dn_slope": 0.815, "drop_pos": 0.965, "drop_width": 0.13} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00086
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.684, "load_range": 3.428, "roughness": 0.037, "up_mid": 6.95, "dn_mid": 4.158, "up_slope": -0.958, "dn_slope": 0.67, "drop_pos": 0.96, "drop_width": 0.12} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00087
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.687, "load_range": 2.78, "roughness": 0.028, "up_mid": 6.063, "dn_mid": 3.893, "up_slope": -0.991, "dn_slope": 0.45, "drop_pos": 0.955, "drop_width": 0.13} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00088
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.422, "load_range": 2.393, "roughness": 0.061, "up_mid": 5.648, "dn_mid": 3.835, "up_slope": -0.414, "dn_slope": 0.375, "drop_pos": 0.95, "drop_width": 0.21} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00089
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.964, "load_range": 1.847, "roughness": 0.049, "up_mid": 5.739, "dn_mid": 4.208, "up_slope": -0.35, "dn_slope": -0.692, "drop_pos": 0.44, "drop_width": 0.76} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00090
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.34, "load_range": 3.72, "roughness": 0.038, "up_mid": 10.496, "dn_mid": 7.377, "up_slope": -1.264, "dn_slope": 0.529, "drop_pos": 0.95, "drop_width": 0.18} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00091
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.971, "load_range": 3.127, "roughness": 0.008, "up_mid": 6.438, "dn_mid": 3.779, "up_slope": -0.401, "dn_slope": 0.76, "drop_pos": 0.955, "drop_width": 0.215} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00092
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.45, "load_range": 4.78, "roughness": 0.033, "up_mid": 10.888, "dn_mid": 6.788, "up_slope": -0.518, "dn_slope": 1.019, "drop_pos": 0.965, "drop_width": 0.155} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00093
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.109, "load_range": 4.106, "roughness": 0.007, "up_mid": 12.412, "dn_mid": 8.919, "up_slope": -0.618, "dn_slope": 0.968, "drop_pos": 0.96, "drop_width": 0.215} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00094
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.878, "load_range": 5.4, "roughness": 0.033, "up_mid": 13.266, "dn_mid": 8.771, "up_slope": -1.844, "dn_slope": 0.912, "drop_pos": 0.975, "drop_width": 0.16} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00095
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.327, "load_range": 4.241, "roughness": 0.019, "up_mid": 12.409, "dn_mid": 8.858, "up_slope": -0.531, "dn_slope": 1.034, "drop_pos": 0.965, "drop_width": 0.18} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00096
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.017, "load_range": 2.35, "roughness": 0.019, "up_mid": 5.823, "dn_mid": 3.989, "up_slope": -1.072, "dn_slope": 0.331, "drop_pos": 0.945, "drop_width": 0.125} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00097
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.504, "load_range": 2.13, "roughness": 0.027, "up_mid": 9.727, "dn_mid": 7.872, "up_slope": -0.513, "dn_slope": -0.147, "drop_pos": 0.565, "drop_width": 0.47} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00098
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.361, "load_range": 2.811, "roughness": 0.031, "up_mid": 6.455, "dn_mid": 4.029, "up_slope": -0.968, "dn_slope": 0.336, "drop_pos": 0.95, "drop_width": 0.2} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00099
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.021, "load_range": 1.982, "roughness": 0.026, "up_mid": 3.692, "dn_mid": 2.046, "up_slope": -0.6, "dn_slope": 0.4, "drop_pos": 0.99, "drop_width": 0.185} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
