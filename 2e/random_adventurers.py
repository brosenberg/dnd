#!/usr/bin/env python3

import argparse
import random

import items

from character import Character
from currency import get_gold_value
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
        # Rogues are supposed to roll on Shields, but Rogues can't use shields.
        # So instead we give them armor, because they can actually use that.
        "Armor No Shields",
        "Sword",
        "Nonsword",
        "Potions and Oils",
        "Rings",
        "Misc Magic",
    ],
}

TREASURE = {
    "Warrior": "LM",
    "Wizard": "LNQ",
    "Priest": "JKM",
    "Rogue": "JNQ",
    "Elf": "N",
    "Dwarf": "MMMMM",
    "Gnome": "MMM",
    "Halfling": "K",
    "Half-Elf": "N",
    "Human": "K",
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
    level = roll(*LEVEL_RANGE[level_range])
    adventurer = None
    classes = []
    has_any_item = True
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
    items_kwargs = {
        "classes": classes,
        "sub_table": "expanded" if expanded else "standard",
        "extra_filters": {"Weapons": {}, "Armor": {}},
    }
    # Small races use small weapons
    if adventurer.race in ["Gnome", "Halfling"]:
        items_kwargs["extra_filters"]["Weapons"]["Small Race Usable"] = True
        items_kwargs["extra_filters"]["Armor"]["Small Race Usable"] = True

    # Generate magic items for the character, 5% chance per level in each
    # category for their class groups
    for category in get_magic_item_categories(adventurer.class_groups):
        if roll(1, 100, 0) <= level * 5:
            has_any_item = True
            # Give multiclass clerics something other than a sword
            if category == "Sword" and "Cleric" in classes:
                category = "Rod/Staff/Wand"

            item = items.random_magic_item(**items_kwargs, category=category)
            # One reroll on cursed items
            if items.is_cursed(item):
                item = items.random_magic_item(**items_kwargs, category=category)

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

    # High level priests sometimes carry religious artifacts
    if "Priest" in adventurer.class_groups and roll(1, 100, 0) <= 5:
        adventurer.add_equipment("Religious artifact")

    # Give random currency to adventurers who received an item
    # Adventurers who have zero magic items are probably not established
    # enough to have more than their starting funds.
    if has_any_item:
        for class_group in adventurer.class_groups:
            adventurer.give_treasure(TREASURE[class_group])
        if adventurer.race in TREASURE:
            adventurer.give_treasure(TREASURE[adventurer.race])

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
        # Check to see if the adventurer has random ammo and give them a weapon
        # suitable for it, or give ammo for a weapon that needs it.
        for item in adventurer.equipment:
            # Give a weapon for orphan ammo
            weapons = items.appropriate_weapons_by_ammo(item)
            if weapons:
                adventurer.add_equipment(
                    items.random_item(
                        **items_kwargs, category=category, item_list=weapons
                    )
                )
            # Give ammo for weapons needing it
            try:
                ammo, count = items.random_appropriate_ammo(item)
                count *= 2
                adventurer.add_equipment((f"{ammo} x{count}"))
            except TypeError:
                pass

        # Maybe give the adventurer a mount
        mount_chance = 20
        # Elves typically don't ride, so a smaller chance for them
        if adventurer.race == "Elf":
            mount_chance = 2
        if roll(1, 100, 0) < mount_chance * level:
            if level > 2 and ("Warrior" in class_groups or "Cleric" in classes):
                horse_roll = roll(1, 100, 0)
                if horse_roll < roll(1, 12, 0) * level:
                    adventurer.add_equipment("Heavy warhorse")
                elif horse_roll < 15 * level:
                    adventurer.add_equipment("Medium warhorse")
                else:
                    adventurer.add_equipment("Light warhorse")
                if roll(1, 100, 0) < 10 * level:
                    barding = items.random_item(
                        **items_kwargs,
                        item_type="Armor",
                        filters={"Category": "Armor"},
                    )
                    adventurer.add_equipment(f"{barding} barding")
            else:
                adventurer.add_equipment("Riding horse")

        # Everyone should have at least one weapon.
        if not has_weapon:
            filters = {"Cost": get_gold_value(adventurer.currency)}
            if has_ranged_weapon:
                filters["Category"] = "Melee"
            weapon = items.random_item(
                **items_kwargs, item_type="Weapons", filters=filters
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
                    **items_kwargs, item_type="Weapons", filters={"Category": "Melee"}
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
                    **items_kwargs, item_type="Weapons", filters={"Category": "Melee"}
                )

            try:
                adventurer.buy_item(weapon, item_type="Weapons")
                has_weapon = True
            except IndexError:
                # poor lol
                pass

        # Everyone should have armor. Besides wizards.
        if not has_armor and "Wizard" not in class_groups:
            filters = {"Cost": get_gold_value(adventurer.currency), "Category": "Armor"}
            try:
                adventurer.buy_item(
                    items.random_item(
                        **items_kwargs, filters=filters, item_type="Armor"
                    ),
                    item_type="Armor",
                )
            except IndexError:
                # poor lol
                pass

        if not has_shield and intersect(classes, ["Cleric", "Fighter", "Paladin"]):
            filters = {
                "Cost": get_gold_value(adventurer.currency),
                "Category": "Shield",
            }
            try:
                adventurer.buy_item(
                    items.random_item(
                        **items_kwargs, item_type="Armor", filters=filters
                    ),
                    item_type="Armor",
                )
            except IndexError:
                # poor lol
                pass

        # Rangers love to dual-wield and gnomes carry a lot of weapons
        if "Ranger" in classes or adventurer.race == "Gnome":
            filters = {"Cost": get_gold_value(adventurer.currency), "Category": "Melee"}
            try:
                adventurer.buy_item(
                    items.random_item(
                        **items_kwargs, item_type="Weapons", filters=filters
                    ),
                    item_type="Weapons",
                )
            except IndexError:
                # poor lol
                pass

    return adventurer


def random_adventurers(**kwargs):
    s = ""
    no_appearing = roll(1, 8, 0)
    if kwargs.get("epic"):
        level_range = random.choice(LEVEL_RANGES + ["Epic"])
    else:
        level_range = random.choice(LEVEL_RANGES)
    experience = None
    alignments = None
    level_str = f"{LEVEL_RANGE[level_range][0]+LEVEL_RANGE[level_range][2]} - {LEVEL_RANGE[level_range][1]+LEVEL_RANGE[level_range][2]}"

    s += f"{level_range} level ({level_str}) Adventurer Party ({no_appearing} adventurers)\n"

    if kwargs.get("experience"):
        min_mod = 1
        if kwargs.get("slow"):
            min_mod = 2
        experience = random.randint(
            EXPERIENCE_RANGE[level_range][0] * min_mod, EXPERIENCE_RANGE[level_range][1]
        )
        s += f"Base experience: {experience:,}\n"
    if kwargs.get("slow"):
        s += "Using slow advancement for demi-humans optional rule\n"
    if kwargs.get("alignment"):
        alignments = random.choice(load_table("alignment_groups.json"))
        s += f"Alignments: {', '.join(alignments)}\n"
    s += "\n"
    for adventurer in range(0, no_appearing):
        alignment = None
        if kwargs.get("alignment"):
            alignment = random.choice(alignments)
        this_xp = experience
        if this_xp:
            this_xp += random.randint(0, (EXPERIENCE_RANGE[level_range][0] / 10) + 100)
        s += str(
            random_adventurer(
                level_range,
                kwargs.get("expanded", False),
                kwargs.get("equipment", False),
                kwargs.get("classes", False),
                alignment=alignment,
                experience=this_xp,
                slow_advancement=kwargs.get("slow", False),
            )
        )
        s += "\n\n"
    return s.strip()


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
    print(
        random_adventurers(
            alignment=args.alignments,
            classes=args.classes,
            epic=args.epic,
            equipment=args.equipment,
            expanded=args.expanded,
            experience=args.experience,
            slow=args.slow,
        )
    )


if __name__ == "__main__":
    main()
