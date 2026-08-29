#!/usr/bin/env python3
"""Derive high-contrast Palenight variants from the MIT-licensed base theme.

Deepens or lifts chrome/editor surfaces per variant and applies syntax palette
tuning for light backgrounds.
"""
import copy
import json
import os

import ghostty_palette
from variants import ROOT, VARIANTS, upstream_remap

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "base-palenight-italic.json")


def remap_syntax(token_colors, syntax_remap):
  """Retune TextMate foreground/background hues for a variant."""
  if not syntax_remap:
    return
  normalized = {key.upper(): value for key, value in syntax_remap.items()}
  for rule in token_colors:
    settings = rule.get("settings", {})
    for key in ("foreground", "background"):
      value = settings.get(key)
      if not isinstance(value, str) or not value.startswith("#"):
        continue
      base, alpha = value[:7].upper(), value[7:]
      if base in normalized:
        settings[key] = normalized[base] + alpha


def build(variant):
  BG = variant.bg
  BG_DEEP = variant.bg_deep
  BG_RAISED = variant.bg_raised
  FG = variant.fg
  FG_DIM = variant.fg_dim
  BORDER = variant.border
  BORDER_SOFT = variant.border_soft
  AMBER = variant.amber
  AMBER_FILL = variant.amber_bright
  RED = variant.red
  GREEN = variant.green
  BLUE = variant.blue
  ACCENT = variant.accent
  SYNTAX_PURPLE = variant.syntax_purple
  SYNTAX_ORANGE = variant.syntax_orange

  theme = copy.deepcopy(json.load(open(SRC, encoding="utf-8")))
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
    "activityBar.foreground", "statusBar.foreground", "list.foreground",
    "menu.foreground", "dropdown.foreground", "input.foreground", "terminal.foreground",
  ):
    colors[key] = FG

  for key in ("tab.inactiveForeground", "activityBar.inactiveForeground",
              "breadcrumb.foreground", "editorLineNumber.foreground", "descriptionForeground"):
    colors[key] = FG_DIM

  # Contrast accents ---------------------------------------------------------
  colors["editorCursor.foreground"] = AMBER_FILL
  colors["editorCursor.background"] = BG
  colors["terminalCursor.foreground"] = AMBER_FILL
  colors["terminalCursor.background"] = BG

  colors["editorWarning.foreground"] = AMBER + "b3"
  colors["editorOverviewRuler.warningForeground"] = AMBER + "99"
  colors["notificationsWarningIcon.foreground"] = AMBER
  colors["debugConsole.warningForeground"] = AMBER
  colors["activityWarningBadge.background"] = AMBER_FILL
  colors["inputValidation.warningBorder"] = AMBER
  colors["editorBracketMatch.border"] = AMBER_FILL + "80"
  colors["editor.findRangeHighlightBackground"] = AMBER_FILL + "4d"
  colors["editor.selectionHighlightBackground"] = AMBER_FILL + "33"
  colors["gitDecoration.conflictingResourceForeground"] = AMBER + "e6"
  colors["contrastBorder"] = BORDER
  colors["editorIndentGuide.background1"] = variant.indent_guide
  colors["editorIndentGuide.activeBackground1"] = variant.indent_guide_active
  colors["editor.lineHighlightBackground"] = variant.line_highlight
  colors["editor.selectionBackground"] = variant.selection_background

  for key in ("sideBar.border", "panel.border", "activityBar.border",
              "statusBar.border", "titleBar.border", "editorGroup.border", "tab.border"):
    colors[key] = BORDER

  for key in (
    "chat.avatarForeground", "chat.slashCommandForeground",
    "list.inactiveSelectionIconForeground", "menu.selectionForeground",
    "menubar.selectionForeground", "settings.modifiedItemIndicator",
    "statusBar.debuggingForeground", "extensionButton.foreground",
    "editorOverviewRuler.findMatchForeground", "extensionIcon.verifiedForeground",
  ):
    colors[key] = AMBER

  colors["notebook.inactiveFocusedCellBorder"] = AMBER_FILL + "80"
  colors["sash.hoverBorder"] = AMBER_FILL + "80"
  colors["toolbar.activeBackground"] = AMBER_FILL + "26"
  colors["extensionButton.background"] = AMBER_FILL + "14"
  colors["extensionButton.border"] = AMBER_FILL + "14"
  colors["extensionButton.hoverBackground"] = AMBER_FILL + "33"
  colors["extensionButton.separator"] = AMBER_FILL + "33"
  colors["tab.activeModifiedBorder"] = AMBER_FILL + "00"
  colors["statusBarItem.remoteHoverForeground"] = variant.badge_on_amber_fg

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

  for key in ("commandCenter.border", "keybindingLabel.border",
              "keybindingLabel.bottomBorder"):
    colors[key] = BORDER

  for key in ("agentsPanel.border", "sideBarActivityBarTop.border",
              "sideBarSectionHeader.border", "sideBarStickyScroll.border"):
    colors[key] = BORDER + "99"

  colors["widget.border"] = variant.widget_border

  for key in ("menu.selectionBorder", "menubar.selectionBorder", "menubar.selectionBackground",
              "list.dropBetweenBackground", "listFilterWidget.background",
              "listFilterWidget.outline", "listFilterWidget.noMatchesOutline",
              "panelSection.dropBackground", "toolbar.hoverBackground"):
    colors[key] = FG + "1a"

  colors["quickInputList.focusBackground"] = FG + "26"
  colors["commandCenter.foreground"] = FG + "99"
  colors["chat.requestCodeBorder"] = BORDER_SOFT
  colors["chat.checkpointSeparator"] = FG_DIM
  colors["editorStickyScrollHover.background"] = variant.sticky_scroll_hover
  colors["editor.findMatchHighlightBorder"] = variant.find_match_highlight_border
  colors["editor.lineHighlightBorder"] = BORDER + "ff"
  colors["extensionIcon.preReleaseForeground"] = variant.extension_pre_release
  colors["button.separator"] = variant.button_separator

  for key in ("editorIndentGuide.activeBackground", "tree.indentGuidesStroke",
              "editorWhitespace.foreground", "terminalCommandGuide.foreground"):
    colors[key] = variant.muted_structural

  colors["disabledForeground"] = variant.disabled_fg
  colors["icon.foreground"] = FG
  colors["inlineChatInput.border"] = BORDER

  colors["scrollbarSlider.background"] = AMBER_FILL + "40"
  colors["scrollbarSlider.hoverBackground"] = AMBER_FILL + "80"
  colors["scrollbarSlider.activeBackground"] = AMBER_FILL + "b3"
  colors["minimapSlider.background"] = AMBER_FILL + "26"
  colors["minimapSlider.hoverBackground"] = AMBER_FILL + "40"
  colors["minimapSlider.activeBackground"] = AMBER_FILL + "66"

  for key in ("badge.background", "activityBarBadge.background",
              "extensionBadge.remoteBackground"):
    colors[key] = AMBER_FILL
  colors["notificationsInfoIcon.foreground"] = AMBER
  for key in ("badge.foreground", "activityBarBadge.foreground",
              "extensionBadge.remoteForeground"):
    colors[key] = variant.badge_on_amber_fg

  colors["button.foreground"] = variant.badge_on_amber_fg
  colors["button.hoverBackground"] = variant.button_hover
  colors["statusBarItem.remoteForeground"] = variant.badge_on_amber_fg
  colors["statusBarItem.remoteHoverBackground"] = variant.button_hover
  colors["selection.background"] = AMBER_FILL + "40"
  colors["inputOption.activeBackground"] = AMBER_FILL + "33"
  colors["inputOption.activeForeground"] = AMBER

  remap_table = upstream_remap(variant)
  for key, value in list(colors.items()):
    if not isinstance(value, str) or not value.startswith("#"):
      continue
    base, alpha = value[:7].upper(), value[7:]
    if base in remap_table:
      colors[key] = remap_table[base] + alpha

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

  colors["statusBar.debuggingBackground"] = BG_RAISED
  colors["statusBarItem.hoverBackground"] = BG_RAISED
  colors["statusBarItem.prominentBackground"] = BG_RAISED
  colors["statusBarItem.activeBackground"] = BORDER
  colors["statusBarItem.prominentHoverBackground"] = BORDER

  colors["editor.wordHighlightBackground"] = BORDER
  colors["editor.wordHighlightStrongBackground"] = BORDER_SOFT
  colors["peekViewResult.selectionBackground"] = BORDER

  colors["editor.findMatchBackground"] = AMBER_FILL + "66"

  colors["list.activeSelectionForeground"] = variant.badge_on_amber_fg
  colors["list.activeSelectionIconForeground"] = variant.badge_on_amber_fg
  colors["editorSuggestWidget.selectedForeground"] = variant.badge_on_amber_fg
  colors["editorSuggestWidget.selectedIconForeground"] = variant.badge_on_amber_fg
  colors["extensionButton.prominentForeground"] = variant.badge_on_amber_fg
  colors["quickInputList.focusForeground"] = FG

  colors["list.activeSelectionBackground"] = AMBER_FILL
  colors["editorSuggestWidget.selectedBackground"] = AMBER_FILL
  colors["editor.findMatchHighlightBackground"] = AMBER_FILL + "40"
  colors["editor.hoverHighlightBackground"] = AMBER_FILL + "33"
  colors["editor.inactiveSelectionBackground"] = variant.inactive_selection
  colors["editor.rangeHighlightBackground"] = AMBER_FILL + "20"
  colors["terminal.findMatchBackground"] = AMBER_FILL + "80"
  colors["terminal.findMatchHighlightBackground"] = AMBER_FILL + "40"

  for key in (
    "editorWidget.border", "editorHoverWidget.border", "debugExceptionWidget.border",
    "peekView.border", "dropdown.border", "input.border", "editorWidget.resizeBorder",
    "editorSuggestWidget.border", "notificationCenter.border", "notifications.border",
    "notificationToast.border", "menu.border", "quickInput.border",
    "editorGroup.dropIntoPromptBorder", "debugToolBar.border",
  ):
    colors[key] = BORDER_SOFT

  colors["profileBadge.background"] = AMBER_FILL
  colors["profileBadge.foreground"] = variant.badge_on_amber_fg
  colors["terminal.selectionBackground"] = variant.terminal_selection
  colors["terminal.inactiveSelectionBackground"] = variant.terminal_inactive_selection

  _, ghostty_ansi = ghostty_palette.load(ROOT / variant.ghostty_path)
  for index, name in enumerate(ghostty_palette.ANSI_NAMES):
    colors[f"terminal.ansi{name}"] = ghostty_ansi[index]

  for key in ("focusBorder", "list.focusOutline", "inputOption.activeBorder",
              "tab.activeBorderTop", "panelTitle.activeBorder", "activityBar.activeBorder",
              "activityBarTop.activeBorder", "notebook.focusedCellBorder",
              "editor.findMatchBorder"):
    colors[key] = AMBER_FILL
  for key in ("editorLineNumber.activeForeground",
              "list.highlightForeground", "list.focusHighlightForeground",
              "pickerGroup.foreground", "textLink.foreground"):
    colors[key] = AMBER
  for key in ("button.background", "progressBar.background",
              "statusBarItem.remoteBackground"):
    colors[key] = AMBER_FILL

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
    colors[key] = variant.badge_on_amber_fg

  colors["editorBracketHighlight.foreground1"] = AMBER
  colors["editorBracketHighlight.foreground2"] = BLUE
  colors["editorBracketHighlight.foreground3"] = SYNTAX_ORANGE
  colors["editorBracketHighlight.foreground4"] = ACCENT
  colors["editorBracketHighlight.foreground5"] = SYNTAX_PURPLE
  colors["editorBracketHighlight.foreground6"] = GREEN
  colors["editorBracketHighlight.unexpectedBracket.foreground"] = RED

  for key in ("editorInlayHint.foreground", "editorInlayHint.typeForeground",
              "editorInlayHint.parameterForeground", "editorGhostText.foreground"):
    colors[key] = FG_DIM
  for key in ("editorInlayHint.background", "editorInlayHint.typeBackground",
              "editorInlayHint.parameterBackground"):
    colors[key] = BG_RAISED

  colors["editorStickyScroll.background"] = BG
  colors["editorStickyScroll.border"] = BORDER

  colors["gitDecoration.addedResourceForeground"] = GREEN + "e6"

  colors["statusBarItem.errorBackground"] = RED
  colors["statusBarItem.warningBackground"] = AMBER_FILL
  for key in ("statusBarItem.errorForeground", "statusBarItem.warningForeground"):
    colors[key] = variant.badge_on_amber_fg
  colors["problemsErrorIcon.foreground"] = RED
  colors["problemsWarningIcon.foreground"] = AMBER
  colors["problemsInfoIcon.foreground"] = BLUE
  colors["editorHint.foreground"] = FG_DIM

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

  colors["charts.foreground"] = FG
  colors["charts.lines"] = BORDER
  colors["charts.red"] = RED
  colors["charts.green"] = GREEN
  colors["charts.blue"] = BLUE
  colors["charts.yellow"] = AMBER_FILL
  colors["charts.orange"] = SYNTAX_ORANGE
  colors["charts.purple"] = SYNTAX_PURPLE

  for key in ("tab.hoverBackground", "tab.unfocusedHoverBackground",
              "notebook.cellEditorBackground", "inlineChat.background"):
    colors[key] = BG_RAISED
  colors["list.filterMatchBackground"] = AMBER_FILL + "33"
  colors["list.filterMatchBorder"] = AMBER_FILL + "80"
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

  colors["contrastActiveBorder"] = BG_DEEP + "00"
  colors["merge.border"] = BG + "00"
  colors["chat.slashCommandBackground"] = "#ffffff00"
  colors["commandCenter.activeBorder"] = BORDER + "00"
  colors["tab.unfocusedActiveBorderTop"] = "#676E9500"

  colors["chat.requestBackground"] = BG
  colors["chat.avatarBackground"] = BG_DEEP
  colors["chat.editedFileForeground"] = BLUE
  colors["chat.linesAddedForeground"] = GREEN
  colors["chat.linesRemovedForeground"] = RED
  colors["chat.findMatchBackground"] = AMBER_FILL + "66"
  colors["chat.findMatchHighlightBackground"] = AMBER_FILL + "40"
  colors["chat.thinkingShimmer"] = FG
  colors["chat.inputWorkingBorderColor1"] = AMBER_FILL
  colors["chat.inputWorkingBorderColor2"] = AMBER_FILL + "80"
  colors["chat.inputWorkingBorderColor3"] = variant.chat_input_border_3
  colors["chat.voiceGlowBaseColor"] = AMBER_FILL
  colors["chat.requestBorder"] = BORDER + "66"
  colors["textLink.activeForeground"] = variant.text_link_active

  colors["inlineChat.foreground"] = FG
  colors["inlineChat.border"] = BORDER_SOFT
  colors["inlineChat.shadow"] = BG_DEEP
  colors["inlineChatInput.background"] = BG_RAISED
  colors["inlineChatInput.focusBorder"] = AMBER_FILL
  colors["inlineChatInput.placeholderForeground"] = FG_DIM
  colors["inlineChatDiff.inserted"] = GREEN + "80"
  colors["inlineChatDiff.removed"] = RED + "80"

  colors["surface.background"] = BG
  colors["surface.foreground"] = FG
  colors["panelSectionHeader.background"] = BG
  colors["panelSectionHeader.border"] = BORDER + "99"
  colors["panelSection.border"] = BORDER

  colors["list.inactiveSelectionBackground"] = BORDER
  colors["list.inactiveSelectionForeground"] = FG

  colors["agents.background"] = BG_DEEP
  colors["agentsPanel.background"] = BG
  colors["agentsPanel.foreground"] = FG
  colors["agentsCard.border"] = BORDER
  colors["agentsBottomPanel.border"] = BORDER
  colors["agentsGradient.tintColor"] = AMBER_FILL
  colors["agentsChatInput.background"] = BG_RAISED
  colors["agentsChatInput.foreground"] = FG
  colors["agentsChatInput.border"] = BORDER_SOFT
  colors["agentsChatInput.focusBorder"] = AMBER_FILL
  colors["agentsChatInput.placeholderForeground"] = FG_DIM
  colors["agentsNewSessionButton.background"] = BG_DEEP + "00"
  colors["agentsNewSessionButton.foreground"] = FG
  colors["agentsNewSessionButton.border"] = BORDER_SOFT
  colors["agentsNewSessionButton.hoverBackground"] = BG_RAISED
  for key in ("agentsBadge.background", "agentsUnreadBadge.background"):
    colors[key] = AMBER_FILL
  for key in ("agentsBadge.foreground", "agentsUnreadBadge.foreground"):
    colors[key] = variant.badge_on_amber_fg
  colors["activeSessionView.background"] = BG
  colors["inactiveSessionView.background"] = BG_DEEP
  colors["activeSessionView.foreground"] = FG
  colors["inactiveSessionView.foreground"] = FG_DIM
  colors["agentStatusIndicator.background"] = BG_DEEP
  colors["agentFeedbackEditorWidget.background"] = BG_RAISED
  colors["agentFeedbackEditorWidget.border"] = BORDER_SOFT
  colors["agentFeedbackInputWidget.border"] = BORDER_SOFT
  colors["agentsUpdateButton.downloadingBackground"] = AMBER_FILL + "66"
  colors["agentsUpdateButton.downloadedBackground"] = AMBER_FILL + "b3"

  colors.update(variant.workbench_overrides)

  remap_syntax(theme["tokenColors"], variant.syntax_remap)

  for rule in theme["tokenColors"]:
    if rule.get("name") == "Global settings":
      rule["settings"]["background"] = BG
      rule["settings"]["foreground"] = FG
      break

  theme["name"] = variant.name
  theme["type"] = variant.theme_type
  theme["semanticClass"] = variant.semantic_class
  theme.pop("maintainers", None)
  theme["author"] = "Gaurang Karia"
  theme["semanticHighlighting"] = True

  dst = ROOT / variant.vscode_path
  dst.parent.mkdir(parents=True, exist_ok=True)
  with open(dst, "w", encoding="utf-8") as destination:
    json.dump(theme, destination, indent=2)

  print(f"wrote {dst}: {len(colors)} colors, {len(theme['tokenColors'])} token rules")


def main():
  for variant in VARIANTS:
    build(variant)


if __name__ == "__main__":
  main()
