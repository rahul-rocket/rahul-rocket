#!/usr/bin/env python3
"""Rewrite the Latest Gists section of README.md from the public gists API.

Called by .github/workflows/gists.yml. Writes only between the
<!--START_SECTION:gists--> and <!--END_SECTION:gists--> markers, and leaves the
file untouched when the rendered list is identical to what is already there, so
the workflow's commit step has nothing to push on a quiet day.

Exits non-zero if the markers are missing or the API call fails, so a broken
section shows as a failed run rather than silently going stale.
"""

from __future__ import annotations

import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

README = pathlib.Path(__file__).resolve().parents[2] / "README.md"
START = "<!--START_SECTION:gists-->"
END = "<!--END_SECTION:gists-->"
EMPTY = "No public gists yet."


def fetch_gists(owner: str, limit: int) -> list[dict]:
    """Return the most recently updated public gists, newest first."""
    # per_page is capped at the API maximum we need; the endpoint already sorts
    # by updated_at descending, so the first `limit` entries are the newest.
    url = f"https://api.github.com/users/{owner}/gists?per_page={limit}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": f"{owner}-profile-readme",
        },
    )

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)

    return payload[:limit]


def describe(gist: dict) -> str:
    """One Markdown list item for a gist: a linked title and its date."""
    # A gist has no name of its own. Its description is optional, so fall back
    # to the first filename, which is what the gist page itself shows.
    description = (gist.get("description") or "").strip()
    if not description:
        files = gist.get("files") or {}
        description = next(iter(files), "Untitled gist")

    # Collapse newlines and escape the two characters that would break the link
    # text if a description happened to contain them.
    title = " ".join(description.split()).replace("[", "\\[").replace("]", "\\]")

    updated = (gist.get("updated_at") or "")[:10]
    suffix = f" — {updated}" if updated else ""
    return f"[{title}]({gist['html_url']}){suffix}"


def render(gists: list[dict]) -> str:
    if not gists:
        return EMPTY
    return "\n".join(f"{n}. {describe(g)}" for n, g in enumerate(gists, start=1))


def main() -> int:
    owner = os.environ.get("OWNER")
    if not owner:
        print("::error::OWNER is not set.", file=sys.stderr)
        return 1

    try:
        limit = int(os.environ.get("MAX_GISTS", "5"))
    except ValueError:
        print("::error::MAX_GISTS must be an integer.", file=sys.stderr)
        return 1

    try:
        gists = fetch_gists(owner, limit)
    except (urllib.error.URLError, json.JSONDecodeError, OSError) as error:
        print(f"::error::Could not read gists for {owner}: {error}", file=sys.stderr)
        return 1

    readme = README.read_text(encoding="utf-8")
    start = readme.find(START)
    end = readme.find(END)
    if start == -1 or end == -1 or end < start:
        print(
            f"::error::{README.name} is missing the {START} / {END} markers.",
            file=sys.stderr,
        )
        return 1

    updated = readme[: start + len(START)] + "\n" + render(gists) + "\n" + readme[end:]
    if updated == readme:
        print(f"::notice::Latest Gists is already up to date ({len(gists)} listed).")
        return 0

    README.write_text(updated, encoding="utf-8")
    print(f"::notice::Latest Gists updated with {len(gists)} entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
