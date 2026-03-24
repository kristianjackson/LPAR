"""Profile schema and validation helpers for LPS."""

from __future__ import annotations

from typing import Any

REQUIRED_TOP_LEVEL_FIELDS = ("headline", "about", "experience")
REQUIRED_EXPERIENCE_FIELDS = ("title", "company", "description")


def empty_profile() -> dict[str, Any]:
    """Return a canonical empty profile object."""
    return {
        "headline": "",
        "about": "",
        "experience": [],
    }


def validate_profile(profile: dict[str, Any]) -> list[str]:
    """Return a list of validation errors; empty list means valid."""
    errors: list[str] = []

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in profile:
            errors.append(f"Missing top-level field: {field}")

    if "headline" in profile and not isinstance(profile["headline"], str):
        errors.append("Field 'headline' must be a string")

    if "about" in profile and not isinstance(profile["about"], str):
        errors.append("Field 'about' must be a string")

    experience = profile.get("experience")
    if experience is None:
        return errors

    if not isinstance(experience, list):
        errors.append("Field 'experience' must be a list")
        return errors

    for i, item in enumerate(experience):
        if not isinstance(item, dict):
            errors.append(f"experience[{i}] must be an object")
            continue

        for field in REQUIRED_EXPERIENCE_FIELDS:
            if field not in item:
                errors.append(f"experience[{i}] missing field: {field}")
            elif not isinstance(item[field], str):
                errors.append(f"experience[{i}].{field} must be a string")

    return errors
