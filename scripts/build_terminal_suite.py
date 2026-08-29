#!/usr/bin/env python3
"""Generate cross-terminal Amber Material configurations from source palettes."""

import json
from pathlib import Path

import ghostty_palette
from variants import ROOT, VARIANTS


def write_json(path, value):
  path.parent.mkdir(parents=True, exist_ok=True)
  with path.open("w", encoding="utf-8") as destination:
    json.dump(value, destination, indent=2, ensure_ascii=False)
    destination.write("\n")


def rgb(color):
  value = color.removeprefix("#")
  return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def build(variant):
  ghostty_source = ROOT / variant.ghostty_path
  vscode_source = ROOT / variant.vscode_path

  options, ansi = ghostty_palette.load(ghostty_source)
  vscode = json.loads(vscode_source.read_text(encoding="utf-8"))
  ui = vscode["colors"]

  background = options["background"]
  foreground = options["foreground"]
  amber = options["cursor-color"]
  selection = options["selection-background"]
  selection_foreground = options["selection-foreground"]
  surface = ui["editor.background"]
  surface_deep = ui["activityBar.background"]
  surface_raised = ui["editorWidget.background"]
  border = ui["editorWidget.border"]
  dim = ansi[8]

  claude_theme = {
    "name": variant.name,
    "base": variant.claude_base,
    "overrides": {
      "claude": amber,
      "claudeShimmer": ansi[11],
      "text": foreground,
      "inverseText": background,
      "inactive": dim,
      "inactiveShimmer": foreground,
      "subtle": border,
      "suggestion": ansi[11],
      "permission": ansi[4],
      "permissionShimmer": ansi[12],
      "remember": ansi[5],
      "success": ansi[2],
      "error": ansi[1],
      "warning": ansi[3],
      "warningShimmer": ansi[11],
      "merged": ansi[5],
      "promptBorder": amber,
      "promptBorderShimmer": ansi[11],
      "planMode": ansi[4],
      "autoAccept": ansi[2],
      "bashBorder": ansi[6],
      "ide": ansi[4],
      "fastMode": amber,
      "fastModeShimmer": ansi[11],
      "userMessageBackground": surface_raised,
      "userMessageBackgroundHover": ui["editorGroupHeader.tabsBackground"],
      "bashMessageBackgroundColor": surface_deep,
      "memoryBackgroundColor": surface_raised,
      "selectionBg": selection,
      "rate_limit_fill": amber,
      "rate_limit_empty": border,
      "briefLabelYou": ansi[4],
      "briefLabelClaude": amber,
      "red_FOR_SUBAGENTS_ONLY": ansi[1],
      "blue_FOR_SUBAGENTS_ONLY": ansi[4],
      "green_FOR_SUBAGENTS_ONLY": ansi[2],
      "yellow_FOR_SUBAGENTS_ONLY": ansi[3],
      "purple_FOR_SUBAGENTS_ONLY": ansi[5],
      "orange_FOR_SUBAGENTS_ONLY": ansi[9],
      "pink_FOR_SUBAGENTS_ONLY": ansi[13],
      "cyan_FOR_SUBAGENTS_ONLY": ansi[6],
    },
  }
  write_json(ROOT / variant.claude_path, claude_theme)

  opencode_theme = {
    "$schema": "https://opencode.ai/theme.json",
    "defs": {
      "background": background,
      "foreground": foreground,
      "surface": surface,
      "surfaceDeep": surface_deep,
      "surfaceRaised": surface_raised,
      "border": border,
      "dim": dim,
      "amber": amber,
      "amberBright": ansi[11],
      "red": ansi[1],
      "brightRed": ansi[9],
      "green": ansi[2],
      "brightGreen": ansi[10],
      "blue": ansi[4],
      "brightBlue": ansi[12],
      "purple": ansi[5],
      "brightPurple": ansi[13],
      "cyan": ansi[6],
      "diffAddedBackground": ui["diffEditor.insertedLineBackground"],
      "diffRemovedBackground": ui["diffEditor.removedLineBackground"],
      "diffAddedLineNumberBackground": ui["diffEditor.insertedTextBackground"],
      "diffRemovedLineNumberBackground": ui["diffEditor.removedTextBackground"],
    },
    "theme": {
      "primary": "amber",
      "secondary": "amber",
      "accent": "amberBright",
      "error": "red",
      "warning": "amber",
      "success": "green",
      "info": "blue",
      "text": "foreground",
      "textMuted": "dim",
      "selectedListItemText": "background",
      "background": "background",
      "backgroundPanel": "surface",
      "backgroundElement": "surfaceRaised",
      "backgroundMenu": "surfaceRaised",
      "border": "border",
      "borderActive": "amber",
      "borderSubtle": "border",
      "diffAdded": "green",
      "diffRemoved": "red",
      "diffContext": "dim",
      "diffHunkHeader": "blue",
      "diffHighlightAdded": "brightGreen",
      "diffHighlightRemoved": "brightRed",
      "diffAddedBg": "diffAddedBackground",
      "diffRemovedBg": "diffRemovedBackground",
      "diffContextBg": "surfaceDeep",
      "diffLineNumber": "dim",
      "diffAddedLineNumberBg": "diffAddedLineNumberBackground",
      "diffRemovedLineNumberBg": "diffRemovedLineNumberBackground",
      "markdownText": "foreground",
      "markdownHeading": "amber",
      "markdownLink": "blue",
      "markdownLinkText": "cyan",
      "markdownCode": "green",
      "markdownBlockQuote": "dim",
      "markdownEmph": "amberBright",
      "markdownStrong": "amber",
      "markdownHorizontalRule": "border",
      "markdownListItem": "amber",
      "markdownListEnumeration": "cyan",
      "markdownImage": "blue",
      "markdownImageText": "cyan",
      "markdownCodeBlock": "foreground",
      "syntaxComment": "dim",
      "syntaxKeyword": "purple",
      "syntaxFunction": "blue",
      "syntaxVariable": "brightPurple",
      "syntaxString": "green",
      "syntaxNumber": "brightGreen",
      "syntaxType": "brightBlue",
      "syntaxOperator": "cyan",
      "syntaxPunctuation": "foreground",
    },
  }
  write_json(ROOT / variant.opencode_path, opencode_theme)

  windows_scheme = {
    "name": variant.name,
    "cursorColor": amber,
    "selectionBackground": selection,
    "background": background,
    "foreground": foreground,
    "black": ansi[0],
    "red": ansi[1],
    "green": ansi[2],
    "yellow": ansi[3],
    "blue": ansi[4],
    "purple": ansi[5],
    "cyan": ansi[6],
    "white": ansi[7],
    "brightBlack": ansi[8],
    "brightRed": ansi[9],
    "brightGreen": ansi[10],
    "brightYellow": ansi[11],
    "brightBlue": ansi[12],
    "brightPurple": ansi[13],
    "brightCyan": ansi[14],
    "brightWhite": ansi[15],
  }
  write_json(
    ROOT / variant.windows_terminal_path,
    {"schemes": [windows_scheme]},
  )

  selection_fg_rgb = ";".join(str(channel) for channel in rgb(selection_foreground))
  selection_bg_rgb = ";".join(str(channel) for channel in rgb(selection))
  amber_rgb = ";".join(str(channel) for channel in rgb(amber))
  background_rgb = ";".join(str(channel) for channel in rgb(background))

  powershell = f"""# {variant.name} — PowerShell 7 / PSReadLine
# Generated by scripts/build_terminal_suite.py; edit the source palettes instead.
#Requires -Version 7.2

${variant.powershell_class}Escape = [char]0x1b
${variant.powershell_class}Colors = @{{
    ContinuationPrompt      = "{dim}"
    Emphasis                = "{ansi[11]}"
    Error                   = "{ansi[1]}"
    Selection               = "${{{variant.powershell_class}Escape}}[38;2;{selection_fg_rgb};48;2;{selection_bg_rgb}m"
    Default                 = "{foreground}"
    Comment                 = "{dim}"
    Keyword                 = "{ansi[5]}"
    String                  = "{ansi[2]}"
    Operator                = "{ansi[6]}"
    Variable                = "{ansi[5]}"
    Command                 = "{amber}"
    Parameter               = "{ansi[11]}"
    Type                    = "{ansi[4]}"
    Number                  = "{ansi[10]}"
    Member                  = "{ansi[12]}"
    InlinePrediction        = "{dim}"
    ListPrediction          = "{foreground}"
    ListPredictionSelected  = "${{{variant.powershell_class}Escape}}[38;2;{background_rgb};48;2;{amber_rgb}m"
    ListPredictionTooltip   = "{dim}"
}}

if (Get-Module -ListAvailable -Name PSReadLine) {{
    Import-Module PSReadLine
    Set-PSReadLineOption -Colors ${variant.powershell_class}Colors
}}
"""
  power_shell_path = ROOT / variant.powershell_path
  power_shell_path.parent.mkdir(parents=True, exist_ok=True)
  power_shell_path.write_text(powershell, encoding="utf-8")

  starship = f"""# {variant.name} — Starship prompt
# Generated by scripts/build_terminal_suite.py; edit the source palettes instead.
"$schema" = "https://starship.rs/config-schema.json"

add_newline = true
palette = "{variant.starship_palette}"
format = \"$os$username$hostname$directory$git_branch$git_status$package$nodejs$python$rust$golang$java$dotnet$docker_context$kubernetes$aws$azure$gcloud$line_break$character\"
right_format = "$status$cmd_duration$time"

[palettes.{variant.starship_palette}]
background = "{background}"
foreground = "{foreground}"
surface = "{surface}"
surface_deep = "{surface_deep}"
surface_raised = "{surface_raised}"
border = "{border}"
dim = "{dim}"
amber = "{amber}"
amber_bright = "{ansi[11]}"
red = "{ansi[1]}"
bright_red = "{ansi[9]}"
green = "{ansi[2]}"
bright_green = "{ansi[10]}"
blue = "{ansi[4]}"
bright_blue = "{ansi[12]}"
purple = "{ansi[5]}"
bright_purple = "{ansi[13]}"
cyan = "{ansi[6]}"
bright_cyan = "{ansi[14]}"
white = "{ansi[15]}"
selection = "{selection}"

[os]
disabled = false
format = "[$symbol]($style)"
style = "bold amber"

[os.symbols]
Macos = " "
Windows = "󰍲 "
Linux = " "
Ubuntu = " "
Debian = " "
Fedora = " "
Arch = " "

[username]
format = "[$user]($style)"
show_always = true
style_root = "bold red"
style_user = "dim"

[hostname]
format = "[@$hostname](bold blue) "
ssh_only = false

[directory]
format = "[$path]($style)[$read_only]($read_only_style) "
read_only = " 󰌾"
read_only_style = "red"
style = "bold amber"
truncation_length = 4
truncate_to_repo = true

[git_branch]
format = "on [$symbol$branch(:$remote_branch)]($style) "
symbol = " "
style = "bold blue"

[git_status]
format = "([$all_status$ahead_behind]($style) )"
style = "bold amber_bright"

[package]
format = "via [$symbol$version]($style) "
symbol = "󰏗 "
style = "purple"

[nodejs]
format = "via [$symbol($version )]($style)"
symbol = " "
style = "green"

[python]
format = "via [$symbol($version )]($style)"
symbol = " "
style = "amber_bright"

[rust]
format = "via [$symbol($version )]($style)"
symbol = "󱘗 "
style = "bright_red"

[golang]
format = "via [$symbol($version )]($style)"
symbol = " "
style = "cyan"

[java]
format = "via [$symbol($version )]($style)"
symbol = " "
style = "bright_red"

[dotnet]
format = "via [$symbol($version )(🎯 $tfm )]($style)"
symbol = " "
style = "purple"

[docker_context]
format = "via [$symbol$context]($style) "
symbol = " "
style = "blue"

[kubernetes]
disabled = false
format = 'on [$symbol$context( \\($namespace\\))]($style) '
symbol = "󱃾 "
style = "cyan"

[aws]
format = 'on [$symbol($profile )(\\($region\\) )]($style)'
symbol = " "
style = "amber"

[azure]
format = "on [$symbol($subscription)]($style) "
symbol = " "
style = "blue"

[gcloud]
format = 'on [$symbol$account(@$domain)(\\($region\\))]($style) '
symbol = "󱇶 "
style = "bright_blue"

[status]
disabled = false
format = "[$symbol$status]($style) "
symbol = " "
style = "bold red"

[cmd_duration]
format = "took [$duration]($style) "
min_time = 2_000
style = "dimmed dim"

[time]
disabled = false
format = "[$time]($style)"
style = "dimmed dim"
time_format = "%H:%M"

[character]
success_symbol = "[❯](bold amber)"
error_symbol = "[❯](bold red)"
vimcmd_symbol = "[❮](bold amber)"
"""
  starship_path = ROOT / variant.starship_path
  starship_path.parent.mkdir(parents=True, exist_ok=True)
  starship_path.write_text(starship, encoding="utf-8")

  print(f"wrote {variant.claude_path}, {variant.opencode_path}, "
        f"{variant.windows_terminal_path}, {variant.powershell_path}, "
        f"{variant.starship_path}")


def main():
  for variant in VARIANTS:
    build(variant)


if __name__ == "__main__":
  main()
