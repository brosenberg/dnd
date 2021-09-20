#!/usr/bin/env python3

import argparse
import random

import items
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


def random_adventurer(level_range, expanded, more_equipment):
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
    has_weapon = False
    has_armor = False
    has_shield = False
    for category in MAGIC_ITEMS[char_class]:
        if roll(1, 100, 0) <= level * 5:
            if category == "Armor No Shields":
                has_armor = True
            elif category == "Nonsword":
                has_weapon = True
            elif category == "Shields":
                has_shield = True
            elif category == "Sword":
                has_weapon = True
            item = mig.roll_category(category)
            if items.is_ranged_weapon(item):
                has_weapon = False
            # One reroll on cursed items
            if item.endswith("-1") or "ursed" in item:
                item = mig.roll_category(category)
            adventurer.add_equipment(item)
    if level > 7 and (char_class == "Cleric" or char_class == "Fighter"):
        if not has_armor:
            adventurer.add_equipment("Plate mail")
            has_armor = True
        if not has_shield and not more_equipment:
            adventurer.add_equipment("Medium shield")
            has_shield = True
        adventurer.add_equipment("Medium warhorse")
    if more_equipment:
        if not has_armor and char_class != "Mage":
            armor_type = None
            if char_class == "Druid":
                armor_type = "Druid"
            elif char_class in ["Thief", "Ranger"]:
                armor_type = "Rogue"
            elif char_class == "Bard":
                if level > 2:
                    armor_type = "Bard"
                else:
                    armor_type = "Rogue"
            elif char_class in ["Fighter", "Cleric", "Paladin"]:
                if level > 3:
                    armor_type = "High"
            adventurer.add_equipment(
                items.random_armor(expanded=expanded, specific=armor_type)
            )

        if (
            level > 1
            and not has_shield
            and char_class in ["Cleric", "Fighter", "Paladin"]
        ):
            adventurer.add_equipment(items.random_shield())

        if not has_weapon:
            weapon_type = None
            if char_class == "Cleric":
                weapon_type = "Cleric"
            elif char_class == "Druid":
                weapon_type = "Druid"
            elif char_class == "Rogue":
                weapon_type = "Rogue"
            elif char_class == "Mage":
                weapon_type = "Wizard"
            weapon = items.random_weapon(expanded=expanded, specific=weapon_type)
            thrown_weapons = items.load_table("thrown_weapons.json")
            ammo = items.appropriate_ammo_type(weapon)
            if ammo:
                ammo = f"{ammo} x{roll(6, 6, 0)}"
                adventurer.add_equipment(weapon)
                adventurer.add_equipment(ammo)
                while items.is_ranged_weapon(weapon):
                    weapon = items.random_weapon(
                        expanded=expanded, specific=weapon_type
                    )
            elif weapon in thrown_weapons:
                adventurer.add_equipment(f"{weapon} x{roll(2, 4, 0)}")
                while items.is_ranged_weapon(weapon):
                    weapon = items.random_weapon(
                        expanded=expanded, specific=weapon_type
                    )

            adventurer.add_equipment(weapon)
    # Rangers love to dual-wield
    if char_class == "Ranger" and level > 1:
        weapon = items.random_weapon(expanded=expanded)
        while items.is_ranged_weapon(weapon):
            weapon = items.random_weapon(expanded=expanded)
        adventurer.add_equipment(weapon)

    return adventurer


def main():
    parser = argparse.ArgumentParser(description="Generate adventurers")
    parser.add_argument(
        "-e",
        "--equipment",
        default=False,
        action="store_true",
        help="supply adventurer with more equipment",
    )
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
        print(random_adventurer(level_range, args.expanded, args.equipment))
        print()


if __name__ == "__main__":
    main()
