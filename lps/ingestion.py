"""Profile ingestion helpers for LPS."""

from __future__ import annotations

from typing import Any


class IngestionError(ValueError):
    """Raised when ingestion input cannot be parsed into the canonical schema."""


def parse_profile_text(text: str, source_format: str) -> dict[str, Any]:
    """Parse profile content from a supported ingestion format."""
    if source_format == "markdown":
        return parse_markdown_profile(text)
    if source_format == "paste":
        return parse_paste_profile(text)
    raise IngestionError(f"Unsupported source format: {source_format}")


def parse_markdown_profile(text: str) -> dict[str, Any]:
    """Parse profile content from the supported Markdown contract."""
    sections = _parse_markdown_sections(text)
    return {
        "headline": _normalize_inline_text(sections["headline"], "headline"),
        "about": _normalize_block_text(sections["about"], "about"),
        "experience": _parse_markdown_experience(sections["experience"]),
    }


def parse_paste_profile(text: str) -> dict[str, Any]:
    """Parse labeled pasted profile text into the canonical schema."""
    headline: str | None = None
    about_lines: list[str] = []
    experience_lines: list[str] = []
    current_section: str | None = None

    for raw_line in text.splitlines():
        stripped = raw_line.strip()

        if stripped.lower().startswith("headline:"):
            if headline is not None:
                raise IngestionError("Paste format can only contain one 'Headline:' line.")

            headline = stripped.split(":", 1)[1].strip()
            current_section = None
            continue

        if stripped.lower() == "about:":
            current_section = "about"
            continue

        if stripped.lower() == "experience:":
            current_section = "experience"
            continue

        if not stripped:
            if current_section == "about":
                about_lines.append("")
            continue

        if current_section == "about":
            about_lines.append(raw_line)
            continue

        if current_section == "experience":
            experience_lines.append(stripped)
            continue

        raise IngestionError(
            "Paste format must use 'Headline:', 'About:', and 'Experience:' labels."
        )

    if headline is None:
        raise IngestionError("Paste format requires a 'Headline: <text>' line.")

    return {
        "headline": _normalize_inline_text(headline, "headline"),
        "about": _normalize_block_text("\n".join(about_lines), "about"),
        "experience": _parse_paste_experience(experience_lines),
    }


def _parse_markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_section: str | None = None
    current_lines: list[str] = []

    for raw_line in text.splitlines():
        if raw_line.startswith("# "):
            if current_section is not None:
                sections[current_section] = "\n".join(current_lines)

            current_section = raw_line[2:].strip().lower()
            current_lines = []
            continue

        if current_section is None:
            if raw_line.strip():
                raise IngestionError("Markdown input must start with '# Headline'.")
            continue

        current_lines.append(raw_line)

    if current_section is not None:
        sections[current_section] = "\n".join(current_lines)

    for required_section in ("headline", "about", "experience"):
        if required_section not in sections:
            raise IngestionError(
                f"Markdown input is missing the '# {required_section.title()}' section."
            )

    return sections


def _parse_markdown_experience(section_text: str) -> list[dict[str, str]]:
    experiences: list[dict[str, str]] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    for raw_line in section_text.splitlines():
        if raw_line.startswith("## "):
            if current_heading is not None:
                experiences.append(_build_markdown_experience(current_heading, current_lines))

            current_heading = raw_line[3:].strip()
            current_lines = []
            continue

        if current_heading is None:
            if raw_line.strip():
                raise IngestionError(
                    "Markdown experience entries must use '## Title | Company' headings."
                )
            continue

        current_lines.append(raw_line)

    if current_heading is not None:
        experiences.append(_build_markdown_experience(current_heading, current_lines))

    if not experiences:
        raise IngestionError("Markdown input must include at least one experience entry.")

    return experiences


def _build_markdown_experience(heading: str, lines: list[str]) -> dict[str, str]:
    title, company = _split_experience_heading(
        heading, "Markdown experience headings must use '## Title | Company'."
    )
    return {
        "title": title,
        "company": company,
        "description": _normalize_block_text("\n".join(lines), f"{title} description"),
    }


def _parse_paste_experience(lines: list[str]) -> list[dict[str, str]]:
    experiences: list[dict[str, str]] = []

    for line in lines:
        if not line.startswith("- "):
            raise IngestionError(
                "Paste experience lines must use '- Title | Company | Description'."
            )

        parts = [part.strip() for part in line[2:].split("|", 2)]
        if len(parts) != 3 or any(not part for part in parts):
            raise IngestionError(
                "Paste experience lines must use '- Title | Company | Description'."
            )

        experiences.append(
            {
                "title": parts[0],
                "company": parts[1],
                "description": parts[2],
            }
        )

    if not experiences:
        raise IngestionError("Paste input must include at least one experience entry.")

    return experiences


def _split_experience_heading(heading: str, error_message: str) -> tuple[str, str]:
    parts = [part.strip() for part in heading.split("|", 1)]
    if len(parts) != 2 or any(not part for part in parts):
        raise IngestionError(error_message)
    return parts[0], parts[1]


def _normalize_inline_text(text: str, field_name: str) -> str:
    normalized = " ".join(line.strip() for line in text.splitlines() if line.strip())
    if not normalized:
        raise IngestionError(f"The {field_name} field cannot be empty.")
    return normalized


def _normalize_block_text(text: str, field_name: str) -> str:
    lines = [line.strip() for line in text.splitlines()]

    while lines and not lines[0]:
        lines.pop(0)

    while lines and not lines[-1]:
        lines.pop()

    normalized_lines: list[str] = []
    previous_blank = False

    for line in lines:
        if line:
            normalized_lines.append(line)
            previous_blank = False
            continue

        if not previous_blank:
            normalized_lines.append("")
        previous_blank = True

    normalized = "\n".join(normalized_lines).strip()
    if not normalized:
        raise IngestionError(f"The {field_name} field cannot be empty.")
    return normalized
