#!/usr/bin/env python3
"""Variant profiles for Amber Material High Contrast (dark and light)."""

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

UPSTREAM_PURPLE = "#7E57C2"
UPSTREAM_PURPLE_DEEP = "#694CA4"
UPSTREAM_TEAL = "#80CBC4"


@dataclass(frozen=True)
class Variant:
    id: str
    name: str
    semantic_class: str
    theme_type: str  # "dark" or "light"
    ui_theme: str  # "vs-dark" or "vs"
    claude_base: str

    # Workbench surfaces
    bg: str
    bg_deep: str
    bg_raised: str
    fg: str
    fg_dim: str
    border: str
    border_soft: str

    # Accent and semantic colors
    amber: str
    amber_bright: str
    red: str
    green: str
    blue: str
    accent: str  # cyan debug/info
    syntax_purple: str
    syntax_orange: str

    # Variant-specific workbench tuning
    indent_guide: str
    indent_guide_active: str
    line_highlight: str
    selection_background: str
    terminal_selection: str
    terminal_inactive_selection: str
    inactive_selection: str
    widget_border: str
    find_match_highlight_border: str
    extension_pre_release: str
    button_separator: str
    sticky_scroll_hover: str
    badge_on_amber_fg: str
    text_link_active: str
    button_hover: str
    muted_structural: str
    disabled_fg: str
    chat_input_border_3: str

    # Output paths (relative to ROOT)
    ghostty_path: str
    vscode_path: str
    codex_path: str
    claude_path: str
    opencode_path: str
    windows_terminal_path: str
    powershell_path: str
    starship_path: str
    grok_json_path: str
    grok_pager_path: str
    starship_palette: str
    powershell_class: str
    codex_uuid_seed: str
    grok_pager_block_bg: str  # "dark" or "light"
    # Prompt text on the Ghostty surface. Distinct from cursor-color, which can
    # stay the bright fill gold even when that gold is too light as glyphs.
    prompt_amber: str
    prompt_amber_bright: str
    prompt_dim: str

    # Ghostty terminal palette (source for build_ghostty.py)
    ghostty_background: str
    ghostty_foreground: str
    ghostty_cursor: str
    ghostty_selection_bg: str
    ghostty_selection_fg: str
    ghostty_ansi: tuple[str, ...]

    upstream_remap_extra: dict[str, str] = field(default_factory=dict)
    syntax_remap: dict[str, str] = field(default_factory=dict)
    # Applied last so Palenight leftovers cannot win on light surfaces.
    workbench_overrides: dict[str, str] = field(default_factory=dict)


DARK = Variant(
    id="dark",
    name="Amber Material High Contrast",
    semantic_class="amber-material-high-contrast",
    theme_type="dark",
    ui_theme="vs-dark",
    claude_base="dark-ansi",
    bg="#22252F",
    bg_deep="#1C1F27",
    bg_raised="#2A2E3A",
    fg="#D2D7E4",
    fg_dim="#8A91A6",
    border="#333846",
    border_soft="#3A4052",
    amber="#FFCB6B",
    amber_bright="#FFCB6B",
    red="#ff5572",
    green="#a9c77d",
    blue="#82AAFF",
    accent="#89DDFF",
    syntax_purple="#C792EA",
    syntax_orange="#F78C6C",
    indent_guide="#2F3543",
    indent_guide_active="#4A5265",
    line_highlight="#2A2E3A80",
    selection_background="#7580B860",
    terminal_selection="#3A4055",
    terminal_inactive_selection="#3A405580",
    inactive_selection="#3A4055",
    widget_border="#ffffff0f",
    find_match_highlight_border="#ffffff80",
    extension_pre_release="#ffffff1a",
    button_separator="#00000033",
    sticky_scroll_hover="#555C824d",
    badge_on_amber_fg="#1C1F27",
    text_link_active="#FFD98A",
    button_hover="#FFD98A",
    muted_structural="#4E5579",
    disabled_fg="#676E95ff",
    chat_input_border_3="#FFD98A",
    ghostty_path="ghostty/amber-material",
    vscode_path="themes/amber-material-hc.json",
    codex_path="codex/amber-material-high-contrast.tmTheme",
    claude_path="claude-code/amber-material-high-contrast.json",
    opencode_path="opencode/amber-material-high-contrast.json",
    windows_terminal_path="windows-terminal/amber-material-high-contrast.json",
    powershell_path="powershell/AmberMaterial.ps1",
    starship_path="starship/amber-material.toml",
    grok_json_path="grok/amber-material-high-contrast.json",
    grok_pager_path="grok/pager.toml",
    starship_palette="amber_material",
    powershell_class="AmberMaterial",
    codex_uuid_seed="https://github.com/gkaria/amber-material-theme#codex",
    grok_pager_block_bg="dark",
    prompt_amber="#FFCB6B",
    prompt_amber_bright="#FFE08A",
    prompt_dim="#B8B3A8",
    ghostty_background="#1D2021",
    ghostty_foreground="#E7E1D1",
    ghostty_cursor="#FFCB6B",
    ghostty_selection_bg="#4A3F28",
    ghostty_selection_fg="#FFF4D6",
    ghostty_ansi=(
        "#1D2021", "#FF6B6B", "#B8D96D", "#FFCB6B", "#70B7FF", "#D9A0FF",
        "#66D9D0", "#E7E1D1", "#888B84", "#FF8787", "#D0EA8A", "#FFE08A",
        "#94CAFF", "#E8BDFF", "#8BE9E1", "#FFFFFF",
    ),
)

