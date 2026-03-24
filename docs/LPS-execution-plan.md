# LPS Execution Plan

## Purpose
Translate the PRD into a current, dependency-based delivery sequence for a solo builder, while keeping the repo easy to hand off later.

## Current Baseline (2026-03-24)
- Phase 0 is complete.
- Implemented code:
  - schema definition and validation helpers
  - local filesystem storage helpers
  - CLI commands: `init`, `ingest`, `analyze`, `rewrite`, `versions`, `diff`, `validate`
  - schema, ingestion, analysis, rewrite, and versioning tests
- Verified commands in the current shell:
  - `python3 --version` works
  - `python3 -m lps.cli --help` works
  - `python3 -m lps.cli ingest --format markdown --input tests/fixtures/sample_profile.md` works after dev setup
  - `python3 -m lps.cli rewrite /tmp/lps-ingest-check/profiles/markdown-check.json --lens ai --workspace /tmp/lps-rewrite-check` works
  - `python3 -m lps.cli versions save /tmp/lps-rewrite-check/rewrites/markdown-check-ai.json --variant-id ai-core --workspace /tmp/lps-version-check` works
  - `/tmp/lps-venv/bin/python -m pytest -q` passes
- Dev setup baseline:
  - `pyproject.toml` declares `pytest` in the `dev` extra
  - the recommended path is `python3 -m venv .venv` then `.venv/bin/python -m pip install -e ".[dev]"`

## Solo Delivery Workflow
Default operating model:
1. Work in small, reviewable slices.
2. Use a short-lived branch when the slice is non-trivial, risky, or spans multiple files.
3. Run the most relevant checks before committing.
4. Commit with clear, scoped messages.
5. Update docs whenever commands, paths, or workflow expectations change.

Optional collaboration workflow:
- Open a PR when handing work to another reviewer, changing architecture, or taking on a higher-risk refactor.
- Include scope, verification notes, and any rollback considerations.

### Commit Message Convention
- `feat: <what changed>`
- `fix: <what changed>`
- `chore: <what changed>`
- `docs: <what changed>`
- `refactor: <what changed>`
- `test: <what changed>`

## Phase 0 - Complete
Goal achieved: establish a stable local data model and a working CLI skeleton.

Delivered:
- project package layout
- schema v1
- local storage conventions for profile JSON
- workspace initialization
- validation command
- baseline tests

Exit criteria met:
- the repo can create a starter workspace
- the repo can validate a schema v1 profile
- the implementation is local-only and human-readable

## Active Delivery Sequence

### Phase 1 - Ingestion and Parsing
Dependencies:
- Phase 0 complete

Deliverables:
- parser module boundary for source adapters
- Markdown ingestion path
- manual paste ingestion path
- normalization layer that outputs schema v1 JSON
- structured error reporting for malformed input

Verification gates:
- ingest from Markdown into `.lps/profiles/`
- ingest from pasted content into `.lps/profiles/`
- invalid inputs return actionable validation or parsing errors

Exit criteria:
- user can ingest profile source material in under 3 minutes
- output is a valid profile JSON document stored locally

Current status:
- implemented with the `ingest` CLI command
- covered by parser and CLI tests
- the next work begins at Phase 2 analysis

Risks to manage:
- ambiguous Markdown section boundaries
- input formats drifting away from the schema
- error messages that are technically correct but not actionable

### Phase 2 - Analysis Engine
Dependencies:
- Phase 1 complete

Deliverables:
- heuristic scoring rubric
- per-lens gap analysis
- prioritized weaknesses and improvements
- analysis artifact format stored under `.lps/analysis/`

Verification gates:
- report includes numeric scores with explanations
- report distinguishes between general quality issues and lens-specific positioning gaps
- report can be generated from any valid profile JSON

Exit criteria:
- each run returns at least 3 prioritized weaknesses and 3 improvements
- analysis output is saved locally and remains human-readable

