# LLM-synthetic packs: paste, save, import

Each `llm-packs/<spec>/<spec>_batch_NNN.md` is self-contained: paste the WHOLE file into a chat LLM (new chat per
file). It replies with ONE JSON array (one object per `item_id`). Save that reply, then import.

1. Paste `llm-packs/L3/L3_batch_001.md` into the LLM.
2. Save the reply as `llm-packs/L3/replies/L3_batch_001.json` (`.json`, `.md` or `.txt`; fences/prose are tolerated).
3. Import everything (idempotent, safe to re-run): `cd backend && uv run mantle-data llm import ../llm-packs`
4. The report lists accepted / rejected (with reasons) / duplicates / missing. Re-paste only the bad ones:
   `uv run mantle-data llm pack L3 --retry-failed` -> `llm-packs/L3/L3_retry_001.md` (repeat 2-3).
5. Need more? `uv run mantle-data llm pack L3 --n 120` appends NEW items and batches after the existing ones.

Accepted records go to `backend/data/llm/<spec>.jsonl` (`source=llm_synthetic`) and the DuckDB table `llm_records`
(if the DB is locked by the API, run `uv run mantle-data db load` later).

## Order, volume, and what each feeds

| # | Spec | Batches (items each) | Feeds in the app |
|---|------|----------------------|------------------|
| 1 | L3 rod failure reports | 20 (12) | M4 text features, failure tooltips |
| 2 | L4 pump unseat incidents | 10 (20) | M4 text features, failure tooltips |
| 3 | L5 workover tickets | 15 (20) | M4 text features, failure tooltips, cost context |
| 4 | L8 dyno expert annotations | 12 (25) | dyno card diagnosis text (M1 explanations) |
| 5 | L13 strategy playbook | 10 (15) | "today's practice" baseline strategies in the Arena |
| 6 | L1 well master records | 10 (10) | well detail pages, completion context |
| 7 | L2 CSS cycle design sheets | 10 (15) | cycle plan vs actual notes, Arena context |
| 8 | L9 lab fluid reports | 10 (12) | fluid/viscosity context for the twin |
| 9 | L7 alarm narratives | 10 (30) | alarm triage notes in the live view |
| 10 | L10 steam generator logs | 10 (20) | steam supply context |
| 11 | L12 copilot Q&A | 10 (25) | future copilot (grounded Q&A) |
| 12 | L6 operator shift logs (10 lines/item) | 10 (20) | free-text shift context for M4 |
| 13 | L11 energy tariff notes | 5 (10) | cost/tariff context |

Starter volume is ~100-300 records per spec (L6: 2,000 lines). Start with L3-L5: a few batches already show the
pipeline end to end.

Only paste files named `*_batch_NNN.md` / `*_retry_NNN.md`. Keep replies in `replies/`. `manifest.jsonl` (what each
item_id was rendered with) and `status.json` (failed/missing items) are managed by the CLI; do not edit them.
