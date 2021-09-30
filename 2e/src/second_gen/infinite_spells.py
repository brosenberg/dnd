#!/usr/bin/env python3

import random

from second_gen.dice import roll
from second_gen.generate_scroll import random_spell


def get_page():
    contents = "Blank"
    contents_roll = roll(1, 100, 0)
    spell_class = None
    spell_level = 0
    if contents_roll > 60:
        spell_class = "Wizard"
    elif contents_roll > 30:
        spell_class = "Priest"
    if spell_class == "Wizard":
        spell_level = roll(1, 12, 0)
        if spell_level > 9:
            spell_level = roll(1, 8, 0)
    elif spell_class == "Priest":
        spell_level = roll(1, 10, 0)
        if spell_level > 7:
            spell_level = roll(1, 6, 0)
    if spell_class:
        contents = (
            f"{spell_class} - {spell_level}:{random_spell(spell_level, spell_class)}"
        )
    return contents


def main():
    print(get_page())


if __name__ == "__main__":
    main()
