"""Deterministic rewrite helpers for LPS."""

from __future__ import annotations

from datetime import datetime, timezone
import re
from typing import Any


NUMBER_PATTERN = re.compile(r"\b\d+(?:\.\d+)?%?\b")

LENS_REWRITE_CONFIG = {
    "ai": {
        "label": "AI leadership",
        "headline_prefix": "AI Leadership",
        "headline_suffix": "Strategy, Delivery, and Adoption",
        "primary_opener": "I lead AI strategy, delivery, and adoption with a clear operating lens.",
        "secondary_opener": "I turn AI initiatives into execution, adoption, and measurable business outcomes.",
        "factuality_terms": ("ai leadership", "strategy", "adoption"),
    },
    "transformation": {
        "label": "Transformation leadership",
        "headline_prefix": "Transformation Leadership",
        "headline_suffix": "Operating Model, Delivery, and Change",
        "primary_opener": "I lead transformation work that connects strategy, delivery, and operating change.",
        "secondary_opener": "I turn complex programs into usable operating shifts with measurable results.",
        "factuality_terms": ("transformation", "operating model", "change"),
    },
    "consulting": {
        "label": "Consulting leadership",
        "headline_prefix": "Consulting Leadership",
        "headline_suffix": "Advisory, Clients, and Delivery",
        "primary_opener": "I lead client-facing work that translates strategy into shipped outcomes and trusted execution.",
        "secondary_opener": "I bring advisory judgment, delivery rigor, and stakeholder alignment to complex programs.",
        "factuality_terms": ("consulting", "advisory", "clients"),
    },
}


def rewrite_profile(
    profile: dict[str, Any],
    lens: str,
    source_profile: str,
) -> dict[str, Any]:
    """Create deterministic profile variants for the selected lens."""
    if lens not in LENS_REWRITE_CONFIG:
        raise ValueError(f"Unsupported lens: {lens}")

    config = LENS_REWRITE_CONFIG[lens]
    role_summaries = _build_role_summaries(profile["experience"])
    source_text = "\n".join(
        [
            str(profile["headline"]),
            str(profile["about"]),
            *[str(item["description"]) for item in profile["experience"]],
        ]
    ).lower()

    variants = [
        {
            "id": f"{lens}-core",
            "label": f"{config['label']} core",
            "profile": {
                "headline": _merge_headline(config["headline_prefix"], str(profile["headline"])),
                "about": _build_about_variant(
                    str(profile["about"]),
                    config["primary_opener"],
                    role_summaries,
                ),
                "experience": [
                    {
                        "title": str(item["title"]),
                        "company": str(item["company"]),
                        "description": _rewrite_experience_core(item),
                    }
                    for item in profile["experience"]
                ],
            },
        },
        {
            "id": f"{lens}-operator",
            "label": f"{config['label']} operator",
            "profile": {
                "headline": _append_headline_suffix(str(profile["headline"]), config["headline_suffix"]),
                "about": _build_about_variant(
                    str(profile["about"]),
                    config["secondary_opener"],
                    role_summaries,
                ),
                "experience": [
                    {
                        "title": str(item["title"]),
                        "company": str(item["company"]),
                        "description": _rewrite_experience_operator(item),
                    }
                    for item in profile["experience"]
                ],
            },
        },
    ]

    introduced_terms = [term for term in config["factuality_terms"] if term not in source_text]
    metrics = NUMBER_PATTERN.findall(source_text)

    return {
        "artifact_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_profile": source_profile,
        "lens": lens,
        "lens_label": config["label"],
        "variants": variants,
        "factuality_checklist": _build_factuality_checklist(
            profile,
            lens,
            introduced_terms,
            metrics,
        ),
        "source_evidence": {
            "titles": [str(item["title"]) for item in profile["experience"]],
            "companies": [str(item["company"]) for item in profile["experience"]],
            "metrics": metrics,
        },
    }


def _merge_headline(prefix: str, source_headline: str) -> str:
    if prefix.lower() in source_headline.lower():
        return source_headline
    return f"{prefix} | {source_headline}"


def _append_headline_suffix(source_headline: str, suffix: str) -> str:
    if suffix.lower() in source_headline.lower():
        return source_headline
    return f"{source_headline} | {suffix}"


def _build_about_variant(source_about: str, opener: str, role_summaries: list[str]) -> str:
    evidence = "Recent examples include " + "; ".join(role_summaries[:2])
    return " ".join(part for part in (opener, _ensure_sentence(source_about), evidence) if part).strip()


def _build_role_summaries(experience: list[dict[str, Any]]) -> list[str]:
    summaries: list[str] = []
    for item in experience:
        title = str(item["title"])
        company = str(item["company"])
        description = _ensure_sentence(str(item["description"]))
        summaries.append(f"{title} at {company}: {description}")
    return summaries


def _rewrite_experience_core(item: dict[str, Any]) -> str:
    return f"{item['title']} at {item['company']}: {_ensure_sentence(str(item['description']))}"


def _rewrite_experience_operator(item: dict[str, Any]) -> str:
    return (
        f"At {item['company']}, as {item['title']}, "
        f"{_lowercase_first(_ensure_sentence(str(item['description'])))}"
    )


def _build_factuality_checklist(
    profile: dict[str, Any],
    lens: str,
    introduced_terms: list[str],
    metrics: list[str],
) -> list[str]:
    checklist = [
        "Verify every rewritten headline, about sentence, and experience entry against the source profile before publishing.",
        f"Confirm that the selected lens ({LENS_REWRITE_CONFIG[lens]['label']}) is genuinely supported by your experience and target role.",
        "Check that company names, titles, and chronology still match the source profile exactly.",
    ]

    if metrics:
        checklist.append(
            "Verify that every metric used in the rewrite already appears in the source profile: "
            + ", ".join(metrics)
            + "."
        )
    else:
        checklist.append(
            "No source metrics were detected. Avoid adding any numbers or scale claims unless you can verify them."
        )

    if introduced_terms:
        checklist.append(
            "Review the added positioning language and remove anything not fully supported by the source profile: "
            + ", ".join(introduced_terms)
            + "."
        )

    if len(profile["experience"]) < 2:
        checklist.append(
            "The source profile has limited role breadth, so avoid overstating the span or duration of leadership experience."
        )

    return checklist


def _ensure_sentence(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return ""
    if stripped.endswith((".", "!", "?")):
        return stripped
    return stripped + "."


def _lowercase_first(text: str) -> str:
    if not text:
        return text
    return text[:1].lower() + text[1:]
