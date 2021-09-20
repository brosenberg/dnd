#!/usr/bin/env python3

import json
import random
import re
import os

from magic_item import MagicItemGen
from utils import load_table


ARMOR_STATS = load_table("armor_stats.json")
SHIELDS = load_table("shields.json")
THROWN_WEAPONS = load_table("weapons_thrown.json")


def appropriate_ammo_type(weapon):
    if weapon.startswith("Blowgun"):
        return random.choice(["Barbed dart", "Needle"])
    elif "crossbow" in weapon or weapon.startswith("Cho-ku-no"):
        if "Hand " in weapon:
            return "Hand quarrel"
        elif "Heavy " in weapon:
            return "Heavy bolt"
        return "Light bolt"
    elif " bow" in weapon:
        if "long" in weapon.lower():
            return "Sheaf arrow"
        else:
            return "Flight arrow"
    elif weapon.startswith("Daikyu"):
        return "Daikyu arrow"
    elif "sling" in weapon.lower():
        return "Sling bullet"


def appropriate_armor(char_class, level=1):
    if char_class == "Druid":
        return "Druid"
    elif char_class in ["Thief", "Ranger"]:
        return "Rogue"
    elif char_class == "Bard":
        if level > 2:
            return "Bard"
        else:
            return "Rogue"
    elif char_class in ["Fighter", "Cleric", "Paladin"]:
        if level > 3:
            return "High"
    return None


def appropriate_weapon(char_class, class_group, level=1):
    if char_class == "Cleric":
        return "Cleric"
    elif char_class == "Druid":
        return "Druid"
    elif char_class == "Rogue":
        return "Rogue"
    elif class_group == "Warrior" and level > 1:
        return "Warrior"
    elif class_group == "Wizard":
        return "Wizard"
    return None


def get_ac(item):
    ac = get_armor_ac(item)
    if ac:
        return (ac, None)
    ac = get_shield_ac_bonus(item)
    if ac:
        return (None, ac)
    return (None, get_other_ac_bonus(item))


def get_adjustment(item):
    magic = re.match(r"^(.+?) ([+-][0-9]+)(, .+?)?$", item)
    adjustment = 0
    if magic:
        return (magic.group(1), int(magic.group(2)))
    return (item, 0)


def get_armor_ac(armor):
    remove_list = [" of Blending", " of Missile Attraction"]
    for remove in remove_list:
        armor = armor.replace(remove, "")
    bracers_of_defense = re.match(r"^Bracers of Defense \(AC ([0-9]+)\)$", armor)
    if bracers_of_defense:
        return int(bracers_of_defense.group(1))
    armor, adjustment = get_adjustment(armor)
    armor = armor.title()
    try:
        return ARMOR_STATS[armor]["AC"] - adjustment
    except KeyError:
        pass


def get_shield_ac_bonus(shield):
    if is_shield(shield):
        _, adjustment = get_adjustment(shield)
        return 1 + adjustment
    return None


def get_other_ac_bonus(item):
    protection_items = ["Ring of Protection", "Cloak of Protection"]
    for protection_item in protection_items:
        if protection_item in item:
            _, adjustment = get_adjustment(item)
            return adjustment
    return None


def is_crossbow_ammo(item):
    return (
        "Bolt" in item
        or "Heavy bolt" in item
        or "Light bolt" in item
        or "quarrel" in item.lower()
    )


def is_cursed(item):
    return (
        re.search(r"-[0-9]+", item)
        or "ursed" in item
        or "Clumsiness" in item
        or "Contrariness" in item
        or "Delusion" in item
    )


def is_ranged_weapon(item):
    return (
        appropriate_ammo_type(item)
        or item in THROWN_WEAPONS
        or "arrow" in item.lower()
        or is_crossbow_ammo(item)
        or is_sling_ammo(item)
    )


def is_sling_ammo(item):
    return "sling bullet" in item.lower() or "sling stone" in item.lower()


def is_shield(item):
    for shield in SHIELDS:
        if item.startswith(shield):
            return True
    return False


def random_armor(expanded=False, specific=None):
    armor = None
    if not specific:
        armors = load_table("armor_low.json")
    elif specific == "High":
        armors = load_table("armor_high.json")
    elif specific == "Druid":
        armors = load_table("armor_druid.json")
    elif specific == "Rogue":
        armors = load_table("armor_rogue.json")
    elif specific == "Bard":
        armors = load_table("armor_bard.json")
    return random.choice(armors)


def random_shield():
    return random.choice(SHIELDS)


def random_item_count(item):
    if item in THROWN_WEAPONS:
        if item in ["Dart", "Shuriken"]:
            return (3, 4, 0)
        else:
            return (1, 2, 0)
    elif "arrow" in item.lower():
        return (random.randint(2, 4), 6, 0)
    elif is_crossbow_ammo(item):
        return (2, random.choice([6, 10]), 0)
    elif is_sling_ammo(item):
        return (3, 4, 0)
    elif item.startswith("Barbed dart") or item.startswith("Needle"):
        return (3, 4, 0)
    return None


def random_weapon(expanded=False, specific=None):
    mig = MagicItemGen(expanded)
    weapon = None
    if not specific:
        weapons = load_table("weapons_generic.json")
    elif specific == "Cleric":
        weapons = load_table("weapons_cleric.json")
    elif specific == "Druid":
        weapons = load_table("weapons_druid.json")
    elif specific == "Rogue":
        weapons = load_table("weapons_rogue.json")
    elif specific == "Warrior":
        weapons = load_table("weapons_warrior.json")
    elif specific == "Wizard":
        weapons = load_table("weapons_wizard.json")
    weapon = random.choice(weapons)
    return mig.diversify_weapon(weapon)


def main():
    # print(get_armor_ac("Hide armor +3"))
    # print(get_armor_ac("Leather of Blending +1"))
    # print(get_armor_ac("Plate mail -4"))
    # print(get_armor_ac("Plate Mail of Etherealness"))
    for _ in range(0, 10):
        print(random_weapon())


if __name__ == "__main__":
    main()
