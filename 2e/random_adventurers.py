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


def random_adventurer(level_range, expanded, more_equipment, more_classes):
    mig = magic_item.MagicItemGen(expanded)
    level = roll(
        LEVEL_RANGE[level_range][0],
        LEVEL_RANGE[level_range][1],
        LEVEL_RANGE[level_range][2],
    )
    adventurer = None
    if more_classes:
        # If char_class is None, a class is randomly chosen
        class_group = random.choice(["Warrior", "Wizard", "Priest", "Rogue"])
        adventurer = Character(class_group=class_group, level=level)
        char_class = adventurer.char_class
    else:
        class_roll = roll(1, 10, 0)
        char_class = "Fighter"
        if class_roll > 8:
            char_class = "Mage"
        elif class_roll > 6:
            char_class = "Thief"
        elif class_roll > 4:
            char_class = "Cleric"
        adventurer = Character(char_class=char_class, level=level)
    has_weapon = False
    has_armor = False
    has_shield = False
    for category in MAGIC_ITEMS[adventurer.class_group]:
        if roll(1, 100, 0) <= level * 5:
            if category == "Armor No Shields":
                has_armor = True
            elif category in ["Nonsword", "Sword", "Rod/Staff/Wand"]:
                has_weapon = True
            elif category == "Shields":
                has_shield = True
            item = mig.roll_category(category)
            if items.is_ranged_weapon(item):
                has_weapon = False
            # One reroll on cursed items
            if item.endswith("-1") or "ursed" in item or "Clumsiness" in item or "Contrariness" in item:
                item = mig.roll_category(category)
            adventurer.add_equipment(item)

    if not more_equipment:
        if level > 7 and char_class in ["Cleric", "Fighter", "Paladin"]:
            if not has_armor:
                adventurer.add_equipment("Plate mail")
                has_armor = True
            if not has_shield:
                adventurer.add_equipment("Medium shield")
                has_shield = True
            adventurer.add_equipment("Medium warhorse")
    else:
        # Maybe give the adventurer a mount
        if roll(1, 100, 0) < 20 * level:
            if level > 2 and (
                adventurer.class_group == "Warrior" or char_class == "Cleric"
            ):
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
                        barding = items.random_armor(expanded=expanded)
                    else:
                        barding = items.random_armor(expanded=expanded, specific="High")
                    adventurer.add_equipment(f"{barding} barding")
            else:
                adventurer.add_equipment("Riding horse")

        # Everyone should have armor. Besides wizards.
        if not has_armor and adventurer.class_group != "Wizard":
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

        # Everyone should have at least one weapon.
        if not has_weapon:
            weapon_type = None
            if char_class == "Cleric":
                weapon_type = "Cleric"
            elif char_class == "Druid":
                weapon_type = "Druid"
            elif char_class == "Rogue":
                weapon_type = "Rogue"
            elif adventurer.class_group == "Warrior" and level > 1:
                weapon_type = "Warrior"
            elif adventurer.class_group == "Wizard":
                weapon_type = "Wizard"
            weapon = items.random_weapon(expanded=expanded, specific=weapon_type)
            thrown_weapons = items.load_table("weapons_thrown.json")
            ammo = items.appropriate_ammo_type(weapon)
            if ammo:
                ammo_dice, ammo_die, ammo_mod = items.random_item_count(ammo)
                ammo_dice *= 2
                ammo = f"{ammo} x{roll(ammo_dice, ammo_die, ammo_mod)}"
                adventurer.add_equipment(weapon)
                adventurer.add_equipment(ammo)
                while items.is_ranged_weapon(weapon):
                    weapon = items.random_weapon(
                        expanded=expanded, specific=weapon_type
                    )
            elif weapon in thrown_weapons:
                ammo_dice, ammo_die, ammo_mod = items.random_item_count(weapon)
                ammo_die *= 2
                ammo_dice += 1
                adventurer.add_equipment(f"{weapon} x{roll(ammo_dice, ammo_die, ammo_mod)}")
                while items.is_ranged_weapon(weapon):
                    weapon = items.random_weapon(
                        expanded=expanded, specific=weapon_type
                    )

            adventurer.add_equipment(weapon)

        # Rangers love to dual-wield
        if char_class == "Ranger" and level > 1:
            weapon = items.random_weapon(expanded=expanded, specific="Warrior")
            while items.is_ranged_weapon(weapon):
                weapon = items.random_weapon(expanded=expanded)
            adventurer.add_equipment(weapon)

    return adventurer


def main():
    parser = argparse.ArgumentParser(description="Generate adventurers")
    parser.add_argument(
        "-c",
        "--classes",
        default=False,
        action="store_true",
        help="generate more classes",
    )
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
        print(
            random_adventurer(level_range, args.expanded, args.equipment, args.classes)
        )
        print()


if __name__ == "__main__":
    main()
