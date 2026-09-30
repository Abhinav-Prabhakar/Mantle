# L8 dyno_expert_annotation - batch 011 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_011.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00250 .. L8-00274 (each has an `item_id` you must echo).

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

### item_id: L8-00250
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.966, "load_range": 4.092, "roughness": 0.031, "up_mid": 11.447, "dn_mid": 8.379, "up_slope": -1.47, "dn_slope": 0.952, "drop_pos": 0.98, "drop_width": 0.12} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00251
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.665, "load_range": 1.78, "roughness": 0.032, "up_mid": 4.928, "dn_mid": 3.93, "up_slope": -0.221, "dn_slope": 0.721, "drop_pos": 0.97, "drop_width": 0.125} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00252
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.412, "load_range": 2.049, "roughness": 0.012, "up_mid": 10.642, "dn_mid": 8.797, "up_slope": -0.345, "dn_slope": 0.201, "drop_pos": 0.96, "drop_width": 0.095} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00253
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.198, "load_range": 4.145, "roughness": 0.021, "up_mid": 10.39, "dn_mid": 7.496, "up_slope": -2.504, "dn_slope": 0.781, "drop_pos": 1.0, "drop_width": 0.1} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00254
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.477, "load_range": 2.837, "roughness": 0.041, "up_mid": 6.684, "dn_mid": 4.507, "up_slope": -1.128, "dn_slope": 0.3, "drop_pos": 0.92, "drop_width": 0.115} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00255
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.574, "load_range": 2.079, "roughness": 0.017, "up_mid": 7.279, "dn_mid": 5.346, "up_slope": -0.13, "dn_slope": 0.246, "drop_pos": 0.95, "drop_width": 0.15} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00256
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.63, "load_range": 2.243, "roughness": 0.018, "up_mid": 5.659, "dn_mid": 3.581, "up_slope": -0.213, "dn_slope": 0.242, "drop_pos": 0.95, "drop_width": 0.14} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00257
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.794, "load_range": 3.416, "roughness": 0.037, "up_mid": 7.824, "dn_mid": 5.569, "up_slope": -0.649, "dn_slope": 1.34, "drop_pos": 0.99, "drop_width": 0.11} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00258
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.193, "load_range": 1.599, "roughness": 0.011, "up_mid": 6.715, "dn_mid": 5.389, "up_slope": -0.536, "dn_slope": 0.135, "drop_pos": 0.96, "drop_width": 0.085} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00259
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.453, "load_range": 2.762, "roughness": 0.023, "up_mid": 5.857, "dn_mid": 3.619, "up_slope": -0.827, "dn_slope": 0.595, "drop_pos": 1.0, "drop_width": 0.2} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00260
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.069, "load_range": 3.584, "roughness": 0.02, "up_mid": 8.586, "dn_mid": 5.715, "up_slope": -0.588, "dn_slope": 0.957, "drop_pos": 0.97, "drop_width": 0.16} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00261
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.96, "load_range": 2.866, "roughness": 0.025, "up_mid": 5.938, "dn_mid": 3.991, "up_slope": -0.705, "dn_slope": 0.907, "drop_pos": 0.985, "drop_width": 0.125} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00262
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.836, "load_range": 4.564, "roughness": 0.053, "up_mid": 6.949, "dn_mid": 2.985, "up_slope": -1.33, "dn_slope": 0.733, "drop_pos": 0.98, "drop_width": 0.225} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00263
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.602, "load_range": 1.386, "roughness": 0.014, "up_mid": 4.983, "dn_mid": 3.732, "up_slope": -0.304, "dn_slope": 0.089, "drop_pos": 0.95, "drop_width": 0.095} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00264
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.404, "load_range": 1.647, "roughness": 0.019, "up_mid": 5.318, "dn_mid": 4.178, "up_slope": -0.1, "dn_slope": 0.58, "drop_pos": 0.955, "drop_width": 0.115} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00265
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.19, "load_range": 3.426, "roughness": 0.042, "up_mid": 7.465, "dn_mid": 4.919, "up_slope": -1.101, "dn_slope": 0.866, "drop_pos": 0.97, "drop_width": 0.135} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00266
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.578, "load_range": 3.274, "roughness": 0.019, "up_mid": 8.873, "dn_mid": 5.903, "up_slope": -0.785, "dn_slope": 0.348, "drop_pos": 0.95, "drop_width": 0.205} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00267
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.138, "load_range": 3.685, "roughness": 0.019, "up_mid": 10.549, "dn_mid": 7.434, "up_slope": -1.144, "dn_slope": 0.528, "drop_pos": 0.945, "drop_width": 0.14} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00268
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.563, "load_range": 2.211, "roughness": 0.038, "up_mid": 6.267, "dn_mid": 4.49, "up_slope": -0.294, "dn_slope": 0.302, "drop_pos": 0.95, "drop_width": 0.145} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00269
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.355, "load_range": 1.445, "roughness": 0.008, "up_mid": 5.369, "dn_mid": 4.365, "up_slope": -0.285, "dn_slope": 0.49, "drop_pos": 0.985, "drop_width": 0.115} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00270
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.953, "load_range": 2.533, "roughness": 0.051, "up_mid": 6.304, "dn_mid": 4.261, "up_slope": -0.552, "dn_slope": -0.818, "drop_pos": 0.285, "drop_width": 0.73} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00271
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.45, "load_range": 2.258, "roughness": 0.014, "up_mid": 5.311, "dn_mid": 3.337, "up_slope": -0.851, "dn_slope": -0.264, "drop_pos": 0.54, "drop_width": 0.645} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00272
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.098, "load_range": 1.766, "roughness": 0.022, "up_mid": 5.31, "dn_mid": 3.686, "up_slope": -0.095, "dn_slope": 0.15, "drop_pos": 0.765, "drop_width": 0.34} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00273
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.342, "load_range": 3.172, "roughness": 0.015, "up_mid": 10.749, "dn_mid": 8.227, "up_slope": -1.93, "dn_slope": 0.352, "drop_pos": 1.0, "drop_width": 0.485} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00274
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.854, "load_range": 3.463, "roughness": 0.049, "up_mid": 6.678, "dn_mid": 3.63, "up_slope": -0.622, "dn_slope": -0.328, "drop_pos": 0.865, "drop_width": 0.695} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