LIGHT = Variant(
    id="light",
    name="Amber Material Light High Contrast",
    semantic_class="amber-material-light-high-contrast",
    theme_type="light",
    ui_theme="vs",
    claude_base="light-ansi",
    bg="#FAF6EE",
    bg_deep="#F0EBE0",
    bg_raised="#FFFFFF",
    fg="#1E2228",
    fg_dim="#5A6070",
    border="#D8D2C6",
    border_soft="#E8E2D8",
    amber="#A65F00",
    amber_bright="#FFCB6B",
    red="#C62828",
    green="#4A7C1B",
    blue="#2E5DB8",
    accent="#0E7490",
    syntax_purple="#7B3F9E",
    syntax_orange="#C45A2E",
    indent_guide="#E0DBD0",
    indent_guide_active="#C8C2B6",
    line_highlight="#F0EBE080",
    selection_background="#FFCB6B40",
    terminal_selection="#E8D5A8",
    terminal_inactive_selection="#E8D5A880",
    inactive_selection="#E8E2D8",
    widget_border="#0000000f",
    find_match_highlight_border="#00000040",
    extension_pre_release="#0000001a",
    button_separator="#00000020",
    sticky_scroll_hover="#E0DBD04d",
    badge_on_amber_fg="#1E2228",
    text_link_active="#A65F00",
    button_hover="#FFD98A",
    muted_structural="#9CA3B0",
    disabled_fg="#9CA3B0ff",
    chat_input_border_3="#FFD98A",
    ghostty_path="ghostty/amber-material-light",
    vscode_path="themes/amber-material-light-hc.json",
    codex_path="codex/amber-material-light-high-contrast.tmTheme",
    claude_path="claude-code/amber-material-light-high-contrast.json",
    opencode_path="opencode/amber-material-light-high-contrast.json",
    windows_terminal_path="windows-terminal/amber-material-light-high-contrast.json",
    powershell_path="powershell/AmberMaterialLight.ps1",
    starship_path="starship/amber-material.toml",
    grok_json_path="grok/amber-material-light-high-contrast.json",
    grok_pager_path="grok/pager-light.toml",
    starship_palette="amber_material_light",
    powershell_class="AmberMaterialLight",
    codex_uuid_seed="https://github.com/gkaria/amber-material-theme#codex-light",
    grok_pager_block_bg="light",
    prompt_amber="#C99200",
    prompt_amber_bright="#D4A017",
    prompt_dim="#5A6070",
    ghostty_background="#FBF7EE",
    ghostty_foreground="#2B2926",
    ghostty_cursor="#C99200",
    ghostty_selection_bg="#E8D5A8",
    ghostty_selection_fg="#1E2228",
    ghostty_ansi=(
        "#FBF7EE", "#C62828", "#4A7C1B", "#FFCB6B", "#2E5DB8", "#7B3F9E",
        "#0E7490", "#2B2926", "#8A8580", "#D32F2F", "#5A9A24", "#FFE08A",
        "#3D6BB8", "#9B59C7", "#0E9AAF", "#1E2228",
    ),
    syntax_remap={
        "#697098": "#6B7289",
        "#BFC7D5": "#1E2228",
        "#C3E88D": "#4A7C1B",
        "#C792EA": "#7B3F9E",
        "#82AAFF": "#2E5DB8",
        "#FFCB6B": "#A67C00",
        "#F78C6C": "#C45A2E",
        "#89DDFF": "#0E7490",
        "#A9C77D": "#4A7C1B",
        "#FF5572": "#C62828",
        "#80CBC4": "#0E7490",
        "#FFFFFF": "#1E2228",
        "#EEFFFF": "#1E2228",
        "#7986E7": "#5B4FCF",
        "#CDEBF7": "#2E7A8F",
        "#D9F5DD": "#3D7A2E",
        "#FF5874": "#C62828",
        "#EF5350": "#C62828",
        "#FFCA28": "#A67C00",
        "#E2C08D": "#2E5DB8",
        "#E2B93D": "#2E5DB8",
        "#9CCC65": "#4A7C1B",
        "#99B76D": "#4A7C1B",
        "#64B5F6": "#2E5DB8",
        "#7E57C2": "#C68400",
        "#694CA4": "#C68400",
        "#262A39": "#D8D2C6",
        "#232635": "#F0EBE0",
        "#292D3E": "#FAF6EE",
        "#383D51": "#E8E2D8",
        "#32374D": "#E8E2D8",
        "#2E3250": "#E0DBD0",
    },
    workbench_overrides={
        # Palenight paints explorer hover/focus in white for dark chrome.
        # On cream that makes file names vanish; keep ink on an amber wash.
        "list.foreground": "#1E2228",
        "list.hoverForeground": "#1E2228",
        "list.focusForeground": "#1E2228",
        "list.hoverBackground": "#FFCB6B4D",
        "list.focusBackground": "#FFCB6B66",
        "list.inactiveSelectionBackground": "#FFCB6B66",
        "list.inactiveSelectionForeground": "#1E2228",
        "list.inactiveSelectionIconForeground": "#1E2228",
        "list.inactiveFocusBackground": "#FFCB6B4D",
        "list.filterMatchBackground": "#FFCB6B80",
        "editorSuggestWidget.highlightForeground": "#A65F00",
        "peekViewResult.fileForeground": "#1E2228",
        "peekViewResult.lineForeground": "#1E2228",
        "peekViewResult.selectionForeground": "#1E2228",
        "peekViewTitleDescription.foreground": "#5A6070",
        "peekViewTitleLabel.foreground": "#1E2228",
        "notifications.foreground": "#1E2228",
        "editorActiveLineNumber.foreground": "#A65F00",
        "breadcrumb.activeSelectionForeground": "#A65F00",
        # Git status tints were still Palenight-on-dark (pale green, 56% gray).
        "gitDecoration.untrackedResourceForeground": "#3D6A16",
        "gitDecoration.ignoredResourceForeground": "#5A6070",
        "gitDecoration.deletedResourceForeground": "#C62828",
        "gitDecoration.modifiedResourceForeground": "#2E5DB8",
        "gitDecoration.addedResourceForeground": "#3D6A16",
        "gitDecoration.conflictingResourceForeground": "#A65F00",
    },
)

VARIANTS = (DARK, LIGHT)


def upstream_remap(variant: Variant) -> dict[str, str]:
    """Return the upstream workbench color sweep table for a variant."""
    return {
        UPSTREAM_PURPLE: variant.amber,
        UPSTREAM_PURPLE_DEEP: variant.amber,
        UPSTREAM_TEAL: variant.amber,
        "#BFC7D5": variant.fg,
        "#262A39": variant.border,
        "#232635": variant.bg_deep,
        "#EF5350": variant.red,
        "#FFCA28": variant.amber,
        "#E2C08D": variant.blue,
        "#E2B93D": variant.blue,
        "#9CCC65": variant.green,
        "#99B76D": variant.green,
        "#64B5F6": variant.blue,
        **variant.upstream_remap_extra,
    }


def resolve_path(variant: Variant, relative: str) -> Path:
    return ROOT / relative
