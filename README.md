# Amber Material High Contrast

A high-contrast dark and light theme pair for VS Code and Cursor with an amber
accent, plus warm, Material-inspired high-contrast Ghostty terminal themes and a
bundled Amber Material file icon theme. The same amber identity also ships for
Codex, Claude Code, OpenCode, Windows Terminal, PowerShell, and Starship — the
editor and the terminal keep deliberately different surfaces, described under
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
environment in both dark and light variants:

- **Amber is the identity.** `#FFCB6B` marks fills, highlights, and buttons on both
  variants. On cream, amber *text* (links, line numbers) uses `#A65F00`, and the
  Ghostty caret plus Starship prompt use a yellower `#C99200` so glyphs stay
  readable without turning brown.
- **Material is the design language.** Layered surfaces, deliberate color roles,
  and restrained structural borders create hierarchy.
- **High Contrast is the functional promise.** Code, controls, and semantic
  states remain easy to distinguish on both the dark and light surfaces.

The theme's direct lineage is:

`Material-inspired design → Palenight → Amber Material High Contrast`

It retains Palenight's syntax foundation while giving the workbench and
terminal a distinct amber-led, higher-contrast identity.

## Install

This is a VS Code extension. The same VSIX installs in VS Code and in Cursor.
It is not listed on the VS Code Marketplace or Open VSX — package it from this
repository and install the file locally.

```sh
npx @vscode/vsce package
```

That writes `amber-material-theme-1.1.0.vsix` in the repository root.

### VS Code

```sh
code --install-extension amber-material-theme-1.1.0.vsix
```

### Cursor

```sh
cursor --install-extension amber-material-theme-1.1.0.vsix
```

Alternatively, in Cursor open the Command Palette (**Cmd+Shift+P** on macOS,
**Ctrl+Shift+P** on Windows/Linux) and run *Extensions: Install from VSIX…*,
then choose that file.

Then, in either editor, select both bundled themes:

1. **Cmd+K Cmd+T** / **Ctrl+K Ctrl+T** → *Amber Material High Contrast* or
   *Amber Material Light High Contrast*
2. **Cmd+Shift+P** / **Ctrl+Shift+P** → *Preferences: File Icon Theme* → *Amber Material Icons*

## Build

Run these in order — each step reads the output of the ones before it:

```sh
python3 scripts/build_ghostty.py      # ghostty/amber-material{,-light}
python3 scripts/build_theme.py        # themes/amber-material{-light,}-hc.json
python3 scripts/build_codex_theme.py  # codex/amber-material{-light,}-high-contrast.tmTheme
python3 scripts/build_terminal_suite.py   # Claude, OpenCode, Windows, PowerShell, Starship
python3 scripts/build_grok_theme.py   # grok/ palette export and pager.toml / pager-light.toml
python3 scripts/vendor_material_icons.py  # pinned VS Code icon snapshot
python3 scripts/check_generated.py    # verify nothing drifted
```

Tests for the drift check itself:

```sh
python3 scripts/test_check_generated.py
```

`scripts/build_ghostty.py` owns the terminal palette and runs first, because
the VS Code theme takes its 16 ANSI colors from it. `scripts/build_theme.py` is
the source of truth for everything else in VS Code and Cursor: it reads the
upstream MIT base (`scripts/base-palenight-italic.json`) and applies this
variant's palette on top. There is no second, Cursor-only theme file.
`scripts/build_codex_theme.py` combines the VS Code TextMate scopes
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

To re-accent the entire theme, edit the `DARK` and `LIGHT` profiles in
`scripts/variants.py`. Light keeps three amber roles on purpose: fill gold
(`amber_bright`, `#FFCB6B`), cream-readable text (`amber`, `#A65F00`), and
Ghostty/Starship prompt gold (`prompt_amber`, `#C99200`).

## VS Code palette (dark)

The same palette is the source of truth in Cursor. There is no second,
Cursor-only theme JSON.

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

## VS Code palette (light)

