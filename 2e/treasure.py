#!/usr/bin/env python3

import argparse
import random

import jewelry
import gems
import magic_item

ORDER = [
    "cp",
    "sp",
    "gp",
    "pp",
    "gems",
    "art/jewelry",
    "potions",
    "scrolls",
    "magic items",
    "complex",
]

TREASURE = {
    "A": {
        "cp": [25, 1000, 3000],
        "sp": [30, 200, 2000],
        "gp": [40, 1000, 6000],
        "pp": [35, 100, 1000],
        "gems": [60, 10, 40],
        "art/jewelry": [50, 2, 12],
        "magic items": [30, 3, 3],
    },
    "B": {
        "cp": [50, 1000, 6000],
        "sp": [25, 1000, 3000],
        "gp": [25, 200, 2000],
        "pp": [25, 100, 1000],
        "gems": [30, 1, 8],
        "art/jewelry": [20, 1, 4],
        "complex": [10, [[1, "magic armor or magic weapon"]]],
    },
    "C": {
        "cp": [20, 1000, 10000],
        "sp": [30, 1000, 6000],
        "pp": [10, 100, 600],
        "gems": [25, 1, 6],
        "art/jewelry": [20, 1, 3],
        "magic items": [10, 2, 2],
    },
    "D": {
        "cp": [10, 1000, 6000],
        "sp": [15, 1000, 10000],
        "gp": [50, 1000, 3000],
        "pp": [15, 100, 600],
        "gems": [30, 1, 10],
        "art/jewelry": [25, 1, 6],
        "complex": [15, [[2, "magic items"], [1, "potions"]]],
    },
    "E": {
        "cp": [5, 1000, 6000],
        "sp": [25, 1000, 10000],
        "gp": [25, 1000, 4000],
        "pp": [25, 300, 1800],
        "gems": [15, 1, 12],
        "art/jewelry": [10, 1, 6],
        "complex": [
            25,
            [
                [3, "magic items"],
                [1, "scrolls"],
            ],
        ],
    },
    "F": {
        "sp": [10, 3000, 18000],
        "gp": [40, 1000, 6000],
        "pp": [15, 1000, 4000],
        "gems": [20, 2, 20],
        "art/jewelry": [10, 1, 8],
        "complex": [30, [[5, "non-weapon magic items"]]],
    },
    "G": {
        "gp": [50, 2000, 20000],
        "pp": [50, 1000, 10000],
        "gems": [30, 3, 18],
        "art/jewelry": [25, 1, 6],
        "magic items": [35, 5, 5],
    },
    "H": {
        "cp": [25, 3000, 18000],
        "sp": [40, 2000, 20000],
        "gp": [55, 2000, 20000],
        "pp": [40, 1000, 8000],
        "gems": [50, 3, 30],
        "art/jewelry": [50, 2, 20],
        "magic items": [15, 6, 6],
    },
    "I": {
        "pp": [30, 100, 600],
        "gems": [55, 2, 12],
        "art/jewelry": [50, 2, 8],
        "magic items": [15, 1, 1],
    },
    "J": {
        "cp": [100, 3, 24],
    },
    "K": {
        "sp": [100, 3, 18],
    },
    "L": {
        "pp": [100, 2, 12],
    },
    "M": {
        "gp": [100, 2, 8],
    },
    "N": {
        "pp": [100, 1, 6],
    },
    "O": {
        "cp": [100, 10, 40],
        "sp": [100, 10, 30],
    },
    "P": {
        "sp": [100, 10, 60],
        "pp": [100, 1, 20],
    },
    "Q": {
        "gems": [100, 1, 4],
    },
    "R": {
        "gp": [100, 2, 20],
        "pp": [100, 10, 60],
        "gems": [100, 2, 8],
        "art/jewelry": [100, 1, 3],
    },
    "S": {
        "potions": [100, 1, 8],
    },
    "T": {
        "scrolls": [100, 1, 8],
    },
    "U": {
        "gems": [90, 2, 16],
        "art/jewelry": [80, 1, 6],
        "magic items": [70, 1, 1],
    },
    "V": {
        "magic items": [100, 2, 2],
    },
    "W": {
        "gp": [100, 5, 30],
        "pp": [100, 1, 8],
        "gems": [60, 2, 16],
        "art/jewelry": [50, 1, 8],
        "magic items": [60, 2, 2],
    },
    "X": {
        "potions": [100, 2, 2],
    },
    "Y": {
        "gp": [
            100,
            200,
            1200,
        ],
    },
    "Z": {
        "cp": [100, 100, 300],
        "sp": [100, 100, 400],
        "gp": [100, 100, 600],
        "pp": [100, 100, 400],
        "gems": [55, 1, 6],
        "art/jewelry": [50, 2, 12],
        "magic items": [50, 3, 3],
    },
}


