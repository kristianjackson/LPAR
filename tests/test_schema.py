from lps.schema import validate_profile


def test_validate_profile_accepts_minimal_valid_profile() -> None:
    errors = validate_profile(
        {
            "headline": "AI Transformation Leader",
            "about": "I build AI products.",
            "experience": [
                {
                    "title": "Director, AI",
                    "company": "ExampleCorp",
                    "description": "Led AI strategy and execution.",
                }
            ],
        }
    )

    assert errors == []


def test_validate_profile_rejects_missing_fields() -> None:
    errors = validate_profile({"headline": "x"})

    assert "Missing top-level field: about" in errors
    assert "Missing top-level field: experience" in errors