| Role | Hex |
| --- | --- |
| Editor / sidebar surface | `#FAF6EE` |
| Activity bar / status bar | `#F0EBE0` |
| Raised (tabs, widgets, hovers) | `#FFFFFF` |
| Foreground | `#1E2228` |
| Dimmed foreground | `#5A6070` |
| Structural border | `#D8D2C6` |
| Container border (recessive) | `#E8E2D8` |
| **Accent (amber fill)** | `#FFCB6B` |
| **Accent (amber on cream)** | `#A65F00` |
| Error / deletion | `#C62828` |
| Addition | `#4A7C1B` |
| Info / modification | `#2E5DB8` |

Editor and sidebar share that first surface on purpose. Cursor paints chat and
composer with `editor.background` rather than `sideBar.background`; because
those two tokens are the same hex here, the auxiliary bar matches Explorer
instead of looking like a different panel. Ghostty's caret and Starship's
prompt gold on cream are `#C99200`, not a VS Code workbench token.

### Border convention

Amber marks **state**, not structure. Focus rings, the active tab underline, and
the active sidebar indicator are amber; widget, popup, input, and peek-view
outlines use the recessive border (`#3A4052` dark, `#E8E2D8` light) so the UI
isn't a grid of yellow boxes.

## What a color theme does *not* control

The package ships both a color theme and a file icon theme, but VS Code and
Cursor keep them as separate selections. Font and layout preferences remain
user settings:

| Concern | Setting |
| --- | --- |
| Font family | `editor.fontFamily` |
| Font size | `editor.fontSize` |
| Line height | `editor.lineHeight` |
| Ligatures | `editor.fontLigatures` |
| Italics | controlled by the theme's `tokenColors` (this theme ships them) |
| File icons | the bundled *Amber Material Icons* theme |

### Cursor chat, composer, and Agents Window

Chat, composer, the auxiliary bar, and the parts of the agent panel that honor
a color theme use the VS Code tokens this generator already sets: `chat.*`,
`inlineChat.*`, `agents*`, `textLink.*`, scrollbars, tabs, and the status bar.

Two Cursor surfaces are **not** themeable from this package, and we do not
inject CSS or invent private tokens to fake them:

- **Agents Window chrome.** Some of that window ignores `workbench.colorTheme`.
  The `agents*` keys cover the slots VS Code actually registers; the rest of
  that chrome stays on Cursor's own default until Cursor themes it.
- **Agent chat file-path and citation links.** Those often use Cursor's
  `--cursor-text-link` color, which does not follow `textLink.foreground`.
  Markdown links that *do* honor `textLink.foreground` render in amber
  (`#FFCB6B` dark, `#A65F00` light).

### Suggested companion settings

These are optional. `workbench.colorTheme` and `workbench.iconTheme` are the
same keys in VS Code and in Cursor; set them after installing the VSIX if you
want the themes selected without using the Command Palette.

```jsonc
{
  "workbench.colorTheme": "Amber Material High Contrast", // or "Amber Material Light High Contrast"

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

`ghostty/amber-material` and `ghostty/amber-material-light` use purpose-built
terminal palettes: warm Gruvbox Material-style bases, clearer Material
Design-inspired ANSI colors, and the same amber identity accent as the VS Code
themes.

### Dark

| Role | Hex |
| --- | --- |
| Background | `#1D2021` |
| Foreground | `#E7E1D1` |
| Cursor / ANSI yellow | `#FFCB6B` |
| Selection background | `#4A3F28` |
| Selection foreground | `#FFF4D6` |

### Light

| Role | Hex |
| --- | --- |
| Background | `#FBF7EE` |
| Foreground | `#2B2926` |
| Cursor | `#C99200` |
| ANSI yellow | `#FFCB6B` |
| Selection background | `#E8D5A8` |
| Selection foreground | `#1E2228` |

### What the editor and the terminal share

The 16 ANSI colors are shared per variant: each VS Code theme takes its
`terminal.ansi*` values from the matching Ghostty file, so the same command
renders the same way in Ghostty and in VS Code's integrated terminal.

The surfaces are not. Ghostty's standalone window uses a slightly different
base from the editor so a dedicated terminal does not look like a second
workbench panel:

