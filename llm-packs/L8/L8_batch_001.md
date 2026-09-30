# L8 dyno_expert_annotation - batch 001 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_001.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00000 .. L8-00024 (each has an `item_id` you must echo).

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

### item_id: L8-00000
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.924, "load_range": 0.802, "roughness": 0.002, "up_mid": 4.177, "dn_mid": 3.477, "up_slope": -0.129, "dn_slope": 0.156, "drop_pos": 0.955, "drop_width": 0.24} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00001
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.451, "load_range": 3.113, "roughness": 0.041, "up_mid": 7.083, "dn_mid": 4.75, "up_slope": -1.142, "dn_slope": 0.584, "drop_pos": 0.845, "drop_width": 0.295} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00002
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.036, "load_range": 1.482, "roughness": 0.023, "up_mid": 5.998, "dn_mid": 5.23, "up_slope": -0.078, "dn_slope": -0.744, "drop_pos": 0.175, "drop_width": 0.87} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00003
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.314, "load_range": 1.403, "roughness": 0.008, "up_mid": 4.905, "dn_mid": 3.548, "up_slope": -0.04, "dn_slope": -0.269, "drop_pos": 0.56, "drop_width": 0.485} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00004
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.387, "load_range": 3.436, "roughness": 0.018, "up_mid": 12.548, "dn_mid": 9.561, "up_slope": -0.452, "dn_slope": 0.677, "drop_pos": 0.96, "drop_width": 0.17} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00005
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.703, "load_range": 2.081, "roughness": 0.007, "up_mid": 9.964, "dn_mid": 8.319, "up_slope": -0.694, "dn_slope": 0.503, "drop_pos": 1.0, "drop_width": 0.15} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00006
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.459, "load_range": 2.642, "roughness": 0.032, "up_mid": 6.553, "dn_mid": 4.291, "up_slope": -0.468, "dn_slope": 0.369, "drop_pos": 0.965, "drop_width": 0.135} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00007
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.434, "load_range": 1.487, "roughness": 0.006, "up_mid": 5.635, "dn_mid": 4.28, "up_slope": -0.168, "dn_slope": -0.493, "drop_pos": 0.455, "drop_width": 0.635} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00008
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.652, "load_range": 2.56, "roughness": 0.017, "up_mid": 7.258, "dn_mid": 5.247, "up_slope": -0.54, "dn_slope": 0.676, "drop_pos": 0.98, "drop_width": 0.115} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00009
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.028, "load_range": 2.577, "roughness": 0.025, "up_mid": 5.739, "dn_mid": 3.607, "up_slope": -0.476, "dn_slope": 0.59, "drop_pos": 0.975, "drop_width": 0.15} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00010
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.699, "load_range": 1.874, "roughness": 0.008, "up_mid": 4.487, "dn_mid": 2.961, "up_slope": -0.353, "dn_slope": 0.481, "drop_pos": 0.97, "drop_width": 0.16} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00011
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.717, "load_range": 1.483, "roughness": 0.022, "up_mid": 5.515, "dn_mid": 4.092, "up_slope": -0.111, "dn_slope": -0.165, "drop_pos": 0.54, "drop_width": 0.3} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00012
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.471, "load_range": 3.381, "roughness": 0.038, "up_mid": 10.471, "dn_mid": 7.992, "up_slope": -1.403, "dn_slope": 0.353, "drop_pos": 1.0, "drop_width": 0.07} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00013
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.791, "load_range": 4.512, "roughness": 0.025, "up_mid": 10.831, "dn_mid": 6.662, "up_slope": -0.647, "dn_slope": 0.474, "drop_pos": 0.95, "drop_width": 0.165} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00014
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.797, "load_range": 3.017, "roughness": 0.008, "up_mid": 7.977, "dn_mid": 5.182, "up_slope": -0.252, "dn_slope": 0.18, "drop_pos": 0.75, "drop_width": 0.515} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00015
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.92, "load_range": 3.882, "roughness": 0.038, "up_mid": 8.59, "dn_mid": 5.424, "up_slope": -0.845, "dn_slope": 0.996, "drop_pos": 0.82, "drop_width": 0.245} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00016
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.243, "load_range": 1.569, "roughness": 0.014, "up_mid": 10.259, "dn_mid": 8.846, "up_slope": -0.343, "dn_slope": 0.135, "drop_pos": 0.96, "drop_width": 0.095} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00017
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.206, "load_range": 2.346, "roughness": 0.009, "up_mid": 2.646, "dn_mid": 0.582, "up_slope": -0.437, "dn_slope": 0.429, "drop_pos": 0.955, "drop_width": 0.25} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00018
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.127, "load_range": 3.164, "roughness": 0.011, "up_mid": 6.332, "dn_mid": 3.449, "up_slope": -0.4, "dn_slope": 0.401, "drop_pos": 0.8, "drop_width": 0.42} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00019
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.867, "load_range": 2.913, "roughness": 0.021, "up_mid": 8.934, "dn_mid": 6.469, "up_slope": -0.718, "dn_slope": 0.54, "drop_pos": 0.96, "drop_width": 0.18} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00020
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.791, "load_range": 2.529, "roughness": 0.013, "up_mid": 7.381, "dn_mid": 5.148, "up_slope": -0.547, "dn_slope": 0.269, "drop_pos": 0.95, "drop_width": 0.13} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00021
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.173, "load_range": 2.682, "roughness": 0.018, "up_mid": 8.528, "dn_mid": 6.188, "up_slope": -0.719, "dn_slope": 0.365, "drop_pos": 0.955, "drop_width": 0.175} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00022
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.825, "load_range": 1.749, "roughness": 0.013, "up_mid": 8.977, "dn_mid": 7.418, "up_slope": -0.306, "dn_slope": 0.233, "drop_pos": 0.965, "drop_width": 0.13} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00023
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.313, "load_range": 3.802, "roughness": 0.01, "up_mid": 8.051, "dn_mid": 4.539, "up_slope": -0.595, "dn_slope": 0.253, "drop_pos": 0.675, "drop_width": 0.5} (and the true class gas_interference for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00024
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.103, "load_range": 3.408, "roughness": 0.021, "up_mid": 8.974, "dn_mid": 5.921, "up_slope": -0.658, "dn_slope": 0.485, "drop_pos": 0.95, "drop_width": 0.175} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
