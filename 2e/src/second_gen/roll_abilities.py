#!/usr/bin/env python3

import random

from second_gen.dice import roll


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


def roll_array_order(order):
    return sorted([roll(x, 6, 0, drop=x - 3) for x in order], reverse=True)[:6]


def get_abilities(
    priority, minimums, maximums, modifiers, order=[4, 4, 4, 4, 4, 4], extrao_str=False
):
    array = roll_array_order(order)
    abilities = {x: 0 for x in ABILITIES}
    for ability in priority:
        abilities[ability] = array.pop(0)
    remaining = [x for x in abilities if abilities[x] == 0]
    random.shuffle(remaining)
    for ability in remaining:
        abilities[ability] = array.pop(0)
    for ability in modifiers:
        abilities[ability] += modifiers[ability]
    for ability in minimums:
        if abilities[ability] < minimums[ability]:
            abilities[ability] = minimums[ability]
    for ability in maximums:
        if abilities[ability] > maximums[ability]:
            abilities[ability] = maximums[ability]
    if extrao_str and abilities["Strength"] == 18:
        abilities["Extrao Strength"] = roll(1, 100, 0)
    else:
        abilities["Extrao Strength"] = None
    return abilities


def main():
    priority = ["Strength", "Constitution", "Dexterity"]
    minimums = {"Charisma": 16}
    print(get_abilities(priority, minimums, extrao_str=True))


if __name__ == "__main__":
    main()
