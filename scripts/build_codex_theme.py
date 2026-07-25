#!/usr/bin/env python3
"""Generate a Codex CLI .tmTheme from the Amber Material source palettes.

Codex runs inside a terminal, so the global surface colors come from the
Ghostty theme. Syntax scopes come from the VS Code theme's TextMate rules.
"""
import json
import os
import plistlib
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

VSCODE_SRC = os.path.join(ROOT, "themes", "amber-material-hc.json")
GHOSTTY_SRC = os.path.join(ROOT, "ghostty", "amber-material")
DST = os.path.join(ROOT, "codex", "amber-material-high-contrast.tmTheme")

THEME_NAME = "Amber Material High Contrast"
THEME_UUID = str(
    uuid.uuid5(
        uuid.NAMESPACE_URL,
        "https://github.com/gkaria/amber-material-theme#codex",
    )
).upper()


def load_ghostty_colors(path):
    """Read the first value for each non-palette Ghostty color option."""
    colors = {}
    with open(path, encoding="utf-8") as source:
        for raw_line in source:
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith("palette"):
                continue
            key, separator, value = line.partition("=")
            if separator:
                colors.setdefault(key.strip(), value.strip())
    return colors


def opaque(color):
    """Return #RRGGBB when a VS Code color includes an alpha channel."""
    if isinstance(color, str) and color.startswith("#") and len(color) == 9:
        return color[:7]
    return color


with open(VSCODE_SRC, encoding="utf-8") as source:
    vscode_theme = json.load(source)

ghostty = load_ghostty_colors(GHOSTTY_SRC)
required = {
    "background",
    "foreground",
    "cursor-color",
    "selection-background",
}
missing = sorted(required - ghostty.keys())
if missing:
    raise ValueError(f"missing Ghostty colors: {', '.join(missing)}")

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
    "name": THEME_NAME,
    "settings": settings,
    "uuid": THEME_UUID,
}

os.makedirs(os.path.dirname(DST), exist_ok=True)
with open(DST, "wb") as destination:
    plistlib.dump(theme, destination, fmt=plistlib.FMT_XML, sort_keys=False)

print(f"wrote {DST}: {len(settings) - 1} token rules")
