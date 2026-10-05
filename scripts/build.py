#!/usr/bin/env python3
"""Awesome AI Architect generator.

Fetches the GitHub stars and public repositories of one user, classifies every
repository into an AI-engineering taxonomy (see ../config.toml), tracks star
momentum over time and renders:

  README.md            the awesome list
  data/repos.json      the dataset consumed by the web explorer
  data/history.json    daily star snapshots used for momentum

Standard library only. Python 3.11+ (tomllib).

Usage:
  python3 scripts/build.py                     # live, uses $GITHUB_TOKEN if set
  python3 scripts/build.py --fixture FILE      # offline, from a fixture
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"


# --------------------------------------------------------------------------- config

def load_config(path: Path = ROOT / "config.toml") -> dict:
    with path.open("rb") as fh:
        cfg = tomllib.load(fh)
    ids = [c["id"] for c in cfg["category"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("config.toml: duplicate category id")
    if "triage" not in ids:
        raise SystemExit("config.toml: a 'triage' category is required")
    for repo, cat in cfg.get("overrides", {}).items():
        if cat not in ids:
            raise SystemExit(f"config.toml: override {repo} -> unknown category '{cat}'")
    return cfg


def adapt_for_fork(cfg: dict, env: dict | None = None) -> dict:
    """Zero-config forks: in GitHub Actions, take the identity from the repository owner.

    A fork needs no edit: the owner's stars are fetched, the README and explorer
    point to the fork, and the original owner's overrides are dropped.
    """
    env = os.environ if env is None else env
    full = env.get("GITHUB_REPOSITORY", "")
    owner = env.get("GITHUB_REPOSITORY_OWNER") or full.partition("/")[0]
    lst = cfg["list"]
    if not full or not owner or owner.lower() == lst["user"].lower():
        return cfg
    name = full.partition("/")[2]
    lst.update(
        user=owner,
        repo=full,
        author=owner,
        author_url=f"https://github.com/{owner}",
        site_url=f"https://{owner.lower()}.github.io/{name}/",
        exclude_own=[owner, name],
        exclude_starred=[],
    )
    cfg["overrides"] = {}
    return cfg


# --------------------------------------------------------------------------- fetch

def _request(url: str, token: str | None, accept: str) -> tuple[list, str]:
    headers = {
        "Accept": accept,
        "User-Agent": "awesome-ai-architect",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
                return json.load(resp), resp.headers.get("Link", "")
        except urllib.error.HTTPError as err:
            retryable = err.code >= 500 or (err.code in (403, 429) and err.headers.get("Retry-After"))
            if not retryable or attempt == 4:
                raise
            time.sleep(int(err.headers.get("Retry-After") or 2 ** (attempt + 1)))
        except urllib.error.URLError:
            if attempt == 4:
                raise
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError("unreachable")


def _paginate(url: str, token: str | None, accept: str = "application/vnd.github+json") -> list:
    items: list = []
    while url:
        page, link = _request(url, token, accept)
        items.extend(page)
        match = re.search(r'<([^>]+)>;\s*rel="next"', link)
        url = match.group(1) if match else ""
    return items


def fetch_live(user: str, token: str | None) -> dict:
    starred = _paginate(
        f"{API}/users/{user}/starred?per_page=100&sort=created&direction=desc",
        token,
        accept="application/vnd.github.star+json",
    )
    own = _paginate(f"{API}/users/{user}/repos?type=owner&sort=pushed&per_page=100", token)
    return {"starred": starred, "own": own}


# --------------------------------------------------------------------------- normalize

def _norm(text: str) -> str:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text or "")
    return re.sub(r"[\s_\-]+", " ", text.lower()).strip()


def normalize(raw: dict, starred_at: str | None, mine: bool) -> dict:
    lic = raw.get("license") or {}
    owner = raw.get("owner") or {}
    full = raw["full_name"]
    return {
        "full_name": full,
        "owner": owner.get("login") or full.split("/")[0],
        "name": raw.get("name") or full.split("/")[1],
        "url": raw.get("html_url") or f"https://github.com/{full}",
        "description": (raw.get("description") or "").strip(),
        "homepage": raw.get("homepage") or "",
        "language": raw.get("language") or "",
        "license": lic.get("spdx_id") if lic.get("spdx_id") not in (None, "NOASSERTION") else "",
        "stars": raw.get("stargazers_count", 0),
        "forks": raw.get("forks_count", 0),
        "open_issues": raw.get("open_issues_count", 0),
        "topics": sorted(raw.get("topics") or []),
        "created_at": raw.get("created_at"),
        "pushed_at": raw.get("pushed_at") or raw.get("updated_at"),
        "starred_at": starred_at,
        "archived": bool(raw.get("archived")),
        "fork": bool(raw.get("fork")),
        "mine": mine,
    }


def collect(payload: dict, cfg: dict) -> list[dict]:
    lst = cfg["list"]
    user = lst["user"].lower()
    excl_own = {n.lower() for n in lst.get("exclude_own", [])}
    excl_star = {n.lower() for n in lst.get("exclude_starred", [])}
    repos: dict[str, dict] = {}

    for raw in payload.get("own", []):
        if raw.get("private") or raw.get("fork") or raw["name"].lower() in excl_own:
            continue
        repos[raw["full_name"].lower()] = normalize(raw, None, mine=True)

    for entry in payload.get("starred", []):
        raw, starred_at = (entry["repo"], entry.get("starred_at")) if "repo" in entry else (entry, None)
        key = raw["full_name"].lower()
        if raw.get("private") or key in excl_star:
            continue
        if key in repos:  # starring your own repo keeps it in "mine"
            repos[key]["starred_at"] = starred_at
            continue
        repos[key] = normalize(raw, starred_at, mine=key.split("/")[0] == user)
    return list(repos.values())


# --------------------------------------------------------------------------- classify

def _compile(cfg: dict) -> list[dict]:
    compiled = []
    for cat in cfg["category"]:
        compiled.append({
            "id": cat["id"],
            "topics": set(cat.get("topics", [])),
            "weak": set(cat.get("weak_topics", [])),
            "patterns": [
                re.compile(r"(?<![a-z0-9])" + re.escape(_norm(k)) + r"(?![a-z0-9])")
                for k in cat.get("keywords", [])
            ],
        })
    return compiled


def score(repo: dict, compiled: list[dict], weights: dict) -> dict[str, int]:
    topics = set(repo["topics"])
    name = _norm(repo["name"])
    desc = _norm(repo["description"])
    scores: dict[str, int] = {}
    for cat in compiled:
        s = weights["strong_topic"] * len(topics & cat["topics"])
        s += weights["weak_topic"] * len(topics & cat["weak"])
        name_hits = sum(1 for p in cat["patterns"] if p.search(name))
        desc_hits = sum(1 for p in cat["patterns"] if p.search(desc))
        # Caps stop long descriptions from outvoting curated topics.
        s += weights["name"] * min(name_hits, 2)
        s += weights["description"] * min(desc_hits, 3)
        if s:
            scores[cat["id"]] = s
    return scores


def classify(repos: list[dict], cfg: dict) -> None:
    compiled = _compile(cfg)
    order = {c["id"]: i for i, c in enumerate(compiled)}
    weights = cfg["scoring"]
    overrides = {k.lower(): v for k, v in cfg.get("overrides", {}).items()}
    for repo in repos:
        scores = score(repo, compiled, weights)
        ranked = sorted(scores, key=lambda cid: (-scores[cid], order[cid]))
        forced = overrides.get(repo["full_name"].lower())
        primary = forced or (ranked[0] if ranked else "triage")
        repo["category"] = primary
        repo["tags"] = [
            cid for cid in ranked
            if cid != primary and scores[cid] >= weights["secondary_min"]
        ][: weights["max_secondary"]]
        repo["score"] = scores.get(primary, 0)
        # Topics that explain the classification first, generic ones last.
        rank = {cid: i for i, cid in enumerate([primary, *repo["tags"]])}
        by_id = {c["id"]: c for c in compiled}

        def topic_rank(t: str) -> tuple[int, int, str]:
            hits = [rank[cid] for cid in rank if t in by_id[cid]["topics"]]
            weak = [rank[cid] for cid in rank if t in by_id[cid]["weak"]]
            return (min(hits) if hits else 50 + min(weak) if weak else 99, len(t), t)

        repo["key_topics"] = sorted(repo["topics"], key=topic_rank)[:5]
        repo["classified_by"] = "override" if forced else ("rules" if ranked else "none")


# --------------------------------------------------------------------------- momentum

def update_history(repos: list[dict], history: dict, today: dt.date, keep_days: int) -> dict:
    history = dict(history)
    history[today.isoformat()] = {r["full_name"]: r["stars"] for r in repos}
    cutoff = today - dt.timedelta(days=keep_days)
    return {d: v for d, v in sorted(history.items()) if dt.date.fromisoformat(d) >= cutoff}


def apply_momentum(repos: list[dict], history: dict, today: dt.date) -> None:
    """Stars gained since the snapshot closest to 30 days ago (at least 1 day old)."""
    past = sorted(d for d in history if dt.date.fromisoformat(d) < today)
    target = today - dt.timedelta(days=30)
    base_day = next((d for d in past if dt.date.fromisoformat(d) >= target), None)
    base = history.get(base_day, {}) if base_day else {}
    window = (today - dt.date.fromisoformat(base_day)).days if base_day else 0
    for repo in repos:
        before = base.get(repo["full_name"])
        repo["stars_delta"] = repo["stars"] - before if before is not None else None
        repo["delta_days"] = window if before is not None else None


def health(repo: dict, today: dt.date) -> str:
    if repo["archived"]:
        return "archived"
    if not repo["pushed_at"]:
        return "unknown"
    days = (today - dt.date.fromisoformat(repo["pushed_at"][:10])).days
    return "active" if days <= 90 else "maintained" if days <= 365 else "dormant"


# --------------------------------------------------------------------------- render

def fmt_num(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    if n >= 1_000:
        return f"{n / 1_000:.1f}k".replace(".0k", "k")
    return str(n)


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _anchor(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower()).strip()
    return re.sub(r"\s", "-", slug)


def _when(iso: str | None) -> str:
    return iso[:7] if iso else ""


def _row(r: dict, titles: dict, show_cat: bool = False) -> str:
    desc = _cell(r["description"]) or "_No description._"
    if r["archived"]:
        desc = f"**Archived.** {desc}"
    stars = fmt_num(r["stars"])
    if r.get("stars_delta"):
        stars += f" <sub>+{fmt_num(r['stars_delta'])}</sub>"
    meta = r["language"] or ""
    if show_cat:
        meta = f"{titles[r['category']]}"
    tags = " ".join(f"`{t}`" for t in r.get("key_topics", r["topics"])[:4])
    tags = f"<br><sub>{tags}</sub>" if tags else ""
    return (f"| [**{_cell(r['name'])}**]({r['url']})<br><sub>{_cell(r['owner'])}</sub> "
            f"| {desc}{tags} | {stars} | {meta} | {_when(r['pushed_at'])} |")


def render_readme(repos: list[dict], cfg: dict, today: dt.date) -> str:
    lst = cfg["list"]
    cats = [c for c in cfg["category"]]
    titles = {c["id"]: c["title"] for c in cats}
    starred = [r for r in repos if not r["mine"]]
    mine = sorted((r for r in repos if r["mine"]), key=lambda r: (-r["stars"], r["name"].lower()))
    by_cat: dict[str, list[dict]] = {c["id"]: [] for c in cats}
    for r in starred:
        by_cat[r["category"]].append(r)
    non_empty = [c for c in cats if by_cat[c["id"]]]
    top_n = lst.get("readme_top", 20)
    hl = lst.get("highlight_size", 10)
    head = "| Project | What it does | Stars | {} | Last push |\n|:--|:--|--:|:--|:--|"

    out: list[str] = []
    repo = lst.get("repo", "")
    out.append(f"# {lst['title']}\n")
    out.append(
        "[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) "
        + (f"[![GitHub stars](https://img.shields.io/github/stars/{repo}?style=social)](https://github.com/{repo}/stargazers) " if repo else "")
        + 
        f"![Projects](https://img.shields.io/badge/projects-{len(repos)}-0f766e) "
        f"![Updated](https://img.shields.io/badge/updated-{today.isoformat().replace('-', '--')}-0f766e) "
        "![Auto-classified](https://img.shields.io/badge/classified-automatically-0f766e) "
        "![No API keys](https://img.shields.io/badge/API%20keys-none-0f766e)\n"
    )
    out.append(f"> {lst['tagline']}\n")
    if lst.get("site_url"):
        out.append(
            f"<a href=\"{lst['site_url']}\"><img src=\"site/social-preview.png\" "
            "alt=\"Interactive map of the GenAI stack, categories sized by number of projects\" width=\"100%\"></a>\n"
        )
        out.append(f"**[Open the interactive explorer]({lst['site_url']})**: search, filter by category, sort by stars, momentum or recency.\n")
    out.append(
        f"{len(starred)} starred projects and {len(mine)} original projects across "
        f"{len(non_empty)} categories. Regenerated every day by GitHub Actions from "
        f"[@{lst['user']}]({lst['author_url']})'s stars: star a repository and it shows up here, classified, the next morning.\n"
    )
    if repo:
        out.append(
            f"**Want this for your own stars?** [Fork it](https://github.com/{repo}/fork), turn on Pages, done. "
            "No config to edit, no API key. See [Use it for your own stars](#use-it-for-your-own-stars). "
            "If the map helps you, a star keeps it visible.\n"
        )

    out.append("## Contents\n")
    out.append("- [Recently starred](#recently-starred)")
    rising_pool = [r for r in starred if r.get("stars_delta")]
    if rising_pool:
        out.append("- [Rising](#rising)")
    for c in non_empty:
        out.append(f"- [{c['title']}](#{_anchor(c['title'])}) ({len(by_cat[c['id']])})")
    if mine:
        out.append(f"- [Built by {lst['author'].split()[0]}](#built-by-{_anchor(lst['author'].split()[0])}) ({len(mine)})")
    out.append("- [How it works](#how-it-works)")
    out.append("- [Use it for your own stars](#use-it-for-your-own-stars)")
    out.append("- [Suggest a project](#suggest-a-project)\n")

    recent = sorted((r for r in starred if r["starred_at"]), key=lambda r: r["starred_at"], reverse=True)[:hl]
    out.append("## Recently starred\n")
    out.append(head.format("Category"))
    out.extend(_row(r, titles, show_cat=True) for r in recent)
    out.append("")

    if rising_pool:
        rising = sorted(rising_pool, key=lambda r: -r["stars_delta"])[:hl]
        days = max(r["delta_days"] or 0 for r in rising)
        out.append("## Rising\n")
        out.append(f"Most stars gained over the last {days} day{'s' if days != 1 else ''} among starred projects.\n")
        out.append(head.format("Category"))
        out.extend(_row(r, titles, show_cat=True) for r in rising)
        out.append("")

    for c in non_empty:
        items = sorted(by_cat[c["id"]], key=lambda r: (r["archived"], -r["stars"]))
        out.append(f"## {c['title']}\n")
        out.append(f"{c['blurb']}\n")
        out.append(head.format("Language"))
        out.extend(_row(r, titles) for r in items[:top_n])
        out.append("")
        if len(items) > top_n:
            out.append(f"<details><summary>{len(items) - top_n} more in {c['title']}</summary>\n")
            out.append(head.format("Language"))
            out.extend(_row(r, titles) for r in items[top_n:])
            out.append("\n</details>\n")

    if mine:
        out.append(f"## Built by {lst['author'].split()[0]}\n")
        out.append("Original open-source work, classified with the same taxonomy.\n")
        out.append(head.format("Category"))
        out.extend(_row(r, titles, show_cat=True) for r in mine)
        out.append("")

    out.append("## How it works\n")
    out.append(
        "1. A scheduled GitHub Action fetches every public star and public original repository of "
        f"[@{lst['user']}]({lst['author_url']}) through the GitHub API.\n"
        "2. Each repository is scored against a taxonomy of AI-engineering categories using its topics, "
        "name and description. Topics weigh most because maintainers curate them.\n"
        "3. Daily snapshots of star counts give a momentum signal (stars gained over about 30 days).\n"
        "4. This README, a JSON dataset and the interactive explorer are regenerated and published.\n\n"
        "The taxonomy, weights and manual overrides live in [`config.toml`](config.toml). "
        "The generator is a single dependency-free Python file: [`scripts/build.py`](scripts/build.py). "
        "Fork it, change one line (`user`), and get the same list for your own stars.\n"
    )
    out.append("## Use it for your own stars\n")
    out.append(
        f"1. [Fork this repository](https://github.com/{repo}/fork).\n"
        "2. In the Actions tab of your fork, enable workflows.\n"
        "3. In Settings > Pages, set Source to **GitHub Actions**.\n"
        "4. Run the workflow once. Your stars, your README and your explorer, refreshed every day. "
        "The fork detects its owner on its own; edit `config.toml` only to tune the taxonomy.\n\n"
        "No secrets, no API keys and no dependencies: the default `GITHUB_TOKEN` reads public stars.\n"
    )
    out.append("## Suggest a project\n")
    out.append(
        "This list mirrors what one practitioner actually uses and follows. "
        + (f"Know a project that belongs here? [Open a suggestion](https://github.com/{repo}/issues/new?template=suggest.yml). " if repo else "")
        + "Accepted suggestions get starred, then classified on the next run.\n"
    )
    out.append("## License\n")
    out.append(
        "Code: [MIT](LICENSE). List content: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). "
        "Project descriptions belong to their respective authors.\n"
    )
    return "\n".join(out)


# --------------------------------------------------------------------------- main

def build(payload: dict, cfg: dict, today: dt.date, out_dir: Path = ROOT) -> dict:
    repos = collect(payload, cfg)
    classify(repos, cfg)
    for r in repos:
        r["health"] = health(r, today)

    data_dir = out_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    hist_path = data_dir / "history.json"
    history = json.loads(hist_path.read_text()) if hist_path.exists() else {}
    history = update_history(repos, history, today, cfg["list"].get("history_days", 35))
    apply_momentum(repos, history, today)

    repos.sort(key=lambda r: (-r["stars"], r["full_name"].lower()))
    counts = {c["id"]: 0 for c in cfg["category"]}
    for r in repos:
        counts[r["category"]] += 1
    dataset = {
        "generated_at": today.isoformat(),
        "user": cfg["list"]["user"],
        "repo": cfg["list"].get("repo", ""),
        "title": cfg["list"]["title"],
        "tagline": cfg["list"]["tagline"],
        "categories": [
            {"id": c["id"], "title": c["title"], "short": c.get("short", c["title"]),
             "blurb": c["blurb"], "count": counts[c["id"]]}
            for c in cfg["category"]
        ],
        "repos": repos,
    }
    (data_dir / "repos.json").write_text(json.dumps(dataset, ensure_ascii=False, indent=1) + "\n")
    hist_path.write_text(json.dumps(history, separators=(",", ":"), sort_keys=True) + "\n")
    (out_dir / "README.md").write_text(render_readme(repos, cfg, today))
    return dataset


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fixture", type=Path, help="offline JSON payload {starred: [...], own: [...]}")
    ap.add_argument("--today", help="override date (YYYY-MM-DD), for tests")
    ap.add_argument("--out", type=Path, default=ROOT, help="output directory (default: repository root)")
    args = ap.parse_args(argv)

    cfg = adapt_for_fork(load_config())
    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(dt.timezone.utc).date()
    if args.fixture:
        payload = json.loads(args.fixture.read_text())
    else:
        payload = fetch_live(cfg["list"]["user"], os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"))
    dataset = build(payload, cfg, today, args.out)

    counts = {c["id"]: c["count"] for c in dataset["categories"] if c["count"]}
    print(f"{len(dataset['repos'])} repositories classified: {json.dumps(counts)}")
    triage = [r["full_name"] for r in dataset["repos"] if r["category"] == "triage"]
    if triage:
        print(f"to triage ({len(triage)}): {', '.join(triage[:20])}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
