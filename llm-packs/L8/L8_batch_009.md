# L8 dyno_expert_annotation - batch 009 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_009.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00200 .. L8-00224 (each has an `item_id` you must echo).

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

### item_id: L8-00200
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.313, "load_range": 5.02, "roughness": 0.033, "up_mid": 9.138, "dn_mid": 4.933, "up_slope": -0.935, "dn_slope": 1.11, "drop_pos": 0.97, "drop_width": 0.165} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00201
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.721, "load_range": 4.767, "roughness": 0.047, "up_mid": 13.202, "dn_mid": 9.609, "up_slope": -1.833, "dn_slope": 0.763, "drop_pos": 0.955, "drop_width": 0.1} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00202
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.685, "load_range": 2.718, "roughness": 0.006, "up_mid": 5.58, "dn_mid": 3.014, "up_slope": -0.464, "dn_slope": 0.048, "drop_pos": 0.85, "drop_width": 0.53} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00203
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.329, "load_range": 1.01, "roughness": 0.004, "up_mid": 3.524, "dn_mid": 2.617, "up_slope": -0.18, "dn_slope": 0.15, "drop_pos": 0.95, "drop_width": 0.26} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00204
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.154, "load_range": 2.187, "roughness": 0.039, "up_mid": 5.664, "dn_mid": 4.209, "up_slope": -0.268, "dn_slope": 0.829, "drop_pos": 0.965, "drop_width": 0.14} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00205
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.198, "load_range": 2.212, "roughness": 0.021, "up_mid": 7.287, "dn_mid": 5.35, "up_slope": -0.207, "dn_slope": 0.33, "drop_pos": 0.97, "drop_width": 0.15} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00206
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.507, "load_range": 2.906, "roughness": 0.016, "up_mid": 10.155, "dn_mid": 7.793, "up_slope": -1.068, "dn_slope": 0.447, "drop_pos": 0.94, "drop_width": 0.13} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00207
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.458, "load_range": 2.374, "roughness": 0.003, "up_mid": 2.765, "dn_mid": 0.671, "up_slope": -0.34, "dn_slope": 0.454, "drop_pos": 0.95, "drop_width": 0.26} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00208
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.185, "load_range": 2.872, "roughness": 0.049, "up_mid": 5.696, "dn_mid": 3.149, "up_slope": -0.471, "dn_slope": 0.408, "drop_pos": 0.74, "drop_width": 0.45} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00209
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.467, "load_range": 1.154, "roughness": 0.002, "up_mid": 2.966, "dn_mid": 1.972, "up_slope": -0.118, "dn_slope": 0.284, "drop_pos": 0.945, "drop_width": 0.255} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00210
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.776, "load_range": 2.335, "roughness": 0.043, "up_mid": 5.719, "dn_mid": 4.22, "up_slope": -0.985, "dn_slope": -0.328, "drop_pos": 0.15, "drop_width": 0.97} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00211
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.71, "load_range": 3.827, "roughness": 0.019, "up_mid": 10.291, "dn_mid": 7.88, "up_slope": -2.22, "dn_slope": 0.858, "drop_pos": 1.0, "drop_width": 0.07} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00212
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.972, "load_range": 1.709, "roughness": 0.013, "up_mid": 5.175, "dn_mid": 3.559, "up_slope": -0.115, "dn_slope": 0.145, "drop_pos": 0.945, "drop_width": 0.115} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00213
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.129, "load_range": 1.789, "roughness": 0.019, "up_mid": 10.547, "dn_mid": 8.944, "up_slope": -0.065, "dn_slope": 0.104, "drop_pos": 0.95, "drop_width": 0.21} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00214
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.795, "load_range": 1.679, "roughness": 0.002, "up_mid": 1.932, "dn_mid": 0.443, "up_slope": -0.214, "dn_slope": 0.311, "drop_pos": 0.94, "drop_width": 0.27} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00215
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.846, "load_range": 3.869, "roughness": 0.042, "up_mid": 6.386, "dn_mid": 3.014, "up_slope": -0.901, "dn_slope": -0.355, "drop_pos": 0.78, "drop_width": 0.57} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00216
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.082, "load_range": 3.028, "roughness": 0.01, "up_mid": 5.881, "dn_mid": 3.164, "up_slope": -0.512, "dn_slope": 0.347, "drop_pos": 0.72, "drop_width": 0.525} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00217
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.949, "load_range": 2.048, "roughness": 0.012, "up_mid": 9.038, "dn_mid": 7.311, "up_slope": -0.658, "dn_slope": 0.263, "drop_pos": 0.965, "drop_width": 0.145} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00218
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.091, "load_range": 3.069, "roughness": 0.005, "up_mid": 8.487, "dn_mid": 5.841, "up_slope": -0.5, "dn_slope": 0.677, "drop_pos": 0.96, "drop_width": 0.235} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00219
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.884, "load_range": 0.412, "roughness": 0.001, "up_mid": 4.486, "dn_mid": 4.153, "up_slope": -0.103, "dn_slope": 0.109, "drop_pos": 0.99, "drop_width": 0.17} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00220
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.247, "load_range": 3.656, "roughness": 0.022, "up_mid": 7.769, "dn_mid": 4.723, "up_slope": -0.908, "dn_slope": 0.779, "drop_pos": 0.97, "drop_width": 0.19} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00221
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.831, "load_range": 3.925, "roughness": 0.019, "up_mid": 4.621, "dn_mid": 1.291, "up_slope": -0.972, "dn_slope": 0.804, "drop_pos": 0.975, "drop_width": 0.215} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00222
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.941, "load_range": 1.768, "roughness": 0.005, "up_mid": 8.898, "dn_mid": 7.617, "up_slope": -0.398, "dn_slope": 0.626, "drop_pos": 0.995, "drop_width": 0.115} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00223
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.137, "load_range": 3.618, "roughness": 0.045, "up_mid": 6.386, "dn_mid": 3.629, "up_slope": -0.436, "dn_slope": 0.693, "drop_pos": 0.975, "drop_width": 0.3} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00224
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.659, "load_range": 7.429, "roughness": 0.032, "up_mid": 12.759, "dn_mid": 6.948, "up_slope": -1.475, "dn_slope": 2.09, "drop_pos": 0.98, "drop_width": 0.165} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
