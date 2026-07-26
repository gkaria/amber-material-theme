# Terminal suite

Amber Material High Contrast uses one terminal palette across Ghostty, Claude
Code, OpenCode, Windows Terminal, PowerShell, and Starship. The generated files
reuse the existing Ghostty ANSI colors and VS Code surface colors; they do not
introduce a separate palette.

VS Code's integrated terminal shares the same 16 ANSI colors, but keeps the
cooler editor surface rather than Ghostty's warm base — see
[What the editor and the terminal share](../README.md#what-the-editor-and-the-terminal-share).

## Build

From the repository root. `build_terminal_suite.py` reads both
`ghostty/amber-material` and `themes/amber-material-hc.json`, so regenerate
those first if either has changed:

```sh
python3 scripts/build_ghostty.py
python3 scripts/build_theme.py
python3 scripts/build_terminal_suite.py
```

This generates:

| Tool | Artifact |
| --- | --- |
| Claude Code | `claude-code/amber-material-high-contrast.json` |
| OpenCode | `opencode/amber-material-high-contrast.json` |
| Windows Terminal | `windows-terminal/amber-material-high-contrast.json` |
| PowerShell 7 | `powershell/AmberMaterial.ps1` |
| Starship | `starship/amber-material.toml` |

## Claude Code

Custom themes require Claude Code 2.1.118 or newer.

macOS and Linux:

```sh
mkdir -p ~/.claude/themes
cp claude-code/amber-material-high-contrast.json ~/.claude/themes/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\themes"
Copy-Item ".\claude-code\amber-material-high-contrast.json" "$HOME\.claude\themes\"
```

Run `/theme` inside Claude Code and choose **Amber Material High Contrast**.
The theme uses `dark-ansi` as its base, so the surrounding terminal still
supplies the shared 16-color palette.

## OpenCode

OpenCode supports user-wide custom JSON themes.

macOS and Linux:

```sh
mkdir -p ~/.config/opencode/themes
cp opencode/amber-material-high-contrast.json ~/.config/opencode/themes/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\opencode\themes"
Copy-Item ".\opencode\amber-material-high-contrast.json" "$HOME\.config\opencode\themes\"
```

Run `/theme` inside OpenCode and choose **amber-material-high-contrast**.
This is the authoritative activation method for an existing profile because a
previously saved theme selection can take precedence over `tui.json`.

For a new or managed profile, create or update `~/.config/opencode/tui.json`:

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "amber-material-high-contrast"
}
```

The theme assigns the existing Amber Material palette to OpenCode's TUI
surfaces, semantic states, diff viewer, Markdown renderer, and syntax
highlighter. It uses explicit truecolor values, so run it in a terminal with
24-bit color support.

## Windows Terminal

Install the color scheme as a per-user Windows Terminal fragment:

```powershell
$FragmentDirectory = "$env:LOCALAPPDATA\Microsoft\Windows Terminal\Fragments\AmberMaterial"
New-Item -ItemType Directory -Force $FragmentDirectory
Copy-Item ".\windows-terminal\amber-material-high-contrast.json" "$FragmentDirectory\amber-material.json"
```

Then open Windows Terminal Settings and select **Amber Material High Contrast**
as the color scheme for the PowerShell profile or profile defaults. Set the
profile font face to `Cascadia Code NF` if that is the family name registered
on the Windows machine.

The fragment defines the background, foreground, cursor, selection, and all 16
ANSI colors. Windows Terminal reloads color-scheme changes after its settings
are saved.

## PowerShell 7

Copy the PSReadLine configuration:

```powershell
$ThemeDirectory = "$HOME\.config\amber-material"
New-Item -ItemType Directory -Force $ThemeDirectory
Copy-Item ".\powershell\AmberMaterial.ps1" "$ThemeDirectory\AmberMaterial.ps1"
```

Add these lines to the PowerShell profile shown by `$PROFILE`:

```powershell
. "$HOME\.config\amber-material\AmberMaterial.ps1"
Invoke-Expression (&starship init powershell)
```

The Windows Terminal scheme controls terminal surfaces and ANSI colors.
`AmberMaterial.ps1` controls PSReadLine syntax, selection, prediction, and
error colors. Starship controls only the prompt.

## Starship

Install Starship and copy the shared prompt configuration.

macOS:

```sh
brew install starship
mkdir -p ~/.config
cp starship/amber-material.toml ~/.config/starship.toml
```

Add this to `~/.zshrc`:

```sh
eval "$(starship init zsh)"
```

Windows:

```powershell
winget install --id Starship.Starship
New-Item -ItemType Directory -Force "$HOME\.config"
Copy-Item ".\starship\amber-material.toml" "$HOME\.config\starship.toml"
```

The prompt uses Nerd Font symbols for Git, operating systems, languages,
containers, cloud providers, and status. Its leading context is always
`user@hostname current-directory`, followed by Git and runtime information;
the same identity layout is used locally and over SSH.

Install and select Cascadia Code NF in
the host terminal. The font itself is not redistributed by this repository.

## Responsibility by layer

| Layer | Controls |
| --- | --- |
| Ghostty or Windows Terminal | Terminal surfaces and ANSI colors |
| Claude Code | Claude-specific TUI roles |
| OpenCode | OpenCode TUI surfaces, diffs, Markdown, and syntax |
| PSReadLine | PowerShell input syntax and prediction colors |
| Starship | Prompt layout, state, and Nerd Font symbols |

## References

- [Claude Code custom themes](https://code.claude.com/docs/en/terminal-config#create-a-custom-theme)
- [OpenCode custom themes](https://opencode.ai/docs/themes)
- [Windows Terminal color schemes](https://learn.microsoft.com/windows/terminal/customize-settings/color-schemes)
- [Windows Terminal fragments](https://learn.microsoft.com/windows/terminal/json-fragment-extensions)
- [PSReadLine colors](https://learn.microsoft.com/powershell/module/psreadline/set-psreadlineoption)
- [Starship configuration](https://starship.rs/config/)
- [Starship Nerd Font symbols](https://starship.rs/presets/nerd-font)
