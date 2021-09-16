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

def potions_and_oils():
    result = roll(1, 6, 0)
    if result < 3:
        return roll_table(load_table("potions_oils_a.json"))
    if result < 5:
        return roll_table(load_table("potions_oils_b.json"))
    else:
        return roll_table(load_table("potions_oils_c.json"))

def main():
    categories = load_table("categories.json")
    print(roll_table(categories))
    print(potions_and_oils())


if __name__ == "__main__":
    main()
