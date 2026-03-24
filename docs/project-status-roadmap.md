# Project Status and Roadmap

## Snapshot (2026-03-24)
- Repository baseline: small local Python CLI project with docs, package code, and tests
- Package/runtime baseline:
  - `python3` is available in the current shell
  - `python3 -m lps.cli --help` works
  - the repo now declares `pytest` in the `dev` extra
  - the recommended setup is `python3 -m venv .venv` then `.venv/bin/python -m pip install -e ".[dev]"`
- Product maturity:
  - Phase 0 complete
  - Phase 1 complete
  - Phase 2 complete
  - Phase 3 complete
  - Phase 4 complete
  - Phase 5 not yet implemented

## Implemented Inventory
- `lps/schema.py`
  - canonical schema v1
  - profile validation
- `lps/storage.py`
  - workspace initialization
  - profile read/write helpers
- `lps/cli.py`
  - `init`
  - `ingest`
  - `analyze`
  - `rewrite`
  - `versions`
  - `diff`
  - `validate`
- `lps/ingestion.py`
  - Markdown ingestion parser
  - labeled paste ingestion parser
  - normalization and actionable parse errors
- `lps/analysis.py`
  - heuristic scoring rubric
  - selected-lens gap analysis
  - prioritized weaknesses and improvements
- `lps/rewrite.py`
  - deterministic lens-specific rewrite generation
  - two saved variants per run
  - factuality checklist generation
- `lps/versioning.py`
  - saved version record generation
  - version listing and lookup
  - unified diff rendering
- `tests/test_schema.py`
  - baseline validation coverage for valid and invalid profiles
- `tests/test_ingestion.py`
  - parser and CLI coverage for Markdown and paste ingestion
- `tests/test_analysis.py`
  - heuristic analysis and CLI coverage
- `tests/test_rewrite.py`
  - rewrite engine and CLI coverage
- `tests/test_versioning.py`
  - versioning and diff CLI coverage
- `README.md`
  - dev setup
  - quickstart for Phase 0 through Phase 4 commands

## Gap to MVP

| Area | Status | What Exists | What Is Missing | Next Move |
| --- | --- | --- | --- | --- |
| Workspace + schema | Complete for MVP baseline | schema v1, storage, init, validate | minor setup polish only | keep stable while later phases land |
| Ingestion | Complete for MVP baseline | parser adapters, normalization, CLI command, fixtures | robustness polish only | move to analysis work |
| Analysis | Complete for MVP baseline | rubric, report format, CLI command, tests | tuning and polish only | move to rewrite work |
| Rewrite | Complete for MVP baseline | lens templates, factuality checklist, saved artifacts, CLI command, tests | quality tuning only | move to versioning work |
| Versioning + diff | Complete for MVP baseline | version store, list/show, diff command, artifact layout, tests | polish only | move to content work |
| Content generation | Not started | no content pipeline | ideas, drafts, outreach, CLI command, saved outputs | start only after version selection is usable |
| Test/dev setup | Complete for repo baseline | `dev` extra includes pytest, README documents venv workflow | optional lockfile or stricter tooling later | use the documented setup for all verification |

## Ordered Next Tickets
1. Define content generation inputs from a selected saved version.
2. Implement the first content idea generator.
3. Add the `content` CLI command.
4. Generate at least 10 ideas, 3 post drafts, and 3 outreach drafts per run.
5. Add content artifact storage conventions under `.lps/content/`.
6. Add content tests across AI, transformation, and consulting lenses.
7. Decide whether content generation should read directly from rewrite artifacts or the normalized version store.
8. Add a short architecture note covering the end-to-end pipeline now that versioning exists.
9. Decide whether content artifacts should be Markdown, plain text, JSON, or a hybrid bundle.
10. Evaluate whether deterministic generation is sufficient for content or whether a model-backed path is justified later.

## Active Blockers and Risks
- Version metadata now exists, so future changes should preserve backward readability for saved version records.
- Multi-lens support is a product requirement in MVP, so analysis and rewrite abstractions should not hard-code a single lens.
- Rewrite quality is currently deterministic and conservative. Higher-quality generation may later need a model-backed path, but the factuality bar should stay unchanged.
- Content generation remains the largest missing area for MVP because it needs to reuse versioned narrative without drifting into generic output.

## Decision Log
- 2026-03-24: Phase 0 is treated as complete and future delivery starts at ingestion/parsing.
- 2026-03-24: MVP remains local-first and CLI-only.
- 2026-03-24: AI, transformation, and consulting remain equal first-class positioning lenses in MVP.
- 2026-03-24: Heuristic scoring is the v1 analysis strategy.
- 2026-03-24: Durable artifacts for v1 are limited to JSON, Markdown, and plain text.
- 2026-03-24: Phase 1 ingestion is implemented with Markdown and labeled paste adapters behind the `ingest` CLI command.
- 2026-03-24: Phase 2 analysis is implemented with heuristic scoring, saved JSON reports, and selected-lens gap analysis.
- 2026-03-24: Phase 3 rewrite is implemented with deterministic variants and factuality checklist artifacts.
- 2026-03-24: Phase 4 versioning is implemented with saved snapshots and unified diffs over versioned profiles.

## Near-Term Acceptance Checks
- Every current command named in the docs exists today:
  - `python3 -m lps.cli init`
  - `python3 -m lps.cli ingest --format <markdown|paste> --input <path>`
  - `python3 -m lps.cli analyze <path> --lens <ai|transformation|consulting>`
  - `python3 -m lps.cli rewrite <path> --lens <ai|transformation|consulting>`
  - `python3 -m lps.cli versions save <rewrite-path> --variant-id <id>`
  - `python3 -m lps.cli versions list`
  - `python3 -m lps.cli versions show <version-id>`
  - `python3 -m lps.cli diff <version-a> <version-b>`
  - `python3 -m lps.cli validate <path>`
  - `python3 -m lps.cli --help`
- Every planned command named in the docs is clearly labeled as planned:
  - `content`
- Phase 0 is documented as complete across the planning set.
- Phase 1 is documented as complete across the planning set.
- Phase 2 is documented as complete across the planning set.
- Phase 3 is documented as complete across the planning set.
- Phase 4 is documented as complete across the planning set.
- Active implementation starts at Phase 5 content generation.
