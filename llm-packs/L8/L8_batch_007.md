# L8 dyno_expert_annotation - batch 007 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_007.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00150 .. L8-00174 (each has an `item_id` you must echo).

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

### item_id: L8-00150
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.678, "load_range": 1.416, "roughness": 0.014, "up_mid": 4.753, "dn_mid": 3.393, "up_slope": -0.012, "dn_slope": 0.081, "drop_pos": 0.94, "drop_width": 0.13} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00151
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.002, "load_range": 5.837, "roughness": 0.042, "up_mid": 12.928, "dn_mid": 7.935, "up_slope": -1.91, "dn_slope": 0.894, "drop_pos": 0.93, "drop_width": 0.225} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00152
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.074, "load_range": 2.951, "roughness": 0.029, "up_mid": 7.319, "dn_mid": 4.706, "up_slope": -0.313, "dn_slope": 0.411, "drop_pos": 0.745, "drop_width": 0.39} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00153
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.539, "load_range": 1.981, "roughness": 0.012, "up_mid": 5.173, "dn_mid": 3.379, "up_slope": -0.249, "dn_slope": 0.282, "drop_pos": 0.96, "drop_width": 0.185} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00154
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.758, "load_range": 4.039, "roughness": 0.04, "up_mid": 6.758, "dn_mid": 3.265, "up_slope": -0.976, "dn_slope": -0.042, "drop_pos": 0.745, "drop_width": 0.53} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00155
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.958, "load_range": 1.481, "roughness": 0.02, "up_mid": 7.68, "dn_mid": 6.55, "up_slope": -0.155, "dn_slope": -0.92, "drop_pos": 0.29, "drop_width": 0.675} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00156
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.086, "load_range": 2.562, "roughness": 0.027, "up_mid": 12.073, "dn_mid": 9.873, "up_slope": -0.037, "dn_slope": 0.375, "drop_pos": 0.95, "drop_width": 0.29} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00157
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.97, "load_range": 5.584, "roughness": 0.034, "up_mid": 12.613, "dn_mid": 7.633, "up_slope": -0.598, "dn_slope": 0.956, "drop_pos": 0.96, "drop_width": 0.2} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00158
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.517, "load_range": 3.553, "roughness": 0.052, "up_mid": 8.974, "dn_mid": 6.017, "up_slope": -1.258, "dn_slope": -0.416, "drop_pos": 0.825, "drop_width": 0.755} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00159
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.929, "load_range": 4.257, "roughness": 0.012, "up_mid": 12.071, "dn_mid": 8.61, "up_slope": -1.211, "dn_slope": 0.981, "drop_pos": 0.985, "drop_width": 0.165} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00160
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.217, "load_range": 1.036, "roughness": 0.001, "up_mid": 1.591, "dn_mid": 0.688, "up_slope": -0.098, "dn_slope": 0.239, "drop_pos": 0.935, "drop_width": 0.27} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00161
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.591, "load_range": 2.208, "roughness": 0.008, "up_mid": 8.634, "dn_mid": 6.658, "up_slope": -0.369, "dn_slope": 0.333, "drop_pos": 0.955, "drop_width": 0.175} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00162
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.561, "load_range": 1.947, "roughness": 0.007, "up_mid": 5.496, "dn_mid": 3.793, "up_slope": -0.356, "dn_slope": 0.354, "drop_pos": 0.955, "drop_width": 0.205} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00163
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.666, "load_range": 2.858, "roughness": 0.03, "up_mid": 7.632, "dn_mid": 5.046, "up_slope": -0.345, "dn_slope": 0.342, "drop_pos": 0.765, "drop_width": 0.34} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00164
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.327, "load_range": 1.447, "roughness": 0.002, "up_mid": 3.371, "dn_mid": 2.126, "up_slope": -0.162, "dn_slope": 0.35, "drop_pos": 0.95, "drop_width": 0.255} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00165
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.795, "load_range": 1.415, "roughness": 0.007, "up_mid": 5.346, "dn_mid": 4.185, "up_slope": -0.466, "dn_slope": 0.292, "drop_pos": 0.99, "drop_width": 0.17} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00166
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.321, "load_range": 1.598, "roughness": 0.027, "up_mid": 4.914, "dn_mid": 3.624, "up_slope": -0.23, "dn_slope": 0.228, "drop_pos": 0.95, "drop_width": 0.11} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00167
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.708, "load_range": 4.025, "roughness": 0.051, "up_mid": 6.866, "dn_mid": 3.729, "up_slope": -0.767, "dn_slope": 1.127, "drop_pos": 0.97, "drop_width": 0.175} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00168
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.552, "load_range": 2.21, "roughness": 0.011, "up_mid": 9.874, "dn_mid": 7.906, "up_slope": -0.588, "dn_slope": 0.028, "drop_pos": 0.595, "drop_width": 0.46} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00169
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.418, "load_range": 6.311, "roughness": 0.045, "up_mid": 11.757, "dn_mid": 6.539, "up_slope": -2.269, "dn_slope": 1.057, "drop_pos": 0.85, "drop_width": 0.34} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00170
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.527, "load_range": 2.321, "roughness": 0.023, "up_mid": 5.844, "dn_mid": 3.977, "up_slope": -0.168, "dn_slope": 0.546, "drop_pos": 0.975, "drop_width": 0.165} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00171
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.162, "load_range": 2.601, "roughness": 0.008, "up_mid": 8.397, "dn_mid": 6.173, "up_slope": -0.423, "dn_slope": 0.561, "drop_pos": 0.955, "drop_width": 0.19} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00172
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.675, "load_range": 5.936, "roughness": 0.03, "up_mid": 9.543, "dn_mid": 4.703, "up_slope": -0.831, "dn_slope": 1.659, "drop_pos": 0.97, "drop_width": 0.18} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00173
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.144, "load_range": 2.412, "roughness": 0.024, "up_mid": 5.268, "dn_mid": 2.983, "up_slope": -0.17, "dn_slope": 0.144, "drop_pos": 0.94, "drop_width": 0.135} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00174
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.451, "load_range": 4.594, "roughness": 0.009, "up_mid": 9.937, "dn_mid": 5.931, "up_slope": -1.206, "dn_slope": 0.89, "drop_pos": 0.945, "drop_width": 0.375} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
