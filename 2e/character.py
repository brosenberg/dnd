#!/usr/bin/env python3

import argparse
import random

from dice import roll
from roll_abilities import get_abilities

ABILITIES = {
    "Fighter": {
        "Primary": ["Strength"],
        "Secondary": ["Constitution", "Dexterity"],
        "Minimums": {"Strength": 9},
    },
    "Wizard": {
        "Primary": ["Intelligence"],
        "Secondary": [],
        "Minimums": {"Intelligence": 9},
    },
    "Cleric": {
        "Primary": ["Wisdom"],
        "Secondary": ["Charisma", "Strength", "Constitution", "Dexterity"],
        "Minimums": {"Wisdom": 9},
    },
    "Thief": {
        "Primary": ["Dexterity"],
        "Secondary": ["Strength", "Constitution"],
        "Minimums": {"Dexterity": 9},
    },
}

WARRIORS = ["Fighter", "Ranger", "Paladin"]


def get_ability_priority(class_name):
    return ABILITIES[class_name]["Primary"] + random.sample(
        ABILITIES[class_name]["Secondary"], len(ABILITIES[class_name]["Secondary"])
    )


class Character(object):
    def __init__(self, char_class, abilities=None, level=1):
        self.char_class = char_class
        self.level = level
        self.abilities = abilities
        if not self.abilities:
            self.abilities = get_abilities(
                get_ability_priority(self.char_class),
                ABILITIES[self.char_class]["Minimums"],
                tries=6+int(self.level/7),
                rolls=3+int(self.level/5),
                extrao_str=self.char_class in WARRIORS
            )
        self.equipment = []

    def __str__(self):
        s = f"{'-'*10}\n"
        s += f"{self.char_class} {self.level}\n"
        for ability in self.abilities:
            s += f"{ability}: {self.abilities[ability]}\n"
        s += "\n"
        s += "Equipment:\n" + "\n".join(self.equipment)
        s += f"\n{'-'*10}"
        return s

    def add_equipment(self, item):
        self.equipment.append(item)


def main():
    parser = argparse.ArgumentParser(description="Create a character")
    print(Character("Fighter"))


if __name__ == "__main__":
    main()
