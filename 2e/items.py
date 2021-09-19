#!/usr/bin/env python3

import json
import re
import os


def load_table(fname):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    return json.load(open(f"{base_dir}/tables/{fname}"))


ARMOR_STATS = load_table("armor_stats.json")
SHIELDS = load_table("shields.json")


def get_armor_ac(armor):
    remove_list = [" of Blending", " of Missile Attraction"]
    for remove in remove_list:
        armor = armor.replace(remove, "")
    magic = re.match(r"^(.+?) ([+-][0-9]+)(, .+?)?$", armor)
    adjustment = 0
    if magic:
        armor = magic.group(1)
        adjustment = int(magic.group(2))
    armor = armor.title()
    try:
        return ARMOR_STATS[armor]["AC"] - adjustment
    except KeyError:
        pass


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
