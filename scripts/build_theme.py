#!/usr/bin/env python3
"""Derive a high-contrast Palenight variant from the MIT-licensed base theme.

Deepens the chrome/editor backgrounds and lifts foreground contrast, leaving the
upstream syntax palette intact.
"""
import json
import os

import ghostty_palette

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SRC = os.path.join(HERE, "base-palenight-italic.json")
DST = os.path.join(ROOT, "themes", "amber-material-hc.json")

# Darker, cooler base than stock Palenight (#292D3E) for a higher-contrast feel.
BG        = "#22252F"  # editor / sidebar surface
BG_DEEP   = "#1C1F27"  # activity bar, status bar, tab bar troughs
BG_RAISED = "#2A2E3A"  # hovers, active tabs, widgets
FG        = "#D2D7E4"  # lifted from #BFC7D5
FG_DIM    = "#8A91A6"
BORDER    = "#333846"
BORDER_SOFT = "#3A4052"  # container/box outlines — deliberately recessive
ACCENT    = "#89DDFF"  # debug console info; the syntax palette's cyan

# AMBER is the workbench accent. Change this one value to re-accent the whole
# theme: cursors, scrollbars, badges, focus rings, selections, links.
AMBER     = "#FFCB6B"
RED       = "#ff5572"  # errors, deletions
GREEN     = "#a9c77d"  # additions
BLUE      = "#82AAFF"  # info, modifications

# Hues already carried by the syntax palette, named here so the workbench keys
# that mirror syntax roles (bracket pairs, symbol icons, debug values) reuse
# them instead of introducing new colors.
SYNTAX_PURPLE = "#C792EA"  # keywords
SYNTAX_ORANGE = "#F78C6C"  # numbers, constants

# Upstream accents this variant replaces wholesale. Kept as named constants so
# the sweep below reads as intent rather than magic hex.
UPSTREAM_PURPLE      = "#7E57C2"
UPSTREAM_PURPLE_DEEP = "#694CA4"
UPSTREAM_TEAL        = "#80CBC4"

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
    "activityBar.foreground", "statusBar.foreground",
    "menu.foreground", "dropdown.foreground", "input.foreground", "terminal.foreground",
):
    colors[key] = FG

for key in ("tab.inactiveForeground", "activityBar.inactiveForeground",
            "breadcrumb.foreground", "editorLineNumber.foreground", "descriptionForeground"):
    colors[key] = FG_DIM

# Contrast accents ---------------------------------------------------------
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
colors["contrastBorder"] = BORDER
colors["editorIndentGuide.background1"] = "#2F3543"
colors["editorIndentGuide.activeBackground1"] = "#4A5265"
colors["editor.lineHighlightBackground"] = "#2A2E3A80"
colors["editor.selectionBackground"] = "#7580B860"

for key in ("sideBar.border", "panel.border", "activityBar.border",
            "statusBar.border", "titleBar.border", "editorGroup.border", "tab.border"):
    colors[key] = BORDER

# Modern UI surfaces -------------------------------------------------------
# The upstream base predates these areas (chat, command center, settings editor,
# sticky scroll, activity bar top), so they would otherwise fall back to VS Code
# defaults and read as untinted against the rest of the theme.

