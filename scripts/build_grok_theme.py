#!/usr/bin/env python3
"""Generate the Grok Build palette export and pager.toml from the source palettes.

Two outputs, because Grok splits appearance across two mechanisms and only one
of them is open to us today:

  grok/amber-material-high-contrast.json
      Every color slot Grok's theme system defines, keyed by the slot names in
      its theming guide. Grok Build validates `[ui].theme` against a closed enum
      (groknight, grokday, tokyonight, rosepine-moon, oscura-midnight), so this
      file cannot be loaded as a theme yet -- see the README. It exists so the
      palette is pinned to the same source as every other target rather than
      re-derived by hand whenever xAI opens theme loading up.

  grok/pager.toml
      The subset Grok reads from disk today: ~/.grok/pager.toml. Only the keys
      that carry color or that shape the blocks the accents land on, so the file
      stays a statement of intent rather than a copy of every default.

Both derive from the Ghostty theme (terminal surfaces, 16 ANSI colors) and the
VS Code theme (editor surfaces, diff backgrounds), exactly like the Codex and
terminal-suite builders.
"""
import json
import os

import ghostty_palette

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

VSCODE_SRC = os.path.join(ROOT, "themes", "amber-material-hc.json")
GHOSTTY_SRC = os.path.join(ROOT, "ghostty", "amber-material")
JSON_DST = os.path.join(ROOT, "grok", "amber-material-high-contrast.json")
PAGER_DST = os.path.join(ROOT, "grok", "pager.toml")

THEME_NAME = "Amber Material High Contrast"


def flatten(color, over):
    """Composite a #RRGGBBAA VS Code color onto an opaque backdrop.

    Grok quantizes every color for the detected terminal capability and has no
    alpha channel to quantize, so the diff colors that VS Code stores as
    #RRGGBBAA have to arrive already flattened.

    Truncating the alpha instead of compositing would be wrong here rather than
    merely approximate: the diff line backgrounds carry alpha 0x14, so dropping
    it turns an 8% tint into a fully saturated fill and the diff text on top
    stops being legible.
    """
    if not (isinstance(color, str) and color.startswith("#") and len(color) == 9):
        return color
    alpha = int(color[7:9], 16) / 255
    channels = (
        round(int(color[i:i + 2], 16) * alpha + int(over[i:i + 2], 16) * (1 - alpha))
        for i in (1, 3, 5)
    )
    return "#" + "".join(f"{channel:02X}" for channel in channels)


with open(VSCODE_SRC, encoding="utf-8") as source:
    vscode_theme = json.load(source)

options, ansi = ghostty_palette.load(GHOSTTY_SRC)
ui = vscode_theme["colors"]

background = options["background"]
foreground = options["foreground"]
amber = options["cursor-color"]
selection = options["selection-background"]

surface = ui["editor.background"]
surface_deep = ui["activityBar.background"]
surface_raised = ui["editorWidget.background"]
border = ui["editorWidget.border"]
dim = ansi[8]
# ANSI 7 is the foreground in this palette, so it cannot carry the slots that
# have to read as distinct from primary text. The VS Code theme already has a
# muted-text color and a raised surface that do.
muted = ui["descriptionForeground"]
surface_highlight = ui["editorIndentGuide.background1"]

