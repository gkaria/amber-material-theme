"""Exercise release revision checks against disposable Git repositories."""

from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import package_release


class ReleaseRevisionTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git("init", "-q")
        (self.root / "README.md").write_text("Committed README\n")
        (self.root / ".gitignore").write_text("dist/\nnode_modules/\n")
        self.git("add", ".")
        self.git("-c", "user.name=Release Test", "-c",
                 "user.email=test@example.invalid", "commit", "-qm", "Fixture")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def test_clean_tree_returns_head(self):
        self.assertEqual(package_release.release_revision(self.root),
                         self.git("rev-parse", "HEAD"))

    def test_ignored_build_outputs_are_allowed(self):
        for folder in ("dist", "node_modules"):
            (self.root / folder).mkdir()
            (self.root / folder / "output").write_text("ignored")
        self.test_clean_tree_returns_head()

    def test_unstaged_document_change_is_rejected(self):
        (self.root / "README.md").write_text("Uncommitted README\n")
        with self.assertRaisesRegex(SystemExit, "clean worktree"):
            package_release.release_revision(self.root)

    def test_staged_document_change_is_rejected(self):
        (self.root / "README.md").write_text("Staged README\n")
        self.git("add", "README.md")
        with self.assertRaisesRegex(SystemExit, "clean worktree"):
            package_release.release_revision(self.root)

    def test_untracked_image_stops_packaging_before_outputs(self):
        (self.root / "docs/images").mkdir(parents=True)
        (self.root / "docs/images/new.png").write_bytes(b"untracked fixture")
        with patch.object(package_release, "ROOT", self.root):
            with self.assertRaisesRegex(SystemExit, "clean worktree"):
                package_release.main()
        self.assertFalse((self.root / "dist").exists())


if __name__ == "__main__":
    unittest.main()
