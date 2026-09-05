#!/usr/bin/env python3
"""Flag MCP tool descriptions too weak for an LLM to route on reliably.

Scans every workflow JSON file under artifacts/ for a Request trigger,
checks its description and its Request Body JSON Schema, and flags:
  - missing or very short trigger descriptions
  - a description with no imperative "when to use" framing
  - schema properties missing a `description`
  - a schema with no `required` array

Exit code is non-zero if any *_shipped_ artifact (i.e. not inside a
broken/ folder, which is supposed to demonstrate bad descriptions) fails.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MIN_DESCRIPTION_WORDS = 15
WHEN_TO_USE_HINTS = ("call this", "use this", "use it when", "when to use", "do not use", "do not call")

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = REPO_ROOT / "artifacts"


def find_workflow_files() -> list[Path]:
    return sorted(ARTIFACTS_DIR.rglob("*.json"))


def is_broken_example(path: Path) -> bool:
    return "broken" in path.parts


def lint_trigger(trigger_name: str, trigger: dict, path: Path) -> list[str]:
    issues = []
    description = trigger.get("description", "") or ""
    word_count = len(description.split())

    if not description:
        issues.append(f"trigger '{trigger_name}' has no description at all")
    elif word_count < MIN_DESCRIPTION_WORDS:
        issues.append(
            f"trigger '{trigger_name}' description is only {word_count} words "
            f"(minimum {MIN_DESCRIPTION_WORDS}) — too short for an LLM to route on reliably"
        )
    elif not any(hint in description.lower() for hint in WHEN_TO_USE_HINTS):
        issues.append(
            f"trigger '{trigger_name}' description has no explicit \"when to use / call this\" framing — "
            "state the trigger condition as an imperative, not just a fact"
        )

    schema = trigger.get("inputs", {}).get("schema", {})
    properties = schema.get("properties", {})
    required = schema.get("required")

    if properties and required is None:
        issues.append(f"trigger '{trigger_name}' schema has properties but no 'required' array")

    for prop_name, prop in properties.items():
        if not prop.get("description"):
            issues.append(f"trigger '{trigger_name}' schema property '{prop_name}' has no description")

    return issues


def lint_file(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []

    definition = data.get("definition")
    if not isinstance(definition, dict):
        return []

    triggers = definition.get("triggers", {})
    issues = []
    for trigger_name, trigger in triggers.items():
        if trigger.get("type") != "Request":
            continue
        issues.extend(lint_trigger(trigger_name, trigger, path))
    return issues


def main() -> int:
    files = find_workflow_files()
    if not files:
        print("No workflow JSON files found under artifacts/ — nothing to lint.")
        return 0

    had_real_failure = False
    for path in files:
        issues = lint_file(path)
        if not issues:
            continue

        rel = path.relative_to(REPO_ROOT)
        broken = is_broken_example(path)
        label = "INFO (expected — broken/ example)" if broken else "FAIL"
        print(f"\n{label}: {rel}")
        for issue in issues:
            print(f"  - {issue}")

        if not broken:
            had_real_failure = True

    if had_real_failure:
        print("\nOne or more shipped artifacts have weak tool descriptions. Fix before merging.")
        return 1

    print("\nAll shipped artifacts pass the description linter.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
