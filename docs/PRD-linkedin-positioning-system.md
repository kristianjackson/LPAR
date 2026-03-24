# Product Requirements Document (PRD)

## Product
**LinkedIn Positioning System (LPS)**

## Purpose
Define the current product reality, the target MVP, and the defaults that guide implementation from the current Phase 0 scaffold to a usable local-first workflow.

## Current State (Implemented as of 2026-03-24)
- The repo is a local Python CLI project with the `lps` package and nine working commands:
  - `python3 -m lps.cli init`
  - `python3 -m lps.cli ingest --format <markdown|paste> --input <path>`
  - `python3 -m lps.cli analyze <path> --lens <ai|transformation|consulting>`
  - `python3 -m lps.cli rewrite <path> --lens <ai|transformation|consulting>`
  - `python3 -m lps.cli versions save <rewrite-path> --variant-id <id>`
  - `python3 -m lps.cli versions list`
  - `python3 -m lps.cli versions show <version-id>`
  - `python3 -m lps.cli diff <version-a> <version-b>`
  - `python3 -m lps.cli validate <path>`
- Phase 0 is complete:
  - local workspace initialization exists
  - canonical profile schema v1 exists
  - profile read/write helpers exist
  - schema validation tests exist in `tests/test_schema.py`
- Phase 1 ingestion is implemented for:
  - Markdown source files using a documented heading contract
  - manual paste input using labeled sections
- Phase 2 analysis is implemented for:
  - heuristic scoring across clarity, authority, AI signal, leadership signal, and lens fit
  - selected-lens gap analysis for AI, transformation, and consulting positioning
  - saved JSON analysis artifacts under `.lps/analysis/`
- Phase 3 rewrite is implemented for:
  - two deterministic variants per selected lens
  - conservative rewrites for headline, about, and experience entries
  - factuality checklist output and saved JSON artifacts under `.lps/rewrites/`
- Phase 4 versioning is implemented for:
  - saved version snapshots from rewrite artifacts
  - version listing and inspection
  - diff output between any two saved versions
- The current workspace baseline is `.lps/profiles/`, `.lps/analysis/`, `.lps/rewrites/`, and `.lps/versions/`.
- The current product is CLI-only. There is no web UI, remote service, or LinkedIn integration.
- Content generation is planned but not yet implemented.

## Problem Statement
The current LinkedIn profile under-represents actual seniority, scope, and differentiated value. The user needs a repeatable system for evaluating, rewriting, versioning, and extending that profile narrative into posts and outreach without depending on brittle LinkedIn automation.

## Users
- Primary user: the current repo owner, working locally and iterating quickly.
- Secondary user: a future solo operator or engineer who may pick up the repo and continue delivery with minimal onboarding.

## Product Principles
1. Local-first by default.
2. Human-readable artifacts over opaque state.
3. Human approval before narrative changes are adopted.
4. No dependency on LinkedIn APIs or browser automation.
5. One positioning spine reused across profile, posts, and outreach.

## Non-Goals
- LinkedIn automation or bot behavior.
- Bulk scraping or growth-hacking workflows.
- Multi-user collaboration features in MVP.
- Hosted inference or SaaS architecture decisions in MVP.

## Target MVP
The MVP is a local Python CLI workflow that can:
1. Ingest profile source material from paste or Markdown.
2. Normalize that material into the canonical schema.
3. Produce a heuristic analysis report for positioning quality and role fit.
4. Generate rewritten profile variants for multiple positioning lenses.
5. Save versions and diff any two saved variants.
6. Generate narrative-aligned post ideas, post drafts, and outreach drafts from a selected version.

## Locked MVP Defaults
- Positioning lenses are first-class and equal in MVP:
  - AI leadership
  - transformation leadership
  - consulting leadership
- Scoring is heuristic in v1. Calibration loops and learned scoring are post-MVP.
- All durable artifacts stay local and human-readable:
  - JSON for structured data
  - Markdown for rich reports or narrative artifacts
  - plain text where formatting is unnecessary
- The CLI is the only required interface for MVP.
- Export expectations for v1 are limited to JSON, Markdown, and plain text bundles.

## Canonical Data Model v1
The profile schema remains unchanged for v1:

```json
{
  "headline": "string",
  "about": "string",
  "experience": [
    {
      "title": "string",
      "company": "string",
      "description": "string"
    }
  ]
}
```

This schema is intentionally narrow. It is sufficient for the first ingestion, validation, rewrite, and versioning loops. Additional fields can be added after the MVP proves the core workflow.

