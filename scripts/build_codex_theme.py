#!/usr/bin/env python3
"""Generate Codex CLI .tmTheme files from the Amber Material source palettes.

Codex runs inside a terminal, so the global surface colors come from the
Ghostty theme. Syntax scopes come from the VS Code theme's TextMate rules.
"""
import json
import os
import plistlib
import uuid

import ghostty_palette
from variants import ROOT, VARIANTS


def opaque(color):
  """Return #RRGGBB when a VS Code color includes an alpha channel."""
  if isinstance(color, str) and color.startswith("#") and len(color) == 9:
    return color[:7]
  return color


def build(variant):
  vscode_src = ROOT / variant.vscode_path
  ghostty_src = ROOT / variant.ghostty_path
  dst = ROOT / variant.codex_path

  with open(vscode_src, encoding="utf-8") as source:
    vscode_theme = json.load(source)

  ghostty, _ansi = ghostty_palette.load(ghostty_src)
  ui_colors = vscode_theme["colors"]
  settings = [
    {
      "name": "Global settings",
      "settings": {
        "background": ghostty["background"],
        "caret": ghostty["cursor-color"],
        "foreground": ghostty["foreground"],
        "invisibles": opaque(ui_colors["editorWhitespace.foreground"]),
        "lineHighlight": opaque(ui_colors["editor.lineHighlightBackground"]),
        "selection": ghostty["selection-background"],
      },
    }
  ]

  for rule in vscode_theme["tokenColors"]:
    scope = rule.get("scope")
    if not scope:
      continue
    if isinstance(scope, list):
      scope = ", ".join(scope)

    token_settings = {
      key: value
      for key, value in rule.get("settings", {}).items()
      if key in {"background", "fontStyle", "foreground"}
    }
    if not token_settings:
      continue

    output_rule = {"scope": scope, "settings": token_settings}
    if rule.get("name"):
      output_rule["name"] = rule["name"]
    settings.append(output_rule)

  theme = {
    "name": variant.name,
    "settings": settings,
    "uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, variant.codex_uuid_seed)).upper(),
  }

  dst.parent.mkdir(parents=True, exist_ok=True)
  with open(dst, "wb") as destination:
    plistlib.dump(theme, destination, fmt=plistlib.FMT_XML, sort_keys=False)

  print(f"wrote {dst}: {len(settings) - 1} token rules")


def main():
  for variant in VARIANTS:
    build(variant)


if __name__ == "__main__":
  main()
