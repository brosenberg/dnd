#!/usr/bin/env python3

import json
import re
import os


def load_table(fname):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    return json.load(open(f"{base_dir}/tables/{fname}"))


ARMOR_STATS = load_table("armor_stats.json")
SHIELDS = load_table("shields.json")

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
    bracers_of_defense = re.match(r'^Bracers of Defense \(AC ([0-9]+)\)$', armor)
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
    protection_items = ['Ring of Protection', 'Cloak of Protection']
    for protection_item in protection_items:
        if protection_item in item:
            _, adjustment = get_adjustment(item)
            return adjustment
    return None

def is_shield(item):
    for shield in SHIELDS:
        if item.startswith(shield):
            return True
    return False


def main():
    print(get_armor_ac("Hide armor +3"))
    print(get_armor_ac("Leather of Blending +1"))
    print(get_armor_ac("Plate mail -4"))
    print(get_armor_ac("Plate Mail of Etherealness"))


if __name__ == "__main__":
    main()