#!/usr/bin/env python3

import argparse
import random

from dice import roll
from roll_abilities import get_abilities

ABILITIES = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma",
]

RACES = {
    "Dwarf": {
        "Ability Modifiers": {"Constitution": 1, "Charisma": -1},
        "Maximums": {
            "Strength": 18,
            "Dexterity": 17,
            "Constitution": 18,
            "Intelligence": 18,
            "Wisdom": 18,
            "Charisma": 17,
        },
        "Minimums": {
            "Strength": 8,
            "Dexterity": 3,
            "Constitution": 11,
            "Intelligence": 3,
            "Wisdom": 3,
            "Charisma": 3,
        },
    },
    "Elf": {
        "Ability Modifiers": {"Constitution": -1, "Dexterity": 1},
        "Maximums": {
            "Strength": 18,
            "Dexterity": 18,
            "Constitution": 18,
            "Intelligence": 18,
            "Wisdom": 18,
            "Charisma": 18,
        },
        "Minimums": {
            "Strength": 3,
            "Dexterity": 6,
            "Constitution": 7,
            "Intelligence": 8,
            "Wisdom": 3,
            "Charisma": 8,
        },
    },
    "Gnome": {
        "Ability Modifiers": {"Wisdom": -1, "Intelligence": 1},
        "Maximums": {
            "Strength": 18,
            "Dexterity": 18,
            "Constitution": 18,
            "Intelligence": 18,
            "Wisdom": 18,
            "Charisma": 18,
        },
        "Minimums": {
            "Strength": 6,
            "Dexterity": 3,
            "Constitution": 8,
            "Intelligence": 6,
            "Wisdom": 3,
            "Charisma": 3,
        },
    },
    "Half-Elf": {
        "Ability Modifiers": {},
        "Maximums": {
            "Strength": 18,
            "Dexterity": 18,
            "Constitution": 18,
            "Intelligence": 18,
            "Wisdom": 18,
            "Charisma": 18,
        },
        "Minimums": {
            "Strength": 3,
            "Dexterity": 6,
            "Constitution": 6,
            "Intelligence": 4,
            "Wisdom": 3,
            "Charisma": 3,
        },
    },
    "Halfling": {
        "Ability Modifiers": {"Strength": -1, "Dexterity": 1},
        "Maximums": {
            "Strength": 18,
            "Dexterity": 18,
            "Constitution": 18,
            "Intelligence": 18,
            "Wisdom": 17,
            "Charisma": 18,
        },
        "Minimums": {
            "Strength": 7,
            "Dexterity": 7,
            "Constitution": 10,
            "Intelligence": 6,
            "Wisdom": 3,
            "Charisma": 3,
        },
    },
    "Human": {
        "Ability Modifiers": {},
        "Maximums": {
            "Strength": 18,
            "Dexterity": 18,
            "Constitution": 18,
            "Intelligence": 18,
            "Wisdom": 18,
            "Charisma": 18,
        },
        "Minimums": {
            "Strength": 3,
            "Dexterity": 3,
            "Constitution": 3,
            "Intelligence": 3,
            "Wisdom": 3,
            "Charisma": 3,
        },
    },
}