| Variant | Ghostty | Editor / integrated terminal |
| --- | --- | --- |
| Dark | `#1D2021` | `#22252F` |
| Light | `#FBF7EE` | `#FAF6EE` |

### Install the theme

From the repository root:

```sh
mkdir -p ~/.config/ghostty/themes
cp ghostty/amber-material ~/.config/ghostty/themes/amber-material
cp ghostty/amber-material-light ~/.config/ghostty/themes/amber-material-light
```

Ghostty looks up named custom themes in `~/.config/ghostty/themes` (or
`$XDG_CONFIG_HOME/ghostty/themes` when `XDG_CONFIG_HOME` is set).

### Configure Ghostty

Set the theme in your Ghostty configuration:

- macOS: `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty`
- XDG/Linux: `~/.config/ghostty/config.ghostty`

```ini
theme = amber-material          # or amber-material-light
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

Open **Settings → Appearance** and match the Ghostty surfaces so the desktop
app tracks the Codex CLI rather than the VS Code editor:

**Dark**

| Setting | Value |
| --- | --- |
| Base theme | Dark |
| Accent | `#FFCB6B` |
| Background | `#1D2021` |
| Foreground | `#E7E1D1` |
| Code font | `Cascadia Code NF` |

**Light**

| Setting | Value |
| --- | --- |
| Base theme | Light |
| Accent | `#FFCB6B` |
| Background | `#FBF7EE` |
| Foreground | `#2B2926` |
| Code font | `Cascadia Code NF` |

The dark pair is a 12.56:1 text contrast ratio. Accent stays the fill gold on
both; cream-readable amber (`#A65F00`) is for editor text, not this picker.
Keeping the system UI font preserves native macOS readability.

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
cp codex/amber-material-light-high-contrast.tmTheme \
  ~/.codex/themes/amber-material-light-high-contrast.tmTheme
```

Inside an interactive Codex CLI session, run `/theme` and choose
*Amber Material High Contrast* or *Amber Material Light High Contrast*.
Alternatively, configure it directly:

```toml
[tui]
theme = "amber-material-high-contrast"  # or amber-material-light-high-contrast
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

`grok/amber-material-high-contrast.json` and
`grok/amber-material-light-high-contrast.json` are the full palette exports:
all 59 color slots Grok's theme system defines, under the slot names from its
theming guide (`accent_user`, `bg_base`, `diff_insert_bg`, and so on).

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

`grok/pager.toml` and `grok/pager-light.toml` are the parts that take effect now.
Grok reads `~/.grok/pager.toml` for TUI appearance, and it accepts raw colors for
the scrollbar plus the block styling that the accents land on:

```sh
cp grok/pager.toml ~/.grok/pager.toml           # dark
cp grok/pager-light.toml ~/.grok/pager.toml   # light
```

Changes apply on restart. Every key and enum value in the generated file was
verified against the installed binary's own schema strings.

Since `[ui].theme` stays on one of the five built-ins, pick the one closest to
your variant — `groknight` for dark, `grokday` for light:

```toml
[ui]
theme = "groknight"  # or grokday for the light variant
```

Ghostty still controls the surrounding terminal background and ANSI colors, so
running Grok inside the Ghostty theme is what actually makes the session read
as Amber Material.

## Cross-terminal suite

The repository generates coordinated configurations for both dark and light
variants across:

| Tool | Theme responsibility |
| --- | --- |
| Claude Code | TUI accents, text roles, modes, and fullscreen surfaces |
| OpenCode | TUI surfaces, semantic roles, diffs, Markdown, and syntax |
| Windows Terminal | Terminal surfaces and the 16-color ANSI palette |
| PowerShell 7 | PSReadLine syntax, selection, prediction, and error colors |
| Starship | Cross-shell prompt layout, status, and Nerd Font symbols |

All five are generated from the existing Ghostty and VS Code palettes by
`scripts/build_terminal_suite.py`. Starship ships both palettes in one file,
`starship/amber-material.toml`: set `palette = "amber_material"` or
`palette = "amber_material_light"`. Cascadia Code NF is used by Starship for
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
