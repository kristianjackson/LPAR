# LPS Execution Plan (Post-PRD)

## Purpose
This plan translates the PRD into an execution sequence and defines how repo operations (branching, commits, PRs, merges, release tags) will be managed going forward.

## Working Agreement: Repo Operations
I will manage repository operations with the following default flow for each unit of work:

1. Create a scoped branch from `main` using `feat/<area>-<short-name>` or `chore/<short-name>`.
2. Implement a small, reviewable slice.
3. Run relevant checks/tests.
4. Commit with clear messages.
5. Open a PR with summary, risks, and test evidence.
6. Address review comments.
7. Merge with **squash merge** by default (unless you request otherwise).
8. Tag releases at milestone boundaries.

### Commit Message Convention
- `feat: <what changed>`
- `fix: <what changed>`
- `chore: <what changed>`
- `docs: <what changed>`
- `refactor: <what changed>`
- `test: <what changed>`

### PR Quality Bar
A PR should include:
- Scope + rationale.
- Test commands and outputs.
- Risk notes and rollback notes if applicable.
- Updated docs when behavior changes.

## Implementation Sequence (from PRD)

## Phase 0 — Foundation (Week 1)
**Goal:** establish project skeleton and stable local data model.

### Deliverables
- Project structure for `ingestion`, `analysis`, `rewrite`, `versioning`, `content` modules.
- Core profile schema:
  - `headline`
  - `about`
  - `experience[]`
- Local storage conventions (JSON + Markdown artifacts).
- Basic CLI entrypoint for running workflows locally.

### Exit Criteria
- Can load/save a valid profile object locally.
- Can run `init` + `validate` commands successfully.

## Phase 1 — Ingestion + Parsing (Week 1–2)
**Goal:** ingest manual/markdown profile input into structured schema.

### Deliverables
- Markdown parser for profile sections.
- Manual paste ingestion command.
- Validation and normalization pipeline.
- Error reporting for malformed input.

### Exit Criteria
- Ingestion from paste and markdown works end-to-end in <3 minutes.
- Structured output persisted to local store.

## Phase 2 — Analysis Engine (Week 2)
**Goal:** produce actionable quality and positioning diagnostics.

### Deliverables
- Scoring rubric (clarity, authority, AI signal, leadership signal).
- Gap analysis against selected target role.
- Prioritized weaknesses + improvements output format.

### Exit Criteria
- Report contains scores + at least 3 prioritized weaknesses and 3 improvements.

## Phase 3 — Rewrite Engine (Week 3)
**Goal:** generate stronger profile variants aligned to role lenses.

### Deliverables
- Rewrite templates for headline/about/experience.
- Variant generation modes:
  - AI-focused
  - Consulting-focused
  - Transformation-focused
- Factuality guardrails/checklist before save.

### Exit Criteria
- At least 2 high-quality variants generated per run.
- Variants pass factuality checklist.

## Phase 4 — Versioning + Diff (Week 4)
**Goal:** make experimentation first-class.

### Deliverables
- Version store with metadata (timestamp, role lens, prompt hash).
- Version listing and retrieval.
- Diff command for any two versions.

### Exit Criteria
- User can open and diff any two saved versions reliably.

## Phase 5 — Content Generator (Week 4–5)
**Goal:** leverage selected profile narrative for content output.

### Deliverables
- Idea generator (10+ ideas).
- Short-form post drafts.
- Outreach templates/messages.
- Style controls (tone, length, CTA strength).

### Exit Criteria
- At least 10 ideas, 3 post drafts, 3 outreach drafts per run.

## Backlog for Post-MVP
- Optional lightweight web UI.
- Feedback loop to tune scoring.
- Export bundles for easy profile publishing workflows.
- Analytics on variant performance over time.

## Immediate Next 10 Tickets
1. Define canonical profile JSON schema.
2. Create parser interface and test fixtures.
3. Implement markdown ingestion adapter.
4. Implement manual paste ingestion adapter.
5. Add schema validation command.
6. Define analysis score rubric constants.
7. Implement baseline analysis report formatter.
8. Add rewrite prompt templates per role lens.
9. Add version store abstraction.
10. Add diff renderer for profile versions.

## Risks to Manage Weekly
- Hallucinated claims in rewrites.
- Drift between profile narrative and generated content.
- Overly generic language reducing differentiation.

## Decision Log Template
Use this for consequential product/engineering decisions:
- Date:
- Context:
- Decision:
- Alternatives considered:
- Consequences:

## Done Definition for This Plan
This execution plan is considered active once Phase 0 ticketing starts and each phase is tracked by PRs tied to the exit criteria above.