# Amber carries interaction on these surfaces too: chat, menus, notebooks,
# progress, links. Keys whose final value is set further down (the solid-amber
# fills, the recessive container borders, the remote status item) are handled
# there instead of here.
for key in (
    "chat.avatarForeground", "chat.slashCommandForeground",
    "list.inactiveSelectionIconForeground", "menu.selectionForeground",
    "menubar.selectionForeground", "settings.modifiedItemIndicator",
    "statusBar.debuggingForeground", "extensionButton.foreground",
    "editorOverviewRuler.findMatchForeground", "extensionIcon.verifiedForeground",
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

# Foregrounds on the newer surfaces. panelTitle / sideBarTitle are the
# labels Cursor's auxiliary bar (chat, composer) actually draws; the
# Palenight base left them on a cyan-white that does not belong here.
for key in (
    "activityBarTop.foreground", "button.secondaryForeground", "settings.headerForeground",
    "settings.checkboxForeground", "settings.dropdownForeground",
    "settings.numberInputForeground", "settings.textInputForeground",
    "editor.selectionForeground", "editor.findMatchHighlightForeground",
    "editorLink.activeForeground",
    "quickInputList.focusIconForeground", "tab.unfocusedActiveForeground",
    "menu.separatorBackground", "commandCenter.activeForeground",
    "panelTitle.activeForeground", "sideBarTitle.foreground",
    "sideBarSectionHeader.foreground", "titleBar.activeForeground",
    "panelSectionHeader.foreground",
):
    colors[key] = FG

for key in ("quickInput.foreground", "titleBar.inactiveForeground",
            "activityBarTop.inactiveForeground", "panelTitle.inactiveForeground",
            "input.placeholderForeground"):
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
for key in ("commandCenter.border", "keybindingLabel.border",
            "keybindingLabel.bottomBorder"):
    colors[key] = BORDER

for key in ("agentsPanel.border", "sideBarActivityBarTop.border",
            "sideBarSectionHeader.border", "sideBarStickyScroll.border"):
    colors[key] = BORDER + "99"

colors["widget.border"] = "#ffffff0f"

for key in ("menu.selectionBorder", "menubar.selectionBorder", "menubar.selectionBackground",
            "list.dropBetweenBackground", "listFilterWidget.background",
            "listFilterWidget.outline", "listFilterWidget.noMatchesOutline",
            "panelSection.dropBackground", "toolbar.hoverBackground"):
    colors[key] = FG + "1a"

colors["quickInputList.focusBackground"] = FG + "26"
colors["commandCenter.foreground"] = FG + "99"
colors["chat.requestCodeBorder"] = BORDER_SOFT
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

colors["button.foreground"] = BG_DEEP
colors["button.hoverBackground"] = "#FFD98A"
colors["statusBarItem.remoteForeground"] = BG_DEEP
colors["statusBarItem.remoteHoverBackground"] = "#FFD98A"
colors["selection.background"] = AMBER + "40"
colors["inputOption.activeBackground"] = AMBER + "33"
colors["inputOption.activeForeground"] = AMBER

# Sweep leftover upstream values onto this variant's palette ----------------
# The base theme sets ~200 keys; the blocks above only name the ones this
# variant restyles, so anything untouched keeps a Palenight tone. Left alone
# that means competing values for roles this theme has already defined: two
# reds, three warm tones, and the pre-lift foreground. Each mapping below
# sends a value to the constant this theme already uses for the same role.
#
# Alpha is preserved, so every translucent slot keeps its opacity relationship.
UPSTREAM_REMAP = {
    # Accents this variant replaces wholesale.
    UPSTREAM_PURPLE: AMBER,
    UPSTREAM_PURPLE_DEEP: AMBER,
    UPSTREAM_TEAL: AMBER,
    # The foreground this variant lifted to FG.
    "#BFC7D5": FG,
    # Borders on the old chrome tone.
    "#262A39": BORDER,
    # Shadow/embedded surfaces below the editor tone.
    "#232635": BG_DEEP,
    # Second red. RED already carries errors and deletions everywhere else.
    "#EF5350": RED,
    # Second and third warm tones. AMBER already carries warnings.
    "#FFCA28": AMBER,
    # Git/gutter status. The theme assigns BLUE to modifications and GREEN to
    # additions, but the primary gutter and SCM slots kept upstream's hues —
    # so each gutter drew its primary and secondary marks in different colors.
    "#E2C08D": BLUE,
    "#E2B93D": BLUE,
    "#9CCC65": GREEN,
    "#99B76D": GREEN,
    # Info validation, to match BLUE's declared role.
    "#64B5F6": BLUE,
}
for key, value in list(colors.items()):
    if not isinstance(value, str) or not value.startswith("#"):
        continue
    base, alpha = value[:7].upper(), value[7:]
    if base in UPSTREAM_REMAP:
        colors[key] = UPSTREAM_REMAP[base] + alpha

# Surfaces whose old value covered several roles, so they can't go through the
# table above: each lands on the tone this theme uses for that kind of surface.
colors["debugExceptionWidget.background"] = BG_RAISED
colors["debugToolBar.background"] = BG_RAISED
colors["breadcrumbPicker.background"] = BG_RAISED
colors["editorMarkerNavigation.background"] = BG_RAISED
colors["peekViewResult.background"] = BG_RAISED
colors["list.dropBackground"] = BG_RAISED
colors["peekViewTitle.background"] = BG_DEEP
colors["editorGroup.background"] = BG
colors["scrollbar.shadow"] = BG + "00"
colors["pickerGroup.border"] = BORDER
colors["statusBar.debuggingBorder"] = BORDER
colors["statusBar.noFolderBorder"] = BORDER

# Status bar item states: raised on hover, one step further on press.
colors["statusBar.debuggingBackground"] = BG_RAISED
colors["statusBarItem.hoverBackground"] = BG_RAISED
colors["statusBarItem.prominentBackground"] = BG_RAISED
colors["statusBarItem.activeBackground"] = BORDER
colors["statusBarItem.prominentHoverBackground"] = BORDER

# Word highlights stay neutral so they don't compete with the amber selection.
colors["editor.wordHighlightBackground"] = BORDER
colors["editor.wordHighlightStrongBackground"] = BORDER_SOFT
colors["peekViewResult.selectionBackground"] = BORDER

# The active find match was the one find slot still on an upstream blue-grey,
# even though its border and every other match are already amber.
colors["editor.findMatchBackground"] = AMBER + "66"

# Solid amber fills need a dark foreground to stay legible.
colors["list.activeSelectionForeground"] = BG_DEEP
colors["list.activeSelectionIconForeground"] = BG_DEEP
colors["editorSuggestWidget.selectedForeground"] = BG_DEEP
colors["editorSuggestWidget.selectedIconForeground"] = BG_DEEP
colors["extensionButton.prominentForeground"] = BG_DEEP
colors["quickInputList.focusForeground"] = FG

# The selected row in a list or the suggest widget is a solid amber bar, paired
# with the dark foregrounds set just above. Everything else — find matches,
# hovers, ranges — is a translucent wash so the accent stays a signal.
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
colors["terminal.inactiveSelectionBackground"] = "#3A405580"

# Integrated terminal ANSI colors come from the Ghostty theme, so the same
# command renders the same way inside and outside the editor. Upstream's
# palette disagreed with it in 14 of 16 slots and gave five bright colors the
# same value as their normal counterpart, which flattened `ls --color` output.
#
# The terminal's own surfaces (background, foreground, selection) deliberately
# stay on the cool VS Code tones set above: the panel sits beside the editor,
# so it matches its neighbour rather than the standalone terminal.
_, ghostty_ansi = ghostty_palette.load()
for index, name in enumerate(ghostty_palette.ANSI_NAMES):
    colors[f"terminal.ansi{name}"] = ghostty_ansi[index]

# Focus/active affordances and the remaining accent slots. This is the single
# place amber is applied at full strength, so every key here is assigned once.
for key in ("focusBorder", "list.focusOutline", "inputOption.activeBorder",
            "tab.activeBorderTop", "panelTitle.activeBorder", "activityBar.activeBorder",
            "activityBarTop.activeBorder", "notebook.focusedCellBorder",
            "editor.findMatchBorder", "editorLineNumber.activeForeground",
            "list.highlightForeground", "list.focusHighlightForeground",
            "pickerGroup.foreground", "textLink.foreground", "button.background",
            "progressBar.background", "statusBarItem.remoteBackground"):
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

# Areas VS Code gained after the upstream base was written ------------------
# These were unset, so they fell back to stock VS Code colors that were never
# tuned to this palette. Every value below reuses a constant or a syntax hue.

# Bracket pair colorization is on by default, so leaving it unset was the most
# visible gap. Six levels drawn from the syntax palette, cycling warm/cool so
# adjacent depths stay distinguishable.
colors["editorBracketHighlight.foreground1"] = AMBER
colors["editorBracketHighlight.foreground2"] = BLUE
colors["editorBracketHighlight.foreground3"] = SYNTAX_ORANGE
colors["editorBracketHighlight.foreground4"] = ACCENT
colors["editorBracketHighlight.foreground5"] = SYNTAX_PURPLE
colors["editorBracketHighlight.foreground6"] = GREEN
colors["editorBracketHighlight.unexpectedBracket.foreground"] = RED

# Inlay hints and inline suggestions: dim text on the raised tone.
for key in ("editorInlayHint.foreground", "editorInlayHint.typeForeground",
            "editorInlayHint.parameterForeground", "editorGhostText.foreground"):
    colors[key] = FG_DIM
for key in ("editorInlayHint.background", "editorInlayHint.typeBackground",
            "editorInlayHint.parameterBackground"):
    colors[key] = BG_RAISED

# Sticky scroll sits over the editor, so it keeps the editor tone and separates
# with a border instead of a different surface.
colors["editorStickyScroll.background"] = BG
colors["editorStickyScroll.border"] = BORDER

# The only SCM decoration left unset; the others are all assigned above.
colors["gitDecoration.addedResourceForeground"] = GREEN + "e6"

# Status bar and Problems severities reuse the semantic palette. Solid fills
# take a dark foreground, matching the badges.
colors["statusBarItem.errorBackground"] = RED
colors["statusBarItem.warningBackground"] = AMBER
for key in ("statusBarItem.errorForeground", "statusBarItem.warningForeground"):
    colors[key] = BG_DEEP
colors["problemsErrorIcon.foreground"] = RED
colors["problemsWarningIcon.foreground"] = AMBER
colors["problemsInfoIcon.foreground"] = BLUE
colors["editorHint.foreground"] = FG_DIM

# Suggest widget and outline icons, mirroring the syntax roles.
for key in ("symbolIcon.classForeground", "symbolIcon.interfaceForeground",
            "symbolIcon.structForeground", "symbolIcon.moduleForeground",
            "symbolIcon.namespaceForeground", "symbolIcon.packageForeground",
            "symbolIcon.typeParameterForeground", "symbolIcon.eventForeground"):
    colors[key] = AMBER
for key in ("symbolIcon.functionForeground", "symbolIcon.methodForeground",
            "symbolIcon.constructorForeground", "symbolIcon.operatorForeground"):
    colors[key] = BLUE
for key in ("symbolIcon.constantForeground", "symbolIcon.numberForeground",
            "symbolIcon.enumeratorForeground",
            "symbolIcon.enumeratorMemberForeground"):
    colors[key] = SYNTAX_ORANGE
for key in ("symbolIcon.keywordForeground", "symbolIcon.booleanForeground",
            "symbolIcon.nullForeground"):
    colors[key] = SYNTAX_PURPLE
for key in ("symbolIcon.stringForeground", "symbolIcon.textForeground"):
    colors[key] = GREEN
for key in ("symbolIcon.variableForeground", "symbolIcon.propertyForeground",
            "symbolIcon.fieldForeground", "symbolIcon.arrayForeground",
            "symbolIcon.objectForeground", "symbolIcon.keyForeground",
            "symbolIcon.unitForeground", "symbolIcon.valueForeground",
            "symbolIcon.fileForeground", "symbolIcon.folderForeground",
            "symbolIcon.referenceForeground", "symbolIcon.colorForeground"):
    colors[key] = FG
colors["symbolIcon.snippetForeground"] = ACCENT

# Test explorer and debug toolbar icons.
for key in ("testing.iconFailed", "testing.iconErrored", "testing.messageError.decorationForeground"):
    colors[key] = RED
for key in ("testing.iconPassed", "testing.runAction"):
    colors[key] = GREEN
colors["testing.iconQueued"] = AMBER
for key in ("testing.iconUnset", "testing.iconSkipped"):
    colors[key] = FG_DIM

for key in ("debugIcon.breakpointForeground", "debugIcon.stopForeground",
            "debugIcon.disconnectForeground"):
    colors[key] = RED
colors["debugIcon.breakpointDisabledForeground"] = RED + "80"
for key in ("debugIcon.startForeground", "debugIcon.continueForeground",
            "debugIcon.restartForeground"):
    colors[key] = GREEN
for key in ("debugIcon.pauseForeground", "debugIcon.stepOverForeground",
            "debugIcon.stepIntoForeground", "debugIcon.stepOutForeground",
            "debugIcon.stepBackForeground"):
    colors[key] = BLUE

colors["debugTokenExpression.name"] = BLUE
colors["debugTokenExpression.value"] = FG
colors["debugTokenExpression.string"] = GREEN
colors["debugTokenExpression.number"] = SYNTAX_ORANGE
colors["debugTokenExpression.boolean"] = SYNTAX_PURPLE
colors["debugTokenExpression.error"] = RED

# Timeline/SCM graph and other chart visuals.
colors["charts.foreground"] = FG
colors["charts.lines"] = BORDER
colors["charts.red"] = RED
colors["charts.green"] = GREEN
colors["charts.blue"] = BLUE
colors["charts.yellow"] = AMBER
colors["charts.orange"] = SYNTAX_ORANGE
colors["charts.purple"] = SYNTAX_PURPLE

# Remaining chrome that had no tint.
for key in ("tab.hoverBackground", "tab.unfocusedHoverBackground",
            "notebook.cellEditorBackground", "inlineChat.background"):
    colors[key] = BG_RAISED
colors["list.filterMatchBackground"] = AMBER + "33"
colors["list.filterMatchBorder"] = AMBER + "80"
colors["list.errorForeground"] = RED
colors["list.warningForeground"] = AMBER
colors["list.deemphasizedForeground"] = FG_DIM
colors["diffEditor.diagonalFill"] = BORDER
colors["notebook.cellBorderColor"] = BORDER
colors["notebook.outputContainerBackgroundColor"] = BG_DEEP
colors["search.resultsInfoForeground"] = FG_DIM
colors["editorGutter.foldingControlForeground"] = FG_DIM
for key in ("window.activeBorder", "window.inactiveBorder"):
    colors[key] = BORDER

# Deliberately transparent (upstream leaves these off).
colors["contrastActiveBorder"] = BG_DEEP + "00"
colors["merge.border"] = BG + "00"
colors["chat.slashCommandBackground"] = "#ffffff00"
colors["commandCenter.activeBorder"] = BORDER + "00"
colors["tab.unfocusedActiveBorderTop"] = "#676E9500"

# Cursor chat / composer / agents ------------------------------------------
# Cursor's in-editor chat and composer sit in the auxiliary bar and read
# ordinary VS Code workbench tokens. The panel itself is painted with
# editor.background (not sideBar.background); those two are already the
# same surface in this palette (#22252F), so the reported editor-vs-sidebar
# split is not a visual split here. What *was* off is the keys below:
# chat and inline-chat slots that still fell back to stock VS Code colors,
# Palenight leftovers on titles (handled above), and the agents* family
# that VS Code registers for the sessions/agents window.
#
# Tokens this JSON cannot set, and that we therefore do not invent:
# Cursor's --cursor-text-link (file-path / citation links in agent chat)
# and some Agents Window chrome that ignores workbench.colorTheme.

# Chat transcript: requests, avatars, diffs, find, in-flight input.
colors["chat.requestBackground"] = BG
colors["chat.avatarBackground"] = BG_DEEP
colors["chat.editedFileForeground"] = BLUE
colors["chat.linesAddedForeground"] = GREEN
colors["chat.linesRemovedForeground"] = RED
colors["chat.findMatchBackground"] = AMBER + "66"
colors["chat.findMatchHighlightBackground"] = AMBER + "40"
colors["chat.thinkingShimmer"] = FG
colors["chat.inputWorkingBorderColor1"] = AMBER
colors["chat.inputWorkingBorderColor2"] = AMBER + "80"
colors["chat.inputWorkingBorderColor3"] = "#FFD98A"
colors["chat.voiceGlowBaseColor"] = AMBER
colors["chat.requestBorder"] = BORDER + "66"
# Hovered markdown links stay amber. Cursor honors textLink.* for some
# chat markdown; file-path links that use --cursor-text-link still will not.
colors["textLink.activeForeground"] = "#FFD98A"

# Inline composer (Cmd+K / Ctrl+K) — complete the family around the
# background and input border already set above.
colors["inlineChat.foreground"] = FG
colors["inlineChat.border"] = BORDER_SOFT
colors["inlineChat.shadow"] = BG_DEEP
colors["inlineChatInput.background"] = BG_RAISED
colors["inlineChatInput.focusBorder"] = AMBER
colors["inlineChatInput.placeholderForeground"] = FG_DIM
colors["inlineChatDiff.inserted"] = GREEN + "80"
colors["inlineChatDiff.removed"] = RED + "80"

# Auxiliary bar / modern-layout cards. Unknown keys are ignored by hosts
# that predate them; Cursor and current VS Code honor the rest.
colors["surface.background"] = BG
colors["surface.foreground"] = FG
colors["panelSectionHeader.background"] = BG
colors["panelSectionHeader.border"] = BORDER + "99"
colors["panelSection.border"] = BORDER

# Conversation list: Palenight's inactive selection was a near-invisible
# cool wash (#929ac9) that made the chat history look untinted.
colors["list.inactiveSelectionBackground"] = BORDER
colors["list.inactiveSelectionForeground"] = FG

# Agent sessions window — official VS Code tokens, not Cursor-private CSS.
# Some Agents Window chrome still ignores the color theme; these cover the
# parts that do not.
colors["agents.background"] = BG_DEEP
colors["agentsPanel.background"] = BG
colors["agentsPanel.foreground"] = FG
colors["agentsCard.border"] = BORDER
colors["agentsBottomPanel.border"] = BORDER
colors["agentsGradient.tintColor"] = AMBER
colors["agentsChatInput.background"] = BG_RAISED
colors["agentsChatInput.foreground"] = FG
colors["agentsChatInput.border"] = BORDER_SOFT
colors["agentsChatInput.focusBorder"] = AMBER
colors["agentsChatInput.placeholderForeground"] = FG_DIM
colors["agentsNewSessionButton.background"] = BG_DEEP + "00"
colors["agentsNewSessionButton.foreground"] = FG
colors["agentsNewSessionButton.border"] = BORDER_SOFT
colors["agentsNewSessionButton.hoverBackground"] = BG_RAISED
for key in ("agentsBadge.background", "agentsUnreadBadge.background"):
    colors[key] = AMBER
for key in ("agentsBadge.foreground", "agentsUnreadBadge.foreground"):
    colors[key] = BG_DEEP
colors["activeSessionView.background"] = BG
colors["inactiveSessionView.background"] = BG_DEEP
colors["activeSessionView.foreground"] = FG
colors["inactiveSessionView.foreground"] = FG_DIM
colors["agentStatusIndicator.background"] = BG_DEEP
colors["agentFeedbackEditorWidget.background"] = BG_RAISED
colors["agentFeedbackEditorWidget.border"] = BORDER_SOFT
colors["agentFeedbackInputWidget.border"] = BORDER_SOFT
colors["agentsUpdateButton.downloadingBackground"] = AMBER + "66"
colors["agentsUpdateButton.downloadedBackground"] = AMBER + "b3"

# The "Global settings" token rule is the only block a plain TextMate consumer
# reads for its base surface. VS Code masks it with editor.background and the
# Codex builder substitutes Ghostty's values over it, so it went unnoticed on
# the upstream tones — but on its own it still described Palenight.
for rule in theme["tokenColors"]:
    if rule.get("name") == "Global settings":
        rule["settings"]["background"] = BG
        rule["settings"]["foreground"] = FG
        break

# Identity -----------------------------------------------------------------
theme["name"] = "Amber Material High Contrast"
theme["semanticClass"] = "amber-material-high-contrast"
theme.pop("maintainers", None)
theme["author"] = "Gaurang Karia"
theme["semanticHighlighting"] = True

os.makedirs(os.path.dirname(DST), exist_ok=True)
with open(DST, "w", encoding="utf-8") as destination:
    json.dump(theme, destination, indent=2)

print(f"wrote {DST}: {len(colors)} colors, {len(theme['tokenColors'])} token rules")
