#!/usr/bin/env python3

import json
import random
import re
import os

from dice import roll
from magic_item import MagicItemGen
from utils import load_table


AMMOS = load_table("weapons_ammos.json")
ARMOR_STATS = load_table("armor_stats.json")
SHIELDS = load_table("shields.json")
SPECIAL_MAGIC_WEAPONS = load_table("weapons_magic_special.json")
THROWN_WEAPONS = load_table("weapons_thrown.json")
WEAPONS = load_table("weapons_master_list.json")


def appropriate_ammo_type(weapon):
    try:
        return random.choice(WEAPONS[base_weapon(weapon)]["Ammo"])
    except KeyError:
        pass
    return None


def appropriate_armor_group(char_class):
    if char_class == "Druid":
        return "druid"
    if char_class in ["Thief", "Ranger"]:
        return "rogue"
    if char_class == "Bard":
        return "bard"
    if char_class in ["Fighter", "Cleric", "Paladin"]:
        return "warrior"
    return "none"


def appropriate_weapons_by_ammo(ammo):
    def in_ammo(item, ammo_list):
        for ammo_type in ammo_list:
            if ammo_type in item:
                return True
        return False

    weapons = []
    for weapon in WEAPONS:
        try:
            if in_ammo(ammo, WEAPONS[weapon]["Ammo"]):
                weapons.append(weapon)
        except KeyError:
            pass
    return weapons


def base_weapon(item):
    candidates = []
    for weapon in WEAPONS:
        if item.startswith(weapon):
            candidates.append(weapon)
    if candidates:
        return sorted(candidates, key=len)[-1]
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
    if magic:
        return (magic.group(1), int(magic.group(2)))
    return (item, 0)


def get_armor_ac(armor):
    if armor == "Bracers of Defenselessness":
        return 10
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


def is_cursed(item):
    return (
        re.search(r"-[0-9]+", item)
        or "ursed" in item
        or "Clumsiness" in item
        or "Contrariness" in item
        or "Delusion" in item
        or "Defenselessness" in item
        or "Stammering" in item
        or "Jewel of Attacks" in item
    )


def is_melee_weapon(item):
    return is_weapon_in_categories(item, ["Melee"])


def is_missile_weapon(item):
    return is_weapon_in_categories(item, ["Ammo", "Ranged", "Thrown"])


def is_thrown_weapon(item):
    return is_weapon_in_categories(item, ["Thrown"])


def is_shield(item):
    for shield in SHIELDS:
        if item.startswith(shield):
            return True
    return False


def is_weapon_in_categories(item, categories):
    base = base_weapon(item)
    for weapon in WEAPONS:
        if WEAPONS[weapon]["Category"] in categories and base == weapon:
            return True
    return False


def is_two_handed_melee(weapon):
    base = base_weapon(weapon)
    return WEAPONS[base]["Hands"] == 2 and WEAPONS[base]["Category"] == "Melee"


def random_armor(expanded=False, table=None, classes=[], level=1):
    armors = []
    if table:
        armors = load_table(table)
    else:
        armor_groups = list(set([appropriate_armor_group(x) for x in classes]))
        if len(armor_groups) == 1:
            armor_group = armor_groups[0]
            if armor_group == "warrior":
                if level > 3:
                    armors = load_table("armor_high.json")
                else:
                    armors = load_table("armor_low.json")
            elif armor_group == "bard":
                if level > 2:
                    armors = load_table("armor_bard.json")
                else:
                    armors = load_table("armor_rogue.json")
            else:
                table = f"armor_{appropriate_armor_group(armor_group)}.json"
                armors = load_table(table)
        else:
            table = f"armor_{appropriate_armor_group(classes[0])}.json"
            armors = set(load_table(table))
            for class_name in classes[1:]:
                table = f"armor_{appropriate_armor_group(class_name)}.json"
                armors = armors.intersection(set(load_table(table)))
            armors = list(armors)
    try:
        return random.choice(armors)
    except IndexError:
        return None


def random_appropriate_ammo(weapon):
    try:
        ammo = appropriate_ammo_type(weapon)
        dice, die, mod = random_item_count(ammo)
        count = roll(dice, die, mod)
        return (ammo, count)
    except TypeError:
        return None


def random_item_count(item):
    try:
        return WEAPONS[base_weapon(item)]["Quantity"]
    # FIXME
    except:
        pass
    return None


def random_shield():
    return random.choice(SHIELDS)


def random_special_magic_weapon():
    special = random.choice(SPECIAL_MAGIC_WEAPON)
    try:
        base_item = SPECIAL_MAGIC_WEAPON[special]
    except KeyError:


def random_weapon(
    expanded=False, classes=[], class_groups=[], table=None, weapon_filter=None, level=1
):
    mig = MagicItemGen(expanded)
    weapon = None
    if table:
        weapons = load_table(table)
    else:
        if "Cleric" in classes:
            weapons = load_table("weapons_cleric.json")
        elif "Druid" in classes:
            weapons = load_table("weapons_druid.json")
        elif "Warrior" in class_groups or "Bard" in classes:
            if level > 1:
                weapons = load_table("weapons_warrior.json")
            else:
                weapons = load_table("weapons_generic.json")
        elif "Rogue" in classes:
            weapons = load_table("weapons_rogue.json")
        else:
            weapons = load_table("weapons_wizard.json")
    if weapon_filter:
        weapons = [x for x in weapons if weapon_filter(x)]
    return mig.diversify_weapon(random.choice(weapons))


def main():
    # print(get_armor_ac("Hide armor +3"))
    # print(get_armor_ac("Leather of Blending +1"))
    # print(get_armor_ac("Plate mail -4"))
    # print(get_armor_ac("Plate Mail of Etherealness"))
    # for _ in range(0, 10):
    #    print(random_weapon())
    print(appropriate_ammo_type("Light crossbow"))
    print(appropriate_weapons_by_ammo("Flight arrow"))
    print(base_weapon("Bastard sword +5"))
    print(random_item_count("Dart"))


if __name__ == "__main__":
    main()
