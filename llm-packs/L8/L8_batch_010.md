# L8 dyno_expert_annotation - batch 010 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_010.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00225 .. L8-00249 (each has an `item_id` you must echo).

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

### item_id: L8-00225
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.664, "load_range": 2.904, "roughness": 0.02, "up_mid": 7.019, "dn_mid": 5.256, "up_slope": -1.151, "dn_slope": 0.754, "drop_pos": 0.995, "drop_width": 0.095} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00226
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.423, "load_range": 2.354, "roughness": 0.025, "up_mid": 6.636, "dn_mid": 4.596, "up_slope": -0.246, "dn_slope": 0.405, "drop_pos": 0.96, "drop_width": 0.14} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00227
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.205, "load_range": 3.283, "roughness": 0.027, "up_mid": 11.029, "dn_mid": 8.163, "up_slope": -0.683, "dn_slope": 0.473, "drop_pos": 0.96, "drop_width": 0.11} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00228
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.02, "load_range": 1.826, "roughness": 0.006, "up_mid": 5.716, "dn_mid": 4.114, "up_slope": -0.169, "dn_slope": 0.379, "drop_pos": 0.955, "drop_width": 0.205} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00229
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.709, "load_range": 3.837, "roughness": 0.043, "up_mid": 9.411, "dn_mid": 6.58, "up_slope": -0.581, "dn_slope": 1.305, "drop_pos": 0.98, "drop_width": 0.12} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00230
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.289, "load_range": 2.181, "roughness": 0.011, "up_mid": 11.192, "dn_mid": 9.182, "up_slope": -0.291, "dn_slope": 0.192, "drop_pos": 0.955, "drop_width": 0.11} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00231
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.814, "load_range": 2.283, "roughness": 0.012, "up_mid": 5.185, "dn_mid": 3.132, "up_slope": -0.361, "dn_slope": 0.325, "drop_pos": 0.955, "drop_width": 0.185} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00232
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.633, "load_range": 1.826, "roughness": 0.007, "up_mid": 5.531, "dn_mid": 4.056, "up_slope": -0.627, "dn_slope": 0.394, "drop_pos": 1.0, "drop_width": 0.16} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00233
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.986, "load_range": 3.256, "roughness": 0.007, "up_mid": 4.658, "dn_mid": 1.785, "up_slope": -0.501, "dn_slope": 0.609, "drop_pos": 0.95, "drop_width": 0.26} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00234
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.921, "load_range": 3.29, "roughness": 0.026, "up_mid": 6.82, "dn_mid": 3.978, "up_slope": -0.482, "dn_slope": 0.642, "drop_pos": 0.965, "drop_width": 0.175} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00235
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.795, "load_range": 3.839, "roughness": 0.009, "up_mid": 9.326, "dn_mid": 6.03, "up_slope": -0.558, "dn_slope": 0.791, "drop_pos": 0.845, "drop_width": 0.4} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00236
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.795, "load_range": 2.584, "roughness": 0.01, "up_mid": 11.854, "dn_mid": 9.565, "up_slope": -0.6, "dn_slope": 0.389, "drop_pos": 0.955, "drop_width": 0.215} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00237
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.072, "load_range": 1.76, "roughness": 0.019, "up_mid": 9.041, "dn_mid": 7.512, "up_slope": -0.062, "dn_slope": 0.159, "drop_pos": 0.955, "drop_width": 0.235} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00238
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.018, "load_range": 2.011, "roughness": 0.012, "up_mid": 2.682, "dn_mid": 1.028, "up_slope": -0.509, "dn_slope": 0.488, "drop_pos": 0.985, "drop_width": 0.18} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00239
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.726, "load_range": 4.862, "roughness": 0.02, "up_mid": 9.576, "dn_mid": 5.735, "up_slope": -1.077, "dn_slope": 1.362, "drop_pos": 0.985, "drop_width": 0.16} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00240
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.753, "load_range": 7.105, "roughness": 0.038, "up_mid": 11.292, "dn_mid": 5.656, "up_slope": -1.81, "dn_slope": 1.844, "drop_pos": 0.99, "drop_width": 0.145} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00241
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.26, "load_range": 4.002, "roughness": 0.008, "up_mid": 10.773, "dn_mid": 7.295, "up_slope": -1.038, "dn_slope": 0.653, "drop_pos": 0.8, "drop_width": 0.43} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00242
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.309, "load_range": 1.213, "roughness": 0.002, "up_mid": 2.485, "dn_mid": 1.406, "up_slope": -0.159, "dn_slope": 0.216, "drop_pos": 0.94, "drop_width": 0.27} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00243
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.595, "load_range": 7.059, "roughness": 0.049, "up_mid": 13.388, "dn_mid": 7.742, "up_slope": -3.35, "dn_slope": 0.715, "drop_pos": 0.945, "drop_width": 0.38} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00244
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.143, "load_range": 1.022, "roughness": 0.006, "up_mid": 5.459, "dn_mid": 4.515, "up_slope": -0.179, "dn_slope": 0.1, "drop_pos": 0.955, "drop_width": 0.135} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00245
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.416, "load_range": 5.831, "roughness": 0.013, "up_mid": 12.266, "dn_mid": 6.98, "up_slope": -1.607, "dn_slope": 0.569, "drop_pos": 0.93, "drop_width": 0.48} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00246
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.548, "load_range": 0.423, "roughness": 0.002, "up_mid": 1.541, "dn_mid": 1.173, "up_slope": -0.097, "dn_slope": 0.078, "drop_pos": 0.97, "drop_width": 0.225} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00247
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.142, "load_range": 6.328, "roughness": 0.057, "up_mid": 12.834, "dn_mid": 7.283, "up_slope": -1.665, "dn_slope": 0.895, "drop_pos": 0.925, "drop_width": 0.185} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00248
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.942, "load_range": 6.227, "roughness": 0.049, "up_mid": 12.156, "dn_mid": 6.968, "up_slope": -1.104, "dn_slope": 1.547, "drop_pos": 0.91, "drop_width": 0.31} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00249
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.149, "load_range": 1.607, "roughness": 0.01, "up_mid": 6.359, "dn_mid": 5.124, "up_slope": -0.299, "dn_slope": 0.44, "drop_pos": 0.97, "drop_width": 0.115} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
