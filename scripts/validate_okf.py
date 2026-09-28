#!/usr/bin/env python3
"""OKF v0.2 bundle conformance validator (stdlib + pyyaml).

Checks, for every in-scope Markdown file under the bundle root:

* parseable YAML frontmatter with a non-empty ``type`` key, except that
  files named ``index.md`` must carry NO frontmatter (the root
  ``index.md`` may carry only ``okf_version``);
* every local link (bundle-rooted ``]( /... )`` or relative ``]( ../x.md )``)
  resolves to an existing file (a directory link resolves when
  ``<dir>/index.md`` exists; external URLs and pure fragment links are
  skipped);
* in files named ``log.md``, every ``##`` heading is a ``YYYY-MM-DD`` date.

Out of scope: ``README.md``, ``.agents/**``, ``.github/**``,
``scripts/**``, ``site/**`` (plus ``.git/**``). In CI (a clean checkout)
the files on disk are exactly the tracked files.

Usage: ``python scripts/validate_okf.py [bundle-root]``.
Exit status is 0 on success, 1 on any failure.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "validate_okf: PyYAML is required (pip install pyyaml)\n"
    )
    sys.exit(2)

LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
SKIP_LINK_PREFIXES = ("http://", "https://", "mailto:", "#")
LOG_HEADING_RE = re.compile(r"^##\s+(.*\S)\s*$")
LOG_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:\s|$)")

EXCLUDED_DIRS = {".git", ".agents", ".github", "scripts", "site"}


def bundle_root() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return Path(__file__).resolve().parent.parent


def in_scope(root: Path, path: Path) -> bool:
    rel = path.relative_to(root)
    if path.name == "README.md":
        return False
    return not any(part in EXCLUDED_DIRS for part in rel.parts)


def split_frontmatter(text: str):
    """Return (mapping-or-None, error-or-None, has_block)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None, False
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "unterminated YAML frontmatter (missing closing ---)", True
    raw = "\n".join(lines[1:end])
    try:
        data = yaml.safe_load(raw) if raw.strip() else {}
    except yaml.YAMLError as exc:
        return None, f"unparseable YAML frontmatter: {exc}", True
    if data is None:
        data = {}
    if not isinstance(data, dict):
        return None, "YAML frontmatter must be a mapping", True
    return data, None, True


def check_frontmatter(rel: str, fm, has_block: bool, errors: list[str]) -> None:
    is_index = rel == "index.md" or rel.endswith("/index.md")
    is_root_index = rel == "index.md"
    if is_root_index:
        if has_block:
            if set(fm.keys()) != {"okf_version"}:
                errors.append(
                    f"{rel}: root index.md frontmatter must contain "
                    f"only okf_version, got keys {sorted(fm.keys())}"
                )
            elif str(fm["okf_version"]) != "0.2":
                errors.append(
                    f"{rel}: root index.md okf_version must be "
                    f'"0.2", got {fm["okf_version"]!r}'
                )
        return
    if is_index:
        if has_block:
            errors.append(f"{rel}: index.md must carry no frontmatter")
        return
    type_value = fm.get("type") if isinstance(fm, dict) else None
    if not isinstance(type_value, str) or not type_value.strip():
        errors.append(
            f"{rel}: missing required frontmatter key: non-empty type"
        )


def resolve_link(root: Path, src_rel: str, target: str) -> bool:
    if target.startswith(SKIP_LINK_PREFIXES):
        return True
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return True
    if target.startswith("/"):
        candidate = root / target[1:]
    else:
        candidate = root / Path(src_rel).parent / target
    if candidate.is_file():
        return True
    if candidate.is_dir() and (candidate / "index.md").is_file():
        return True
    stem = target[1:] if target.startswith("/") else target
    base = root if target.startswith("/") else root / Path(src_rel).parent
    if not stem.endswith(".md") and (base / (stem + ".md")).is_file():
        return True
    return False


def check_links(rel: str, text: str, root: Path, errors: list[str]) -> None:
    for lineno, line in enumerate(text.split("\n"), start=1):
        for match in LINK_RE.finditer(line):
            target = match.group(1)
            if not resolve_link(root, rel, target):
                errors.append(
                    f"{rel}:{lineno}: link {target} "
                    f"does not resolve to an existing file"
                )


def check_log(rel: str, text: str, errors: list[str]) -> None:
    for lineno, line in enumerate(text.split("\n"), start=1):
        heading = LOG_HEADING_RE.match(line)
        if not heading:
            continue
        date_match = LOG_DATE_RE.match(heading.group(1))
        if not date_match:
            errors.append(
                f"{rel}:{lineno}: log.md date heading must be "
                f"YYYY-MM-DD, got {heading.group(1)!r}"
            )
            continue
        try:
            datetime.strptime(date_match.group(1), "%Y-%m-%d")
        except ValueError:
            errors.append(
                f"{rel}:{lineno}: log.md date heading is not a valid "
                f"calendar date: {date_match.group(1)!r}"
            )


def main() -> int:
    root = bundle_root()
    if not root.is_dir():
        sys.stderr.write(f"validate_okf: bundle root not found: {root}\n")
        return 2
    md_files = sorted(
        p for p in root.rglob("*.md") if in_scope(root, p)
    )
    errors: list[str] = []
    for path in md_files:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{rel}: cannot read file: {exc}")
            continue
        fm, fm_error, has_block = split_frontmatter(text)
        if fm_error is not None:
            errors.append(f"{rel}: {fm_error}")
            continue
        check_frontmatter(rel, fm or {}, has_block, errors)
        check_links(rel, text, root, errors)
        if path.name == "log.md":
            check_log(rel, text, errors)
    if errors:
        for message in errors:
            print(f"ERROR: {message}")
        print(
            f"validate_okf: {len(errors)} error(s) in "
            f"{len(md_files)} file(s)",
            file=sys.stderr,
        )
        return 1
    print(f"validate_okf: OK ({len(md_files)} file(s) checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
