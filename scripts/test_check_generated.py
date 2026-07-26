#!/usr/bin/env python3
"""Tests for check_generated.py, focused on the cases it gets wrong.

    python3 scripts/test_check_generated.py

Two review rounds found real defects in check_generated.py, and both were in
paths that were never exercised: a corrupted asset went unnoticed, and a
missing file raised instead of reporting. The happy path was the only thing
anyone had run. These tests cover the failure modes directly, so the checker's
own guarantees are enforced rather than asserted.

Every check runs against a synthetic snapshot in a temporary directory, so a
test can delete or corrupt files without touching the repository. The one
exception is test_repository_is_currently_in_sync, which deliberately checks
the real tree.
"""
import json
import os
import pathlib
import shutil
import tempfile
import unittest

import check_generated
import vendor_material_icons


def build_snapshot(root):
    """Write a small but structurally faithful icon snapshot under root.

    Mirrors the real layout -- definition in icon-themes/, assets under
    icons/amber-material/<category>/, iconPath relative to the definition --
    so the checker's path resolution is exercised for real, with three assets
    instead of 1250.
    """
    (root / "icon-themes").mkdir(parents=True, exist_ok=True)
    files = root / "icons" / "amber-material" / "files"
    folders = root / "icons" / "amber-material" / "folders"
    files.mkdir(parents=True, exist_ok=True)
    folders.mkdir(parents=True, exist_ok=True)
    (root / "vendor").mkdir(parents=True, exist_ok=True)

    (files / "python.svg").write_text("<svg>python</svg>", encoding="utf-8")
    (files / "rust.svg").write_text("<svg>rust</svg>", encoding="utf-8")
    (folders / "folder.svg").write_text("<svg>folder</svg>", encoding="utf-8")

    license_path = root / check_generated.VENDOR_LICENSE
    license_path.write_text("MIT License\n\nCopyright (c)\n", encoding="utf-8")

    definition = {
        "iconDefinitions": {
            "python": {"iconPath": "../icons/amber-material/files/python.svg"},
            "rust": {"iconPath": "../icons/amber-material/files/rust.svg"},
            "folder": {"iconPath": "../icons/amber-material/folders/folder.svg"},
        },
        "fileExtensions": {"py": "python", "rs": "rust"},
        "folder": "folder",
    }
    theme_path = root / check_generated.ICON_THEME
    with theme_path.open("w", encoding="utf-8") as handle:
        json.dump(definition, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    assets_root = root / check_generated.ICON_ASSETS
    manifest = {
        "vendoredDefinitionSha256": check_generated.sha256(theme_path),
        "vendoredAssetsSha256": vendor_material_icons.assets_sha256(assets_root),
        "vendoredLicenseSha256": check_generated.sha256(license_path),
        "assetCount": 3,
    }
    manifest_path = root / check_generated.VENDOR_MANIFEST
    with manifest_path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")


class IconSnapshotTest(unittest.TestCase):
    """check_icon_snapshot against a synthetic tree."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)
        build_snapshot(self.root)
        self._real_root = check_generated.ROOT
        check_generated.ROOT = str(self.root)
        self.addCleanup(self._restore)

    def _restore(self):
        check_generated.ROOT = self._real_root
        self._tmp.cleanup()

    def check(self):
        return check_generated.check_icon_snapshot()

    def assertReports(self, fragment, problems, count=None):
        joined = "\n".join(problems)
        self.assertIn(fragment, joined, f"expected {fragment!r} in:\n{joined}")
        if count is not None:
            self.assertEqual(
                len(problems), count, f"expected {count} problem(s), got:\n{joined}"
            )

    # A consistent snapshot must be silent, or every test below proves nothing.
    def test_consistent_snapshot_reports_nothing(self):
        self.assertEqual(self.check(), [])

    # Absence: these raised FileNotFoundError before the guard was added, so
    # each of these tests fails as an error rather than a failure on regression.
    def test_missing_definition_is_reported_not_raised(self):
        (self.root / check_generated.ICON_THEME).unlink()
        self.assertReports("amber-material-icons.json: missing", self.check(), count=1)

    def test_missing_assets_tree_is_reported_not_raised(self):
        shutil.rmtree(self.root / check_generated.ICON_ASSETS)
        problems = self.check()
        self.assertReports(f"{check_generated.ICON_ASSETS}: missing", problems, count=1)

    def test_both_missing_are_reported_together(self):
        (self.root / check_generated.ICON_THEME).unlink()
        shutil.rmtree(self.root / check_generated.ICON_ASSETS)
        self.assertEqual(len(self.check()), 2)

    def test_missing_manifest_is_reported(self):
        (self.root / check_generated.VENDOR_MANIFEST).unlink()
        self.assertReports(check_generated.VENDOR_MANIFEST, self.check(), count=1)

    # Corruption: the count and the definition digest stay correct in all four
    # of these, so only the asset contents digest can catch them.
    def test_edited_asset_is_reported(self):
        target = self.root / check_generated.ICON_ASSETS / "files" / "python.svg"
        target.write_text("<svg>tampered</svg>", encoding="utf-8")
        self.assertReports("contents digest", self.check())

    def test_single_byte_change_is_reported(self):
        target = self.root / check_generated.ICON_ASSETS / "files" / "python.svg"
        with target.open("a", encoding="utf-8") as handle:
            handle.write(" ")
        self.assertReports("contents digest", self.check())

    def test_renamed_asset_is_reported(self):
        assets = self.root / check_generated.ICON_ASSETS / "files"
        (assets / "python.svg").rename(assets / "python2.svg")
        self.assertReports("contents digest", self.check())

    def test_swapped_asset_contents_are_reported(self):
        assets = self.root / check_generated.ICON_ASSETS / "files"
        python, rust = assets / "python.svg", assets / "rust.svg"
        python_text, rust_text = python.read_text(), rust.read_text()
        python.write_text(rust_text, encoding="utf-8")
        rust.write_text(python_text, encoding="utf-8")
        self.assertReports("contents digest", self.check())

    def test_edited_definition_is_reported(self):
        target = self.root / check_generated.ICON_THEME
        target.write_text(target.read_text() + "\n", encoding="utf-8")
        self.assertReports("vendoredDefinitionSha256", self.check())

    # Structural problems.
    def test_added_asset_is_reported(self):
        assets = self.root / check_generated.ICON_ASSETS / "files"
        (assets / "extra.svg").write_text("<svg>extra</svg>", encoding="utf-8")
        problems = self.check()
        self.assertReports("contents digest", problems)
        self.assertReports("assets on disk", problems)

    def test_unreferenced_asset_is_reported(self):
        # Add an asset and re-record the digest and count, so the only remaining
        # problem is that nothing points at it.
        assets = self.root / check_generated.ICON_ASSETS / "files"
        (assets / "orphan.svg").write_text("<svg>orphan</svg>", encoding="utf-8")
        manifest_path = self.root / check_generated.VENDOR_MANIFEST
        manifest = json.loads(manifest_path.read_text())
        manifest["assetCount"] = 4
        manifest["vendoredAssetsSha256"] = vendor_material_icons.assets_sha256(
            self.root / check_generated.ICON_ASSETS
        )
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        self.assertReports("never referenced", self.check(), count=1)

    def test_definition_pointing_at_missing_file_is_reported(self):
        # Point the definition at a file that does not exist, and keep the
        # digests consistent so only the dangling reference is left.
        theme_path = self.root / check_generated.ICON_THEME
        definition = json.loads(theme_path.read_text())
        definition["iconDefinitions"]["ghost"] = {
            "iconPath": "../icons/amber-material/files/ghost.svg"
        }
        with theme_path.open("w", encoding="utf-8") as handle:
            json.dump(definition, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        manifest_path = self.root / check_generated.VENDOR_MANIFEST
        manifest = json.loads(manifest_path.read_text())
        manifest["vendoredDefinitionSha256"] = check_generated.sha256(theme_path)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        self.assertReports("point at missing files", self.check(), count=1)

    # The third-party license is part of the snapshot: vendor_material_icons.py
    # writes it and the VSIX ships it, so losing it is a licensing problem.
    def test_missing_license_is_reported(self):
        (self.root / check_generated.VENDOR_LICENSE).unlink()
        self.assertReports(f"{check_generated.VENDOR_LICENSE}: missing", self.check(), count=1)

    def test_edited_license_is_reported(self):
        target = self.root / check_generated.VENDOR_LICENSE
        target.write_text("not the MIT license", encoding="utf-8")
        self.assertReports("vendoredLicenseSha256", self.check(), count=1)

    def test_manifest_without_license_digest_is_reported(self):
        manifest_path = self.root / check_generated.VENDOR_MANIFEST
        manifest = json.loads(manifest_path.read_text())
        del manifest["vendoredLicenseSha256"]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        self.assertReports("no vendoredLicenseSha256 recorded", self.check(), count=1)

    # Malformed JSON: a truncated file, conflict markers, or a replaced root
    # value must report rather than raise, for both files the checker parses.
    def test_truncated_manifest_is_reported_not_raised(self):
        target = self.root / check_generated.VENDOR_MANIFEST
        target.write_text('{"vendoredDefinitionSha256": "abc"', encoding="utf-8")
        self.assertReports("not valid JSON", self.check(), count=1)

    def test_manifest_with_conflict_markers_is_reported_not_raised(self):
        target = self.root / check_generated.VENDOR_MANIFEST
        target.write_text(
            '<<<<<<< HEAD\n{"a": 1}\n=======\n{"a": 2}\n>>>>>>> other\n',
            encoding="utf-8",
        )
        self.assertReports("not valid JSON", self.check(), count=1)

    def test_truncated_definition_is_reported_not_raised(self):
        target = self.root / check_generated.ICON_THEME
        target.write_text('{"iconDefinitions": {', encoding="utf-8")
        self.assertReports("not valid JSON", self.check(), count=1)

    def test_non_object_manifest_is_reported(self):
        target = self.root / check_generated.VENDOR_MANIFEST
        target.write_text("[1, 2, 3]", encoding="utf-8")
        self.assertReports("expected a JSON object", self.check(), count=1)

    def test_non_object_definition_is_reported(self):
        target = self.root / check_generated.ICON_THEME
        target.write_text('"just a string"', encoding="utf-8")
        self.assertReports("expected a JSON object", self.check(), count=1)

    def test_manifest_without_assets_digest_is_reported(self):
        # An older manifest predating vendoredAssetsSha256 must not silently
        # skip the asset check -- that was the original defect.
        manifest_path = self.root / check_generated.VENDOR_MANIFEST
        manifest = json.loads(manifest_path.read_text())
        del manifest["vendoredAssetsSha256"]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        self.assertReports("no vendoredAssetsSha256 recorded", self.check(), count=1)


class GeneratedFileTest(unittest.TestCase):
    """check_generated_files, which runs the real generator chain."""

    def setUp(self):
        self._real_root = check_generated.ROOT
        self.addCleanup(setattr, check_generated, "ROOT", self._real_root)

    def copy_generated_to(self, root):
        """Copy the committed generated files into a scratch root."""
        for relative in check_generated.GENERATED:
            destination = pathlib.Path(root) / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                pathlib.Path(self._real_root) / relative, destination
            )

    def test_repository_is_currently_in_sync(self):
        # The real tree, not a copy: asserts the committed outputs match what
        # the generators produce right now.
        self.assertEqual(check_generated.check_generated_files(), [])

    def test_hand_edited_output_is_reported(self):
        with tempfile.TemporaryDirectory() as scratch:
            self.copy_generated_to(scratch)
            target = pathlib.Path(scratch) / "themes" / "amber-material-hc.json"
            theme = json.loads(target.read_text())
            theme["colors"]["editor.background"] = "#DEADBE"
            target.write_text(json.dumps(theme, indent=2))
            check_generated.ROOT = scratch
            problems = check_generated.check_generated_files()
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("differs from generator output", problems[0])

    def test_deleted_output_is_reported(self):
        with tempfile.TemporaryDirectory() as scratch:
            self.copy_generated_to(scratch)
            (pathlib.Path(scratch) / "themes" / "amber-material-hc.json").unlink()
            check_generated.ROOT = scratch
            problems = check_generated.check_generated_files()
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("generated but not committed", problems[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
