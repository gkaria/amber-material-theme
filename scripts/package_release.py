#!/usr/bin/env python3
"""Package the VSIX and portable terminal suite without installing user config."""

import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent.parent
TARGETS = (
    "ghostty", "codex", "claude-code", "opencode", "windows-terminal",
    "powershell", "starship", "grok", "palette",
)


def release_revision(root):
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root, text=True,
    )
    if status:
        raise SystemExit(
            "Release packaging requires a clean worktree. Commit or remove "
            "staged, unstaged, and untracked changes before packaging; "
            "README links are pinned to HEAD.\n" + status
        )
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True,
    ).strip()


def main():
    revision = release_revision(ROOT)
    manifest = json.loads((ROOT / "package.json").read_text())
    version = manifest["version"]
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    vsix = output / f"{manifest['name']}-{version}.vsix"
    repository = manifest["repository"]["url"].removesuffix(".git")
    # Invoke the pinned JS entry point directly, including on Windows.
    subprocess.run([
        "node", str(ROOT / "node_modules/@vscode/vsce/vsce"),
        "package", "--no-dependencies", "--out", str(vsix),
        "--baseContentUrl", f"{repository}/blob/{revision}",
        "--baseImagesUrl", f"{repository}/raw/{revision}",
    ], cwd=ROOT, check=True)

    files = [ROOT / name for name in (
        "README.md", "docs/terminal-suite.md", "docs/publishing.md",
        "LICENSE", "LICENSE-upstream-palenight.md",
        "LICENSE-material-icon-theme.txt", "LICENSE-Apache-2.0.txt",
        "THIRD_PARTY_NOTICES.md", "CHANGELOG.md",
    )]
    files.extend(sorted((ROOT / "docs/images").glob("*.png")))
    for target in TARGETS:
        assets = sorted(path for path in (ROOT / target).iterdir()
                        if path.is_file() and not path.name.startswith("."))
        if not assets:
            raise SystemExit(f"No theme files found for {target}")
        files.extend(assets)

    archive = output / f"amber-material-terminal-suite-{version}.zip"
    prefix = f"amber-material-terminal-suite-{version}"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(files):
            # Fixed timestamps and permissions make the terminal ZIP reproducible.
            info = zipfile.ZipInfo(f"{prefix}/{path.relative_to(ROOT).as_posix()}")
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())

    checksum = output / f"amber-material-{version}-SHA256SUMS.txt"
    checksum.write_text("".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
        for path in (vsix, archive)
    ))
    for path in (vsix, archive, checksum):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
