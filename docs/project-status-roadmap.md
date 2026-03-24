# Project Status and Roadmap

## Snapshot (2026-03-24)
- Repository status: clean working tree on `main`
- Package/runtime baseline:
  - `python3` is available in the current shell
  - `python3 -m lps.cli --help` works
  - `python3 -m pytest -q` does not run in the current shell because `pytest` is not installed
- Product maturity:
  - Phase 0 complete
  - Phase 1 through Phase 5 not yet implemented

## Implemented Inventory
- `lps/schema.py`
  - canonical schema v1
  - profile validation
- `lps/storage.py`
  - workspace initialization
  - profile read/write helpers
- `lps/cli.py`
  - `init`
  - `validate`
- `tests/test_schema.py`
  - baseline validation coverage for valid and invalid profiles
- `README.md`
  - quickstart for Phase 0 commands

## Gap to MVP

| Area | Status | What Exists | What Is Missing | Next Move |
| --- | --- | --- | --- | --- |
| Workspace + schema | Complete for MVP baseline | schema v1, storage, init, validate | minor setup polish only | keep stable while later phases land |
| Ingestion | Not started | none beyond direct JSON editing | parser adapters, normalization, CLI command, fixtures | build Markdown and paste ingestion first |
| Analysis | Not started | no scoring or reporting | rubric, report format, CLI command, tests | define heuristic rubric after ingestion is stable |
| Rewrite | Not started | no generation workflow | lens templates, factuality checklist, saved artifacts | design artifact format before implementation |
| Versioning + diff | Not started | no version store | metadata shape, list/open/diff commands, artifact layout | define version metadata before coding |
| Content generation | Not started | no content pipeline | ideas, drafts, outreach, CLI command, saved outputs | start only after version selection is usable |
| Test/dev setup | Partial | test file exists, `pyproject.toml` points pytest at `tests` | install path for pytest and dev workflow docs | add explicit dev setup as the next repo chore |

## Ordered Next Tickets
1. Add developer setup instructions for Python environment creation and `pytest` installation.
2. Add project metadata for test dependencies so the declared test suite is runnable in a clean environment.
3. Create an ingestion package boundary with a parser interface and test fixtures.
4. Define the Markdown source contract:
   - headings map to `headline`, `about`, and `experience`
   - malformed or missing sections produce actionable errors
5. Implement Markdown ingestion and persistence to `.lps/profiles/`.
6. Implement manual paste ingestion using the same normalization pipeline.
7. Add CLI wiring and help text for the planned `ingest` command.
8. Define the heuristic analysis rubric and saved report shape for `.lps/analysis/`.
9. Define rewrite artifact metadata so later versioning and diffing use consistent identifiers.
10. Add a short architecture note once ingestion and analysis boundaries are real in code.

## Active Blockers and Risks
- The repo declares tests but does not yet provide a ready-to-run dev environment, which slows verification and onboarding.
- The ingestion phase needs a documented Markdown contract before parser implementation starts, or parsing behavior will drift.
- Version metadata shape is still undefined. If rewrite artifacts appear before metadata rules are set, reproducibility will be harder to add later.
- Multi-lens support is a product requirement in MVP, so analysis and rewrite abstractions should not hard-code a single lens.

## Decision Log
- 2026-03-24: Phase 0 is treated as complete and future delivery starts at ingestion/parsing.
- 2026-03-24: MVP remains local-first and CLI-only.
- 2026-03-24: AI, transformation, and consulting remain equal first-class positioning lenses in MVP.
- 2026-03-24: Heuristic scoring is the v1 analysis strategy.
- 2026-03-24: Durable artifacts for v1 are limited to JSON, Markdown, and plain text.

## Near-Term Acceptance Checks
- Every current command named in the docs exists today:
  - `python3 -m lps.cli init`
  - `python3 -m lps.cli validate <path>`
  - `python3 -m lps.cli --help`
- Every planned command named in the docs is clearly labeled as planned:
  - `ingest`
  - `analyze`
  - `rewrite`
  - `versions`
  - `diff`
  - `content`
- Phase 0 is documented as complete across the planning set.
- Active implementation starts at Phase 1 ingestion and parsing.
