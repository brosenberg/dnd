#!/usr/bin/env python3

import random

from dice import roll


ABILITIES = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Wisdom",
    "Intelligence",
    "Charisma",
]


def roll_array(tries, rolls):
    return sorted(
        [roll(rolls, 6, 0, drop=rolls - 3) for x in range(0, tries)], reverse=True
    )[:6]


def get_abilities(priority, minimums, tries=7, rolls=4, extrao_str=False):
    array = roll_array(tries, rolls)
    abilities = {x: 0 for x in ABILITIES}
    for ability in priority:
        abilities[ability] = array.pop(0)
    remaining = [x for x in abilities if abilities[x] == 0]
    random.shuffle(remaining)
    for ability in remaining:
        abilities[ability] = array.pop(0)
    for ability in minimums:
        if abilities[ability] < minimums[ability]:
            abilities[ability] = minimums[ability]
    for ability in abilities:
        abilities[ability] = str(abilities[ability])
    if extrao_str and abilities["Strength"] == "18":
        abilities["Strength"] = f"18/{roll(1, 100, 0)}"
    return abilities
    

def main():
    priority = ["Strength", "Constitution", "Dexterity"]
    minimums = {"Charisma": 16}
    print(get_abilities(priority, minimums, extrao_str=True))

if __name__ == "__main__":
    main()
