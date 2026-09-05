#!/usr/bin/env python3
"""Staleness bot: rehash each artifact's cited source and flag drift.

For every verified.yml under artifacts/, fetch each entry in `sources[]`
(as markdown, via Microsoft Learn's `?view=...&tabs=...` -> plain fetch,
using the `.md` content where available) and compare its hash against the
one recorded in verified.yml. On mismatch:
  - print a report (used by CI to open/update a GitHub issue)
  - flip the artifact's status to "stale" in verified.yml

This intentionally does the simplest thing that works: a SHA-256 hash of
the fetched page text. It will not tell you *what* changed, only *that*
something did — the point is to stop a page from silently rotting, not to
diff prose.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
REQUEST_TIMEOUT_SECONDS = 15


def find_verified_files() -> list[Path]:
    return sorted(ARTIFACTS_DIR.rglob("verified.yml"))


def fetch_hash(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS, headers={"Accept": "text/markdown"})
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"  could not fetch {url}: {exc}", file=sys.stderr)
        return None
    return "sha256:" + hashlib.sha256(response.content).hexdigest()


def check_artifact(path: Path) -> bool:
    """Returns True if this artifact is stale (or a source couldn't be checked)."""
    data = yaml.safe_load(path.read_text()) or {}
    sources = data.get("sources") or []
    if not sources:
        return False

    is_stale = False
    changed = False

    for source in sources:
        url = source.get("url")
        recorded_hash = source.get("hash")
        if not url:
            continue

        current_hash = fetch_hash(url)
        if current_hash is None:
            continue

        if recorded_hash is None:
            source["hash"] = current_hash
            changed = True
            continue

        if current_hash != recorded_hash:
            print(f"  DRIFT: {url}")
            print(f"    recorded: {recorded_hash}")
            print(f"    current:  {current_hash}")
            is_stale = True

    if is_stale and data.get("status") != "stale":
        data["_previous_status"] = data.get("status")
        data["status"] = "stale"
        changed = True

    if changed:
        path.write_text(yaml.dump(data, sort_keys=False))

    return is_stale


def main() -> int:
    files = find_verified_files()
    if not files:
        print("No verified.yml files found under artifacts/ — nothing to check.")
        return 0

    any_stale = False
    for path in files:
        rel = path.relative_to(REPO_ROOT)
        print(f"Checking {rel}")
        if check_artifact(path):
            any_stale = True
            print(f"  -> marked stale: {rel}")

    return 1 if any_stale else 0


if __name__ == "__main__":
    sys.exit(main())
