"""Heuristic analysis engine for LPS."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Any


WORD_PATTERN = re.compile(r"\b[\w%+-]+\b")
NUMBER_PATTERN = re.compile(r"\b\d+(?:\.\d+)?%?\b")

IMPACT_KEYWORDS = (
    "led",
    "built",
    "scaled",
    "delivered",
    "launched",
    "grew",
    "transformed",
    "improved",
    "reduced",
    "increased",
    "created",
    "owned",
    "drove",
    "advised",
)

GENERIC_KEYWORDS = (
    "experienced",
    "results-driven",
    "passionate",
    "proven",
    "responsible",
    "worked",
    "various",
    "many",
    "helped",
)

LEADERSHIP_KEYWORDS = (
    "lead",
    "led",
    "leadership",
    "managed",
    "manager",
    "director",
    "head",
    "executive",
    "strategy",
    "strategic",
    "stakeholder",
    "stakeholders",
    "mentor",
    "coached",
)

AI_KEYWORDS = (
    "ai",
    "artificial intelligence",
    "ml",
    "machine learning",
    "llm",
    "model",
    "models",
    "data",
    "automation",
    "agent",
    "agents",
)

TRANSFORMATION_KEYWORDS = (
    "transformation",
    "operating model",
    "change",
    "modernization",
    "adoption",
    "program",
    "programs",
    "roadmap",
    "delivery",
    "execution",
)

CONSULTING_KEYWORDS = (
    "consulting",
    "consultant",
    "advisory",
    "advisor",
    "client",
    "clients",
    "engagement",
    "stakeholder",
    "stakeholders",
    "workshop",
    "enterprise",
    "partner",
    "partners",
)

LENS_RULES = {
    "ai": {
        "label": "AI leadership",
        "keywords": AI_KEYWORDS,
        "gap_checks": (
            (
                lambda signals: signals["lens_keyword_counts"]["ai"] < 3,
                "AI signal is too light for an AI leadership profile.",
                "Name the AI platforms, models, automation programs, or data work you actually own.",
                92,
            ),
            (
                lambda signals: not signals["headline_lens_matches"]["ai"],
                "The headline does not surface AI leadership early enough.",
                "Add AI language to the headline so the target lane is obvious within the first line.",
                86,
            ),
            (
                lambda signals: signals["metric_count"] == 0,
                "AI claims are not backed by quantified delivery or adoption outcomes.",
                "Add metrics that show shipped systems, adoption, efficiency gains, or business impact.",
                80,
            ),
        ),
    },
    "transformation": {
        "label": "Transformation leadership",
        "keywords": TRANSFORMATION_KEYWORDS,
        "gap_checks": (
            (
                lambda signals: signals["lens_keyword_counts"]["transformation"] < 3,
                "Transformation language is too thin for a transformation leadership profile.",
                "Make change leadership, operating model work, and delivery transformation explicit.",
                92,
            ),
            (
                lambda signals: not signals["headline_lens_matches"]["transformation"],
                "The headline does not immediately signal transformation ownership.",
                "Add transformation, operating model, or change execution language to the headline.",
                86,
            ),
            (
                lambda signals: signals["leadership_keyword_count"] < 2,
                "The profile does not show enough operating scope or leadership signal for transformation work.",
                "Call out the teams, functions, or programs you led through change.",
                80,
            ),
        ),
    },
    "consulting": {
        "label": "Consulting leadership",
        "keywords": CONSULTING_KEYWORDS,
        "gap_checks": (
            (
                lambda signals: signals["lens_keyword_counts"]["consulting"] < 3,
                "Consulting or advisory signal is too light for a consulting-oriented profile.",
                "Make advisory, client, stakeholder, and enterprise engagement work more explicit.",
                92,
            ),
            (
                lambda signals: not signals["headline_lens_matches"]["consulting"],
                "The headline does not surface consulting or advisory positioning.",
                "Add consulting, advisory, or client-facing language to the headline.",
                86,
            ),
            (
                lambda signals: signals["metric_count"] == 0,
                "Consulting impact is not grounded in measurable outcomes.",
                "Add client outcomes, program scale, or measurable business results to the profile.",
                80,
            ),
        ),
    },
}


@dataclass(frozen=True)
class Finding:
    priority: int
    weakness: str
    improvement: str


def analyze_profile(
    profile: dict[str, Any],
    lens: str,
    source_profile: str,
) -> dict[str, Any]:
    """Produce a heuristic analysis report for the selected positioning lens."""
    if lens not in LENS_RULES:
        raise ValueError(f"Unsupported lens: {lens}")

    signals = _extract_signals(profile)
    scores = {
        "clarity": _score_clarity(signals),
        "authority": _score_authority(signals),
        "ai_signal": _score_ai_signal(signals),
        "leadership_signal": _score_leadership_signal(signals),
        "lens_fit": _score_lens_fit(signals, lens),
    }
    overall_score = round(sum(scores.values()) / len(scores))
    lens_gaps, gap_findings = _build_lens_gaps(signals, lens)
    findings = _build_findings(signals, lens, gap_findings)

    return {
        "artifact_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_profile": source_profile,
        "lens": lens,
        "lens_label": LENS_RULES[lens]["label"],
        "scores": scores,
        "overall_score": overall_score,
        "score_explanations": _build_score_explanations(signals, lens),
        "weaknesses": [finding.weakness for finding in findings],
        "improvements": [finding.improvement for finding in findings],
        "lens_gaps": lens_gaps,
        "evidence": {
            "headline_words": signals["headline_words"],
            "about_words": signals["about_words"],
            "experience_count": signals["experience_count"],
            "average_experience_words": signals["average_experience_words"],
            "metric_count": signals["metric_count"],
            "impact_keyword_count": signals["impact_keyword_count"],
            "generic_keyword_count": signals["generic_keyword_count"],
            "leadership_keyword_count": signals["leadership_keyword_count"],
            "lens_keyword_counts": signals["lens_keyword_counts"],
        },
    }


def _extract_signals(profile: dict[str, Any]) -> dict[str, Any]:
    headline = str(profile["headline"])
    about = str(profile["about"])
    experiences = profile["experience"]
    experience_descriptions = [str(item["description"]) for item in experiences]
    full_text = "\n".join([headline, about, *experience_descriptions])
    headline_words = _count_words(headline)
    about_words = _count_words(about)
    experience_word_counts = [_count_words(description) for description in experience_descriptions]

    return {
        "headline_words": headline_words,
        "about_words": about_words,
        "experience_count": len(experiences),
        "average_experience_words": round(sum(experience_word_counts) / len(experience_word_counts))
        if experience_word_counts
        else 0,
        "metric_count": len(NUMBER_PATTERN.findall(full_text)),
        "impact_keyword_count": _count_keyword_matches(full_text, IMPACT_KEYWORDS),
        "generic_keyword_count": _count_keyword_matches(full_text, GENERIC_KEYWORDS),
        "leadership_keyword_count": _count_keyword_matches(full_text, LEADERSHIP_KEYWORDS),
        "lens_keyword_counts": {
            "ai": _count_keyword_matches(full_text, AI_KEYWORDS),
            "transformation": _count_keyword_matches(full_text, TRANSFORMATION_KEYWORDS),
            "consulting": _count_keyword_matches(full_text, CONSULTING_KEYWORDS),
        },
        "headline_lens_matches": {
            "ai": _count_keyword_matches(headline, AI_KEYWORDS) > 0,
            "transformation": _count_keyword_matches(headline, TRANSFORMATION_KEYWORDS) > 0,
            "consulting": _count_keyword_matches(headline, CONSULTING_KEYWORDS) > 0,
        },
    }


def _score_clarity(signals: dict[str, Any]) -> int:
    score = 20

    if 6 <= signals["headline_words"] <= 14:
        score += 25
    elif 4 <= signals["headline_words"] <= 18:
        score += 15

    if 35 <= signals["about_words"] <= 120:
        score += 25
    elif 20 <= signals["about_words"] <= 160:
        score += 15

    if signals["experience_count"] >= 2:
        score += 10

    if signals["average_experience_words"] >= 12:
        score += 10

    if signals["generic_keyword_count"] == 0:
        score += 10
    elif signals["generic_keyword_count"] <= 2:
        score += 5

    return min(score, 100)


def _score_authority(signals: dict[str, Any]) -> int:
    score = 10
    score += min(signals["metric_count"] * 12, 36)
    score += min(signals["impact_keyword_count"] * 7, 28)
    score += min(signals["leadership_keyword_count"] * 5, 16)

    if signals["experience_count"] >= 2:
        score += 10

    score -= min(signals["generic_keyword_count"] * 5, 15)
    return max(0, min(score, 100))


def _score_ai_signal(signals: dict[str, Any]) -> int:
    score = signals["lens_keyword_counts"]["ai"] * 18
    if signals["headline_lens_matches"]["ai"]:
        score += 15
    if signals["metric_count"] > 0 and signals["lens_keyword_counts"]["ai"] > 0:
        score += 10
    return min(score, 100)


def _score_leadership_signal(signals: dict[str, Any]) -> int:
    score = signals["leadership_keyword_count"] * 15
    if signals["experience_count"] >= 2:
        score += 10
    if signals["headline_words"] >= 6:
        score += 5
    return min(score, 100)


def _score_lens_fit(signals: dict[str, Any], lens: str) -> int:
    score = signals["lens_keyword_counts"][lens] * 20
    if signals["headline_lens_matches"][lens]:
        score += 15
    if signals["metric_count"] > 0:
        score += 10
    if signals["leadership_keyword_count"] >= 2:
        score += 10
    return min(score, 100)


def _build_score_explanations(signals: dict[str, Any], lens: str) -> dict[str, str]:
    return {
        "clarity": (
            f"Headline length: {signals['headline_words']} words; about length: "
            f"{signals['about_words']} words; experience entries: {signals['experience_count']}."
        ),
        "authority": (
            f"Quantified outcomes found: {signals['metric_count']}; impact terms found: "
            f"{signals['impact_keyword_count']}; leadership terms found: "
            f"{signals['leadership_keyword_count']}."
        ),
        "ai_signal": f"AI-related terms found across the profile: {signals['lens_keyword_counts']['ai']}.",
        "leadership_signal": (
            f"Leadership-related terms found across the profile: {signals['leadership_keyword_count']}."
        ),
        "lens_fit": (
            f"{LENS_RULES[lens]['label']} terms found: {signals['lens_keyword_counts'][lens]}; "
            f"headline match: {signals['headline_lens_matches'][lens]}."
        ),
    }


def _build_lens_gaps(signals: dict[str, Any], lens: str) -> tuple[list[str], list[Finding]]:
    gaps: list[str] = []
    findings: list[Finding] = []

    for predicate, weakness, improvement, priority in LENS_RULES[lens]["gap_checks"]:
        if predicate(signals):
            gaps.append(weakness)
            findings.append(Finding(priority=priority, weakness=weakness, improvement=improvement))

    if not gaps:
        fallback_weakness = (
            f"The profile aligns with {LENS_RULES[lens]['label']}, but the positioning can still be sharper."
        )
        fallback_improvement = (
            "Tighten the headline and about section around the specific role lane you want to win."
        )
        gaps.append(fallback_weakness)
        findings.append(Finding(priority=65, weakness=fallback_weakness, improvement=fallback_improvement))

    return gaps, findings


def _build_findings(signals: dict[str, Any], lens: str, gap_findings: list[Finding]) -> list[Finding]:
    findings: list[Finding] = list(gap_findings)

    if signals["headline_words"] < 6:
        findings.append(
            Finding(
                priority=95,
                weakness="The headline is too short to communicate scope, seniority, and target role.",
                improvement="Expand the headline to include role level, domain, and the outcome you drive.",
            )
        )
    elif signals["headline_words"] > 14:
        findings.append(
            Finding(
                priority=70,
                weakness="The headline is too long to scan quickly.",
                improvement="Tighten the headline so the target role and value proposition land in one line.",
            )
        )

    if signals["about_words"] < 40:
        findings.append(
            Finding(
                priority=90,
                weakness="The about section is too thin to establish a differentiated narrative.",
                improvement="Expand the about section with your leadership scope, domain focus, and signature outcomes.",
            )
        )

    if signals["experience_count"] < 2:
        findings.append(
            Finding(
                priority=88,
                weakness="The profile shows too little experience breadth to support the target level.",
                improvement="Add more role history or more evidence inside existing roles to show sustained senior impact.",
            )
        )

    if signals["average_experience_words"] < 14:
        findings.append(
            Finding(
                priority=82,
                weakness="Experience descriptions are too light to prove scope and outcomes.",
                improvement="Rewrite experience entries to lead with ownership, actions, and measurable outcomes.",
            )
        )

    if signals["metric_count"] == 0:
        findings.append(
            Finding(
                priority=91,
                weakness="The profile lacks quantified impact.",
                improvement="Add specific metrics for scale, revenue, efficiency, adoption, or team scope.",
            )
        )

    if signals["impact_keyword_count"] < 2:
        findings.append(
            Finding(
                priority=78,
                weakness="The profile uses too little outcome-oriented action language.",
                improvement="Use stronger action verbs that show ownership and shipped results.",
            )
        )

    if signals["leadership_keyword_count"] < 2:
        findings.append(
            Finding(
                priority=80,
                weakness="Leadership signal is weaker than the target positioning requires.",
                improvement="Name the teams, functions, stakeholders, or strategy decisions you led.",
            )
        )

    if signals["generic_keyword_count"] > 1:
        findings.append(
            Finding(
                priority=72,
                weakness="Generic résumé language is diluting differentiation.",
                improvement="Replace generic adjectives with concrete domain, scale, and outcome language.",
            )
        )

    fallback_findings = [
        Finding(
            priority=60,
            weakness="The profile could connect the headline and about section more tightly to one positioning spine.",
            improvement="Use the first two sections to repeat the same target-lane story in different levels of detail.",
        ),
        Finding(
            priority=58,
            weakness="The profile could make decision scope clearer.",
            improvement="Mention budget, team size, product surface, or executive audience where that is factual.",
        ),
        Finding(
            priority=55,
            weakness=f"The {LENS_RULES[lens]['label']} narrative could be more explicit in the experience section.",
            improvement="Thread the chosen lens through each role description instead of leaving it only in the headline.",
        ),
    ]

    findings.extend(fallback_findings)
    deduped: list[Finding] = []
    seen: set[str] = set()

    for finding in sorted(findings, key=lambda item: item.priority, reverse=True):
        if finding.weakness in seen:
            continue
        seen.add(finding.weakness)
        deduped.append(finding)
        if len(deduped) == 5:
            break

    return deduped


def _count_words(text: str) -> int:
    return len(WORD_PATTERN.findall(text))


def _count_keyword_matches(text: str, keywords: tuple[str, ...]) -> int:
    normalized = text.lower()
    return sum(len(re.findall(_keyword_pattern(keyword), normalized)) for keyword in keywords)


def _keyword_pattern(keyword: str) -> str:
    return rf"(?<!\w){re.escape(keyword.lower())}(?!\w)"
