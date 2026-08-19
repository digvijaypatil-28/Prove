import json
import re
from typing import Any, Dict, Optional

def clean_json_string(text: str) -> str:
    """Removes markdown code blocks and trims whitespace from JSON strings."""
    if not text:
        return "{}"
    text = text.strip()
    # Remove markdown code block fences if present
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text

def parse_json_safely(text: str) -> Optional[Dict[str, Any]]:
    """Attempts to parse JSON from text safely."""
    cleaned = clean_json_string(text)
    try:
        return json.loads(cleaned)
    except Exception:
        # Match JSON object using regex if surrounded by extra text
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        return None

def normalize_skill_name(skill: str) -> str:
    """Normalizes skill strings for case-insensitive matching."""
    return skill.strip().lower()