## Interfaces

### Implemented CLI Surface
- `python3 -m lps.cli init [--workspace .lps] [--profile-name default]`
  - initializes the local workspace
  - creates a starter profile JSON file
- `python3 -m lps.cli ingest --format <markdown|paste> [--input path] [--workspace .lps] [--profile-name default]`
  - ingests a Markdown or labeled paste source into schema v1
  - writes the resulting profile JSON to `.lps/profiles/`
- `python3 -m lps.cli analyze <path> --lens <ai|transformation|consulting> [--workspace .lps]`
  - analyzes a validated profile against one positioning lens
  - writes the resulting report JSON to `.lps/analysis/`
- `python3 -m lps.cli rewrite <path> --lens <ai|transformation|consulting> [--workspace .lps]`
  - creates two conservative profile variants for one positioning lens
  - writes the resulting artifact JSON to `.lps/rewrites/`
- `python3 -m lps.cli versions save <rewrite-path> --variant-id <id> [--workspace .lps]`
  - saves one rewrite variant as a named version snapshot
  - writes the resulting version JSON to `.lps/versions/`
- `python3 -m lps.cli versions list [--workspace .lps]`
  - lists saved versions
- `python3 -m lps.cli versions show <version-id> [--workspace .lps]`
  - prints a saved version record
- `python3 -m lps.cli diff <version-a> <version-b> [--workspace .lps]`
  - renders a unified diff between two saved versions
- `python3 -m lps.cli validate <path>`
  - reads a profile JSON document
  - validates it against schema v1

### Planned CLI Surface (Not Yet Implemented)
- `python3 -m lps.cli content`
  - generate post ideas, post drafts, and outreach drafts from a selected version

### Workspace Layout
- Current:
  - `.lps/profiles/`
  - `.lps/analysis/`
  - `.lps/rewrites/`
  - `.lps/versions/`
- Planned additions:
  - `.lps/content/`

## Functional Requirements
- FR1: The system must ingest profile source text from manual paste and Markdown files.
- FR2: The system must normalize and persist parsed content into schema v1 JSON.
- FR3: The system must produce a heuristic analysis report with scores, explanations, weaknesses, and improvements.
- FR4: The system must generate rewritten headline, about, and experience variants for all three positioning lenses.
- FR5: The system must store version metadata and support listing, retrieval, and diffing.
- FR6: The system must generate content artifacts tied to a selected profile version.

## Quality Requirements
- NFR1: Core flows must run locally on a standard Python 3 environment.
- NFR2: The ingest -> analyze -> rewrite loop should complete in under 60 seconds on typical local hardware, excluding optional model latency experiments.
- NFR3: Saved artifacts must remain inspectable and editable without proprietary tooling.
- NFR4: Modules should stay separated enough to support future UI or connector layers without rewriting the core data model.
- NFR5: Rewrite outputs must preserve factual accuracy and avoid unsupported claims.

## Acceptance Criteria

### Ingestion
- User can ingest source material from paste or Markdown in under 3 minutes.
- The output is a valid schema v1 JSON profile saved under the local workspace.
- The current implementation supports documented Markdown and labeled paste contracts through the CLI.

### Analysis
- A single run produces:
  - numeric heuristic scores
  - at least 3 prioritized weaknesses
  - at least 3 suggested improvements
  - explicit gaps relative to a selected positioning lens
  - a saved local analysis artifact under `.lps/analysis/`

### Rewrite
- A single run produces at least 2 credible profile variants.
- Rewrites cover headline, about, and experience entries.
- Variants remain factually grounded and include a review checklist before adoption.
- The current implementation writes a saved rewrite artifact under `.lps/rewrites/`.

### Versioning
- The user can save, list, open, and diff any two versions.
- Saved metadata is sufficient to understand how a version was produced.
- The current implementation saves version artifacts under `.lps/versions/`.

### Content Generation
- A single run produces at least:
  - 10 post ideas
  - 3 post drafts
  - 3 outreach drafts
- Outputs stay aligned with the selected profile version and positioning lens.

## Success Criteria
- The user adopts a rewritten profile in actual LinkedIn usage.
- The user can generate 2 or more strong profile variants with low friction.
- The user can produce consistent posts and outreach from the same narrative spine without rebuilding context each time.

## Post-MVP Considerations
- Lightweight UI for local review workflows.
- Feedback loops for improving heuristic scoring over time.
- Broader export bundles or publishing helpers.
- Performance tracking across versions and generated content.
