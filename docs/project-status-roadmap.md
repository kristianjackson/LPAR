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
  - Phase 4 through Phase 5 not yet implemented

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
- `tests/test_schema.py`
  - baseline validation coverage for valid and invalid profiles
- `tests/test_ingestion.py`
  - parser and CLI coverage for Markdown and paste ingestion
- `tests/test_analysis.py`
  - heuristic analysis and CLI coverage
- `tests/test_rewrite.py`
  - rewrite engine and CLI coverage
- `README.md`
  - dev setup
  - quickstart for Phase 0 through Phase 3 commands

## Gap to MVP

| Area | Status | What Exists | What Is Missing | Next Move |
| --- | --- | --- | --- | --- |
| Workspace + schema | Complete for MVP baseline | schema v1, storage, init, validate | minor setup polish only | keep stable while later phases land |
| Ingestion | Complete for MVP baseline | parser adapters, normalization, CLI command, fixtures | robustness polish only | move to analysis work |
| Analysis | Complete for MVP baseline | rubric, report format, CLI command, tests | tuning and polish only | move to rewrite work |
| Rewrite | Complete for MVP baseline | lens templates, factuality checklist, saved artifacts, CLI command, tests | quality tuning only | move to versioning work |
| Versioning + diff | Not started | no version store | metadata shape, list/open/diff commands, artifact layout | define version metadata before coding |
| Content generation | Not started | no content pipeline | ideas, drafts, outreach, CLI command, saved outputs | start only after version selection is usable |
| Test/dev setup | Complete for repo baseline | `dev` extra includes pytest, README documents venv workflow | optional lockfile or stricter tooling later | use the documented setup for all verification |

## Ordered Next Tickets
1. Define stable version identifiers and retrieval conventions.
2. Implement version storage and lookup.
3. Add the `versions` CLI command.
4. Implement diff output that is usable for narrative review, not just raw text comparison.
5. Add the `diff` CLI command.
6. Decide whether saved versions should snapshot both source profiles and rewrite artifacts.
7. Add a short architecture note now that rewrite boundaries are real in code.
8. Define content generation inputs from a selected saved version.
9. Implement the first content idea generator.
10. Decide whether content generation should read directly from rewrite artifacts or a normalized version store.

## Active Blockers and Risks
- Version metadata shape is still undefined. If rewrite artifacts appear before metadata rules are set, reproducibility will be harder to add later.
- Multi-lens support is a product requirement in MVP, so analysis and rewrite abstractions should not hard-code a single lens.
- Rewrite quality is currently deterministic and conservative. Higher-quality generation may later need a model-backed path, but the factuality bar should stay unchanged.

## Decision Log
- 2026-03-24: Phase 0 is treated as complete and future delivery starts at ingestion/parsing.
- 2026-03-24: MVP remains local-first and CLI-only.
- 2026-03-24: AI, transformation, and consulting remain equal first-class positioning lenses in MVP.
- 2026-03-24: Heuristic scoring is the v1 analysis strategy.
- 2026-03-24: Durable artifacts for v1 are limited to JSON, Markdown, and plain text.
- 2026-03-24: Phase 1 ingestion is implemented with Markdown and labeled paste adapters behind the `ingest` CLI command.
- 2026-03-24: Phase 2 analysis is implemented with heuristic scoring, saved JSON reports, and selected-lens gap analysis.
- 2026-03-24: Phase 3 rewrite is implemented with deterministic variants and factuality checklist artifacts.

## Near-Term Acceptance Checks
- Every current command named in the docs exists today:
  - `python3 -m lps.cli init`
  - `python3 -m lps.cli ingest --format <markdown|paste> --input <path>`
  - `python3 -m lps.cli analyze <path> --lens <ai|transformation|consulting>`
  - `python3 -m lps.cli rewrite <path> --lens <ai|transformation|consulting>`
  - `python3 -m lps.cli validate <path>`
  - `python3 -m lps.cli --help`
- Every planned command named in the docs is clearly labeled as planned:
  - `versions`
  - `diff`
  - `content`
- Phase 0 is documented as complete across the planning set.
- Phase 1 is documented as complete across the planning set.
- Phase 2 is documented as complete across the planning set.
- Phase 3 is documented as complete across the planning set.
- Active implementation starts at Phase 4 versioning and diff.
