# Amber Material High Contrast

A high-contrast dark theme for VS Code with an amber accent, plus a warm,
Material-inspired high-contrast Ghostty terminal theme and a bundled Amber
Material file icon theme. The same amber identity also ships for Codex, Claude
Code, OpenCode, Windows Terminal, PowerShell, and Starship — the editor and the
terminal keep deliberately different surfaces, described under
[Ghostty](#ghostty).

Derived from [vscode-palenight-theme](https://github.com/whizkydee/vscode-palenight-theme)
by Olaolu Olawuyi, used under the MIT License.

## Design philosophy

“Material” describes the design language, not a claim that this is an official
Google theme or a reproduction of Google's palette. [Material Design](https://design.google/library/material-design-launch-2014)
began at Google as a system inspired by physical surfaces such as paper and
ink, using hierarchy, spacing, color, light, and motion to make interfaces
easier to understand.

Amber Material High Contrast carries those principles into a developer
environment:

- **Amber is the identity.** `#FFCB6B` marks focus, selection, and active state.
- **Material is the design language.** Layered surfaces, deliberate color roles,
  and restrained structural borders create hierarchy.
- **High Contrast is the functional promise.** Code, controls, and semantic
  states remain easy to distinguish on dark backgrounds.

The theme's direct lineage is:

`Material-inspired design → Palenight → Amber Material High Contrast`

It retains Palenight's syntax foundation while giving the workbench and
terminal a distinct amber-led, higher-contrast identity.

## Install (VS Code)

```sh
npx @vscode/vsce package
code --install-extension amber-material-theme-1.0.0.vsix
```

Then select both bundled themes:

1. **Cmd+K Cmd+T** → *Amber Material High Contrast*
2. **Cmd+Shift+P** → *Preferences: File Icon Theme* → *Amber Material Icons*

## Build

Run these in order — each step reads the output of the ones before it:

```sh
python3 scripts/build_ghostty.py      # ghostty/amber-material
python3 scripts/build_theme.py        # themes/amber-material-hc.json
python3 scripts/build_codex_theme.py  # codex/amber-material-high-contrast.tmTheme
python3 scripts/build_terminal_suite.py   # Claude, OpenCode, Windows, PowerShell, Starship
python3 scripts/build_grok_theme.py   # grok/ palette export and pager.toml
python3 scripts/vendor_material_icons.py  # pinned VS Code icon snapshot
python3 scripts/check_generated.py    # verify nothing drifted
```

Tests for the drift check itself:

```sh
python3 scripts/test_check_generated.py
```

`scripts/build_ghostty.py` owns the terminal palette and runs first, because
the VS Code theme takes its 16 ANSI colors from it. `scripts/build_theme.py` is
the source of truth for everything else in VS Code: it reads the upstream MIT
base (`scripts/base-palenight-italic.json`) and applies this variant's palette
on top. `scripts/build_codex_theme.py` combines the VS Code TextMate scopes
with the Ghostty terminal surfaces for Codex CLI.
`scripts/ghostty_palette.py` is the shared reader for the Ghostty theme.

`scripts/check_generated.py` re-runs the chain into a temporary tree and
compares every generated file, so a hand edit or a stale output fails loudly
instead of sitting in the repository unnoticed. It also verifies the icon
snapshot against the digests recorded in `vendor/material-icon-theme.json`,
since `vendor_material_icons.py` needs an installed VS Code extension and
cannot run offline.

`scripts/test_check_generated.py` covers that checker's failure modes — a
corrupted, renamed or deleted asset, a missing definition, a dangling
reference — against a synthetic snapshot in a temporary directory. The happy
path is easy to get right and was the only thing originally exercised; these
are the cases that were not.

`scripts/vendor_material_icons.py` snapshots Material Icon Theme 5.37.0 from a
locally installed VS Code extension, then deterministically applies amber
folders (`#FFCB6B`) and `0.9` saturation. It has no runtime dependency on
the upstream extension. Never hand-edit generated files in `themes/`,
`ghostty/`, `codex/`, `claude-code/`, `opencode/`, `windows-terminal/`,
`powershell/`, `starship/`, `grok/`, `icon-themes/`, or `icons/amber-material/`.

To re-accent the entire theme, change one constant:

```python
AMBER = "#FFCB6B"   # cursors, scrollbars, badges, focus rings, links
```

## VS Code palette

| Role | Hex |
| --- | --- |
| Editor / sidebar surface | `#22252F` |
| Activity bar / status bar | `#1C1F27` |
| Raised (tabs, widgets, hovers) | `#2A2E3A` |
| Foreground | `#D2D7E4` |
| Dimmed foreground | `#8A91A6` |
| Structural border | `#333846` |
| Container border (recessive) | `#3A4052` |
| **Accent (amber)** | `#FFCB6B` |
| Error / deletion | `#ff5572` |
| Addition | `#a9c77d` |
| Info / modification | `#82AAFF` |

### Border convention

Amber marks **state**, not structure. Focus rings, the active tab underline, and
the active sidebar indicator are amber; widget, popup, input, and peek-view
outlines use the recessive `#3A4052` so the UI isn't a grid of yellow boxes.

## What a color theme does *not* control

The VS Code package ships both a color theme and a file icon theme, but VS Code
keeps them as separate selections. Font and layout preferences remain user
settings:

| Concern | Setting |
| --- | --- |
| Font family | `editor.fontFamily` |
| Font size | `editor.fontSize` |
| Line height | `editor.lineHeight` |
| Ligatures | `editor.fontLigatures` |
| Italics | controlled by the theme's `tokenColors` (this theme ships them) |
| File icons | the bundled *Amber Material Icons* theme |

### Suggested companion settings

```jsonc
{
  "workbench.colorTheme": "Amber Material High Contrast",

  // Cascadia Code NF: ligatures + Nerd Font glyphs for terminal prompts.
  // brew install --cask font-cascadia-code-nf
  "editor.fontFamily": "'Cascadia Code NF', 'Cascadia Code', Menlo, monospace",
  "editor.fontSize": 13,
  "editor.lineHeight": 1.6,
  "editor.fontLigatures": true,

  // Bundled, pinned Material Icon Theme snapshot with amber folders.
  "workbench.iconTheme": "amber-material-icons",

  "terminal.integrated.fontFamily": "'Cascadia Code NF', 'Cascadia Code', Menlo, monospace",
  "terminal.integrated.fontSize": 13
}
```

### Fonts

```sh
brew install --cask font-cascadia-code-nf   # ligatures + Nerd Font glyphs
brew install --cask font-cascadia-mono-nf   # same, without ligatures
```

| Family | Ligatures | Nerd Font glyphs |
| --- | --- | --- |
| `Cascadia Code` | yes | no |
| `Cascadia Mono` | no | no |
| `Cascadia Code NF` | yes | yes |
| `Cascadia Mono NF` | no | yes |

Use the family name exactly as macOS registers it (`Cascadia Code NF`, not
`CascadiaCodeNF`); check with:

```sh
system_profiler SPFontsDataType | grep -i 'family: cascadia'
```

The extension includes **Amber Material Icons**, a static snapshot of
[Material Icon Theme 5.37.0](https://github.com/material-extensions/vscode-material-icon-theme/tree/v5.37.0).
Its SVG assets travel inside the VSIX, so installing the upstream icon
extension is not required and upstream deprecation cannot remove this snapshot.

Cascadia Code NF is intentionally not bundled. It is already installed on this
machine and remains the recommended editor and terminal font; its Nerd Font
glyphs are useful in prompts and code, while Explorer uses the more portable
bundled SVG icons.

## Ghostty

`ghostty/amber-material` uses a purpose-built terminal palette: a warm
Gruvbox Material-style near-black base, clearer Material Design-inspired ANSI
colors, and the same amber identity accent as the VS Code theme.

| Role | Hex |
| --- | --- |
| Background | `#1D2021` |
| Foreground | `#E7E1D1` |
| Cursor / ANSI yellow | `#FFCB6B` |
| Selection background | `#4A3F28` |
| Selection foreground | `#FFF4D6` |

### What the editor and the terminal share

The 16 ANSI colors are shared: `themes/amber-material-hc.json` takes its
`terminal.ansi*` values from this file, so the same command renders the same way
in Ghostty and in VS Code's integrated terminal.

The surfaces are not. Ghostty's warm `#1D2021` base is for a standalone window,
while the integrated terminal keeps the cooler `#22252F` editor tone — that
panel sits beside the editor, so it matches its neighbour rather than the
standalone terminal.

### Install the theme

From the repository root:

```sh
mkdir -p ~/.config/ghostty/themes
cp ghostty/amber-material ~/.config/ghostty/themes/amber-material
```

Ghostty looks up named custom themes in `~/.config/ghostty/themes` (or
`$XDG_CONFIG_HOME/ghostty/themes` when `XDG_CONFIG_HOME` is set).

### Configure Ghostty

Set the theme in your Ghostty configuration:

- macOS: `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty`
- XDG/Linux: `~/.config/ghostty/config.ghostty`

```ini
theme = amber-material
font-family = Cascadia Code NF
font-size = 16
```

Keep your preferred font size if it differs. `Cascadia Code NF` gives VS Code,
Ghostty, and prompts such as Starship or Powerlevel10k the same glyph coverage.
Ghostty 1.2 and newer also include a Nerd Font symbols fallback, so an NF-patched
primary font is optional in Ghostty even though it is useful for consistency
across applications.

Reload the configuration with **Cmd+Shift+,** on macOS or **Ctrl+Shift+,** on
Linux. New terminals will use the updated theme.

### Validate

If the `ghostty` CLI is on `PATH`:

```sh
ghostty +validate-config
```

For the standard macOS app installation:

```sh
/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
```

## Codex

### Desktop app

Open **Settings → Appearance** and use:

| Setting | Value |
| --- | --- |
| Base theme | Dark |
| Accent | `#FFCB6B` |
| Background | `#1D2021` |
| Foreground | `#E7E1D1` |
| Code font | `Cascadia Code NF` |

This pair provides a 12.56:1 text contrast ratio while staying within the
existing Amber Material palette. The background is the warm terminal base, so
the desktop app matches the Codex CLI rather than the VS Code editor surface.
Keeping the system UI font preserves native
macOS readability.

### CLI

The generated Codex CLI theme uses the warmer Ghostty background and foreground
for terminal continuity, then carries over the VS Code TextMate syntax rules.

Regenerate it with the [build chain](#build) — the order matters there, since
`build_codex_theme.py` reads both the Ghostty palette and the VS Code theme, and
`build_theme.py` in turn reads the Ghostty palette. Then install it:

```sh
mkdir -p ~/.codex/themes
cp codex/amber-material-high-contrast.tmTheme \
  ~/.codex/themes/amber-material-high-contrast.tmTheme
```

Inside an interactive Codex CLI session, run `/theme` and choose
*Amber Material High Contrast*. Alternatively, configure it directly:

```toml
[tui]
theme = "amber-material-high-contrast"
```

The `.tmTheme` controls syntax-highlighted code blocks and diffs. Ghostty still
controls the surrounding terminal background and ANSI colors.

Codex theme support is documented in the
[official CLI customization guide](https://learn.chatgpt.com/docs/cli-customization#syntax-highlighting-and-themes).

## Grok Build

`scripts/build_grok_theme.py` generates two files in `grok/`. They are split
this way because Grok divides appearance across two mechanisms, and only one of
them currently accepts outside input.

### What Grok does not load yet

`grok/amber-material-high-contrast.json` is the full palette export: all 59
color slots Grok's theme system defines, under the slot names from its theming
guide (`accent_user`, `bg_base`, `diff_insert_bg`, and so on).

**Grok cannot load it today.** Grok Build validates `[ui].theme` against a
closed set of five built-in themes — `groknight`, `grokday`, `tokyonight`,
`rosepine-moon`, `oscura-midnight` — and rejects anything else with
`unknown theme name`. There is no `custom_theme`, `theme_path`, or theme
directory setting. The bundled `.tmTheme` files for code blocks are compiled
into the binary and, per xAI's own guide, "you cannot replace them with your
own."

The export exists so the palette is derived from the same source as every
other target and stays in the drift check, rather than being reconstructed by
hand if and when xAI opens theme loading up. It is also directly usable as a
machine-readable palette by anything else that reads one.

### What Grok does load

`grok/pager.toml` is the part that takes effect now. Grok reads
`~/.grok/pager.toml` for TUI appearance, and it accepts raw colors for the
scrollbar plus the block styling that the accents land on:

```sh
cp grok/pager.toml ~/.grok/pager.toml
```

Changes apply on restart. Every key and enum value in the generated file was
verified against the installed binary's own schema strings.

Since `[ui].theme` stays on one of the five built-ins, pick the one closest to
this palette — `groknight` is the neutral dark base:

```toml
[ui]
theme = "groknight"
```

Ghostty still controls the surrounding terminal background and ANSI colors, so
running Grok inside the Ghostty theme is what actually makes the session read
as Amber Material.

## Cross-terminal suite

The repository also generates coordinated configurations for:

| Tool | Theme responsibility |
| --- | --- |
| Claude Code | TUI accents, text roles, modes, and fullscreen surfaces |
| OpenCode | TUI surfaces, semantic roles, diffs, Markdown, and syntax |
| Windows Terminal | Terminal surfaces and the 16-color ANSI palette |
| PowerShell 7 | PSReadLine syntax, selection, prediction, and error colors |
| Starship | Cross-shell prompt layout, status, and Nerd Font symbols |

All five are generated from the existing Ghostty and VS Code palettes by
`scripts/build_terminal_suite.py`. Cascadia Code NF is used by Starship for
symbols but remains an installation prerequisite rather than a redistributed
font.

See [Terminal suite setup](docs/terminal-suite.md) for macOS, Linux, and Windows
installation instructions.

## License

This project is currently proprietary and is not offered under an open-source
license. See [LICENSE](LICENSE).

It contains material derived from the MIT-licensed Palenight theme. The
upstream copyright and license are retained in
[LICENSE-upstream-palenight.md](LICENSE-upstream-palenight.md).

The bundled icon theme is derived from the MIT-licensed Material Icon Theme.
Its license and the relevant icon-source notices are retained in
[LICENSE-material-icon-theme.txt](LICENSE-material-icon-theme.txt),
[LICENSE-Apache-2.0.txt](LICENSE-Apache-2.0.txt), and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
