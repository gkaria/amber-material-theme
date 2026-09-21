#!/usr/bin/env python3
"""Write the public Amber Material role palette.

This is the port contract: named roles, not the 520 derived workbench keys.
No-italic companions share these colors, so they are not a third variant.
"""

import json

from contrast import contrast, normalize
from variants import ROOT, terminal_variants

# (role name, variant attribute, use, contrast against this attribute or None)
ROLES = (
    ("editor.background", "bg", "surface", None),
    ("editor.backgroundDeep", "bg_deep", "surface", None),
    ("editor.backgroundRaised", "bg_raised", "surface", None),
    ("editor.foreground", "fg", "text", "bg"),
    ("editor.foregroundDim", "fg_dim", "text", "bg"),
    ("editor.foregroundDisabled", "disabled_fg", "text", "bg"),
    ("accent.fill", "amber_bright", "fill", None),
    ("accent.text", "amber", "text", "bg"),
    ("syntax.gold", "syntax_gold", "text", "bg"),
    ("syntax.orange", "syntax_orange", "text", "bg"),
    ("syntax.purple", "syntax_purple", "text", "bg"),
    ("syntax.red", "red", "text", "bg"),
    ("syntax.green", "green", "text", "bg"),
    ("syntax.blue", "blue", "text", "bg"),
    ("syntax.cyan", "accent", "text", "bg"),
    ("border", "border", "border", None),
    ("border.soft", "border_soft", "border", None),
    ("terminal.background", "ghostty_background", "surface", None),
    ("terminal.foreground", "ghostty_foreground", "text", "ghostty_background"),
    ("terminal.cursor", "ghostty_cursor", "text", "ghostty_background"),
    ("terminal.prompt", "prompt_amber", "text", "ghostty_background"),
    ("terminal.promptBright", "prompt_amber_bright", "text", "ghostty_background"),
)

DESTINATION = ROOT / "palette" / "amber-material.json"


def role_entry(variant, attribute, use, against):
    raw = getattr(variant, attribute)
    entry = {"hex": normalize(raw), "use": use}
    if against is not None:
        backdrop = normalize(getattr(variant, against))
        entry["contrastAgainst"] = against
        entry["contrast"] = round(contrast(entry["hex"], backdrop), 2)
    return entry


def palette():
    variants = {}
    for variant in terminal_variants():
        variants[variant.id] = {
            "name": variant.name,
            "roles": {
                name: role_entry(variant, attribute, use, against)
                for name, attribute, use, against in ROLES
            },
        }
    return {
        "name": "Amber Material",
        "contrastMinimum": 4.5,
        "variants": variants,
    }


def main():
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(
        json.dumps(palette(), indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {DESTINATION.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
