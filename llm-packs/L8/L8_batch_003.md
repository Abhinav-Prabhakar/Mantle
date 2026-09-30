# L8 dyno_expert_annotation - batch 003 (25 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 25 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L8/replies/L8_batch_003.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L8-00050 .. L8-00074 (each has an `item_id` you must echo).

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

### item_id: L8-00050
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.583, "load_range": 1.34, "roughness": 0.01, "up_mid": 5.078, "dn_mid": 3.907, "up_slope": -0.28, "dn_slope": 0.101, "drop_pos": 0.955, "drop_width": 0.095} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00051
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.908, "load_range": 1.317, "roughness": 0.017, "up_mid": 6.346, "dn_mid": 5.109, "up_slope": -0.057, "dn_slope": 0.084, "drop_pos": 0.72, "drop_width": 0.18} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00052
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.756, "load_range": 1.698, "roughness": 0.015, "up_mid": 5.195, "dn_mid": 3.618, "up_slope": -0.297, "dn_slope": 0.141, "drop_pos": 0.965, "drop_width": 0.14} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00053
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.202, "load_range": 2.161, "roughness": 0.012, "up_mid": 5.019, "dn_mid": 3.09, "up_slope": -0.449, "dn_slope": 0.319, "drop_pos": 0.955, "drop_width": 0.205} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00054
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.977, "load_range": 2.015, "roughness": 0.021, "up_mid": 7.63, "dn_mid": 6.12, "up_slope": -0.449, "dn_slope": 0.463, "drop_pos": 0.96, "drop_width": 0.095} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00055
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.279, "load_range": 2.334, "roughness": 0.036, "up_mid": 8.292, "dn_mid": 6.799, "up_slope": -0.777, "dn_slope": 0.629, "drop_pos": 0.975, "drop_width": 0.095} (and the true class standing_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00056
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.649, "load_range": 3.114, "roughness": 0.006, "up_mid": 7.84, "dn_mid": 5.31, "up_slope": -0.69, "dn_slope": 0.826, "drop_pos": 0.99, "drop_width": 0.175} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00057
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.75, "load_range": 3.072, "roughness": 0.03, "up_mid": 6.402, "dn_mid": 3.543, "up_slope": -0.293, "dn_slope": 0.308, "drop_pos": 0.95, "drop_width": 0.15} (and the true class excessive_friction for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00058
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.08, "load_range": 4.167, "roughness": 0.044, "up_mid": 12.108, "dn_mid": 8.589, "up_slope": -0.936, "dn_slope": 0.557, "drop_pos": 0.95, "drop_width": 0.205} (and the true class pump_off for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00059
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.156, "load_range": 2.264, "roughness": 0.015, "up_mid": 5.373, "dn_mid": 3.536, "up_slope": -0.368, "dn_slope": 0.464, "drop_pos": 0.97, "drop_width": 0.16} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00060
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.385, "load_range": 3.459, "roughness": 0.017, "up_mid": 6.742, "dn_mid": 3.751, "up_slope": -0.889, "dn_slope": 0.593, "drop_pos": 0.955, "drop_width": 0.195} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00061
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.237, "load_range": 3.54, "roughness": 0.019, "up_mid": 12.514, "dn_mid": 10.098, "up_slope": -1.008, "dn_slope": 1.014, "drop_pos": 0.985, "drop_width": 0.12} (and the true class normal for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00062
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.376, "load_range": 2.186, "roughness": 0.016, "up_mid": 6.11, "dn_mid": 4.688, "up_slope": -0.853, "dn_slope": 0.492, "drop_pos": 0.99, "drop_width": 0.105} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00063
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.339, "load_range": 1.635, "roughness": 0.004, "up_mid": 7.354, "dn_mid": 5.974, "up_slope": -0.217, "dn_slope": 0.419, "drop_pos": 0.965, "drop_width": 0.23} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00064
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.253, "load_range": 0.634, "roughness": 0.004, "up_mid": 3.12, "dn_mid": 2.573, "up_slope": -0.17, "dn_slope": 0.111, "drop_pos": 0.975, "drop_width": 0.22} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00065
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.501, "load_range": 1.331, "roughness": 0.002, "up_mid": 1.964, "dn_mid": 0.858, "up_slope": -0.284, "dn_slope": 0.331, "drop_pos": 0.98, "drop_width": 0.195} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00066
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.936, "load_range": 2.872, "roughness": 0.012, "up_mid": 6.786, "dn_mid": 4.369, "up_slope": -0.489, "dn_slope": 0.671, "drop_pos": 0.965, "drop_width": 0.19} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00067
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.909, "load_range": 2.481, "roughness": 0.009, "up_mid": 7.058, "dn_mid": 5.243, "up_slope": -0.59, "dn_slope": 0.791, "drop_pos": 0.99, "drop_width": 0.125} (and the true class tubing_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00068
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.996, "load_range": 2.833, "roughness": 0.015, "up_mid": 9.635, "dn_mid": 7.464, "up_slope": -1.452, "dn_slope": 0.512, "drop_pos": 1.0, "drop_width": 0.145} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00069
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 1.236, "load_range": 2.548, "roughness": 0.017, "up_mid": 8.81, "dn_mid": 6.685, "up_slope": -0.697, "dn_slope": 0.385, "drop_pos": 0.91, "drop_width": 0.125} (and the true class rod_float for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00070
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.609, "load_range": 0.753, "roughness": 0.003, "up_mid": 1.598, "dn_mid": 0.924, "up_slope": -0.161, "dn_slope": 0.106, "drop_pos": 0.965, "drop_width": 0.25} (and the true class parted_rods for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00071
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.656, "load_range": 2.127, "roughness": 0.019, "up_mid": 10.396, "dn_mid": 8.464, "up_slope": -0.243, "dn_slope": -0.058, "drop_pos": 0.56, "drop_width": 0.525} (and the true class fluid_pound for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00072
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.709, "load_range": 2.524, "roughness": 0.011, "up_mid": 10.735, "dn_mid": 8.755, "up_slope": -0.883, "dn_slope": 0.459, "drop_pos": 0.97, "drop_width": 0.135} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00073
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.424, "load_range": 4.18, "roughness": 0.006, "up_mid": 8.839, "dn_mid": 5.598, "up_slope": -1.036, "dn_slope": 1.246, "drop_pos": 0.995, "drop_width": 0.145} (and the true class unseated_pump for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

### item_id: L8-00074
You are a rod-lift diagnostics expert. Given this dynamometer card summary {"stroke_ratio": 2.172, "load_range": 2.331, "roughness": 0.023, "up_mid": 6.03, "dn_mid": 4.172, "up_slope": -0.905, "dn_slope": 0.33, "drop_pos": 0.94, "drop_width": 0.13} (and the true class travelling_valve_leak for reference), write the annotation an expert would attach: the visual cues on the card, the diagnosis, confidence, and the corrective action.

## Output contract
Return a JSON array of exactly 25 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
