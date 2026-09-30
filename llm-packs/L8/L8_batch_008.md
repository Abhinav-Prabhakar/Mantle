# L8 dyno_expert_annotation - batch 008 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_008.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00175 .. L8-00199 (each has an `item_id` you must echo).

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

### item_id: L8-00175
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.728, "load_range": 5.009, "roughness": 0.019, "up_mid": 11.203, "dn_mid": 6.651, "up_slope": -1.216, "dn_slope": 0.544, "drop_pos": 0.75, "drop_width": 0.415} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00176
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.54, "load_range": 1.751, "roughness": 0.012, "up_mid": 4.737, "dn_mid": 3.746, "up_slope": -0.492, "dn_slope": 0.616, "drop_pos": 0.995, "drop_width": 0.105} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00177
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.413, "load_range": 5.45, "roughness": 0.047, "up_mid": 9.865, "dn_mid": 5.242, "up_slope": -2.218, "dn_slope": -0.01, "drop_pos": 0.89, "drop_width": 0.76} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00178
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.051, "load_range": 1.933, "roughness": 0.03, "up_mid": 4.982, "dn_mid": 3.305, "up_slope": -0.151, "dn_slope": 0.193, "drop_pos": 0.95, "drop_width": 0.135} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00179
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.732, "load_range": 3.713, "roughness": 0.041, "up_mid": 10.28, "dn_mid": 6.983, "up_slope": -0.62, "dn_slope": 0.192, "drop_pos": 0.945, "drop_width": 0.275} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00180
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.915, "load_range": 2.122, "roughness": 0.015, "up_mid": 7.615, "dn_mid": 5.76, "up_slope": -0.437, "dn_slope": 0.332, "drop_pos": 0.96, "drop_width": 0.145} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00181
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.539, "load_range": 5.515, "roughness": 0.011, "up_mid": 10.604, "dn_mid": 6.604, "up_slope": -1.821, "dn_slope": 1.665, "drop_pos": 1.0, "drop_width": 0.105} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00182
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.89, "load_range": 2.07, "roughness": 0.006, "up_mid": 5.481, "dn_mid": 3.526, "up_slope": -0.17, "dn_slope": -0.059, "drop_pos": 0.665, "drop_width": 0.565} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00183
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.995, "load_range": 1.81, "roughness": 0.017, "up_mid": 4.899, "dn_mid": 3.555, "up_slope": -0.524, "dn_slope": 0.428, "drop_pos": 0.985, "drop_width": 0.095} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00184
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.895, "load_range": 2.912, "roughness": 0.03, "up_mid": 6.247, "dn_mid": 3.964, "up_slope": -0.364, "dn_slope": 0.816, "drop_pos": 0.96, "drop_width": 0.13} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00185
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.183, "load_range": 2.66, "roughness": 0.023, "up_mid": 11.295, "dn_mid": 9.246, "up_slope": -0.345, "dn_slope": -0.607, "drop_pos": 0.715, "drop_width": 0.85} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00186
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.099, "load_range": 4.281, "roughness": 0.028, "up_mid": 11.538, "dn_mid": 7.719, "up_slope": -0.979, "dn_slope": 0.598, "drop_pos": 0.955, "drop_width": 0.19} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00187
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.647, "load_range": 3.313, "roughness": 0.046, "up_mid": 8.254, "dn_mid": 5.501, "up_slope": -0.605, "dn_slope": -0.178, "drop_pos": 0.87, "drop_width": 0.825} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00188
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.778, "load_range": 1.797, "roughness": 0.007, "up_mid": 5.891, "dn_mid": 4.419, "up_slope": -0.388, "dn_slope": 0.4, "drop_pos": 0.96, "drop_width": 0.13} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00189
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.366, "load_range": 1.7, "roughness": 0.01, "up_mid": 8.13, "dn_mid": 6.521, "up_slope": -0.237, "dn_slope": -0.024, "drop_pos": 0.595, "drop_width": 0.37} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00190
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.645, "load_range": 2.117, "roughness": 0.018, "up_mid": 8.19, "dn_mid": 6.556, "up_slope": -0.163, "dn_slope": 0.624, "drop_pos": 0.96, "drop_width": 0.09} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00191
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.699, "load_range": 5.65, "roughness": 0.023, "up_mid": 12.465, "dn_mid": 7.799, "up_slope": -1.308, "dn_slope": 1.269, "drop_pos": 0.97, "drop_width": 0.16} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00192
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.283, "load_range": 2.393, "roughness": 0.009, "up_mid": 5.778, "dn_mid": 3.542, "up_slope": -0.363, "dn_slope": -0.135, "drop_pos": 0.595, "drop_width": 0.53} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00193
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.392, "load_range": 2.517, "roughness": 0.033, "up_mid": 5.514, "dn_mid": 3.165, "up_slope": -0.301, "dn_slope": 0.205, "drop_pos": 0.935, "drop_width": 0.155} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00194
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.73, "load_range": 3.184, "roughness": 0.015, "up_mid": 8.606, "dn_mid": 5.736, "up_slope": -1.093, "dn_slope": -0.343, "drop_pos": 0.52, "drop_width": 0.61} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00195
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.111, "load_range": 4.752, "roughness": 0.035, "up_mid": 13.838, "dn_mid": 9.543, "up_slope": -0.995, "dn_slope": 0.585, "drop_pos": 0.955, "drop_width": 0.2} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00196
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.851, "load_range": 3.478, "roughness": 0.05, "up_mid": 12.032, "dn_mid": 9.566, "up_slope": -1.785, "dn_slope": 0.463, "drop_pos": 0.82, "drop_width": 0.33} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00197
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.31, "load_range": 3.403, "roughness": 0.01, "up_mid": 11.325, "dn_mid": 9.838, "up_slope": -1.076, "dn_slope": 1.713, "drop_pos": 1.0, "drop_width": 0.025} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00198
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.319, "load_range": 2.051, "roughness": 0.019, "up_mid": 6.559, "dn_mid": 4.9, "up_slope": -0.538, "dn_slope": 0.409, "drop_pos": 0.965, "drop_width": 0.105} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00199
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.302, "load_range": 2.501, "roughness": 0.017, "up_mid": 12.065, "dn_mid": 9.852, "up_slope": -0.355, "dn_slope": 0.382, "drop_pos": 0.965, "drop_width": 0.145} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
