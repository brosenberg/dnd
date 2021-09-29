#!/usr/bin/env python3

import argparse
import random

import items

# import magic_item

from character import Character
from dice import roll
from roll_abilities import get_abilities
from utils import intersect
from utils import load_table

LEVEL_RANGES = ["Low", "Medium", "High", "Very high"]

LEVEL_RANGE = {
    "Low": (1, 3, 0),
    "Medium": (1, 4, 3),
    "High": (1, 6, 6),
    "Very high": (1, 12, 8),
    "Epic": (1, 10, 20),
}

EXPERIENCE_RANGE = {
    "Low": [0, 4545],
    "Medium": [10000, 31818],
    "High": [75000, 272727],
    "Very high": [660000, 2200000],
    "Epic": [4500000, 15000000],
}

MAGIC_ITEMS = {
    "Warrior": ["Armor No Shields", "Shields", "Sword", "Nonsword", "Potions and Oils"],
    "Wizard": ["Scrolls", "Rings", "Rod/Staff/Wand", "Misc Magic"],
    "Priest": [
        "Armor No Shields",
        "Shields",
        "Nonsword",
        "Potions and Oils",
        "Scrolls",
        "Misc Magic",
    ],
    "Rogue": [
        "Shields",
        "Sword",
        "Nonsword",
        "Potions and Oils",
        "Rings",
        "Misc Magic",
    ],
}


def get_magic_item_categories(class_groups):
    categories = []
    for class_group in class_groups:
        categories += MAGIC_ITEMS[class_group]
    return list(set(categories))


def random_adventurer(
    level_range,
    expanded,
    more_equipment,
    more_classes,
    alignment=None,
    experience=None,
    slow_advancement=False,
):
    level = roll(
        LEVEL_RANGE[level_range][0],
        LEVEL_RANGE[level_range][1],
        LEVEL_RANGE[level_range][2],
    )
    adventurer = None
    classes = []
    has_weapon = False
    has_ranged_weapon = False
    has_armor = False
    has_shield = False
    if more_classes:
        class_group = random.choice(["Warrior", "Wizard", "Priest", "Rogue"])
        adventurer = Character(
            class_group=class_group,
            level=level,
            alignment=alignment,
            experience=experience,
            expanded=expanded,
            slow_advancement=slow_advancement,
        )
        classes = adventurer.classes
    else:
        class_roll = roll(1, 10, 0)
        classes = ["Fighter"]
        if class_roll > 8:
            classes = ["Mage"]
        elif class_roll > 6:
            classes = ["Thief"]
        elif class_roll > 4:
            classes = ["Cleric"]
        adventurer = Character(
            classes=classes,
            level=level,
            alignment=alignment,
            experience=experience,
            expanded=expanded,
            slow_advancement=slow_advancement,
        )
    class_groups = adventurer.class_groups
    for category in get_magic_item_categories(adventurer.class_groups):
        if roll(1, 100, 0) <= level * 5:

            item = items.random_magic_item(category=category, classes=classes)
            # One reroll on cursed items
            if items.is_cursed(item):
                item = items.random_magic_item(category=category, classes=classes)

            if category == "Armor No Shields":
                has_armor = True
            elif category in ["Nonsword", "Sword", "Rod/Staff/Wand"]:
                if items.is_missile_weapon(item):
                    has_ranged_weapon = True
                else:
                    has_weapon = True
            elif category == "Shields":
                has_shield = True
            adventurer.add_equipment(item)

    # Roll standard items
    if not more_equipment:
        if level > 7 and intersect(classes, ["Cleric", "Fighter", "Paladin"]):
            if not has_armor:
                adventurer.add_equipment("Plate mail")
                has_armor = True
            if not has_shield:
                adventurer.add_equipment("Medium shield")
                has_shield = True
            adventurer.add_equipment("Medium warhorse")
    # Roll more variety of items
    else:
        # Check to see if the adventurer has random ammo and give them a weapon for it
        appropriate_items = []
        for item in adventurer.equipment:
            # Give a weapon for orphan ammo
            try:
                appropriate_items.append(
                    random.choice(items.appropriate_weapons_by_ammo(item))
                )
                has_ranged_weapon = True
                continue
            except IndexError:
                pass
            # Give ammo for weapons needing it
            try:
                ammo, count = items.random_appropriate_ammo(item)
                count *= 2
                appropriate_items.append(f"{ammo} x{count}")
            except TypeError:
                pass
        for item in appropriate_items:
            adventurer.add_equipment(item)

        # Maybe give the adventurer a mount
        if roll(1, 100, 0) < 20 * level:
            if level > 2 and ("Warrior" in class_groups or "Cleric" in classes):
                horse_roll = roll(1, 100, 0)
                if horse_roll < roll(1, 12, 0) * level:
                    adventurer.add_equipment("Heavy warhorse")
                elif horse_roll < 15 * level:
                    adventurer.add_equipment("Medium warhorse")
                else:
                    adventurer.add_equipment("Light warhorse")
                if roll(1, 100, 0) < 10 * level:
                    barding = None
                    if roll(1, 100, 0) < 51:
                        barding = items.random_armor(
                            expanded=expanded, table="armor_low.json"
                        )
                    else:
                        barding = items.random_armor(
                            expanded=expanded, table="armor_low.json"
                        )
                    adventurer.add_equipment(f"{barding} barding")
            else:
                adventurer.add_equipment("Riding horse")

        # Everyone should have armor. Besides wizards.
        if not has_armor:
            adventurer.add_equipment(
                items.random_item(
                    item_type="Armor", classes=classes, filters={"Category": "Armor"}
                )
            )

        if (
            level > 1
            and not has_shield
            and intersect(classes, ["Cleric", "Fighter", "Paladin"])
        ):
            adventurer.add_equipment(
                items.random_item(
                    item_type="Armor", classes=classes, filters={"Category": "Shield"}
                )
            )

        # Everyone should have at least one weapon.
        if not has_weapon:
            filters = {}
            if has_ranged_weapon:
                filters = {"Category": "Melee"}
            weapon = items.random_item(
                item_type="Weapons", classes=classes, filters=filters
            )

            # If the weapon requires ammo, give some ammo for it
            ammo = items.appropriate_ammo_type(weapon)
            if ammo:
                ammo_dice, ammo_die, ammo_mod = items.random_item_count(ammo)
                ammo_dice *= 2
                ammo = f"{ammo} x{roll(ammo_dice, ammo_die, ammo_mod)}"
                adventurer.add_equipment(weapon)
                adventurer.add_equipment(ammo)
                has_ranged_weapon = True
                weapon = items.random_item(
                    item_type="Weapons", classes=classes, filters={"Category": "Melee"}
                )
            # If the weapon is thrown, give a few of them
            elif items.is_thrown_weapon(weapon):
                ammo_dice, ammo_die, ammo_mod = items.random_item_count(weapon)
                count = roll(ammo_dice, ammo_die, ammo_mod)
                if count > 1:
                    adventurer.add_equipment(f"{weapon} x{count}")
                else:
                    adventurer.add_equipment(weapon)
                has_ranged_weapon = True
                weapon = items.random_item(
                    item_type="Weapons", classes=classes, filters={"Category": "Melee"}
                )

            adventurer.add_equipment(weapon)
            has_weapon = True

        # Rangers love to dual-wield
        if "Ranger" in classes and level > 1:
            adventurer.add_equipment(
                weapon=items.random_item(
                    item_type="Weapons", classes=classes, filters={"Category": "Melee"}
                )
            )

    return adventurer


