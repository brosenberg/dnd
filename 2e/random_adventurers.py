#!/usr/bin/env python3

import argparse
import random

import magic_item

from character import Character
from dice import roll
from roll_abilities import get_abilities

LEVEL_RANGE = {
    "Low": (1, 3, 0),
    "Medium": (1, 4, 3),
    "High": (1, 6, 6),
    "Very high": (1, 12, 8),
}

MAGIC_ITEMS = {
    "Fighter": ["Armor No Shields", "Shields", "Sword", "Nonsword", "Potions and Oils"],
    "Mage": ["Scrolls", "Rings", "Rod/Staff/Wand", "Misc Magic"],
    "Cleric": [
        "Armor No Shields",
        "Shields",
        "Nonsword",
        "Potions and Oils",
        "Scrolls",
        "Misc Magic",
    ],
    "Thief": [
        "Shields",
        "Sword",
        "Nonsword",
        "Potions and Oils",
        "Rings",
        "Misc Magic",
    ],
}


def random_adventurer(level_range, expanded):
    mig = magic_item.MagicItemGen(expanded)
    class_roll = roll(1, 10, 0)
    char_class = "Fighter"
    if class_roll > 8:
        char_class = "Mage"
    elif class_roll > 6:
        char_class = "Thief"
    elif class_roll > 4:
        char_class = "Cleric"
    level = roll(
        LEVEL_RANGE[level_range][0],
        LEVEL_RANGE[level_range][1],
        LEVEL_RANGE[level_range][2],
    )
    adventurer = Character(char_class, level=level)
    has_armor = False
    has_shield = False
    for category in MAGIC_ITEMS[char_class]:
        if roll(1, 100, 0) <= level * 5:
            if category == "Armor No Shields":
                has_armor = True
            elif category == "Shields":
                has_shield = True
            item = mig.roll_category(category)
            # One reroll on cursed items
            if item.endswith('-1') or 'ursed' in item:
                item = mig.roll_category(category)
            adventurer.add_equipment(item)
    if level > 7 and (char_class == "Cleric" or char_class == "Fighter"):
        if not has_armor:
            adventurer.add_equipment("plate mail")
        if not has_shield:
            adventurer.add_equipment("medium shield")
        adventurer.add_equipment("unbarded medium warhorse")
    return adventurer


def main():
    parser = argparse.ArgumentParser(description="Generate adventurers")
    parser.add_argument(
        "-x",
        "--expanded",
        default=False,
        action="store_true",
        help="use expanded item generation tables",
    )
    args = parser.parse_args()
    no_appearing = roll(1, 8, 0)
    level_range = random.choice(list(LEVEL_RANGE.keys()))
    print(f"{level_range} level Adventurer Party ({no_appearing} adventurers)")
    print()
    for adventurer in range(0, no_appearing):
        print(random_adventurer(level_range, args.expanded))
        print()


if __name__ == "__main__":
    main()
