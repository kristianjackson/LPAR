"""Deterministic content generation for LPS."""

from __future__ import annotations

from datetime import datetime, timezone
import re
from typing import Any


NUMBER_PATTERN = re.compile(r"\b\d+(?:\.\d+)?%?\b")

LENS_LANGUAGE = {
    "ai": "AI leadership",
    "transformation": "transformation leadership",
    "consulting": "consulting leadership",
}


def generate_content_bundle(version_record: dict[str, Any]) -> dict[str, Any]:
    """Generate ideas, post drafts, and outreach drafts from a saved version."""
    profile = version_record["profile"]
    lens = version_record["lens"]
    lens_label = version_record["lens_label"]

    headline = profile["headline"]
    about = profile["about"]
    experience = profile["experience"]
    first_role = _role_label(experience[0])
    second_role = _role_label(experience[1]) if len(experience) > 1 else first_role
    first_description = _first_sentence(experience[0]["description"])
    second_description = _first_sentence(experience[1]["description"]) if len(experience) > 1 else first_description
    metric = _first_metric([headline, about, *(item["description"] for item in experience)])

    ideas = [
        f"What {lens_label.lower()} looks like after the pilot stage",
        f"How I frame {lens_label.lower()} work so it sounds like an operating capability, not a buzzword",
        f"The lesson from {first_role} that still shapes how I lead programs",
        f"What {metric} taught me about translating strategy into execution",
        f"Why adoption matters more than demos in {lens_label.lower()} work",
        f"The difference between a strong {lens_label.lower()} narrative and a generic one",
        f"What changed in my approach after {second_role}",
        f"How to surface seniority in a headline without sounding inflated",
        f"The review checklist I use before sharing a new {lens_label.lower()} variant",
        f"The questions I ask before I take on a new {lens_label.lower()} mandate",
    ]

    post_drafts = [
        {
            "id": "post-1",
            "label": "Point of view",
            "text": (
                f"Most teams talk about {lens_label.lower()} as if the hard part is choosing the right initiative.\n\n"
                f"In practice, the harder part is turning that choice into execution, adoption, and repeatable outcomes.\n\n"
                f"My current narrative is anchored in work like {first_role}, where {first_description.lower()}\n\n"
                "That is the bar I want my profile and my content to clear every time."
            ),
        },
        {
            "id": "post-2",
            "label": "Case study",
            "text": (
                f"One pattern I keep seeing: language gets sharper when it is anchored in delivery evidence.\n\n"
                f"In {first_role}, {first_description.lower()}\n\n"
                f"In {second_role}, {second_description.lower()}\n\n"
                "That is the shift from generic positioning to credible positioning."
            ),
        },
        {
            "id": "post-3",
            "label": "Checklist",
            "text": (
                f"Three checks I now use before publishing a new {lens_label.lower()} narrative:\n"
                "1. Does the headline name the lane clearly?\n"
                "2. Does the about section prove scope and outcomes?\n"
                "3. Does each role description show what changed because of the work?\n\n"
                "That simple pass removes a surprising amount of generic language."
            ),
        },
    ]

    outreach_drafts = [
        {
            "id": "outreach-1",
            "label": "Hiring manager intro",
            "text": (
                f"Hi <name>, I am exploring {lens_label.lower()} opportunities where strategy, delivery, and adoption need to stay connected. "
                f"My recent work includes {first_role}, where {first_description.lower()} If that is relevant to your team, I would be glad to compare notes."
            ),
        },
        {
            "id": "outreach-2",
            "label": "Peer reconnect",
            "text": (
                f"Hi <name>, I have been sharpening my {lens_label.lower()} narrative and thought of you. "
                f"A lot of it comes back to lessons from {second_role}, especially around how to turn positioning into operating results. "
                "Would be interested in hearing what you are seeing on your side as well."
            ),
        },
        {
            "id": "outreach-3",
            "label": "Advisory note",
            "text": (
                f"Hi <name>, I work across {LENS_LANGUAGE[lens]} themes where the challenge is less about the idea and more about execution quality. "
                f"Work like {first_role} has made me especially interested in teams that need clear operating change, credible delivery, and measurable outcomes. "
                "If that is a current priority for you, I would be happy to continue the conversation."
            ),
        },
    ]

    return {
        "artifact_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_version": version_record["version_id"],
        "lens": lens,
        "lens_label": lens_label,
        "ideas": ideas,
        "post_drafts": post_drafts,
        "outreach_drafts": outreach_drafts,
        "source_highlights": {
            "headline": headline,
            "about_focus": _first_sentence(about),
            "roles": [_role_label(item) for item in experience],
        },
    }


def _role_label(item: dict[str, Any]) -> str:
    return f"{item['title']} at {item['company']}"


def _first_sentence(text: str) -> str:
    normalized = " ".join(text.strip().split())
    if not normalized:
        return ""

    match = re.search(r"(?<=[.!?])\s", normalized)
    if match:
        return normalized[: match.start()].strip()
    return normalized


def _first_metric(text_blocks: list[str]) -> str:
    for block in text_blocks:
        match = NUMBER_PATTERN.search(block)
        if match:
            return match.group(0)
    return "stronger operating results"
