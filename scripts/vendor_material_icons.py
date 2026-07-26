#!/usr/bin/env python3
"""Vendor the pinned Amber Material Icons snapshot from a VS Code install.

The script copies the installed Material Icon Theme's static definition and SVG
assets, rewrites asset paths, and deterministically applies this theme's amber
folder color and saturation.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parent.parent
PINNED_VERSION = "5.37.0"
UPSTREAM_ID = "PKief.material-icon-theme"
AMBER = "#ffcb6b"
UPSTREAM_FOLDER_COLOR = "#90a4ae"
SATURATION = "0.9"

DEST_THEME = ROOT / "icon-themes" / "amber-material-icons.json"
DEST_ICONS = ROOT / "icons" / "amber-material"
DEST_LICENSE = ROOT / "LICENSE-material-icon-theme.txt"
DEST_METADATA = ROOT / "vendor" / "material-icon-theme.json"


def destination_directory(asset_name: str) -> Path:
    """Group generated assets into browsable file and folder directories."""
    category = "folders" if asset_name.startswith("folder") else "files"
    return DEST_ICONS / category


def discover_source() -> Path:
    """Return the installed directory for the pinned upstream version."""
    candidates = []
    extension_roots = [
        Path.home() / ".vscode" / "extensions",
        Path.home() / ".vscode-insiders" / "extensions",
    ]
    expected = f"pkief.material-icon-theme-{PINNED_VERSION}"
    for extension_root in extension_roots:
        candidate = extension_root / expected
        if candidate.is_dir():
            candidates.append(candidate)

    if not candidates:
        raise FileNotFoundError(
            f"{UPSTREAM_ID} {PINNED_VERSION} is not installed in VS Code"
        )
    return candidates[0].resolve()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assets_sha256(root: Path) -> str:
    """Return one digest covering every vendored asset's path and contents.

    Sorted by relative POSIX path so the result does not depend on filesystem
    walk order, and each path is fed in alongside its bytes so a rename is
    caught as well as an edit. check_generated.py recomputes this to verify the
    committed snapshot, which is the only way to detect a hand-edited SVG --
    counting assets cannot.
    """
    digest = hashlib.sha256()
    assets = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    for path in assets:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def load_source(source: Path):
    package_path = source / "package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    identity = f"{package.get('publisher')}.{package.get('name')}"
    if identity.lower() != UPSTREAM_ID.lower():
        raise ValueError(f"unexpected extension identity: {identity}")
    if package.get("version") != PINNED_VERSION:
        raise ValueError(
            f"expected Material Icon Theme {PINNED_VERSION}, "
            f"found {package.get('version')}"
        )
    if package.get("license") != "MIT":
        raise ValueError(f"unexpected upstream license: {package.get('license')}")

    definition_path = source / "dist" / "material-icons.json"
    definition = json.loads(definition_path.read_text(encoding="utf-8"))
    return package, definition_path, definition


def source_asset(source: Path, definition_path: Path, icon_path: str) -> Path:
    """Resolve and constrain a referenced SVG to the upstream extension."""
    asset = (definition_path.parent / icon_path).resolve()
    try:
        asset.relative_to(source)
    except ValueError as error:
        raise ValueError(f"icon escapes upstream extension: {icon_path}") from error
    if asset.suffix.lower() != ".svg" or not asset.is_file():
        raise ValueError(f"missing or unsupported icon asset: {icon_path}")
    return asset


def brand_svg(svg: str, amber_folder: bool) -> str:
    """Apply the brand color where needed and normalize saturation."""
    if amber_folder:
        svg, replacements = re.subn(
            re.escape(UPSTREAM_FOLDER_COLOR),
            AMBER,
            svg,
            flags=re.IGNORECASE,
        )
        if not replacements and AMBER not in svg.lower():
            raise ValueError("folder asset does not use the expected upstream color")

    if 'id="saturation"' in svg:
        svg, replacements = re.subn(
            r'(<feColorMatrix\b[^>]*\btype="saturate"[^>]*\bvalues=")[^"]*',
            rf"\g<1>{SATURATION}",
            svg,
            count=1,
        )
        if not replacements:
            raise ValueError("existing saturation filter could not be normalized")
    else:
        svg = svg.replace("<svg ", '<svg filter="url(#saturation)" ', 1)
        saturation_filter = (
            '<defs><filter id="saturation"><feColorMatrix '
            f'type="saturate" values="{SATURATION}"/>'
            "</filter></defs>"
        )
        svg = svg.replace("</svg>", f"{saturation_filter}</svg>", 1)

    if f'values="{SATURATION}"' not in svg:
        raise ValueError("saturation filter was not applied")
    return svg


def vendor(source: Path):
    package, definition_path, definition = load_source(source)
    folder_keys = ("folder", "folder-open", "folder-root", "folder-root-open")
    folder_assets = {
        source_asset(
            source,
            definition_path,
            definition["iconDefinitions"][key]["iconPath"],
        )
        for key in folder_keys
    }

    destination_directories = {
        DEST_ICONS / "files",
        DEST_ICONS / "folders",
    }
    for directory in destination_directories:
        directory.mkdir(parents=True, exist_ok=True)
    copied = set()
    source_hashes = {}

    for icon in definition.get("iconDefinitions", {}).values():
        icon_path = icon.get("iconPath")
        if not icon_path:
            continue
        asset = source_asset(source, definition_path, icon_path)
        destination_directory_for_asset = destination_directory(asset.name)
        destination = destination_directory_for_asset / asset.name
        asset_hash = sha256(asset)
        previous_hash = source_hashes.get(asset.name)
        if previous_hash and previous_hash != asset_hash:
            raise ValueError(f"conflicting upstream asset name: {asset.name}")
        source_hashes[asset.name] = asset_hash
        if asset.name not in copied:
            svg = asset.read_text(encoding="utf-8")
            svg = brand_svg(svg, amber_folder=asset in folder_assets)
            destination.write_text(svg, encoding="utf-8")
            destination.chmod(0o644)
            copied.add(asset.name)
        category = destination_directory_for_asset.name
        icon["iconPath"] = f"../icons/amber-material/{category}/{asset.name}"

    for directory in destination_directories:
        for existing in directory.iterdir():
            if existing.is_file() and existing.name not in copied:
                existing.unlink()

    # The snapshot carries a few blocks that are empty upstream too, so they are
    # expected rather than a vendoring bug: "highContrast" (both of its maps),
    # "rootFolderNames" and "rootFolderNamesExpanded". Material Icon Theme fills
    # these at runtime from its own settings, which this static snapshot does not
    # ship. Root folders still get an icon via "rootFolder"/"rootFolderExpanded".
    DEST_THEME.parent.mkdir(parents=True, exist_ok=True)
    with DEST_THEME.open("w", encoding="utf-8") as destination:
        json.dump(definition, destination, indent=2, ensure_ascii=False)
        destination.write("\n")

    license_candidates = [source / "LICENSE.txt", source / "LICENSE"]
    upstream_license = next(
        (candidate for candidate in license_candidates if candidate.is_file()),
        None,
    )
    if not upstream_license:
        raise FileNotFoundError("upstream MIT license was not found")
    shutil.copyfile(upstream_license, DEST_LICENSE)
    DEST_LICENSE.chmod(0o644)

    metadata = {
        "source": "https://github.com/material-extensions/vscode-material-icon-theme",
        "extension": UPSTREAM_ID,
        "version": package["version"],
        "license": package["license"],
        "sourceDefinitionSha256": sha256(definition_path),
        "vendoredDefinitionSha256": sha256(DEST_THEME),
        "vendoredAssetsSha256": assets_sha256(DEST_ICONS),
        "assetCount": len(copied),
        "folderColor": AMBER.upper(),
        "saturation": 0.9,
    }
    DEST_METADATA.parent.mkdir(parents=True, exist_ok=True)
    with DEST_METADATA.open("w", encoding="utf-8") as destination:
        json.dump(metadata, destination, indent=2)
        destination.write("\n")

    print(
        f"vendored {UPSTREAM_ID} {package['version']}: "
        f"{len(copied)} SVG assets"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        help=f"path to an installed {UPSTREAM_ID} {PINNED_VERSION} extension",
    )
    args = parser.parse_args()
    source = args.source.expanduser().resolve() if args.source else discover_source()
    vendor(source)


if __name__ == "__main__":
    main()
