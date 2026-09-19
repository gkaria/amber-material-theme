# Contributing

Thanks for your interest. This repository is small, but it has one rule that
matters more than the rest: **every theme file is generated**. Edit the
sources, re-run the generators, and commit both.

## Prerequisites

- Python 3.10 or newer (standard library only; no packages to install)
- Node.js 22 or newer; run `npm ci --ignore-scripts` for pinned packaging tools
- Optionally, VS Code with the Material Icon Theme extension installed, only
  if you need to refresh the icon snapshot

## Where to make changes

| You want to change... | Edit this |
| --- | --- |
| Any color in either variant | `DARK` / `LIGHT` in `scripts/variants.py` |
| Which VS Code tokens get which role | `scripts/build_theme.py` |
| Ghostty surfaces or ANSI palette | `scripts/build_ghostty.py` |
| Codex `.tmTheme` | `scripts/build_codex_theme.py` |
| Claude Code, OpenCode, Windows Terminal, PowerShell, Starship | `scripts/build_terminal_suite.py` |
| Grok palette export or pager config | `scripts/build_grok_theme.py` |
| Upstream syntax scopes | `scripts/base-palenight-italic.json` (MIT, from Palenight) |

Never hand-edit files under `themes/`, `ghostty/`, `codex/`, `claude-code/`,
`opencode/`, `windows-terminal/`, `powershell/`, `starship/`, `grok/`,
`icon-themes/`, or `icons/amber-material/`. CI will reject the change.

## Build chain

Run the generators in this order. Each step reads the output of the ones
before it:

```sh
python3 scripts/build_ghostty.py
python3 scripts/build_theme.py
python3 scripts/build_codex_theme.py
python3 scripts/build_terminal_suite.py
python3 scripts/build_grok_theme.py
```

Or all at once:

```sh
npm run build
```

Then verify nothing drifted and the checker's own tests still pass:

```sh
npm run check   # python3 scripts/check_generated.py
npm test        # python3 scripts/test_check_generated.py
```

## Icon snapshot

`scripts/vendor_material_icons.py` reads a locally installed Material Icon
Theme extension and writes the pinned snapshot with amber folders. It is not
part of the normal build and cannot run in CI. Only refresh it deliberately,
bump the version in `THIRD_PARTY_NOTICES.md`, and commit the updated
`vendor/material-icon-theme.json` digests alongside the assets.

## Design constraints

Read the "Design philosophy" and "Border convention" sections of the README
before proposing palette changes. In short:

- Amber (`#FFCB6B`) marks **state** (focus, active tab, selection), not
  structure. Borders stay on the recessive grey.
- Both variants must stay high contrast. If you change a foreground or
  background, check the ratio against the surfaces it lands on.
- The 16 ANSI colors are shared between Ghostty and the integrated terminal.
  Editor and terminal *surfaces* are intentionally different.

## Pull requests

- Keep each PR to one concern.
- Include screenshots for visual changes, dark and light if both are affected.
- Update the README palette tables if a documented hex changes.
- Add a line under `[Unreleased]` in `CHANGELOG.md`.

## Testing locally

```sh
npm run package
code --install-extension amber-material-theme-*.vsix     # or: cursor --install-extension ...
```

## License

By contributing you agree that your contributions are licensed under the MIT
License, the same as the project.
