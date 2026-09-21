#!/usr/bin/env python3
"""Contrast gate for Amber Material text roles and generated syntax."""

import unittest

import contrast


class ContrastTests(unittest.TestCase):
    def test_under_ratio_is_reported(self):
        misses = contrast.pairs_under([("sample", "#FFFFFF", "#FFFFFF")])
        self.assertEqual(len(misses), 1)
        self.assertEqual(misses[0][0], "sample")
        self.assertLess(misses[0][3], contrast.AA)

    def test_alpha_suffix_is_ignored(self):
        misses = contrast.pairs_under([("disabled", "#8A91A6ff", "#22252F")])
        self.assertEqual(misses, [])

    def test_variants_and_generated_syntax_clear_aa(self):
        misses = contrast.all_misses()
        rendered = "\n".join(
            f"{name}: {foreground} on {background} = {ratio}"
            for name, foreground, background, ratio in misses
        )
        self.assertEqual(misses, [], rendered)


if __name__ == "__main__":
    unittest.main()