CLASSES = {
    "Fighter": {
        "Primary": ["Strength"],
        "Secondary": ["Constitution", "Dexterity"],
        "Minimums": {"Strength": 9},
        "Races": [x for x in RACES],
    },
    "Paladin": {
        "Primary": ["Charisma", "Wisdom", "Strength", "Constitution"],
        "Secondary": ["Dexterity"],
        "Minimums": {"Strength": 12, "Constitution": 9, "Wisdom": 13, "Charisma": 17},
        "Races": ["Human"],
    },
    "Ranger": {
        "Primary": ["Constitution", "Wisdom"],
        "Secondary": ["Strength", "Dexterity"],
        "Minimums": {"Strength": 13, "Dexterity": 13, "Constitution": 14, "Wisdom": 14},
        "Races": ["Human", "Elf", "Half-Elf"],
    },
    "Mage": {
        "Primary": ["Intelligence"],
        "Secondary": [],
        "Minimums": {"Intelligence": 9},
        "Races": ["Human", "Elf", "Half-Elf"],
    },
    "Abjurer": {
        "Primary": ["Wisdom", "Intelligence"],
        "Secondary": [],
        "Minimums": {"Intelligence": 9, "Wisdom": 15},
        "Races": ["Human"],
    },
    "Conjurer": {
        "Primary": ["Constitution", "Intelligence"],
        "Secondary": [],
        "Minimums": {"Constitution": 15, "Intelligence": 9},
        "Races": ["Human", "Half-Elf"],
    },
    "Diviner": {
        "Primary": ["Wisdom", "Intelligence"],
        "Secondary": [],
        "Minimums": {"Wisdom": 16, "Intelligence": 9},
        "Races": ["Human", "Elf", "Half-Elf"],
    },
    "Enchanter": {
        "Primary": ["Charisma", "Intelligence"],
        "Secondary": [],
        "Minimums": {"Charisma": 16, "Intelligence": 9},
        "Races": ["Human", "Elf", "Half-Elf"],
    },
    "Illusionist": {
        "Primary": ["Dexterity", "Intelligence"],
        "Secondary": [],
        "Minimums": {"Dexterity": 16, "Intelligence": 9},
        "Races": ["Human", "Gnome"],
    },
    "Invoker": {
        "Primary": ["Constitution", "Intelligence"],
        "Secondary": [],
        "Minimums": {"Constitution": 16, "Intelligence": 9},
        "Races": ["Human"],
    },
    "Necromancer": {
        "Primary": ["Wisdom", "Intelligence"],
        "Secondary": [],
        "Minimums": {"Wisdom": 16, "Intelligence": 9},
        "Races": ["Human"],
    },
    "Transmuter": {
        "Primary": ["Dexterity", "Intelligence"],
        "Secondary": [],
        "Minimums": {"Dexterity": 15, "Intelligence": 9},
        "Races": ["Human", "Half-Elf"],
    },
    "Cleric": {
        "Primary": ["Wisdom"],
        "Secondary": ["Charisma", "Strength", "Constitution", "Dexterity"],
        "Minimums": {"Wisdom": 9},
        "Races": [x for x in RACES],
    },
    "Druid": {
        "Primary": ["Charisma", "Wisdom"],
        "Secondary": ["Strength", "Constitution", "Dexterity"],
        "Minimums": {"Wisdom": 12, "Charisma": 15},
        "Races": ["Human", "Half-Elf"],
    },
    "Thief": {
        "Primary": ["Dexterity"],
        "Secondary": ["Strength", "Constitution"],
        "Minimums": {"Dexterity": 9},
        "Races": [x for x in RACES],
    },
    "Bard": {
        "Primary": ["Charisma", "Intelligence", "Dexterity"],
        "Secondary": [],
        "Minimums": {"Dexterity": 12, "Intelligence": 13, "Charisma": 15},
        "Races": ["Human", "Half-Elf"],
    },
}

CLASS_GROUPS = {
    "Warrior": ["Fighter", "Ranger", "Paladin"],
    "Wizard": [
        "Mage",
        "Abjurer",
        "Conjurer",
        "Diviner",
        "Enchanter",
        "Illusionist",
        "Invoker",
        "Necromancer",
        "Transmuter",
    ],
    "Priest": ["Cleric", "Druid"],
    "Rogue": ["Thief", "Bard"],
}


def combine_minimums(minimums):
    minimum = {x: 0 for x in ABILITIES}
    for minima in minimums:
        for ability in minima:
            if minimum[ability] < minima[ability]:
                minimum[ability] = minima[ability]
    return minimum


def get_ability_priority(class_name):
    return CLASSES[class_name]["Primary"] + random.sample(
        CLASSES[class_name]["Secondary"], len(CLASSES[class_name]["Secondary"])
    )


def get_class_group(class_name):
    return [x for x in CLASS_GROUPS if class_name in CLASS_GROUPS[x]][0]


def get_random_class():
    return random.choice(list(CLASSES.keys()))


def get_random_race_by_class(class_name):
    return random.choice(CLASSES[class_name]["Races"])


class Character(object):
    def __init__(self, char_class=None, abilities=None, race=None, level=1):
        self.char_class = char_class
        if not self.char_class:
            self.char_class = get_random_class()
        self.race = race
        if not self.race:
            self.race = get_random_race_by_class(self.char_class)
        self.class_group = get_class_group(char_class)
        self.level = level
        self.abilities = abilities
        if not self.abilities:
            minimums = combine_minimums(
                [CLASSES[self.char_class]["Minimums"], RACES[self.race]["Minimums"]]
            )
            self.abilities = get_abilities(
                get_ability_priority(self.char_class),
                minimums,
                RACES[self.race]["Maximums"],
                RACES[self.race]["Ability Modifiers"],
                tries=6 + int(self.level / 7),
                rolls=3 + int(self.level / 5),
                extrao_str=self.class_group == "Warrior" and self.race != "Halfling",
            )
        self.equipment = []

    def __str__(self):
        s = f"{'-'*10}\n"
        s += f"{self.race} {self.char_class} {self.level}\n"
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
    print(Character(get_random_class(), level=12))


if __name__ == "__main__":
    main()
