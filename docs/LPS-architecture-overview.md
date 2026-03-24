# LPS Architecture Overview

## Purpose
Describe the implemented end-to-end CLI pipeline, the artifact model on disk, and the main module boundaries that keep the repo local-first and easy to evolve.

## System Shape
LPS is a single-process Python CLI application. Every workflow step reads and writes local, human-readable artifacts under a workspace directory. There is no service layer, no remote persistence, and no LinkedIn integration.

The current pipeline is:
1. Ingest source material into the canonical profile schema.
2. Analyze the profile against one positioning lens.
3. Rewrite the profile into lens-specific variants.
4. Save selected rewrite variants as version snapshots.
5. Generate content bundles from a selected saved version.

## Module Boundaries

### CLI orchestration
- `lps/cli.py`
- Owns command parsing, user-facing success and error output, and wiring between storage and domain modules.
- Keeps each command thin: validate input, call one domain function, persist artifacts, print a concise result.

### Core schema and storage
- `lps/schema.py`
- Defines the canonical profile schema and validation logic.
- `lps/storage.py`
- Owns workspace initialization and artifact persistence under `.lps/`.

### Pipeline stages
- `lps/ingestion.py`
- Converts Markdown or labeled paste input into schema v1 JSON.
- `lps/analysis.py`
- Produces deterministic heuristic scoring, ranked weaknesses, improvements, and lens gaps.
- `lps/rewrite.py`
- Produces deterministic, conservative profile variants plus a factuality checklist.
- `lps/versioning.py`
- Snapshots rewrite variants into saved versions and renders diffs between versions.
- `lps/content.py`
- Generates ideas, short post drafts, and outreach drafts from a saved version.

## Workspace Layout
All durable state lives under the workspace root, which defaults to `.lps/`.

```text
.lps/
  profiles/
  analysis/
  rewrites/
  versions/
  content/
```

### Artifact contracts
- `profiles/`
- Canonical schema v1 JSON documents.
- `analysis/`
- Heuristic analysis reports keyed by profile stem and lens.
- `rewrites/`
- Rewrite artifacts keyed by profile stem and lens, with two variants and a factuality checklist.
- `versions/`
- Saved version snapshots keyed by stable version IDs.
- `content/`
- Generated content bundles keyed by version ID.

## Data Flow

### 1. Ingestion
- Input:
  - Markdown file with `# Headline`, `# About`, and `# Experience`
  - labeled paste input with `Headline:`, `About:`, and `Experience:`
- Output:
  - one validated profile JSON document in `profiles/`

### 2. Analysis
- Input:
  - one validated profile JSON document
  - one selected lens: `ai`, `transformation`, or `consulting`
- Output:
  - one analysis report in `analysis/`
  - numeric scores and ranked findings used by humans, not by an automated planner

### 3. Rewrite
- Input:
  - one validated profile JSON document
  - one selected lens
- Output:
  - one rewrite artifact in `rewrites/`
  - two deterministic variants plus a factuality checklist

### 4. Versioning
- Input:
  - one rewrite artifact
  - one selected variant ID
- Output:
  - one saved version record in `versions/`
  - diffable profile snapshots with stable IDs

### 5. Content generation
- Input:
  - one saved version record
- Output:
  - one content bundle in `content/`
  - 10 ideas, 3 post drafts, and 3 outreach drafts

## Design Constraints
- Local-first by default: every artifact is readable without proprietary tooling.
- Deterministic first: current rewrite and content stages do not require model access.
- Factuality over fluency: the rewrite stage always emits a review checklist before final adoption.
- Stable artifact boundaries: later enhancements should preserve backward readability for saved versions and downstream content inputs.
- Multi-lens parity: `ai`, `transformation`, and `consulting` are first-class throughout the pipeline.

## Testing Strategy
- Unit and command-level tests cover each stage module.
- An end-to-end smoke test exercises the full pipeline in one temporary workspace.
- The recommended verification path remains:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest -q
```

## Evolution Points
- Rewrite and content quality can later move to a model-backed path if deterministic generation proves too weak.
- Export helpers can be added on top of saved versions and content bundles without changing the earlier pipeline stages.
- A lightweight UI can sit above the current artifact model if the CLI workflow becomes cumbersome.
