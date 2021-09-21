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
THROWN_WEAPONS = load_table("weapons_thrown.json")
WEAPONS = load_table("weapons_master_list.json")


def appropriate_ammo_type(weapon):
    try:
        return random.choice(WEAPONS[base_weapon(weapon)]["Ammo"])
    except KeyError:
        pass
    return None


def appropriate_armor_group(char_class, level=1):
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


def appropriate_weapon_category(char_class, class_group, level=1):
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
    adjustment = 0
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
    category_weapons = []
    for weapon in WEAPONS:
        if WEAPONS[weapon]["Category"] in [categories]:
            category_weapons.append(weapon)
    for weapon in category_weapons:
        if item.startswith(weapon):
            return True
    return False


def is_two_handed_melee(weapon):
    base = base_weapon(weapon)
    return WEAPONS[base]["Hands"] == 2 and WEAPONS[base]["Category"] == "Melee"


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
    except:
        pass
    return None

def random_shield():
    return random.choice(SHIELDS)


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
    # for _ in range(0, 10):
    #    print(random_weapon())
    print(appropriate_ammo_type("Light crossbow"))
    print(appropriate_weapons_by_ammo("Flight arrow"))
    print(base_weapon("Bastard sword +5"))
    print(random_item_count("Dart"))


if __name__ == "__main__":
    main()
