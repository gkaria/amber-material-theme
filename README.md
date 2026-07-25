# Palenight Amber

A high-contrast dark theme for VS Code with an amber accent, plus a matching
Ghostty terminal theme generated from the same palette.

Derived from [vscode-palenight-theme](https://github.com/whizkydee/vscode-palenight-theme)
by Olaolu Olawuyi, used under the MIT License.

## Install (VS Code)

```sh
npx @vscode/vsce package
code --install-extension palenight-amber-1.0.0.vsix
```

Then **Cmd+K Cmd+T** → *Palenight Amber High Contrast*.

> Packaging from a path under `/tmp` silently produces an empty `.vsix`; build
> from a normal directory.

## Build

```sh
python3 scripts/build_theme.py     # themes/palenight-amber-hc.json
python3 scripts/build_ghostty.py   # ghostty/palenight-amber
```

`scripts/build_theme.py` is the source of truth. It reads the upstream MIT base
(`scripts/base-palenight-italic.json`) and applies this variant's palette on top.
Never hand-edit `themes/*.json` — it is regenerated.

To re-accent the entire theme, change one constant:

```python
AMBER = "#FFCB6B"   # cursors, scrollbars, badges, focus rings, links
```

## Palette

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
  "workbench.colorTheme": "Palenight Amber High Contrast",

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

  "terminal.integrated.fontFamily": "'Cascadia Code'",
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

`ghostty/palenight-amber` is generated from the built VS Code theme's
`terminal.*` slots, so both stay in sync.

```sh
cp ghostty/palenight-amber ~/.config/ghostty/themes/palenight-amber
```

Then in `~/.config/ghostty/config`:

```ini
theme = palenight-amber
font-family = Cascadia Code NF
font-size = 13
```

The NF (Nerd Font) build carries the Powerline and icon glyphs that prompts like
Starship and Powerlevel10k rely on; plain Cascadia Code renders those as tofu.

> Untested — generated from the palette but not yet verified in a running
> Ghostty. Validate with `ghostty +validate-config`.

## License

MIT — see [LICENSE](LICENSE). Retains the upstream Palenight copyright.
