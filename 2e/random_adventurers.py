#!/usr/bin/env python3

import argparse
import random

import items
import magic_item

from character import Character
from dice import roll
from roll_abilities import get_abilities
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
    char_class = None
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
        )
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
        adventurer = Character(
            char_class=char_class,
            level=level,
            alignment=alignment,
            experience=experience,
        )
    for category in MAGIC_ITEMS[adventurer.class_group]:
        if roll(1, 100, 0) <= level * 5:

            def gen_item():
                item = None
                if more_equipment:
                    if category == "Armor No Shields" and char_class not in [
                        "Fighter",
                        "Paladin",
                    ]:
                        armor_type = items.appropriate_armor_group(
                            char_class, level=level
                        )
                        armor = items.random_armor(
                            expanded=expanded, specific=armor_type
                        )
                        item = mig.armor(force_armor=armor)
                    elif (
                        (category == "Sword" or category == "Nonsword")
                        and char_class != "Bard"
                        and adventurer.class_group != "Warrior"
                    ):
                        weapon_type = items.appropriate_weapon_category(
                            char_class, adventurer.class_group, level=level
                        )
                        weapon = items.random_weapon(
                            expanded=expanded, specific=weapon_type
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
        if level > 7 and char_class in ["Cleric", "Fighter", "Paladin"]:
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
            armor_type = items.appropriate_armor_group(char_class, level=level)
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
            weapon_type = items.appropriate_weapon_category(
                char_class, adventurer.class_group, level=level
            )
            weapon = items.random_weapon(expanded=expanded, specific=weapon_type)
            if has_ranged_weapon:
                while items.is_missile_weapon(weapon):
                    weapon = items.random_weapon(
                        expanded=expanded, specific=weapon_type
                    )
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
                while items.is_missile_weapon(weapon):
                    weapon = items.random_weapon(
                        expanded=expanded, specific=weapon_type
                    )
            elif items.is_thrown_weapon(weapon):
                try:
                    ammo_dice, ammo_die, ammo_mod = items.random_item_count(weapon)
                except:
                    breakpoint()
                ammo_die *= 2
                ammo_dice += 1
                count = roll(ammo_dice, ammo_die, ammo_mod)
                adventurer.add_equipment(f"{weapon} x{count}")
                while items.is_missile_weapon(weapon):
                    weapon = items.random_weapon(
                        expanded=expanded, specific=weapon_type
                    )

            adventurer.add_equipment(weapon)

        # Rangers love to dual-wield
        if char_class == "Ranger" and level > 1:
            weapon = items.random_weapon(expanded=expanded, specific="Warrior")
            while items.is_missile_weapon(weapon):
                weapon = items.random_weapon(expanded=expanded)
            adventurer.add_equipment(weapon)

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
        help="use expanded item generation tables",
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
