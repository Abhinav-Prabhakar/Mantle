# L8 dyno_expert_annotation - batch 005 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_005.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00100 .. L8-00124 (each has an `item_id` you must echo).

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

### item_id: L8-00100
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.171, "load_range": 2.155, "roughness": 0.009, "up_mid": 10.257, "dn_mid": 8.332, "up_slope": -0.249, "dn_slope": 0.371, "drop_pos": 0.965, "drop_width": 0.195} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00101
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.688, "load_range": 5.569, "roughness": 0.022, "up_mid": 9.834, "dn_mid": 5.079, "up_slope": -1.246, "dn_slope": 1.123, "drop_pos": 0.965, "drop_width": 0.205} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00102
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.039, "load_range": 5.035, "roughness": 0.014, "up_mid": 11.652, "dn_mid": 7.507, "up_slope": -1.677, "dn_slope": 1.047, "drop_pos": 0.99, "drop_width": 0.175} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00103
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.158, "load_range": 2.148, "roughness": 0.019, "up_mid": 6.62, "dn_mid": 4.652, "up_slope": -0.136, "dn_slope": 0.272, "drop_pos": 0.945, "drop_width": 0.14} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00104
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.269, "load_range": 1.444, "roughness": 0.006, "up_mid": 7.195, "dn_mid": 5.895, "up_slope": -0.183, "dn_slope": 0.222, "drop_pos": 0.955, "drop_width": 0.175} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00105
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.586, "load_range": 2.841, "roughness": 0.024, "up_mid": 5.408, "dn_mid": 2.987, "up_slope": -0.451, "dn_slope": 0.58, "drop_pos": 0.965, "drop_width": 0.17} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00106
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.193, "load_range": 0.659, "roughness": 0.011, "up_mid": 6.721, "dn_mid": 6.254, "up_slope": -0.25, "dn_slope": 0.187, "drop_pos": 1.0, "drop_width": 0.13} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00107
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.34, "load_range": 2.195, "roughness": 0.044, "up_mid": 6.862, "dn_mid": 5.65, "up_slope": -0.893, "dn_slope": 0.591, "drop_pos": 0.98, "drop_width": 0.095} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00108
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.191, "load_range": 2.811, "roughness": 0.033, "up_mid": 11.576, "dn_mid": 9.504, "up_slope": -1.089, "dn_slope": 0.448, "drop_pos": 0.96, "drop_width": 0.085} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00109
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.498, "load_range": 4.796, "roughness": 0.039, "up_mid": 9.489, "dn_mid": 5.578, "up_slope": -1.108, "dn_slope": 0.527, "drop_pos": 0.955, "drop_width": 0.195} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00110
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.43, "load_range": 3.41, "roughness": 0.035, "up_mid": 5.918, "dn_mid": 3.349, "up_slope": -0.436, "dn_slope": 1.194, "drop_pos": 0.97, "drop_width": 0.165} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00111
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.974, "load_range": 2.095, "roughness": 0.027, "up_mid": 6.516, "dn_mid": 4.747, "up_slope": -0.273, "dn_slope": 0.313, "drop_pos": 0.96, "drop_width": 0.15} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00112
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.009, "load_range": 4.008, "roughness": 0.033, "up_mid": 7.276, "dn_mid": 3.738, "up_slope": -0.692, "dn_slope": 0.513, "drop_pos": 0.955, "drop_width": 0.215} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00113
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.3, "load_range": 3.147, "roughness": 0.015, "up_mid": 10.058, "dn_mid": 7.752, "up_slope": -0.553, "dn_slope": 1.057, "drop_pos": 0.985, "drop_width": 0.125} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00114
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.265, "load_range": 3.061, "roughness": 0.012, "up_mid": 9.643, "dn_mid": 7.566, "up_slope": -1.623, "dn_slope": 0.732, "drop_pos": 1.0, "drop_width": 0.075} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00115
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.521, "load_range": 4.007, "roughness": 0.043, "up_mid": 7.399, "dn_mid": 4.055, "up_slope": -0.682, "dn_slope": 0.982, "drop_pos": 0.825, "drop_width": 0.245} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00116
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.515, "load_range": 1.881, "roughness": 0.008, "up_mid": 8.056, "dn_mid": 6.315, "up_slope": -0.262, "dn_slope": 0.136, "drop_pos": 0.675, "drop_width": 0.38} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00117
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.207, "load_range": 1.734, "roughness": 0.027, "up_mid": 5.728, "dn_mid": 4.306, "up_slope": -0.18, "dn_slope": 0.328, "drop_pos": 0.975, "drop_width": 0.125} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00118
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.038, "load_range": 1.917, "roughness": 0.021, "up_mid": 5.016, "dn_mid": 3.154, "up_slope": -0.071, "dn_slope": 0.083, "drop_pos": 0.93, "drop_width": 0.14} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00119
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.536, "load_range": 1.358, "roughness": 0.002, "up_mid": 2.592, "dn_mid": 1.486, "up_slope": -0.252, "dn_slope": 0.383, "drop_pos": 0.985, "drop_width": 0.19} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00120
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.357, "load_range": 2.253, "roughness": 0.009, "up_mid": 6.152, "dn_mid": 4.154, "up_slope": -0.561, "dn_slope": 0.189, "drop_pos": 0.62, "drop_width": 0.675} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00121
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.963, "load_range": 5.835, "roughness": 0.041, "up_mid": 11.0, "dn_mid": 6.368, "up_slope": -2.104, "dn_slope": 1.031, "drop_pos": 0.965, "drop_width": 0.145} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00122
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.775, "load_range": 2.115, "roughness": 0.044, "up_mid": 9.94, "dn_mid": 8.559, "up_slope": -0.823, "dn_slope": 0.092, "drop_pos": 0.955, "drop_width": 0.935} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00123
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.06, "load_range": 1.128, "roughness": 0.01, "up_mid": 4.5, "dn_mid": 3.596, "up_slope": -0.361, "dn_slope": 0.06, "drop_pos": 0.96, "drop_width": 0.075} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00124
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.66, "load_range": 1.876, "roughness": 0.015, "up_mid": 6.885, "dn_mid": 5.147, "up_slope": -0.116, "dn_slope": 0.227, "drop_pos": 0.96, "drop_width": 0.11} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
