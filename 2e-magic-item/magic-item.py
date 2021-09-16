#!/usr/bin/env python3

import json
import random


def roll(dice, sides, mod):
    total = mod
    for die in range(0, dice):
        total += random.randint(1, sides)
    return total


def roll_table(table, mod=0):
    max_roll = sorted([int(x) for x in table.keys()])[-1]
    result = roll(1, max_roll, mod)
    for value in sorted([int(x) for x in table.keys()]):
        if value >= result:
            return (table[str(value)], result)


def load_table(fname):
    return json.load(open(fname))


def load_and_roll(fname):
    return roll_table(load_table(fname))


def potions_and_oils():
    result = roll(1, 6, 0)
    if result < 3:
        return load_and_roll("potions_oils_a.json")
    if result < 5:
        return load_and_roll("potions_oils_b.json")
    else:
        return load_and_roll("potions_oils_c.json")


def weapon():
    result = roll(1, 6, 0)
    base_weapon = None
    adjustment = None
    if result < 3:
        base_weapon = load_and_roll("weapon_type_a.json")
    else:
        base_weapon = load_and_roll("weapon_type_b.json")
    if base_weapon[0] == "Special":
        return ("Special", None)
    elif base_weapon[0] == "Sword" or base_weapon[0] == "Scimitar":
        adjustment = load_and_roll("sword_adjustment.json")
    else:
        adjustment = load_and_roll("weapon_adjustment.json")
    return (f"{base_weapon[0]} {adjustment[0]}", (base_weapon[1], adjustment[1]))


def main():
    categories = load_table("categories.json")
    print(roll_table(categories))
    print(potions_and_oils())
    print(weapon())


if __name__ == "__main__":
    main()
