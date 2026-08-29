#!/usr/bin/env python3
"""Verify every generated file matches what its generator produces today.

Nothing else enforces the rule that files in themes/, ghostty/, codex/, grok/
and the terminal-suite directories are outputs rather than sources. Editing a
generated file by hand, or changing a generator without re-running the chain,
leaves the repository in a state where the committed theme and its stated
source disagree.

Run from anywhere:

    python3 scripts/check_generated.py

Exits 0 when everything is in sync, 1 otherwise, listing what drifted.

The icon snapshot is checked differently. vendor_material_icons.py reads a
locally installed VS Code extension, so it cannot run offline; instead this
verifies the snapshot against the digests and asset count that the vendoring
step recorded in vendor/material-icon-theme.json, recomputing them with the
vendoring script's own functions so the two cannot drift apart.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

import vendor_material_icons

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# In dependency order: build_ghostty owns the terminal palette, build_theme
# consumes it, and the Codex, terminal-suite and Grok builders consume both.
GENERATORS = (
    "build_ghostty.py",
    "build_theme.py",
    "build_codex_theme.py",
    "build_terminal_suite.py",
    "build_grok_theme.py",
)

GENERATED = (
    "ghostty/amber-material",
    "ghostty/amber-material-light",
    "themes/amber-material-hc.json",
    "themes/amber-material-light-hc.json",
    "codex/amber-material-high-contrast.tmTheme",
    "codex/amber-material-light-high-contrast.tmTheme",
    "claude-code/amber-material-high-contrast.json",
    "claude-code/amber-material-light-high-contrast.json",
    "opencode/amber-material-high-contrast.json",
    "opencode/amber-material-light-high-contrast.json",
    "windows-terminal/amber-material-high-contrast.json",
    "windows-terminal/amber-material-light-high-contrast.json",
    "powershell/AmberMaterial.ps1",
    "powershell/AmberMaterialLight.ps1",
    "starship/amber-material.toml",
    "starship/amber-material-light.toml",
    "grok/amber-material-high-contrast.json",
    "grok/amber-material-light-high-contrast.json",
    "grok/pager.toml",
    "grok/pager-light.toml",
)

VENDOR_MANIFEST = "vendor/material-icon-theme.json"
ICON_THEME = "icon-themes/amber-material-icons.json"
ICON_ASSETS = "icons/amber-material"
# Copied verbatim from upstream by vendor_material_icons.py and shipped in the
# VSIX, so it belongs to the snapshot: without it the package ships MIT-derived
# icons with no MIT text.
VENDOR_LICENSE = "LICENSE-material-icon-theme.txt"


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def load_json(relative):
    """Return (data, problem) for a JSON file under ROOT.

    Every failure a hand edit can cause -- deletion, truncation, merge markers,
    a replaced root value -- comes back as a problem string rather than an
    exception, so main() can print the drift report it promises instead of a
    traceback. Exactly one of the two return values is ever set.
    """
    path = os.path.join(ROOT, relative)
    if not os.path.isfile(path):
        return None, f"{relative}: missing"
    try:
        with open(path, encoding="utf-8") as source:
            data = json.load(source)
    except json.JSONDecodeError as error:
        return None, f"{relative}: not valid JSON ({error})"
    except UnicodeDecodeError as error:
        return None, f"{relative}: not valid UTF-8 ({error})"
    if not isinstance(data, dict):
        return None, (
            f"{relative}: expected a JSON object at the top level, "
            f"found {type(data).__name__}"
        )
    return data, None


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
            elif read_bytes(committed) != read_bytes(fresh):
                problems.append(
                    f"{relative}: committed copy differs from generator output"
                )
    return problems


def check_icon_snapshot():
    manifest, problem = load_json(VENDOR_MANIFEST)
    if problem:
        return [problem]

    problems = []

    # A missing or unreadable definition, asset tree, or license is the most
    # severe form of the drift this command exists to diagnose, so report those
    # and stop. Every check below reads one of them, and continuing would only
    # add derived noise: a deleted asset tree otherwise reports a digest
    # mismatch, a count mismatch, and 1250 missing references for one cause.
    theme_path = os.path.join(ROOT, ICON_THEME)
    assets_root = pathlib.Path(ROOT) / ICON_ASSETS
    license_path = os.path.join(ROOT, VENDOR_LICENSE)
    icon_theme, theme_problem = load_json(ICON_THEME)
    if theme_problem:
        problems.append(theme_problem)
    if not assets_root.is_dir():
        problems.append(f"{ICON_ASSETS}: missing")
    if not os.path.isfile(license_path):
        problems.append(
            f"{VENDOR_LICENSE}: missing -- the VSIX would ship MIT-derived "
            "icons with no MIT text"
        )
    if problems:
        return problems

    license_actual = sha256(license_path)
    license_expected = manifest.get("vendoredLicenseSha256")
    if license_expected is None:
        problems.append(
            f"{VENDOR_MANIFEST}: no vendoredLicenseSha256 recorded, so "
            f"{VENDOR_LICENSE} cannot be verified; re-run "
            "vendor_material_icons.py"
        )
    elif license_actual != license_expected:
        problems.append(
            f"{VENDOR_LICENSE}: sha256 {license_actual} does not match "
            f"vendoredLicenseSha256 {license_expected} -- the upstream MIT "
            "text was modified"
        )

    actual = sha256(theme_path)
    expected = manifest.get("vendoredDefinitionSha256")
    if actual != expected:
        problems.append(
            f"{ICON_THEME}: sha256 {actual} does not match "
            f"vendoredDefinitionSha256 {expected}"
        )

    # Asset contents, not just their count: an edited or corrupted SVG leaves
    # the count and the definition digest untouched, so only this catches it.
    assets_actual = vendor_material_icons.assets_sha256(assets_root)
    assets_expected = manifest.get("vendoredAssetsSha256")
    if assets_expected is None:
        problems.append(
            f"{VENDOR_MANIFEST}: no vendoredAssetsSha256 recorded, so asset "
            "contents cannot be verified; re-run vendor_material_icons.py"
        )
    elif assets_actual != assets_expected:
        problems.append(
            f"{ICON_ASSETS}: contents digest {assets_actual} does not match "
            f"vendoredAssetsSha256 {assets_expected} -- an asset was edited, "
            "renamed, added or removed"
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
    theme_problems = check_generated_files()
    icon_problems = check_icon_snapshot()
    if theme_problems or icon_problems:
        print("generated files are out of sync:\n")
        for problem in theme_problems + icon_problems:
            print(f"  - {problem}")
        if theme_problems:
            print(
                "\nRe-run the generators in order, or revert hand edits to "
                "generated files:\n"
                "  " + "\n  ".join(f"python3 scripts/{g}" for g in GENERATORS)
            )
        if icon_problems:
            print(
                "\nFor the icon snapshot, revert the hand edit, or re-vendor "
                "against an installed "
                f"{vendor_material_icons.UPSTREAM_ID} "
                f"{vendor_material_icons.PINNED_VERSION}:\n"
                "  python3 scripts/vendor_material_icons.py"
            )
        return 1

    print(
        f"in sync: {len(GENERATED)} generated files match their generators, "
        "icon snapshot matches its manifest"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
