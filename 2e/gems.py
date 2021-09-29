#!/usr/bin/env python3

import random
import sys

VALUES = (10, 50, 100, 500, 1000, 5000)
GEM_TYPES = [
    [
        "azurite",
        "banded agate",
        "blue quartz",
        "cats' eye agate",
        "eye agate",
        "hematite",
        "lapis lazuli",
        "malachite",
        "moss agate",
        "obsidian",
        "rhodochrosite",
        "tiger eye agate",
        "turquoise",
    ],
    [
        "bloodstone",
        "carnelian",
        "chalcedony",
        "chrysoprase",
        "citrine",
        "jasper",
        "moonstone",
        "onyx",
        "rock crystal",
        "sardonyx",
        "smoky quartz",
        "star rose quartz",
        "zircon",
    ],
    [
        "amber",
        "alexandrite",
        "amethyst",
        "chrysoberyl",
        "coral",
        "green spinel",
        "jade",
        "jet",
        "pearl",
        "red garnet",
        "red spinel",
        "tourmaline",
    ],
    [
        "aquamarine",
        "black pearl",
        "blue spinel",
        "peridot",
        "topaz",
        "violet garnet",
    ],
    [
        "black opal",
        "fire opal",
        "opal",
        "sapphire",
    ],
    [
        "black sapphire",
        "diamond",
        "emerald",
        "jacinth",
        "ruby",
        "star ruby",
        "star sapphire",
    ],
]


def get_gem():
    roll = random.randint(1, 100)
    if roll == 100:
        return 5
    elif roll >= 91:
        return 4
    elif roll >= 71:
        return 3
    elif roll >= 51:
        return 2
    elif roll >= 26:
        return 1
    else:
        return 0


def gem_variant(base):
    value = VALUES[base]
    roll = random.randint(1, 6)
    count = 0
    if roll == 2:
        value *= 2
    elif roll == 3:
        value = int(value * (1 + (random.randint(1, 6) * 0.1)))
    elif roll == 4:
        value = int(value * (1 + (random.randint(1, 4) * 0.1)))
    elif roll == 5:
        value = int(value / 2)
    while roll == 1:
        if roll == 1:
            if base < 6:
                base += 1
                try:
                    value = VALUES[base]
                except IndexError:
                    base = len(VALUES)
                    value = VALUES[-1]
            else:
                value *= 2
                if value > 100000:
                    return 100000
        roll = random.randint(1, 6)
    while roll == 6 and count < 5:
        count += 1
        if roll == 6:
            if base > 0:
                base -= 1
                value = VALUES[base]
            else:
                if value == 10 or value == 1:
                    value /= 2.0
                elif value == 5:
                    value = 1
                else:
                    return 0.1
        roll = random.randint(1, 6)
    return value


def generate_gems(count):
    gems = [0, 0, 0, 0, 0, 0]
    variant_count = 0
    total = 0
    if count >= 10:
        variant_count = int(count / 10)
        count = count - variant_count
    for i in range(0, count):
        gems[get_gem()] += 1
    for i in range(0, 6):
        if gems[i]:
            print(f"{gems[i]} {VALUES[i]} gp {random.choice(GEM_TYPES[i])}")
            total += gems[i] * VALUES[i]
    if variant_count:
        base = get_gem()
        value = gem_variant(base)
        total += value * variant_count
        coin = "gp"
        if value < 1:
            value *= 10
            coin = "sp"
        value = int(value)
        print(f"{variant_count} {value} {coin} {random.choice(GEM_TYPES[base])}")

    print(f"{total} gp total")


def main():
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
        generate_gems(count)
    else:
        print(f"Usage: {sys.argv[0]} [number of gems]")
        sys.exit(1)


if __name__ == "__main__":
    main()
