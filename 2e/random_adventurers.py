#!/usr/bin/env python3

import argparse
import random

import items
import magic_item

from character import Character
from dice import roll
from roll_abilities import get_abilities
from utils import intersect
from utils import load_table

LEVEL_RANGE = {
    "Low": (1, 3, 0),
    "Medium": (1, 4, 3),
    "High": (1, 6, 6),
    "Very high": (1, 12, 8),
}

EXPERIENCE_RANGE = {
    "Low": [0, 4000],
    "Medium": [10000, 58900],
    "High": [75000, 652600],
    "Very high": [300000, 6000000],
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
    level_range, expanded, more_equipment, more_classes, alignment=None, experience=None
):
    mig = magic_item.MagicItemGen(expanded)
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
        )
    class_groups = adventurer.class_groups
    for category in get_magic_item_categories(adventurer.class_groups):
        if roll(1, 100, 0) <= level * 5:

            def gen_item():
                item = None
                if more_equipment:
                    if category == "Armor No Shields" and not intersect(
                        classes,
                        [
                            "Fighter",
                            "Paladin",
                        ],
                    ):
                        armor = items.random_armor(
                            expanded=expanded, classes=classes, level=level
                        )
                        item = mig.armor(force_armor=armor)
                    elif (
                        (category == "Sword" or category == "Nonsword")
                        and "Bard" not in classes
                        and "Warrior" not in adventurer.class_groups
                    ):
                        weapon = items.random_weapon(
                            expanded=expanded,
                            classes=classes,
                            class_groups=class_groups,
                            level=level,
                        )
                        if items.random_item_count(weapon):
                            dice, die, mod = items.random_item_count(weapon)
                            weapon = f"{weapon} ({dice}d{die})"
                        item = mig.weapon(force_weapon=weapon)
                    else:
                        item = mig.roll_category(category)
                else:
                    item = mig.roll_category(category)
                return item

            item = gen_item()
            # One reroll on cursed items
            if items.is_cursed(item):
                item = gen_item()

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
                items.random_armor(expanded=expanded, classes=classes, level=level)
            )

        if (
            level > 1
            and not has_shield
            and intersect(classes, ["Cleric", "Fighter", "Paladin"])
        ):
            adventurer.add_equipment(items.random_shield())

        # Everyone should have at least one weapon.
        if not has_weapon:
            weapon_filter = None
            if has_ranged_weapon:
                weapon_filter = items.is_melee_weapon
            weapon = items.random_weapon(
                expanded=expanded,
                classes=classes,
                class_groups=class_groups,
                weapon_filter=weapon_filter,
            )

            # If the weapon requires ammo, give some ammo for it
            ammo = items.appropriate_ammo_type(weapon)
            if ammo:
                try:
                    ammo_dice, ammo_die, ammo_mod = items.random_item_count(ammo)
                except:
                    breakpoint()
                ammo_dice *= 2
                ammo = f"{ammo} x{roll(ammo_dice, ammo_die, ammo_mod)}"
                adventurer.add_equipment(weapon)
                adventurer.add_equipment(ammo)
                has_ranged_weapon = True
                weapon = items.random_weapon(
                    expanded=expanded,
                    classes=classes,
                    class_groups=class_groups,
                    weapon_filter=items.is_melee_weapon,
                )
            # If the weapon is thrown, give a few of them
            elif items.is_thrown_weapon(weapon):
                try:
                    ammo_dice, ammo_die, ammo_mod = items.random_item_count(weapon)
                except:
                    breakpoint()
                count = roll(ammo_dice, ammo_die, ammo_mod)
                if count > 1:
                    adventurer.add_equipment(f"{weapon} x{count}")
                else:
                    adventurer.add_equipment(weapon)
                has_ranged_weapon = True
                weapon = items.random_weapon(
                    expanded=expanded,
                    classes=classes,
                    class_groups=class_groups,
                    weapon_filter=items.is_melee_weapon,
                )

            adventurer.add_equipment(weapon)
            has_weapon = True

        # Rangers love to dual-wield
        if "Ranger" in classes and level > 1:
            adventurer.add_equipment(
                items.random_weapon(
                    expanded=expanded,
                    table="weapons_warrior.json",
                    weapon_filter=items.is_melee_weapon,
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
    level_range = random.choice(list(LEVEL_RANGE.keys()))
    experience = None
    alignments = None

    print(f"{level_range} level Adventurer Party ({no_appearing} adventurers)")
    if args.experience:
        experience = random.randint(
            EXPERIENCE_RANGE[level_range][0], EXPERIENCE_RANGE[level_range][1]
        )
        print(f"Base experience: {experience:,}")
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
            )
        )
        print()


if __name__ == "__main__":
    main()