def percentile_check(check_val):
    if random.randint(1, 100) <= check_val:
        return True
    else:
        return False


def roll_treasure(ttypes):
    treasure = {}
    for ttype in ttypes:
        if ttype in TREASURE:
            for thing in ORDER:
                # Initialize treasure
                if thing not in treasure:
                    if thing == "complex":
                        treasure["complex"] = {}
                    else:
                        treasure[thing] = 0
                # Don't roll for treasure not present in this treasure type
                if thing not in TREASURE[ttype]:
                    continue
                # See if we successfully rolled for this treasure
                if percentile_check(TREASURE[ttype][thing][0]):
                    # Handle weird magic items, like "Any 3 + 1 scroll"
                    if thing == "complex":
                        for complex_item in TREASURE[ttype]["complex"][1]:
                            if complex_item[1] in ORDER:
                                treasure[complex_item[1]] += complex_item[0]
                            else:
                                if complex_item[1] not in treasure["complex"]:
                                    treasure["complex"][complex_item[1]] = complex_item[
                                        0
                                    ]
                                else:
                                    treasure["complex"][
                                        complex_item[1]
                                    ] += complex_item[0]
                    else:
                        amount = random.randint(
                            TREASURE[ttype][thing][1], TREASURE[ttype][thing][2]
                        )
                        treasure[thing] += amount
        else:
            print("Unknown treasure type: %s" % (ttype,))
    return treasure


def print_treasure(treasure):
    valuables = []
    for thing in ORDER:
        if thing in treasure:
            if not treasure[thing]:
                continue
            if thing == "complex":
                for complex_item in treasure["complex"]:
                    valuables.append(
                        "%s %s"
                        % (
                            "{:,}".format(treasure["complex"][complex_item]),
                            complex_item,
                        )
                    )
            else:
                valuables.append("%s %s" % ("{:,}".format(treasure[thing]), thing))
    print(", ".join(valuables))


def generate_gems(treasure):
    if treasure["gems"]:
        print(f"\nGems ({treasure['gems']}):")
        gems.generate_gems(treasure["gems"])


def generate_jewelry(treasure):
    if treasure["art/jewelry"]:
        print(f"\nJewelry ({treasure['art/jewelry']}):")
        jewelry.generate_jewelry(treasure["art/jewelry"])


def generate_magic_items(treasure, expanded):
    magic_items = []
    mig = magic_item.MagicItemGen(expanded)
    for i in range(0, treasure["magic items"]):
        magic_items.append(mig.random_magic_item())
    for i in range(0, treasure["potions"]):
        magic_items.append(mig.roll_category("Potions and Oils"))
    for i in range(0, treasure["scrolls"]):
        magic_items.append(str(mig.roll_category("Scrolls")))
    try:
        for i in range(0, treasure["complex"]["non-weapon magic items"]):
            magic_items.append(mig.roll_nonweapon())
    except KeyError:
        pass
    try:
        for i in range(0, treasure["complex"]["magic armor or magic weapon"]):
            magic_items.append(mig.armor_or_weapon())
    except KeyError:
        pass
    return sorted(magic_items)


def main():
    parser = argparse.ArgumentParser(description="Generate treasure")
    parser.add_argument("treasure_types", metavar="N", nargs="+")
    parser.add_argument(
        "-n",
        "--nogen",
        default=False,
        action="store_true",
        help="don't generate items",
    )
    parser.add_argument(
        "-x",
        "--expanded",
        default=False,
        action="store_true",
        help="use expanded generation tables",
    )
    args = parser.parse_args()

    treasure = roll_treasure(list("".join(args.treasure_types).upper()))
    print_treasure(treasure)
    if not args.nogen:
        generate_gems(treasure)
        generate_jewelry(treasure)
        magic_items = generate_magic_items(treasure, args.expanded)
        if magic_items:
            print("\nMagic Items, Potions, and Scrolls:")
            print("\n".join(magic_items))


if __name__ == "__main__":
    main()
