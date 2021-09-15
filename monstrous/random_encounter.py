#!/usr/bin/env python3

import json
import random
import sys

FREQUENCIES = ["Common", "Uncommon", "Rare", "Very rare"]
TABLE = {
    "Common": ["01-11", "12-22", "23-33", "34-44", "45-55", "56-66"],
    "Uncommon": ["67-70", "71-74", "75-78", "79-82", "83-86"],
    "Rare": ["87-88", "89-90", "91-92", "93-94", "95-96"],
    "Very rare": ["97", "98", "99", "00"],
}


def gen_enc_table(monsters, terrain):
    terrain = terrain.lower()
    possible = {"Common": [], "Uncommon": [], "Rare": [], "Very rare": []}
    for monster in monsters:
        if (
            "Frequency" not in monsters[monster]
            or monsters[monster]["Frequency"] not in possible
        ):
            continue
        if (
            monsters[monster]["Climate/Terrain"] == "Any"
            or terrain in monsters[monster]["Normalized Terrains"]
            or terrain in monsters[monster]["Climate/Terrain"].lower()
        ):
            possible[monsters[monster]["Frequency"]].append(monster)
    print(f"{terrain.title()} random encounters")
    for freq in FREQUENCIES:
        print(f"{freq}")
        for roll in TABLE[freq]:
            monster = random.choice(possible[freq])
            possible[freq].remove(monster)
            print(f"{roll} {monster}")
        print()


def main():
    try:
        fname, terrain = sys.argv[1:3]
    except ValueError:
        print(f"Usage: {sys.argv[0]} [json] [terrain]")
        sys.exit(1)
    monsters = json.load(open(fname))
    gen_enc_table(monsters, terrain)


if __name__ == "__main__":
    main()
