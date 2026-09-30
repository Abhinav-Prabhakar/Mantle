# L8 dyno_expert_annotation - batch 012 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_012.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00275 .. L8-00299 (each has an `item_id` you must echo).

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

### item_id: L8-00275
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.931, "load_range": 2.615, "roughness": 0.044, "up_mid": 5.876, "dn_mid": 3.49, "up_slope": -0.291, "dn_slope": -0.492, "drop_pos": 0.66, "drop_width": 0.655} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00276
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.391, "load_range": 7.166, "roughness": 0.028, "up_mid": 12.837, "dn_mid": 6.804, "up_slope": -1.57, "dn_slope": 1.556, "drop_pos": 0.97, "drop_width": 0.19} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00277
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.386, "load_range": 2.364, "roughness": 0.008, "up_mid": 8.948, "dn_mid": 6.783, "up_slope": -0.31, "dn_slope": 0.16, "drop_pos": 0.665, "drop_width": 0.53} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00278
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.508, "load_range": 2.242, "roughness": 0.013, "up_mid": 8.464, "dn_mid": 6.618, "up_slope": -0.693, "dn_slope": 0.341, "drop_pos": 0.96, "drop_width": 0.13} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00279
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.951, "load_range": 3.487, "roughness": 0.042, "up_mid": 6.124, "dn_mid": 3.064, "up_slope": -0.961, "dn_slope": 0.434, "drop_pos": 0.89, "drop_width": 0.28} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00280
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.101, "load_range": 0.844, "roughness": 0.003, "up_mid": 4.593, "dn_mid": 3.833, "up_slope": -0.142, "dn_slope": 0.123, "drop_pos": 0.945, "drop_width": 0.265} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00281
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.601, "load_range": 1.978, "roughness": 0.011, "up_mid": 7.512, "dn_mid": 5.66, "up_slope": -0.144, "dn_slope": 0.193, "drop_pos": 0.95, "drop_width": 0.13} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00282
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.92, "load_range": 3.699, "roughness": 0.075, "up_mid": 8.609, "dn_mid": 5.736, "up_slope": -0.477, "dn_slope": 0.587, "drop_pos": 0.95, "drop_width": 0.245} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00283
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.941, "load_range": 2.34, "roughness": 0.02, "up_mid": 6.9, "dn_mid": 4.706, "up_slope": -0.223, "dn_slope": 0.18, "drop_pos": 0.955, "drop_width": 0.1} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00284
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.433, "load_range": 4.111, "roughness": 0.036, "up_mid": 8.386, "dn_mid": 5.703, "up_slope": -0.734, "dn_slope": 1.71, "drop_pos": 0.99, "drop_width": 0.125} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00285
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.383, "load_range": 3.839, "roughness": 0.022, "up_mid": 8.611, "dn_mid": 5.25, "up_slope": -0.674, "dn_slope": 0.678, "drop_pos": 0.96, "drop_width": 0.185} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00286
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.684, "load_range": 1.391, "roughness": 0.008, "up_mid": 5.099, "dn_mid": 3.767, "up_slope": -0.127, "dn_slope": -0.166, "drop_pos": 0.57, "drop_width": 0.26} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00287
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.69, "load_range": 1.997, "roughness": 0.042, "up_mid": 5.365, "dn_mid": 4.344, "up_slope": -0.285, "dn_slope": 0.866, "drop_pos": 0.985, "drop_width": 0.115} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00288
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.55, "load_range": 2.183, "roughness": 0.011, "up_mid": 6.895, "dn_mid": 4.939, "up_slope": -0.272, "dn_slope": 0.254, "drop_pos": 0.95, "drop_width": 0.15} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00289
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.087, "load_range": 2.058, "roughness": 0.009, "up_mid": 7.71, "dn_mid": 5.799, "up_slope": -0.136, "dn_slope": 0.247, "drop_pos": 0.745, "drop_width": 0.35} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00290
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.488, "load_range": 3.15, "roughness": 0.003, "up_mid": 5.128, "dn_mid": 2.383, "up_slope": -0.386, "dn_slope": 0.684, "drop_pos": 0.945, "drop_width": 0.255} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00291
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.96, "load_range": 7.224, "roughness": 0.028, "up_mid": 10.904, "dn_mid": 4.825, "up_slope": -1.287, "dn_slope": 1.694, "drop_pos": 0.97, "drop_width": 0.195} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00292
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.281, "load_range": 1.823, "roughness": 0.022, "up_mid": 6.866, "dn_mid": 5.302, "up_slope": -0.129, "dn_slope": -0.87, "drop_pos": 0.32, "drop_width": 0.745} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00293
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.744, "load_range": 2.123, "roughness": 0.035, "up_mid": 7.899, "dn_mid": 6.467, "up_slope": -0.619, "dn_slope": 0.529, "drop_pos": 0.965, "drop_width": 0.075} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00294
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.431, "load_range": 3.542, "roughness": 0.059, "up_mid": 9.406, "dn_mid": 6.881, "up_slope": -0.555, "dn_slope": 0.775, "drop_pos": 0.975, "drop_width": 0.175} (and the true class plunger_sticking for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00295
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.669, "load_range": 3.692, "roughness": 0.018, "up_mid": 8.145, "dn_mid": 4.904, "up_slope": -0.742, "dn_slope": 0.512, "drop_pos": 0.915, "drop_width": 0.19} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00296
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 3.11, "load_range": 5.56, "roughness": 0.049, "up_mid": 13.025, "dn_mid": 7.989, "up_slope": -1.421, "dn_slope": -0.296, "drop_pos": 0.85, "drop_width": 0.725} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00297
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.856, "load_range": 3.467, "roughness": 0.009, "up_mid": 7.464, "dn_mid": 4.609, "up_slope": -0.874, "dn_slope": 0.793, "drop_pos": 0.975, "drop_width": 0.17} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00298
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.141, "load_range": 5.205, "roughness": 0.046, "up_mid": 11.141, "dn_mid": 6.722, "up_slope": -1.307, "dn_slope": 0.955, "drop_pos": 0.8, "drop_width": 0.25} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00299
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.684, "load_range": 3.003, "roughness": 0.03, "up_mid": 6.097, "dn_mid": 3.417, "up_slope": -0.262, "dn_slope": 0.47, "drop_pos": 0.96, "drop_width": 0.155} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
