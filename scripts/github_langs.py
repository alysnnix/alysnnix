#!/usr/bin/env python3
"""Fetch GitHub language stats and inject ASCII bars between README markers."""
from __future__ import annotations

import json
import os
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

USERNAME = os.environ["GH_USERNAME"]
TOKEN = os.environ["GH_TOKEN"]
INCLUDE_PRIVATE = os.environ.get("INCLUDE_PRIVATE", "false").lower() == "true"

README = Path("README.md")
START = "<!--START:langs-->"
END = "<!--END:langs-->"
BAR_WIDTH = 25
TOP_N = 8

EXCLUDE_LANGS = {"HTML", "CSS", "TeX", "Jupyter Notebook"}

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "github-langs-readme",
    "X-GitHub-Api-Version": "2022-11-28",
}


def api(path: str):
    req = urllib.request.Request(f"https://api.github.com{path}", headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def all_repos():
    endpoint = "/user/repos" if INCLUDE_PRIVATE else f"/users/{USERNAME}/repos"
    page = 1
    while True:
        data = api(f"{endpoint}?per_page=100&page={page}&affiliation=owner")
        if not data:
            return
        yield from data
        page += 1


def human_size(n: int) -> str:
    for unit, div in (("MB", 1_000_000), ("kB", 1_000)):
        if n >= div:
            return f"{n / div:.1f} {unit}"
    return f"{n} B"


def main() -> None:
    totals: dict[str, int] = defaultdict(int)
    for repo in all_repos():
        if repo.get("fork") or repo.get("archived"):
            continue
        for lang, size in api(f"/repos/{repo['full_name']}/languages").items():
            if lang in EXCLUDE_LANGS:
                continue
            totals[lang] += size

    if not totals:
        raise SystemExit("no language data found")

    grand_total = sum(totals.values())
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])[:TOP_N]
    leader_size = ranked[0][1]

    name_w = max(len(n) for n, _ in ranked)
    size_w = max(len(human_size(s)) for _, s in ranked)

    lines: list[str] = []
    for name, size in ranked:
        pct = size / grand_total * 100
        # power-scale the bar relative to the leader so smaller langs stay visible
        bar_ratio = (size / leader_size) ** 0.4
        filled = round(bar_ratio * BAR_WIDTH)
        bar = "█" * filled + "░" * (BAR_WIDTH - filled)
        lines.append(
            f"{name:<{name_w}}   {human_size(size):>{size_w}}   {bar}   {pct:5.2f}%"
        )

    block = "\n".join(lines)
    src = README.read_text()
    new = re.sub(
        rf"({re.escape(START)})(?:.*?)({re.escape(END)})",
        lambda m: f"{m.group(1)}\n```text\n{block}\n```\n{m.group(2)}",
        src,
        flags=re.S,
    )
    README.write_text(new)


if __name__ == "__main__":
    main()
