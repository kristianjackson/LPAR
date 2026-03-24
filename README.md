# LinkedIn Positioning System (LPS)

Local-first tooling for profile ingestion, analysis, rewriting, versioning, and narrative-aligned content generation.

## Current status
Phase 0 is complete and Phase 1 ingestion is now available:
- Local workspace initialization
- Canonical profile schema shape
- Profile validation command
- Markdown ingestion command
- Manual paste ingestion command

## Development setup
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

## Quickstart
```bash
.venv/bin/python -m lps.cli init
.venv/bin/python -m lps.cli ingest --format markdown --input tests/fixtures/sample_profile.md --profile-name sample
.venv/bin/python -m lps.cli analyze .lps/profiles/sample.json --lens ai
.venv/bin/python -m lps.cli validate .lps/profiles/sample.json
```

## Analysis
The `analyze` command reads a profile JSON file, scores it against one positioning lens, and writes a saved report to `.lps/analysis/`.

Supported lenses:
- `ai`
- `transformation`
- `consulting`

## Ingestion formats

### Markdown
Use top-level `#` headings for the core sections and `## Title | Company` entries inside `# Experience`.

```md
# Headline
AI Transformation Leader

# About
I build AI products and lead operating change.

# Experience
## Director, AI | ExampleCorp
Led AI strategy and execution across product and delivery teams.
```

### Manual paste
Use labeled sections with one experience entry per line.

```text
Headline: AI Transformation Leader
About:
I build AI products and lead operating change.

Experience:
- Director, AI | ExampleCorp | Led AI strategy and execution across product and delivery teams.
```