def main():
    parser = argparse.ArgumentParser(description="Generate adventurers")
    parser.add_argument(
        "-a",
        "--alignments",
        default=False,
        action="store_true",
        help="generate adventurers with similar alignments",
    )
    parser.add_argument(
        "-c",
        "--classes",
        default=False,
        action="store_true",
        help="generate more classes",
    )
    parser.add_argument(
        "-e",
        "--experience",
        default=False,
        action="store_true",
        help="generate consistent experience scores across characters",
    )
    parser.add_argument(
        "-p",
        "--epic",
        default=False,
        action="store_true",
        help="generate epic level characters",
    )
    parser.add_argument(
        "-s",
        "--slow",
        default=False,
        action="store_true",
        help="use slow advancement but removed level limits for demi-humans",
    )
    parser.add_argument(
        "-q",
        "--equipment",
        default=False,
        action="store_true",
        help="supply adventurers with more extensive and more reasonable equipment",
    )
    parser.add_argument(
        "-x",
        "--expanded",
        default=False,
        action="store_true",
        help="use expanded generation tables",
    )

    args = parser.parse_args()
    no_appearing = roll(1, 8, 0)
    if args.epic:
        level_range = random.choice(LEVEL_RANGES + ["Epic"])
    else:
        level_range = random.choice(LEVEL_RANGES)
    experience = None
    alignments = None
    level_str = f"{LEVEL_RANGE[level_range][0]+LEVEL_RANGE[level_range][2]} - {LEVEL_RANGE[level_range][1]+LEVEL_RANGE[level_range][2]}"

    print(
        f"{level_range} level ({level_str}) Adventurer Party ({no_appearing} adventurers)"
    )
    if args.experience:
        min_mod = 1
        if args.slow:
            min_mod = 2
        experience = random.randint(
            EXPERIENCE_RANGE[level_range][0] * min_mod, EXPERIENCE_RANGE[level_range][1]
        )
        print(f"Base experience: {experience:,}")
    if args.slow:
        print("Using slow advancement for demi-humans optional rule")
    if args.alignments:
        alignments = random.choice(load_table("alignment_groups.json"))
        print(f"Alignments: {', '.join(alignments)}")
    print()
    for adventurer in range(0, no_appearing):
        alignment = None
        if args.alignments:
            alignment = random.choice(alignments)
        this_xp = experience
        if this_xp:
            this_xp += random.randint(0, (EXPERIENCE_RANGE[level_range][0] / 10) + 100)
        print(
            random_adventurer(
                level_range,
                args.expanded,
                args.equipment,
                args.classes,
                alignment=alignment,
                experience=this_xp,
                slow_advancement=args.slow,
            )
        )
        print()


if __name__ == "__main__":
    main()
