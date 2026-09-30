# L5 workover_ticket - batch 002 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L5/replies/L5_batch_002.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L5-00020 .. L5-00039 (each has an `item_id` you must echo).

## System prompt (applies to every item)
You are generating realistic but entirely fictional operational records for Baghewala, a heavy-oil field in the Bikaner-Nagaur basin, Rajasthan, India, operated by Oil India Limited. Reservoir: Jodhpur Sandstone, 1,080-1,160 m, 17-19 API crude, asphaltene 7-12 wt%, reservoir temperature 46-48 C, low reservoir pressure (~3 MPa). Wells are produced by cyclic steam stimulation (CSS) and conventional beam pumping units with sucker-rod pumps on VFDs. Use Indian field conventions (IST timestamps, INR, metric units with oilfield units in brackets where operators would use them), plausible names for roles (not real people), and terse operator language. Never invent company names other than Oil India Limited and generic vendors ("VFD vendor", "rod supplier"). Output only JSON matching the schema.

## JSON schema for ONE record
```json
{
  "type": "object", "additionalProperties": false,
  "required": ["item_id", "well_id", "job_type", "request", "job_steps", "rig_hours", "materials", "cost_inr", "outcome"],
  "properties": {
    "item_id": {"type": "string", "description": "copy the item_id of the item exactly"},
    "well_id": {"type": "string"},
    "job_type": {"type": "string", "enum": ["rod job", "pump change", "tubing leak repair", "stuffing box repack", "VFD fault", "belt/sheave change", "gearbox oil change", "counterbalance adjustment"]},
    "request": {"type": "string"},
    "job_steps": {"type": "array", "items": {"type": "string"}, "minItems": 2},
    "rig_hours": {"type": "number", "minimum": 0, "maximum": 200},
    "materials": {"type": "array", "items": {"type": "string"}},
    "cost_inr": {"type": "number", "minimum": 0},
    "outcome": {"type": "string"}
  }
}
```

## Items (20)
Write one record per item, following the instruction under each item_id.

### item_id: L5-00020
Write a workover/maintenance ticket for BGW-32: request, job steps, rig hours, materials, cost INR, outcome; job type gearbox oil change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00021
Write a workover/maintenance ticket for BGW-41: request, job steps, rig hours, materials, cost INR, outcome; job type counterbalance adjustment from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00022
Write a workover/maintenance ticket for BGW-01: request, job steps, rig hours, materials, cost INR, outcome; job type rod job from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00023
Write a workover/maintenance ticket for BGW-04: request, job steps, rig hours, materials, cost INR, outcome; job type belt/sheave change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00024
Write a workover/maintenance ticket for BGW-29: request, job steps, rig hours, materials, cost INR, outcome; job type counterbalance adjustment from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00025
Write a workover/maintenance ticket for BGW-34: request, job steps, rig hours, materials, cost INR, outcome; job type gearbox oil change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00026
Write a workover/maintenance ticket for BGW-41: request, job steps, rig hours, materials, cost INR, outcome; job type stuffing box repack from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00027
Write a workover/maintenance ticket for BGW-31: request, job steps, rig hours, materials, cost INR, outcome; job type counterbalance adjustment from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00028
Write a workover/maintenance ticket for BGW-38: request, job steps, rig hours, materials, cost INR, outcome; job type belt/sheave change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00029
Write a workover/maintenance ticket for BGW-02: request, job steps, rig hours, materials, cost INR, outcome; job type pump change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00030
Write a workover/maintenance ticket for BGW-40: request, job steps, rig hours, materials, cost INR, outcome; job type tubing leak repair from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00031
Write a workover/maintenance ticket for BGW-11: request, job steps, rig hours, materials, cost INR, outcome; job type counterbalance adjustment from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00032
Write a workover/maintenance ticket for BGW-03: request, job steps, rig hours, materials, cost INR, outcome; job type rod job from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00033
Write a workover/maintenance ticket for BGW-59: request, job steps, rig hours, materials, cost INR, outcome; job type belt/sheave change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00034
Write a workover/maintenance ticket for BGW-12: request, job steps, rig hours, materials, cost INR, outcome; job type rod job from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00035
Write a workover/maintenance ticket for BGW-14: request, job steps, rig hours, materials, cost INR, outcome; job type pump change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00036
Write a workover/maintenance ticket for BGW-25: request, job steps, rig hours, materials, cost INR, outcome; job type VFD fault from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00037
Write a workover/maintenance ticket for BGW-25: request, job steps, rig hours, materials, cost INR, outcome; job type tubing leak repair from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00038
Write a workover/maintenance ticket for BGW-29: request, job steps, rig hours, materials, cost INR, outcome; job type gearbox oil change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00039
Write a workover/maintenance ticket for BGW-27: request, job steps, rig hours, materials, cost INR, outcome; job type pump change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
