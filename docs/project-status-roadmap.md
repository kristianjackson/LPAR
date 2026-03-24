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
  - Phase 3 through Phase 5 not yet implemented

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
  - `validate`
- `lps/ingestion.py`
  - Markdown ingestion parser
  - labeled paste ingestion parser
  - normalization and actionable parse errors
- `lps/analysis.py`
  - heuristic scoring rubric
  - selected-lens gap analysis
  - prioritized weaknesses and improvements
- `tests/test_schema.py`
  - baseline validation coverage for valid and invalid profiles
- `tests/test_ingestion.py`
  - parser and CLI coverage for Markdown and paste ingestion
- `tests/test_analysis.py`
  - heuristic analysis and CLI coverage
- `README.md`
  - dev setup
  - quickstart for Phase 0 through Phase 2 commands

## Gap to MVP

| Area | Status | What Exists | What Is Missing | Next Move |
| --- | --- | --- | --- | --- |
| Workspace + schema | Complete for MVP baseline | schema v1, storage, init, validate | minor setup polish only | keep stable while later phases land |
| Ingestion | Complete for MVP baseline | parser adapters, normalization, CLI command, fixtures | robustness polish only | move to analysis work |
| Analysis | Complete for MVP baseline | rubric, report format, CLI command, tests | tuning and polish only | move to rewrite work |
| Rewrite | Not started | no generation workflow | lens templates, factuality checklist, saved artifacts | design artifact format before implementation |
| Versioning + diff | Not started | no version store | metadata shape, list/open/diff commands, artifact layout | define version metadata before coding |
| Content generation | Not started | no content pipeline | ideas, drafts, outreach, CLI command, saved outputs | start only after version selection is usable |
| Test/dev setup | Complete for repo baseline | `dev` extra includes pytest, README documents venv workflow | optional lockfile or stricter tooling later | use the documented setup for all verification |

## Ordered Next Tickets
1. Decide the analysis output shape that rewrite generation will consume.
2. Define rewrite artifact metadata so later versioning and diffing use consistent identifiers.
3. Implement rewrite generation for all three positioning lenses.
4. Add the `rewrite` CLI command and save artifacts locally.
5. Add the factuality checklist required before saving or promoting rewrites.
6. Add a short architecture note now that analysis boundaries are real in code.
7. Define stable version identifiers and retrieval conventions.
8. Implement version storage and lookup.
9. Implement diff output that is usable for narrative review, not just raw text comparison.
10. Decide whether rewrite artifacts should include both JSON and Markdown review forms.

## Active Blockers and Risks
- Rewrite artifacts and metadata are still undefined. If rewrite generation lands before the artifact contract is set, versioning work will get harder.
- Version metadata shape is still undefined. If rewrite artifacts appear before metadata rules are set, reproducibility will be harder to add later.
- Multi-lens support is a product requirement in MVP, so analysis and rewrite abstractions should not hard-code a single lens.

## Decision Log
- 2026-03-24: Phase 0 is treated as complete and future delivery starts at ingestion/parsing.
- 2026-03-24: MVP remains local-first and CLI-only.
- 2026-03-24: AI, transformation, and consulting remain equal first-class positioning lenses in MVP.
- 2026-03-24: Heuristic scoring is the v1 analysis strategy.
- 2026-03-24: Durable artifacts for v1 are limited to JSON, Markdown, and plain text.
- 2026-03-24: Phase 1 ingestion is implemented with Markdown and labeled paste adapters behind the `ingest` CLI command.
- 2026-03-24: Phase 2 analysis is implemented with heuristic scoring, saved JSON reports, and selected-lens gap analysis.

## Near-Term Acceptance Checks
- Every current command named in the docs exists today:
  - `python3 -m lps.cli init`
  - `python3 -m lps.cli ingest --format <markdown|paste> --input <path>`
  - `python3 -m lps.cli analyze <path> --lens <ai|transformation|consulting>`
  - `python3 -m lps.cli validate <path>`
  - `python3 -m lps.cli --help`
- Every planned command named in the docs is clearly labeled as planned:
  - `rewrite`
  - `versions`
  - `diff`
  - `content`
- Phase 0 is documented as complete across the planning set.
- Phase 1 is documented as complete across the planning set.
- Phase 2 is documented as complete across the planning set.
- Active implementation starts at Phase 3 rewrite.
