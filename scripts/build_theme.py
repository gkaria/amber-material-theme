#!/usr/bin/env python3
"""Derive a high-contrast Palenight variant from the MIT-licensed base theme.

Deepens the chrome/editor backgrounds and lifts foreground contrast, leaving the
upstream syntax palette intact.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SRC = os.path.join(HERE, "base-palenight-italic.json")
DST = os.path.join(ROOT, "themes", "palenight-amber-hc.json")

# Darker, cooler base than stock Palenight (#292D3E) for a higher-contrast feel.
BG        = "#22252F"  # editor / sidebar surface
BG_DEEP   = "#1C1F27"  # activity bar, status bar, tab bar troughs
BG_RAISED = "#2A2E3A"  # hovers, active tabs, widgets
FG        = "#D2D7E4"  # lifted from #BFC7D5
FG_DIM    = "#8A91A6"
BORDER    = "#333846"
BORDER_SOFT = "#3A4052"  # container/box outlines — deliberately recessive
ACCENT    = "#89DDFF"

# AMBER is the workbench accent. Change this one value to re-accent the whole
# theme: cursors, scrollbars, badges, focus rings, selections, links.
AMBER     = "#FFCB6B"
TEAL      = "#80CBC4"  # retained for syntax lineage; no longer a UI accent
RED       = "#ff5572"  # errors, deletions
GREEN     = "#a9c77d"  # additions
BLUE      = "#82AAFF"  # info, modifications

theme = json.load(open(SRC))
colors = theme["colors"]

# Surfaces -----------------------------------------------------------------
for key in (
    "editor.background", "sideBar.background", "sideBarSectionHeader.background",
    "panel.background", "terminal.background", "breadcrumb.background",
    "editorGutter.background", "notebook.editorBackground", "minimap.background",
    "editorPane.background", "banner.background",
):
    colors[key] = BG

for key in (
    "activityBar.background", "statusBar.background", "editorGroupHeader.tabsBackground",
    "tab.inactiveBackground", "titleBar.activeBackground", "titleBar.inactiveBackground",
    "editorGroupHeader.noTabsBackground", "statusBar.noFolderBackground",
    "activityBar.activeBackground", "terminal.tab.activeBorder",
):
    colors[key] = BG_DEEP

for key in (
    "tab.activeBackground", "list.hoverBackground", "menu.background",
    "editorWidget.background", "editorSuggestWidget.background", "quickInput.background",
    "peekViewEditor.background", "dropdown.background", "input.background",
    "editorHoverWidget.background", "notifications.background", "commandCenter.background",
):
    colors[key] = BG_RAISED

# Foregrounds --------------------------------------------------------------
for key in (
    "editor.foreground", "foreground", "sideBar.foreground", "tab.activeForeground",
    "activityBar.foreground", "statusBar.foreground", "list.activeSelectionForeground",
    "menu.foreground", "dropdown.foreground", "input.foreground", "terminal.foreground",
):
    colors[key] = FG

for key in ("tab.inactiveForeground", "activityBar.inactiveForeground",
            "breadcrumb.foreground", "editorLineNumber.foreground", "descriptionForeground"):
    colors[key] = FG_DIM

# Contrast accents ---------------------------------------------------------
colors["editorLineNumber.activeForeground"] = ACCENT
colors["editorCursor.foreground"] = AMBER
colors["editorCursor.background"] = BG
colors["terminalCursor.foreground"] = AMBER
colors["terminalCursor.background"] = BG

# Amber carries warnings and match highlights, matching the cursor accent.
colors["editorWarning.foreground"] = AMBER + "b3"
colors["editorOverviewRuler.warningForeground"] = AMBER + "99"
colors["notificationsWarningIcon.foreground"] = AMBER
colors["debugConsole.warningForeground"] = AMBER
colors["activityWarningBadge.background"] = AMBER
colors["inputValidation.warningBorder"] = AMBER
colors["editorBracketMatch.border"] = AMBER + "80"
colors["editor.findRangeHighlightBackground"] = AMBER + "4d"
colors["editor.selectionHighlightBackground"] = AMBER + "33"
colors["gitDecoration.conflictingResourceForeground"] = AMBER + "e6"
colors["focusBorder"] = "#3F4657"
colors["contrastBorder"] = BORDER
colors["editorIndentGuide.background1"] = "#2F3543"
colors["editorIndentGuide.activeBackground1"] = "#4A5265"
colors["editor.lineHighlightBackground"] = "#2A2E3A80"
colors["editor.selectionBackground"] = "#7580B860"
colors["tab.activeBorderTop"] = ACCENT
colors["statusBarItem.remoteBackground"] = BG_DEEP

for key in ("sideBar.border", "panel.border", "activityBar.border",
            "statusBar.border", "titleBar.border", "editorGroup.border", "tab.border"):
    colors[key] = BORDER

# Modern UI surfaces -------------------------------------------------------
# The upstream base predates these areas (chat, command center, settings editor,
# sticky scroll, activity bar top), so they would otherwise fall back to VS Code
# defaults and read as untinted against the rest of the theme.

# TEAL is the workbench interaction accent: selections, links, focus, progress.
for key in (
    "activityBar.activeBorder", "activityBarTop.activeBorder", "chat.avatarForeground",
    "chat.slashCommandForeground", "list.activeSelectionIconForeground",
    "list.inactiveSelectionIconForeground", "menu.selectionForeground",
    "menubar.selectionForeground", "notebook.focusedCellBorder", "progressBar.background",
    "settings.modifiedItemIndicator", "statusBar.debuggingForeground",
    "statusBarItem.remoteForeground", "textLink.foreground", "editorWidget.border",
    "editorWidget.resizeBorder", "editor.findMatchBorder", "extensionButton.foreground",
    "editorOverviewRuler.findMatchForeground", "extensionIcon.verifiedForeground",
    "statusBarItem.remoteHoverBackground",
):
    colors[key] = AMBER

colors["notebook.inactiveFocusedCellBorder"] = AMBER + "80"
colors["sash.hoverBorder"] = AMBER + "80"
colors["toolbar.activeBackground"] = AMBER + "26"
colors["extensionButton.background"] = AMBER + "14"
colors["extensionButton.border"] = AMBER + "14"
colors["extensionButton.hoverBackground"] = AMBER + "33"
colors["extensionButton.separator"] = AMBER + "33"
colors["tab.activeModifiedBorder"] = AMBER + "00"
colors["statusBarItem.remoteHoverForeground"] = BG_DEEP

# Foregrounds on the newer surfaces.
for key in (
    "activityBarTop.foreground", "button.secondaryForeground", "settings.headerForeground",
    "settings.checkboxForeground", "settings.dropdownForeground",
    "settings.numberInputForeground", "settings.textInputForeground",
    "editor.selectionForeground", "editor.findMatchHighlightForeground",
    "editorLink.activeForeground", "textLink.activeForeground",
    "quickInputList.focusIconForeground", "tab.unfocusedActiveForeground",
    "extensionBadge.remoteForeground", "menu.separatorBackground",
    "commandCenter.activeForeground",
):
    colors[key] = FG

for key in ("quickInput.foreground", "titleBar.inactiveForeground",
            "activityBarTop.inactiveForeground"):
    colors[key] = FG_DIM

# Input/control surfaces sit on the deep tone.
for key in (
    "settings.checkboxBackground", "settings.dropdownBackground",
    "settings.numberInputBackground", "settings.textInputBackground",
    "button.secondaryBackground", "activityBarTop.background",
):
    colors[key] = BG_DEEP

colors["quickInputTitle.background"] = BG
colors["editorBracketMatch.background"] = BG
colors["editorOverviewRuler.border"] = BG
colors["peekViewEditorGutter.background"] = BG_RAISED
colors["chat.requestBubbleBackground"] = BG_RAISED
colors["chat.requestBubbleHoverBackground"] = BG_RAISED
colors["textPreformat.background"] = BORDER + "ff"
colors["textPreformat.foreground"] = FG + "b3"
colors["menu.selectionBackground"] = BORDER + "ff"

# Borders, separators, subtle overlays.
for key in ("menu.border", "commandCenter.border", "keybindingLabel.border",
            "keybindingLabel.bottomBorder"):
    colors[key] = BORDER

for key in ("agentsPanel.border", "sideBarActivityBarTop.border",
            "sideBarSectionHeader.border", "sideBarStickyScroll.border"):
    colors[key] = BORDER + "99"

for key in ("chat.requestBorder", "notificationToast.border", "widget.border"):
    colors[key] = "#ffffff0f"

for key in ("menu.selectionBorder", "menubar.selectionBorder", "menubar.selectionBackground",
            "list.dropBetweenBackground", "listFilterWidget.background",
            "listFilterWidget.outline", "listFilterWidget.noMatchesOutline",
            "panelSection.dropBackground", "toolbar.hoverBackground"):
    colors[key] = FG + "1a"

colors["quickInputList.focusBackground"] = FG + "26"
colors["inputOption.activeBackground"] = FG + "4d"
colors["commandCenter.foreground"] = FG + "99"
colors["chat.requestCodeBorder"] = "#474D6C"
colors["chat.checkpointSeparator"] = FG_DIM
colors["editorStickyScrollHover.background"] = "#555C824d"
colors["editor.findMatchHighlightBorder"] = "#ffffff80"
colors["editor.lineHighlightBorder"] = BORDER + "ff"
colors["extensionIcon.preReleaseForeground"] = "#ffffff1a"
colors["button.separator"] = "#00000033"

# Muted structural strokes.
for key in ("editorIndentGuide.activeBackground", "tree.indentGuidesStroke",
            "editorWhitespace.foreground", "terminalCommandGuide.foreground"):
    colors[key] = "#4E5579"

colors["disabledForeground"] = "#676E95ff"
colors["icon.foreground"] = FG
colors["inlineChatInput.border"] = BORDER

# Amber accent: scrollbars, badges/counts, and remaining accent slots --------
# Upstream Palenight uses purple here; amber is the accent for this variant.
colors["scrollbarSlider.background"] = AMBER + "40"
colors["scrollbarSlider.hoverBackground"] = AMBER + "80"
colors["scrollbarSlider.activeBackground"] = AMBER + "b3"
colors["minimapSlider.background"] = AMBER + "26"
colors["minimapSlider.hoverBackground"] = AMBER + "40"
colors["minimapSlider.activeBackground"] = AMBER + "66"

# Counts: SCM change count, activity bar badges, notification/extension counts.
for key in ("badge.background", "activityBarBadge.background",
            "notificationsInfoIcon.foreground", "extensionBadge.remoteBackground"):
    colors[key] = AMBER
for key in ("badge.foreground", "activityBarBadge.foreground",
            "extensionBadge.remoteForeground"):
    colors[key] = BG_DEEP

# Remaining interaction accents that were teal.
for key in ("focusBorder", "list.focusOutline", "editorLineNumber.activeForeground",
            "tab.activeBorderTop", "panelTitle.activeBorder", "activityBar.activeBorder",
            "list.highlightForeground", "list.focusHighlightForeground",
            "pickerGroup.foreground", "textLink.foreground", "button.background",
            "progressBar.background", "editorWidget.border", "editorWidget.resizeBorder",
            "selection.background", "inputOption.activeBorder",
            "statusBarItem.remoteBackground"):
    colors[key] = AMBER
colors["button.foreground"] = BG_DEEP
colors["button.hoverBackground"] = "#FFD98A"
colors["statusBarItem.remoteForeground"] = BG_DEEP
colors["statusBarItem.remoteHoverBackground"] = "#FFD98A"
colors["selection.background"] = AMBER + "40"
colors["inputOption.activeBackground"] = AMBER + "33"
colors["inputOption.activeForeground"] = AMBER

# Sweep any remaining upstream purple/teal onto the amber accent, preserving
# each slot's original alpha so opacity relationships stay intact.
for key, value in list(colors.items()):
    if not isinstance(value, str) or not value.startswith("#"):
        continue
    base, alpha = value[:7].upper(), value[7:]
    if base in ("#7E57C2", "#694CA4", "#80CBC4"):
        colors[key] = AMBER + alpha

# Solid amber fills need a dark foreground to stay legible.
colors["list.activeSelectionForeground"] = BG_DEEP
colors["list.activeSelectionIconForeground"] = BG_DEEP
colors["editorSuggestWidget.selectedForeground"] = BG_DEEP
colors["editorSuggestWidget.selectedIconForeground"] = BG_DEEP
colors["extensionButton.prominentForeground"] = BG_DEEP
colors["quickInputList.focusForeground"] = FG

# Selections/highlights read better as translucent washes than solid amber.
colors["list.activeSelectionBackground"] = AMBER
colors["editorSuggestWidget.selectedBackground"] = AMBER
colors["editor.findMatchHighlightBackground"] = AMBER + "40"
colors["editor.hoverHighlightBackground"] = AMBER + "33"
colors["editor.inactiveSelectionBackground"] = "#3A4055"
colors["editor.rangeHighlightBackground"] = AMBER + "20"
colors["terminal.findMatchBackground"] = AMBER + "80"
colors["terminal.findMatchHighlightBackground"] = AMBER + "40"

# Structural borders recede; only active/focus state stays amber.
# Containers (widgets, popups, inputs, peek view) get a muted slate so every
# box on screen isn't outlined in yellow.
for key in (
    "editorWidget.border", "editorHoverWidget.border", "debugExceptionWidget.border",
    "peekView.border", "dropdown.border", "input.border", "editorWidget.resizeBorder",
    "editorSuggestWidget.border", "notificationCenter.border", "notifications.border",
    "notificationToast.border", "menu.border", "quickInput.border",
    "editorGroup.dropIntoPromptBorder", "debugToolBar.border",
):
    colors[key] = BORDER_SOFT

colors["profileBadge.background"] = AMBER
colors["profileBadge.foreground"] = BG_DEEP
colors["terminal.selectionBackground"] = "#3A4055"
# Upstream sets ansiBlack to the same grey as brightBlack, which makes black
# text nearly invisible; give it a true dark tone.
colors["terminal.ansiBlack"] = "#1C1F27"
colors["terminal.inactiveSelectionBackground"] = "#3A405580"

# Focus/active affordances keep the accent.
for key in ("focusBorder", "list.focusOutline", "inputOption.activeBorder",
            "tab.activeBorderTop", "panelTitle.activeBorder", "activityBar.activeBorder",
            "activityBarTop.activeBorder", "notebook.focusedCellBorder",
            "editor.findMatchBorder"):
    colors[key] = AMBER

# Semantic status colors reuse the existing syntax palette.
for key in ("activityErrorBadge.background", "debugConsole.errorForeground"):
    colors[key] = RED
colors["editorOverviewRuler.errorForeground"] = RED + "99"
colors["editorGutter.deletedSecondaryBackground"] = RED + "99"
colors["diffEditor.removedLineBackground"] = RED + "14"

colors["debugConsole.infoForeground"] = ACCENT
colors["editorInfo.foreground"] = BLUE + "b3"
colors["editorOverviewRuler.infoForeground"] = BLUE + "99"
colors["editorGutter.modifiedSecondaryBackground"] = BLUE + "99"
colors["editorGutter.addedSecondaryBackground"] = GREEN + "99"
colors["diffEditor.insertedLineBackground"] = GREEN + "14"

for key in ("activityErrorBadge.foreground", "activityWarningBadge.foreground"):
    colors[key] = "#000000"

# Deliberately transparent (upstream leaves these off).
colors["contrastActiveBorder"] = BG_DEEP + "00"
colors["merge.border"] = BG + "00"
colors["chat.slashCommandBackground"] = "#ffffff00"
colors["commandCenter.activeBorder"] = BORDER + "00"
colors["tab.unfocusedActiveBorderTop"] = "#676E9500"

# Identity -----------------------------------------------------------------
theme["name"] = "Palenight Amber High Contrast"
theme.pop("maintainers", None)
theme["author"] = "Gaurang Karia"
theme["semanticHighlighting"] = True

json.dump(theme, open(DST, "w"), indent=2)
print(f"wrote {DST}: {len(colors)} colors, {len(theme['tokenColors'])} token rules")
