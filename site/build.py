#!/usr/bin/env python3
"""Build the static OKF viewer site for this bundle.

Stages the bundle markdown (excluding repo scaffolding such as README.md,
scripts/, and this site/ directory) and runs the vendored OKF
`generate_visualization` over it, writing a self-contained index.html.

Usage:
    python3 site/build.py [--out site/dist]

Requires: pyyaml (the only third-party import in the vendored viewer).
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "site" / "vendor"))

from viewer.generator import generate_visualization  # noqa: E402

BUNDLE_NAME = "Friedman-cli OKF"
REPO_URL = "https://github.com/FriedmanJP/Friedman-cli-OKF/blob/main/"

# Top-level *.md files that are part of the OKF bundle (index.md files are
# skipped by the generator; README.md is repo scaffolding, not a concept;
# log.md stays in the bundle but out of the viewer, where it is an
# untagged orphan node).
ROOT_MD = ("index.md", "overview.md")


def stage_bundle(dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for name in ROOT_MD:
        shutil.copy2(REPO_ROOT / name, dest / name)
    for child in sorted(REPO_ROOT.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if child.name in ("scripts", "site"):
            continue
        if not any(child.glob("*.md")):
            continue
        shutil.copytree(child, dest / child.name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="site/dist", help="output directory")
    args = ap.parse_args()

    out_dir = (REPO_ROOT / args.out).resolve()
    with tempfile.TemporaryDirectory(prefix="okf-stage-") as tmp:
        stage = Path(tmp) / "bundle"
        stage_bundle(stage)
        out_path = out_dir / "index.html"
        stats = generate_visualization(
            stage, out_path, bundle_name=BUNDLE_NAME, repo_url=REPO_URL
        )
    # The deployed page is served from a subpath; keep a .nojekyll marker
    # so GitHub Pages serves the directory listing-free build as-is.
    (out_dir / ".nojekyll").touch()
    print(
        f"site: {stats['concepts']} concepts, {stats['edges']} edges, "
        f"{stats['bytes']} bytes -> {out_path.relative_to(REPO_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
