#!/usr/bin/env python3
"""Publish every Markdown file under gists/ to gist.github.com.

Each file becomes one public gist. The mapping from repository path to gist ID
is recorded in gists/published.json and committed back, so a second run updates
the gists it created the first time instead of creating duplicates.

Standard library only, and no third-party action: the same reasoning that
applied to the old update_gists.py holds here, and this job runs with a token
that can write to the account's gists, so keeping it off the supply chain
matters more, not less.

Environment:
  GIST_TOKEN  A classic PAT with the `gist` scope. The built-in GITHUB_TOKEN
              cannot create gists — it is scoped to this repository, and gists
              are account-level. This is the one input that must be a secret
              you create by hand.
  DRY_RUN     "true" to log what would happen and call nothing.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.github.com"
GIST_DIR = Path("gists")
REGISTRY = GIST_DIR / "published.json"

# gists/README.md is the index for humans reading the repository. It links to
# paths inside the repo, which would be broken links inside a gist.
EXCLUDE = {"README.md"}


def die(message: str) -> None:
    print(f"::error::{message}", file=sys.stderr)
    sys.exit(1)


def request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(f"{API}{path}", data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "rahul-rocket-gist-publisher")
    if body is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read() or "{}")


def describe(text: str, fallback: str) -> str:
    """Use the file's first H1 as the gist description.

    The description is the only part of a gist GitHub indexes for search — a
    gist body is not searchable — so it is worth taking from the title rather
    than leaving blank.
    """
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()[:256]
    return fallback


def main() -> None:
    token = os.environ.get("GIST_TOKEN", "")
    if not token:
        die(
            "GIST_TOKEN is not set. Create a classic PAT with the 'gist' scope "
            "and add it as a repository secret named GIST_TOKEN."
        )

    dry_run = os.environ.get("DRY_RUN", "").lower() == "true"

    if not GIST_DIR.is_dir():
        die(f"{GIST_DIR}/ does not exist.")

    files = sorted(
        path
        for path in GIST_DIR.rglob("*.md")
        if path.name not in EXCLUDE
    )
    if not files:
        print("::notice::No gist sources found. Nothing to publish.")
        return

    registry: dict[str, dict[str, str]] = {}
    if REGISTRY.exists():
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    summary: list[str] = []

    for path in files:
        key = path.as_posix()
        content = path.read_text(encoding="utf-8")
        if not content.strip():
            print(f"::warning::Skipping empty file {key}")
            continue

        payload = {
            "description": describe(content, path.stem),
            "files": {path.name: {"content": content}},
        }

        known = registry.get(key, {}).get("id")

        if dry_run:
            action = "update" if known else "create"
            print(f"[dry run] would {action} {key} as {path.name}")
            continue

        if known:
            try:
                result = request("PATCH", f"/gists/{known}", token, payload)
                verb = "updated"
            except urllib.error.HTTPError as error:
                if error.code != 404:
                    die(f"Updating gist {known} for {key} failed: {error.code}")
                # The gist was deleted on gist.github.com. Recreate it rather
                # than failing the run — the registry entry is now a dangling
                # ID and the repository is the source of truth.
                print(f"::warning::Gist {known} for {key} is gone; recreating.")
                payload["public"] = True
                result = request("POST", "/gists", token, payload)
                verb = "recreated"
        else:
            payload["public"] = True
            try:
                result = request("POST", "/gists", token, payload)
            except urllib.error.HTTPError as error:
                if error.code == 404:
                    die(
                        f"Creating a gist for {key} returned 404. GitHub "
                        "returns 404, not 403, for a scope it will not grant, "
                        "so GIST_TOKEN is almost certainly missing the 'gist' "
                        "scope. Note that a fine-grained token cannot reach "
                        "gists at all — it must be a classic PAT."
                    )
                if error.code == 401:
                    die(f"GIST_TOKEN was rejected as invalid or expired.")
                if error.code == 403:
                    # Not a scope problem: GitHub uses 404 for those. Most
                    # likely secondary rate limiting, or an egress proxy
                    # between this job and api.github.com that only permits
                    # repository-scoped paths.
                    die(
                        f"Creating a gist for {key} returned 403. This is not "
                        "a missing scope. Check the response body in the log "
                        "above: a 'documentation_url' pointing anywhere other "
                        "than docs.github.com means a proxy blocked the call, "
                        "not GitHub."
                    )
                die(f"Creating a gist for {key} failed: {error.code}")
            verb = "created"

        registry[key] = {"id": result["id"], "url": result["html_url"]}
        print(f"{verb}: {key} -> {result['html_url']}")
        summary.append(f"| `{key}` | {verb} | {result['html_url']} |")

    if dry_run:
        return

    REGISTRY.write_text(
        json.dumps(dict(sorted(registry.items())), indent=2) + "\n",
        encoding="utf-8",
    )

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary and summary:
        with open(step_summary, "a", encoding="utf-8") as handle:
            handle.write("## Published gists\n\n")
            handle.write("| Source | Action | Gist |\n| --- | --- | --- |\n")
            handle.write("\n".join(summary) + "\n")


if __name__ == "__main__":
    main()
