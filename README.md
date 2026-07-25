# Amber Material High Contrast

A high-contrast dark theme for VS Code with an amber accent, plus a warm,
Material-inspired high-contrast Ghostty terminal theme.

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

Then **Cmd+K Cmd+T** → *Amber Material High Contrast*.

## Build

```sh
python3 scripts/build_theme.py     # themes/amber-material-hc.json
python3 scripts/build_ghostty.py   # ghostty/amber-material
```

`scripts/build_theme.py` is the source of truth for VS Code. It reads the
upstream MIT base (`scripts/base-palenight-italic.json`) and applies this
variant's palette on top. `scripts/build_ghostty.py` owns the separate terminal
palette. Never hand-edit generated files in `themes/` or `ghostty/`.

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

A VS Code color theme only sets colors. These are user settings, not theme
properties — a theme extension cannot bundle them:

| Concern | Setting |
| --- | --- |
| Font family | `editor.fontFamily` |
| Font size | `editor.fontSize` |
| Line height | `editor.lineHeight` |
| Ligatures | `editor.fontLigatures` |
| Italics | controlled by the theme's `tokenColors` (this theme ships them) |
| File icons | a separate *icon theme* extension |

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

  // Icons: Material Icon Theme (MIT), tinted to match the amber accent.
  "workbench.iconTheme": "material-icon-theme",
  "material-icon-theme.folders.color": "#FFCB6B",
  "material-icon-theme.rootFolders.color": "#FFCB6B",
  "material-icon-theme.saturation": 0.9,

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

Icon themes are separate extensions because they ship SVG assets, not colors.
[Material Icon Theme](https://github.com/material-extensions/vscode-material-icon-theme)
is MIT-licensed and exposes folder/file color settings, so its folder icons can
be tinted to this theme's accent.

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

## License

This project is currently proprietary and is not offered under an open-source
license. See [LICENSE](LICENSE).

It contains material derived from the MIT-licensed Palenight theme. The
upstream copyright and license are retained in
[LICENSE-upstream-palenight.md](LICENSE-upstream-palenight.md).