Current status:
- implemented with the `analyze` CLI command
- covered by analysis tests and CLI verification
- the next work begins at Phase 3 rewrite

Risks to manage:
- scoring rules that are too vague to trust
- generic recommendations that do not improve positioning
- analysis output that cannot be traced back to source profile content

### Phase 3 - Rewrite Engine
Dependencies:
- Phase 2 complete

Deliverables:
- rewrite workflow for headline, about, and experience
- lens-aware prompts or templates for:
  - AI leadership
  - transformation leadership
  - consulting leadership
- factuality review checklist
- rewrite artifacts stored under `.lps/rewrites/`

Verification gates:
- generated variants cover all three core sections
- at least 2 strong variants are generated in one run
- review output explicitly flags claims that need confirmation

Exit criteria:
- the user can compare multiple credible variants without losing source fidelity
- the rewrite flow is usable across all three MVP positioning lenses

Current status:
- implemented with the `rewrite` CLI command
- covered by rewrite tests and CLI verification
- the next work begins at Phase 4 versioning and diff

Risks to manage:
- embellished claims or unsupported metrics
- different lenses collapsing into the same generic language
- output quality depending too heavily on undocumented prompt behavior

### Phase 4 - Versioning and Diff
Dependencies:
- Phase 3 complete

Deliverables:
- version metadata format
- save, list, and retrieve flows
- diff command for any two saved versions
- version artifacts stored under `.lps/versions/`

Verification gates:
- versions can be retrieved by stable identifiers
- metadata captures enough context to understand version origin
- diff output is readable enough for profile review decisions

Exit criteria:
- user can reliably save and compare any two variants
- version records are inspectable without bespoke tooling

Current status:
- implemented with the `versions` and `diff` CLI commands
- covered by versioning tests and CLI verification
- the next work begins at Phase 5 content generation

Risks to manage:
- metadata shape becoming inconsistent across commands
- diffs that are technically accurate but not useful for narrative review
- version identifiers that are hard to reference from the CLI

### Phase 5 - Content Generation
Dependencies:
- Phase 4 complete

Deliverables:
- post idea generator
- short-form post draft generator
- outreach draft generator
- content artifacts stored under `.lps/content/`

Verification gates:
- content is generated from a selected saved version rather than detached prompts
- outputs preserve the chosen positioning lens
- output bundles are saved as Markdown or plain text

Exit criteria:
- a run produces at least 10 post ideas, 3 post drafts, and 3 outreach drafts
- generated content stays aligned with the chosen profile narrative

Risks to manage:
- narrative drift between profile and generated content
- repetitive outputs across formats
- content generation happening before version selection is stable

## Cross-Cutting Rules
- Keep the canonical schema stable until MVP pressure requires change.
- Prefer explicit local artifacts over hidden state.
- Do not imply or build LinkedIn automation.
- Preserve a clear line between implemented commands and planned commands in docs and CLI help.
- Treat factual accuracy as a release gate for rewrite-related work.

## Immediate Next Tickets
1. Define content generation inputs from a selected saved version.
2. Implement the first content idea generator.
3. Add content artifact storage conventions under `.lps/content/`.
4. Add CLI wiring for `content`.
5. Generate at least 10 ideas, 3 post drafts, and 3 outreach drafts per run.
6. Decide whether content generation should read directly from rewrite artifacts or the normalized version store.
7. Add content tests across AI, transformation, and consulting lenses.
8. Decide whether content artifacts should be Markdown, plain text, JSON, or a hybrid bundle.
9. Add a short architecture note covering the full profile -> analysis -> rewrite -> version -> content flow.
10. Evaluate whether deterministic generation is sufficient for content or whether a model-backed path is justified later.

## MVP Completion Definition
The MVP is complete when one user can:
1. ingest a profile into schema v1
2. analyze it with actionable heuristic feedback
3. generate multiple role-aligned rewrites
4. save and diff versions
5. generate narrative-aligned posts and outreach from a selected version