# Grok's slot list, in the order its theming guide documents them. Grouped the
# same way so a slot added upstream is easy to place.
theme = {
    "name": THEME_NAME,
    "backgrounds": {
        "bg_base": background,
        "bg_light": surface_raised,
        "bg_dark": surface_deep,
        # Not editor.lineHighlightBackground: that is #RRGGBBAA over the editor
        # surface, and flattening its alpha away lands on bg_light exactly.
        "bg_highlight": surface_highlight,
        # Not editorGroupHeader.tabsBackground (identical to
        # activityBar.background, so hover would collide with bg_dark) and not
        # list.hoverBackground (identical to editorWidget.background, which
        # would collide with bg_light). menu.selectionBackground is the
        # highlighted-row surface and is distinct from every other background
        # slot, so hover actually reads as a state change.
        "bg_hover": flatten(ui["menu.selectionBackground"], surface),
        "bg_terminal": background,
        "bg_visual": selection,
    },
    # Each accent marks a different kind of turn, so they lean on distinct hues
    # rather than shades of amber: amber stays the user's own accent (and the
    # OSC 12 cursor color), and the rest map to the role each ANSI color already
    # plays in the editor theme.
    "accents": {
        "accent_user": amber,
        "accent_assistant": ansi[4],
        "accent_thinking": ansi[5],
        "accent_tool": ansi[6],
        "accent_system": dim,
        "accent_error": ansi[1],
        "accent_success": ansi[2],
        "accent_running": ansi[11],
        "accent_skill": ansi[13],
        "accent_plan": ansi[12],
        "accent_verify": ansi[10],
        "accent_feedback": ansi[14],
        "accent_remember": ansi[5],
        "accent_model": ansi[9],
    },
    "text": {
        "text_primary": foreground,
        "text_secondary": muted,
    },
    "grays": {
        "gray_dim": border,
        "gray": dim,
        "gray_bright": ansi[15],
    },
    # `warning` is amber, the same color as accent_user and command. That is
    # inherited, not accidental: every warning slot in the VS Code theme is
    # #FFCB6B, and the 16-color palette has no second warm hue between amber and
    # red. Picking something else here would make Grok the one target whose
    # warnings disagree with the rest of the suite, so the collision stays and
    # position carries the distinction instead.
    "semantic": {
        "command": amber,
        "path": ansi[6],
        "running": ansi[11],
        "warning": ansi[3],
        "fuzzy_accent": ansi[11],
    },
    "borders": {
        "selection_border": amber,
        "hover_border": border,
        "prompt_border": border,
        "prompt_border_active": amber,
        "scrollbar_bg": surface_deep,
        "scrollbar_fg": border,
    },
    "paste": {
        "paste_bg": surface_raised,
        "paste_fg": foreground,
        "paste_dim": dim,
    },
    # The line backgrounds are tints over the editor surface in VS Code, so they
    # flatten onto that same surface here rather than onto bg_base.
    "diff": {
        "diff_delete_bg": flatten(ui["diffEditor.removedLineBackground"], surface),
        "diff_delete_fg": ansi[9],
        "diff_insert_bg": flatten(ui["diffEditor.insertedLineBackground"], surface),
        "diff_insert_fg": ansi[10],
        "diff_equal_fg": foreground,
        "diff_gutter_fg": dim,
    },
    # Headings step down h1..h6 from amber through the cooler accents so nesting
    # depth stays readable without any one level dominating.
    "markdown": {
        "md_heading_h1": amber,
        "md_heading_h2": ansi[11],
        "md_heading_h3": ansi[4],
        "md_heading_h4": ansi[12],
        "md_heading_h5": ansi[5],
        "md_heading_h6": ansi[13],
        "md_code": ansi[2],
        "md_code_bg": surface,
        "md_text": foreground,
        "md_muted": dim,
        "md_task_checked": ansi[2],
        "md_task_unchecked": dim,
        "link_fg": ansi[4],
    },
}

os.makedirs(os.path.dirname(JSON_DST), exist_ok=True)
with open(JSON_DST, "w", encoding="utf-8") as destination:
    json.dump(theme, destination, indent=2, ensure_ascii=False)
    destination.write("\n")

slot_count = sum(
    len(value) for value in theme.values() if isinstance(value, dict)
)

# Only the keys Grok honors from disk today, and only where Amber Material
# actually differs from the shipped defaults. scrollbar_bg/scrollbar_fg are the
# one place pager.toml takes raw colors, so they carry the palette; everything
# else here shapes the blocks those accents land on.
pager = f"""# {THEME_NAME} — Grok Build pager
# Generated by scripts/build_grok_theme.py; edit the source palettes instead.
# Install to ~/.grok/pager.toml (see README).
#
# Grok's `[ui].theme` only accepts its five built-in themes, so the surrounding
# TUI keeps whichever of those is active. These are the appearance settings Grok
# does read from disk.

[scrollback.layout]
outer_vpad = 1
outer_hpad_left = 2
outer_hpad_right = 2
block_pad_left = 2
block_pad_right = 2

[scrollback.scrollbar]
enabled = true
gap_left = 0
gap_right = 0
scrollbar_bg = "{surface_deep}"
scrollbar_fg = "{border}"

[scrollback.display]
sticky_headers = true
expandable_indicator = true
# Amber Material runs high-contrast, so dimmed accents stay further from the
# background than Grok's 0.5 default to keep collapsed blocks legible.
dim_accent = 0.6

[animation]
fps = 30
wave_rows = 32

[scrollback.blocks.edit]
indent = true
hunk_separator = "…"
dual_line_numbers = false
bg = "dark"

[scrollback.blocks.thinking]
accent_enabled = true
animate = true
truncated_lines = 3
bg_blend = 70
header = true
header_bright = false

[scrollback.blocks.tool]
muted_collapsed = true
dim_details = true
bullet = "diamond"

[scrollback.blocks.execute]
accent_enabled = true
header_style = "label"
muted_command_collapsed = true
first_lines = 2
last_lines = 3

[scrollback.blocks.prompt]
vpad = true
bg = "light"
show_prefix = true
min_lines = 2

[prompt]
collapse_unfocused = true
mouse_hover = true
show_prefix = true
"""

with open(PAGER_DST, "w", encoding="utf-8") as destination:
    destination.write(pager)

print(f"wrote {JSON_DST}: {slot_count} color slots")
print(f"wrote {PAGER_DST}")
