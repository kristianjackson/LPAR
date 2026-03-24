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
  - Phase 2 through Phase 5 not yet implemented

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
  - `validate`
- `lps/ingestion.py`
  - Markdown ingestion parser
  - labeled paste ingestion parser
  - normalization and actionable parse errors
- `tests/test_schema.py`
  - baseline validation coverage for valid and invalid profiles
- `tests/test_ingestion.py`
  - parser and CLI coverage for Markdown and paste ingestion
- `README.md`
  - dev setup
  - quickstart for Phase 0 and Phase 1 commands

## Gap to MVP

| Area | Status | What Exists | What Is Missing | Next Move |
| --- | --- | --- | --- | --- |
| Workspace + schema | Complete for MVP baseline | schema v1, storage, init, validate | minor setup polish only | keep stable while later phases land |
| Ingestion | Complete for MVP baseline | parser adapters, normalization, CLI command, fixtures | robustness polish only | move to analysis work |
| Analysis | Not started | no scoring or reporting | rubric, report format, CLI command, tests | define heuristic rubric after ingestion is stable |
| Rewrite | Not started | no generation workflow | lens templates, factuality checklist, saved artifacts | design artifact format before implementation |
| Versioning + diff | Not started | no version store | metadata shape, list/open/diff commands, artifact layout | define version metadata before coding |
| Content generation | Not started | no content pipeline | ideas, drafts, outreach, CLI command, saved outputs | start only after version selection is usable |
| Test/dev setup | Complete for repo baseline | `dev` extra includes pytest, README documents venv workflow | optional lockfile or stricter tooling later | use the documented setup for all verification |

## Ordered Next Tickets
1. Define the heuristic analysis rubric and saved report shape for `.lps/analysis/`.
2. Add the `analyze` CLI command and persist analysis artifacts locally.
3. Add analysis tests for strong, weak, and malformed inputs.
4. Decide the analysis output shape that rewrite generation will consume.
5. Define rewrite artifact metadata so later versioning and diffing use consistent identifiers.
6. Add a short architecture note now that ingestion boundaries are real in code.
7. Implement rewrite generation for all three positioning lenses.
8. Add the factuality checklist required before saving or promoting rewrites.
9. Define stable version identifiers and retrieval conventions.
10. Implement diff output that is usable for narrative review, not just raw text comparison.

## Active Blockers and Risks
- The analysis phase needs a documented rubric before implementation starts, or later scoring will be difficult to compare across runs.
- Version metadata shape is still undefined. If rewrite artifacts appear before metadata rules are set, reproducibility will be harder to add later.
- Multi-lens support is a product requirement in MVP, so analysis and rewrite abstractions should not hard-code a single lens.

## Decision Log
- 2026-03-24: Phase 0 is treated as complete and future delivery starts at ingestion/parsing.
- 2026-03-24: MVP remains local-first and CLI-only.
- 2026-03-24: AI, transformation, and consulting remain equal first-class positioning lenses in MVP.
- 2026-03-24: Heuristic scoring is the v1 analysis strategy.
- 2026-03-24: Durable artifacts for v1 are limited to JSON, Markdown, and plain text.
- 2026-03-24: Phase 1 ingestion is implemented with Markdown and labeled paste adapters behind the `ingest` CLI command.

## Near-Term Acceptance Checks
- Every current command named in the docs exists today:
  - `python3 -m lps.cli init`
  - `python3 -m lps.cli ingest --format <markdown|paste> --input <path>`
  - `python3 -m lps.cli validate <path>`
  - `python3 -m lps.cli --help`
- Every planned command named in the docs is clearly labeled as planned:
  - `analyze`
  - `rewrite`
  - `versions`
  - `diff`
  - `content`
- Phase 0 is documented as complete across the planning set.
- Phase 1 is documented as complete across the planning set.
- Active implementation starts at Phase 2 analysis.
