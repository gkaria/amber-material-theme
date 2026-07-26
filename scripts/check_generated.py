#!/usr/bin/env python3
"""Verify every generated file matches what its generator produces today.

Nothing else enforces the rule that files in themes/, ghostty/, codex/ and the
terminal-suite directories are outputs rather than sources. Editing a generated
file by hand, or changing a generator without re-running the chain, leaves the
repository in a state where the committed theme and its stated source disagree.

Run from anywhere:

    python3 scripts/check_generated.py

Exits 0 when everything is in sync, 1 otherwise, listing what drifted.

The icon snapshot is checked differently. vendor_material_icons.py reads a
locally installed VS Code extension, so it cannot run offline; instead this
verifies the snapshot against the SHA256 and asset count that the vendoring
step recorded in vendor/material-icon-theme.json.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# In dependency order: build_ghostty owns the terminal palette, build_theme
# consumes it, and the Codex and terminal-suite builders consume both.
GENERATORS = (
    "build_ghostty.py",
    "build_theme.py",
    "build_codex_theme.py",
    "build_terminal_suite.py",
)

GENERATED = (
    "ghostty/amber-material",
    "themes/amber-material-hc.json",
    "codex/amber-material-high-contrast.tmTheme",
    "claude-code/amber-material-high-contrast.json",
    "opencode/amber-material-high-contrast.json",
    "windows-terminal/amber-material-high-contrast.json",
    "powershell/AmberMaterial.ps1",
    "starship/amber-material.toml",
)

VENDOR_MANIFEST = "vendor/material-icon-theme.json"
ICON_THEME = "icon-themes/amber-material-icons.json"
ICON_ASSETS = "icons/amber-material"


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def rebuild(workspace):
    """Run the generator chain against a copy of scripts/ inside workspace."""
    shutil.copytree(HERE, os.path.join(workspace, "scripts"))
    for generator in GENERATORS:
        result = subprocess.run(
            [sys.executable, os.path.join(workspace, "scripts", generator)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return f"{generator} failed:\n{result.stderr.strip()}"
    return None


def check_generated_files():
    problems = []
    with tempfile.TemporaryDirectory() as workspace:
        failure = rebuild(workspace)
        if failure:
            return [failure]

        for relative in GENERATED:
            committed = os.path.join(ROOT, relative)
            fresh = os.path.join(workspace, relative)
            if not os.path.exists(fresh):
                problems.append(f"{relative}: no generator produced this file")
            elif not os.path.exists(committed):
                problems.append(f"{relative}: generated but not committed")
            elif open(committed, "rb").read() != open(fresh, "rb").read():
                problems.append(
                    f"{relative}: committed copy differs from generator output"
                )
    return problems


def check_icon_snapshot():
    problems = []
    manifest_path = os.path.join(ROOT, VENDOR_MANIFEST)
    if not os.path.exists(manifest_path):
        return [f"{VENDOR_MANIFEST}: missing"]

    with open(manifest_path, encoding="utf-8") as source:
        manifest = json.load(source)

    theme_path = os.path.join(ROOT, ICON_THEME)
    actual = sha256(theme_path)
    expected = manifest.get("vendoredDefinitionSha256")
    if actual != expected:
        problems.append(
            f"{ICON_THEME}: sha256 {actual} does not match "
            f"vendoredDefinitionSha256 {expected}"
        )

    on_disk = sum(
        len(files) for _, _, files in os.walk(os.path.join(ROOT, ICON_ASSETS))
    )
    if on_disk != manifest.get("assetCount"):
        problems.append(
            f"{ICON_ASSETS}: {on_disk} assets on disk, "
            f"manifest records {manifest.get('assetCount')}"
        )

    # Every icon the theme references must exist, and nothing should be shipped
    # that the theme never points at.
    with open(theme_path, encoding="utf-8") as source:
        icon_theme = json.load(source)
    theme_dir = os.path.dirname(theme_path)
    referenced = set()
    missing = []
    for name, definition in icon_theme.get("iconDefinitions", {}).items():
        icon_path = definition.get("iconPath")
        if not icon_path:
            continue
        resolved = os.path.normpath(os.path.join(theme_dir, icon_path))
        referenced.add(resolved)
        if not os.path.exists(resolved):
            missing.append(name)
    if missing:
        problems.append(
            f"{ICON_THEME}: {len(missing)} definitions point at missing files "
            f"(e.g. {', '.join(sorted(missing)[:3])})"
        )

    present = set()
    for directory, _, files in os.walk(os.path.join(ROOT, ICON_ASSETS)):
        for name in files:
            present.add(os.path.normpath(os.path.join(directory, name)))
    orphans = present - referenced
    if orphans:
        sample = ", ".join(
            os.path.relpath(path, ROOT) for path in sorted(orphans)[:3]
        )
        problems.append(
            f"{ICON_ASSETS}: {len(orphans)} assets are never referenced "
            f"(e.g. {sample})"
        )
    return problems


def main():
    problems = check_generated_files() + check_icon_snapshot()
    if problems:
        print("generated files are out of sync:\n")
        for problem in problems:
            print(f"  - {problem}")
        print(
            "\nRe-run the generators in order, or revert hand edits to "
            "generated files:\n"
            "  " + "\n  ".join(f"python3 scripts/{g}" for g in GENERATORS)
        )
        return 1

    print(
        f"in sync: {len(GENERATED)} generated files match their generators, "
        "icon snapshot matches its manifest"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
