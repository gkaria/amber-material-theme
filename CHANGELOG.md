# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Fixed

- Reject uncommitted release inputs before packaging commit-pinned README links.

## [1.1.1] - 2026-09-19

### Added

- Extension icon and real dark/light VS Code screenshots for the listing.

- Pinned extension packaging tools, opt-in registry publishing workflow, and
  terminal-suite release ZIP with SHA-256 checksums.
- Publishing setup and distribution guide for editor and terminal themes.

### Changed

- `LICENSE` is the bare MIT text so GitHub detects the license. Palenight
  attribution now lives in `THIRD_PARTY_NOTICES.md` with the icon theme
  notice.

### Fixed

- Exclude Grok exports, build artifacts, and development dependencies from VSIX.

- README License section treats `THIRD_PARTY_NOTICES.md` as the index for
  Palenight and the icon theme, matching the post-relicense layout.
- Pull request template asks for a `[Unreleased]` changelog line, matching
  `CONTRIBUTING.md`.
- Changelog compare links no longer reference a missing `v1.0.0` tag.

## [1.1.0] - 2026-09-12

### Added

- Light high-contrast variant across every target: VS Code / Cursor, Ghostty,
  Codex, Claude Code, OpenCode, Windows Terminal, PowerShell, Starship, and
  Grok.
- Starship ships both palettes in one file; switch with
  `palette = "amber_material"` or `palette = "amber_material_light"`.
- Grok Build support: full palette export plus `pager.toml` /
  `pager-light.toml`.
- GitHub Actions CI running the drift check, its tests, and a VSIX package.
- Issue and pull request templates, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  and this changelog.

### Changed

- Relicensed under the MIT License. Previously proprietary; third-party
  material was already MIT / Apache-2.0 and is unchanged.
- Publisher identifier is now `gkaria`.
- Regenerated `starship/amber-material.toml` so the committed file matches
  the generator (dark palette default).
- VS Code theme is first-class in Cursor: `chat.*`, `inlineChat.*`, `agents*`,
  and `textLink.*` tokens are set; editor and sidebar share one surface so the
  auxiliary bar matches Explorer.
- Light amber roles documented: fill gold `#FFCB6B`, cream-readable text
  `#A65F00`, prompt gold `#C99200`.

## [1.0.0] - 2026-07-26

### Added

- Amber Material High Contrast dark theme for VS Code and Cursor, derived from
  the MIT-licensed Palenight theme.
- Ghostty terminal theme; the VS Code integrated terminal takes its 16 ANSI
  colors from it.
- Codex CLI `.tmTheme`, and a coordinated terminal suite for Claude Code,
  OpenCode, Windows Terminal, PowerShell, and Starship.
- Bundled Amber Material Icons: a pinned snapshot of Material Icon Theme
  5.37.0 with amber folders and `0.9` saturation.
- `scripts/check_generated.py` drift check with tests covering its failure
  modes.

[Unreleased]: https://github.com/gkaria/amber-material-theme/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/gkaria/amber-material-theme/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/gkaria/amber-material-theme/releases/tag/v1.1.0
[1.0.0]: https://github.com/gkaria/amber-material-theme/commit/c4dc0cc
