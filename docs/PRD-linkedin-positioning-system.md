# Product Requirements Document (PRD)

## Product Name
**LinkedIn Positioning System (LPS)**  
_Working name; can be changed later._

## Problem Statement
Current LinkedIn presence under-represents true seniority and impact, and lacks a repeatable process for iteration or experimentation.

### Current pain points
- Profile under-signals actual level and scope.
- Profile is static; there is no deliberate experimentation loop.
- Messaging is not clearly aligned to target roles (AI leadership, transformation leadership, consulting leadership).

### Platform constraints
- LinkedIn is not automation-friendly.
- Building directly against LinkedIn APIs or unstable UI flows introduces fragility.

## Solution Overview
A **local-first, AI-powered positioning system** that:
1. Ingests profile content.
2. Analyzes strengths, weaknesses, and role-fit.
3. Rewrites profile sections for stronger impact.
4. Tracks versions and diffs over time.
5. Generates content (posts + outreach) aligned to the same narrative.

> The system must provide core value without any dependency on LinkedIn APIs.

## Core Objectives
1. **Clarity**  
   Profile communicates seniority, scope, and value within 10 seconds.
2. **Positioning**  
   Align narrative to target archetypes (e.g., AI leader, transformation leader, consultant).
3. **Iteration**  
   Enable rapid versioning and experimentation across profile variants.
4. **Leverage**  
   Reuse positioning foundation to generate posts and outreach with consistent voice.

## Non-Goals
- Full LinkedIn automation bot.
- DM automation workflows.
- Scraping other profiles at scale.
- Growth-hacking/spam behavior.

## Users
- **Primary user:** current owner/operator (single user, local use).
- **Secondary user:** future productized users with similar career-positioning needs.

## MVP Scope

### 1) Profile Ingestion
**Inputs**
- Manual paste.
- Markdown import.

**Parsed structure**
- Headline.
- About section.
- Experience entries.

**MVP acceptance criteria**
- User can ingest source profile in <3 minutes.
- Parser outputs valid structured profile object for all three core sections.

### 2) Analysis Engine
**Outputs**
- Numeric scores (e.g., clarity, authority, AI signal, leadership signal).
- Key weaknesses.
- Positioning gaps relative to selected target role.

**MVP acceptance criteria**
- User receives actionable analysis report in one run.
- At least 3 prioritized weaknesses and 3 suggested improvements are produced.

### 3) Rewrite Engine
**Outputs**
- Improved headline.
- Improved About section.
- Rewritten experience entries.
- Multiple variants by positioning lens (AI-focused, consulting-focused, transformation-focused).

**MVP acceptance criteria**
- Generate at least 2 high-quality variants per run.
- Variants preserve factual accuracy while improving positioning strength.

### 4) Versioning
**Capabilities**
- Save multiple profile versions.
- Compare diffs between versions.
- Track metadata (timestamp, target role, model prompt/profile context).

**MVP acceptance criteria**
- User can list, open, and diff any two versions.
- Rewrites are reproducible from saved metadata.

### 5) Content Generator
**Outputs**
- Post ideas.
- Short-form post drafts.
- Outreach messages.

**MVP acceptance criteria**
- Generate at least 10 post ideas tied to selected profile variant.
- Generate at least 3 usable post drafts and 3 outreach drafts per run.

## Success Criteria
- Rewritten profile is actually deployed/used.
- User can generate 2–3 high-quality profile variants quickly.
- User can produce posts consistently without high cognitive load.

## Product Principles
1. **Local-first by default**: user data remains local unless explicitly exported.
2. **Narrative consistency**: profile and content outputs share a coherent positioning spine.
3. **Human-in-the-loop**: AI proposes; user approves final wording.
4. **No brittle automation dependency**: utility should remain independent of LinkedIn API availability.

## Functional Requirements
- FR1: System must ingest profile text from paste or markdown file.
- FR2: System must parse and persist structured profile data.
- FR3: System must produce an analysis report with scores + explanations.
- FR4: System must generate role-specific rewrites for core profile sections.
- FR5: System must maintain version history and provide diff view.
- FR6: System must generate content artifacts from selected profile version.

## Quality Requirements (Non-Functional)
- NFR1: Local execution supported for core flows.
- NFR2: End-to-end run (ingest → analyze → rewrite) should complete in under 60 seconds on typical local hardware.
- NFR3: Version data must be durable and human-readable (e.g., JSON/Markdown).
- NFR4: System should be modular to support future connectors and UI layers.

## Risks and Mitigations
- **Risk:** Hallucinated or embellished claims in rewrites.  
  **Mitigation:** Add factuality guardrails + “claim verification checklist” before finalizing.
- **Risk:** Generic outputs lacking differentiation.  
  **Mitigation:** Force inclusion of specific impact metrics and leadership evidence when available.
- **Risk:** Overfitting to one target role.  
  **Mitigation:** Maintain explicit multi-variant strategy and side-by-side comparison.

## Open Questions
1. Which target role taxonomy should be first-class in MVP (AI, transformation, consulting, or all three equally)?
2. Should scoring be purely heuristic in MVP, or calibrated over time with user feedback?
3. What export formats are required in v1 (Markdown, plain text, JSON bundles)?

## Proposed Milestones
- **Milestone 1:** Ingestion + parsing + schema.
- **Milestone 2:** Analysis engine + scoring rubric.
- **Milestone 3:** Rewrite engine + role variants.
- **Milestone 4:** Version store + diff tooling.
- **Milestone 5:** Content generator + templates.

## Definition of Done (MVP)
MVP is complete when one user can:
1. Import existing profile.
2. Receive clear analysis and prioritized gaps.
3. Generate at least two strong, role-aligned rewrites.
4. Save, compare, and select a version.
5. Generate ready-to-edit posts and outreach from that version.
