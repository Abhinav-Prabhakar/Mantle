# L5 workover_ticket - batch 014 (20 items)

## How to use
1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.
2. It must reply with ONE JSON array only: exactly 20 objects, no prose, no markdown fences.
3. Save the reply as `llm-packs/L5/replies/L5_batch_014.json` (any *.json / *.md / *.txt name inside `replies/` works).
4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`

Items in this file: L5-00260 .. L5-00279 (each has an `item_id` you must echo).

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

### item_id: L5-00260
Write a workover/maintenance ticket for BGW-29: request, job steps, rig hours, materials, cost INR, outcome; job type tubing leak repair from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00261
Write a workover/maintenance ticket for BGW-19: request, job steps, rig hours, materials, cost INR, outcome; job type gearbox oil change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00262
Write a workover/maintenance ticket for BGW-14: request, job steps, rig hours, materials, cost INR, outcome; job type tubing leak repair from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00263
Write a workover/maintenance ticket for BGW-06: request, job steps, rig hours, materials, cost INR, outcome; job type belt/sheave change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00264
Write a workover/maintenance ticket for BGW-38: request, job steps, rig hours, materials, cost INR, outcome; job type belt/sheave change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00265
Write a workover/maintenance ticket for BGW-04: request, job steps, rig hours, materials, cost INR, outcome; job type belt/sheave change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00266
Write a workover/maintenance ticket for BGW-15: request, job steps, rig hours, materials, cost INR, outcome; job type counterbalance adjustment from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00267
Write a workover/maintenance ticket for BGW-20: request, job steps, rig hours, materials, cost INR, outcome; job type counterbalance adjustment from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00268
Write a workover/maintenance ticket for BGW-57: request, job steps, rig hours, materials, cost INR, outcome; job type tubing leak repair from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00269
Write a workover/maintenance ticket for BGW-11: request, job steps, rig hours, materials, cost INR, outcome; job type VFD fault from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00270
Write a workover/maintenance ticket for BGW-39: request, job steps, rig hours, materials, cost INR, outcome; job type stuffing box repack from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00271
Write a workover/maintenance ticket for BGW-36: request, job steps, rig hours, materials, cost INR, outcome; job type belt/sheave change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00272
Write a workover/maintenance ticket for BGW-54: request, job steps, rig hours, materials, cost INR, outcome; job type stuffing box repack from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00273
Write a workover/maintenance ticket for BGW-55: request, job steps, rig hours, materials, cost INR, outcome; job type counterbalance adjustment from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00274
Write a workover/maintenance ticket for BGW-02: request, job steps, rig hours, materials, cost INR, outcome; job type gearbox oil change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00275
Write a workover/maintenance ticket for BGW-10: request, job steps, rig hours, materials, cost INR, outcome; job type VFD fault from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00276
Write a workover/maintenance ticket for BGW-04: request, job steps, rig hours, materials, cost INR, outcome; job type rod job from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00277
Write a workover/maintenance ticket for BGW-60: request, job steps, rig hours, materials, cost INR, outcome; job type pump change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00278
Write a workover/maintenance ticket for BGW-24: request, job steps, rig hours, materials, cost INR, outcome; job type belt/sheave change from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

### item_id: L5-00279
Write a workover/maintenance ticket for BGW-22: request, job steps, rig hours, materials, cost INR, outcome; job type counterbalance adjustment from {rod job, pump change, tubing leak repair, stuffing box repack, VFD fault, belt/sheave change, gearbox oil change, counterbalance adjustment}.

## Output contract
Return a JSON array of exactly 20 objects, in the order listed above. Each object has `item_id` (copied exactly) plus every field of the schema, and no other keys.
No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.
