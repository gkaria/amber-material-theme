#!/usr/bin/env python3
"""WCAG 2.1 contrast for Amber Material text roles.

The drift check proves generated files match their generators. This module
proves those colors stay at or above 4.5:1, which is the theme's promise.
"""

import json

from variants import ROOT, VARIANTS

AA = 4.5

EDITOR_TEXT_ROLES = (
    "fg",
    "fg_dim",
    "amber",
    "red",
    "green",
    "blue",
    "accent",
    "syntax_purple",
    "syntax_orange",
    "syntax_gold",
    "disabled_fg",
)


def _channel(value):
    value = value / 255
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def normalize(color):
    """Return #RRGGBB, ignoring an alpha suffix. None when it is not a color."""
    if not isinstance(color, str) or not color.startswith("#"):
        return None
    digits = color[1:]
    if len(digits) == 8:
        digits = digits[:6]
    if len(digits) != 6:
        return None
    try:
        int(digits, 16)
    except ValueError:
        return None
    return "#" + digits.upper()


def contrast(foreground, background):
    def luminance(color):
        red, green, blue = (int(color[i:i + 2], 16) for i in (1, 3, 5))
        return (
            0.2126 * _channel(red)
            + 0.7152 * _channel(green)
            + 0.0722 * _channel(blue)
        )

    lighter = max(luminance(foreground), luminance(background))
    darker = min(luminance(foreground), luminance(background))
    return (lighter + 0.05) / (darker + 0.05)


def pairs_under(pairs, minimum=AA):
    """Return (name, foreground, background, ratio) for pairs under minimum.

    `pairs` is an iterable of (name, foreground, background). Colors may carry
    an alpha suffix; it is stripped before measuring.
    """
    misses = []
    for name, foreground, background in pairs:
        fg = normalize(foreground)
        bg = normalize(background)
        if fg is None or bg is None:
            misses.append((name, foreground, background, None))
            continue
        ratio = contrast(fg, bg)
        if ratio < minimum:
            misses.append((name, fg, bg, ratio))
    return misses


def role_pairs(variant):
    """Named text roles. Surface and border remaps are not text."""
    pairs = [
        (f"{variant.id} {role}", getattr(variant, role), variant.bg)
        for role in EDITOR_TEXT_ROLES
    ]
    pairs.append((
        f"{variant.id} ghostty foreground",
        variant.ghostty_foreground,
        variant.ghostty_background,
    ))
    pairs.append((
        f"{variant.id} prompt",
        variant.prompt_amber,
        variant.ghostty_background,
    ))
    pairs.append((
        f"{variant.id} prompt bright",
        variant.prompt_amber_bright,
        variant.ghostty_background,
    ))
    for index, color in enumerate(variant.ghostty_ansi):
        if index == 0:
            continue
        pairs.append((
            f"{variant.id} ansi {index}",
            color,
            variant.ghostty_background,
        ))
    return pairs


def token_pairs(theme):
    """TextMate foregrounds against the editor background.

    Rules that set their own background (Invalid Broken) paint on that color,
    not on the editor, so they are not text-on-editor pairs.
    """
    background = theme["colors"]["editor.background"]
    pairs = []
    for rule in theme.get("tokenColors", []):
        settings = rule.get("settings") or {}
        if settings.get("background"):
            continue
        foreground = settings.get("foreground")
        if not foreground:
            continue
        name = rule.get("name") or ", ".join(
            rule.get("scope") if isinstance(rule.get("scope"), list)
            else [rule.get("scope") or ""]
        )
        pairs.append((name, foreground, background))
    return pairs


def variant_misses(variant):
    misses = pairs_under(role_pairs(variant))
    theme_path = ROOT / variant.vscode_path
    if theme_path.is_file():
        theme = json.loads(theme_path.read_text(encoding="utf-8"))
        for name, foreground, background, ratio in pairs_under(token_pairs(theme)):
            misses.append((f"{variant.id} token {name}", foreground, background, ratio))
    return misses


def all_misses():
    misses = []
    for variant in VARIANTS:
        misses.extend(variant_misses(variant))
    return misses
