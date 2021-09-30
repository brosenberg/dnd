#!/usr/bin/env python3

import random
import sys

from dice import roll
from simple_gen import gen
from utils import load_table

GEMS = load_table("gems.json")


def gem_variant(gem_type):
    value = GEMS[gem_type]["Base Value"]
    result = roll(1, 6, 0)
    count = 0
    if result == 2:
        value *= 2
    elif result == 3:
        value = int(value * (1 + (roll(10, 6, 0) * 0.01)))
    elif result == 4:
        value = int(value * (1 + (roll(10, 4, 0) * 0.01)))
    elif result == 5:
        value = int(value / 2)
    while result == 1:
        if result == 1:
            if GEMS["Gem Order"].index(gem_type) < len(GEMS["Gem Order"]) - 1:
                gem_type = GEMS["Gem Order"][GEMS["Gem Order"].index(gem_type) + 1]
                value = GEMS[gem_type]["Base Value"]
            else:
                value *= 2
                if value > 100000:
                    return 100000
        result = roll(1, 6, 0)
    while result == 6 and count < 5:
        count += 1
        if result == 6:
            if GEMS["Gem Order"].index(gem_type) > 0:
                gem_type = GEMS["Gem Order"][GEMS["Gem Order"].index(gem_type) - 1]
                value = GEMS[gem_type]["Base Value"]
            else:
                if value > 5:
                    value = 5
                elif value > 1:
                    value = 1
                elif value > 0.5:
                    value = 0.5
                else:
                    return 0.1
        result = roll(1, 6, 0)
    return value


def generate_gem():
    gem_type = gen(**GEMS["Gem Type"])
    value = GEMS[gem_type]["Base Value"]
    stone = random.choice(GEMS[gem_type]["Stones"])
    if roll(1, 100, 0) <= 10:
        value = gem_variant(gem_type)
    return [stone, value]


def generate_gems(count):
    gems = {}
    for _ in range(0, count):
        stone, value = generate_gem()
        if value not in gems:
            gems[value] = [stone]
        else:
            gems[value].append(stone)
    return gems


def format_gems(gems):
    s = ""
    total = 0
    for value in sorted(gems):
        total += value * len(gems[value])
        for gem in set(gems[value]):
            s += f"{gem} ({value} gp)"
            if gems[value].count(gem) > 1:
                s += f" x{gems[value].count(gem)}"
            s += "\n"
    s += f"{total} gp total"
    return s


def main():
    try:
        print(format_gems(generate_gems(int(sys.argv[1]))))
    except IndexError:
        print(f"Usage: {sys.argv[0]} [number of gems]")
        sys.exit(1)


if __name__ == "__main__":
    main()
