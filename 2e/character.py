#!/usr/bin/env python3

import argparse
import random

from dice import roll
from generate_scroll import random_spell
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
    "Warrior": {
        "Classes": ["Fighter", "Ranger", "Paladin"],
        "Hit Die": 10,
        "Hit Dice": [
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 0),
            (9, 3),
            (9, 6),
            (9, 9),
            (9, 12),
            (9, 15),
            (9, 18),
            (9, 21),
            (9, 24),
            (9, 27),
            (9, 30),
            (9, 33),
        ],
    },
    "Wizard": {
        "Classes": [
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
        "Hit Die": 4,
        "Hit Dice": [
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 0),
            (10, 0),
            (10, 1),
            (10, 2),
            (10, 3),
            (10, 4),
            (10, 5),
            (10, 6),
            (10, 7),
            (10, 8),
            (10, 9),
            (10, 10),
        ],
    },
    "Priest": {
        "Classes": ["Cleric", "Druid"],
        "Hit Die": 8,
        "Hit Dice": [
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 0),
            (9, 2),
            (9, 4),
            (9, 6),
            (9, 8),
            (9, 10),
            (9, 12),
            (9, 14),
            (9, 16),
            (9, 18),
            (9, 20),
            (9, 22),
        ],
    },
    "Rogue": {
        "Classes": ["Thief", "Bard"],
        "Hit Die": 6,
        "Hit Dice": [
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 0),
            (10, 0),
            (10, 2),
            (10, 4),
            (10, 6),
            (10, 8),
            (10, 10),
            (10, 12),
            (10, 14),
            (10, 16),
            (10, 18),
            (10, 20),
        ],
    },
}

SPELL_PROGRESSION = {
    "Paladin": {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [1],
        10: [2],
        11: [2, 1],
        12: [2, 2],
        13: [2, 2, 1],
        14: [3, 2, 1],
        15: [3, 2, 1, 1],
        16: [3, 3, 2, 1],
        17: [3, 3, 3, 1],
        18: [3, 3, 3, 1],
        19: [3, 3, 3, 2],
        20: [3, 3, 3, 3],
    },
    "Ranger": {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [1],
        9: [2],
        10: [2, 1],
        11: [2, 2],
        12: [2, 2, 1],
        13: [3, 2, 1],
        14: [3, 2, 2],
        15: [3, 3, 2],
        16: [3, 3, 3],
        17: [3, 3, 3],
        18: [3, 3, 3],
        19: [3, 3, 3],
        20: [3, 3, 3],
    },
    "Wizard": {
        1:  [1],
        2:  [2],
        3:  [2, 1],
        4:  [3, 2],
        5:  [4, 2, 1],
        6:  [4, 2, 2],
        7:  [4, 3, 2, 1],
        8:  [4, 3, 3, 2],
        9:  [4, 3, 3, 2, 1],
        10: [4, 4, 3, 2, 2],
        11: [4, 4, 4, 3, 3],
        12: [4, 4, 4, 4, 4, 1],
        13: [5, 5, 5, 4, 4, 2],
        14: [5, 5, 5, 4, 4, 2, 1],
        15: [5, 5, 5, 5, 5, 2, 1],
        16: [5, 5, 5, 5, 5, 3, 2, 1],
        17: [5, 5, 5, 5, 5, 3, 3, 2],
        18: [5, 5, 5, 5, 5, 3, 3, 2, 1],
        19: [5, 5, 5, 5, 5, 3, 3, 3, 1],
        20: [5, 5, 5, 5, 5, 4, 3, 3, 2],
    },
    "Priest": {
        1:  [1],
        2:  [2],
        3:  [2, 1],
        4:  [3, 2],
        5:  [3, 3, 1],
        6:  [3, 3, 2],
        7:  [3, 3, 2, 1],
        8:  [3, 3, 3, 2],
        9:  [4, 4, 3, 2, 1],
        10: [4, 4, 3, 3, 2],
        11: [5, 4, 4, 3, 2, 1],
        12: [6, 5, 5, 3, 2, 2],
        13: [6, 6, 6, 4, 2, 2, 1],
        14: [6, 6, 6, 5, 3, 2, 1],
        15: [6, 6, 6, 6, 4, 2, 1],
        16: [7, 7, 7, 6, 4, 3, 8],
        17: [7, 7, 7, 7, 5, 3, 2],
        18: [8, 8, 8, 8, 6, 4, 2],
        19: [9, 9, 8, 8, 6, 4, 2],
        20: [9, 9, 9, 8, 7, 5, 2],
    },
    "Bard": {
        1:  [],
        2:  [1],
        3:  [2],
        4:  [2, 1],
        5:  [3, 1],
        6:  [3, 2],
        7:  [3, 2, 1],
        8:  [3, 3, 1],
        9:  [3, 3, 2],
        10: [3, 3, 2, 1],
        11: [5, 3, 3, 1],
        12: [3, 3, 3, 2],
        13: [3, 3, 3, 2, 1],
        14: [3, 3, 3, 3, 1],
        15: [3, 3, 3, 3, 2],
        16: [4, 3, 3, 3, 2, 1],
        17: [4, 4, 3, 3, 3, 1],
        18: [4, 4, 4, 3, 3, 2],
        19: [4, 4, 4, 4, 3, 2],
        20: [4, 4, 4, 4, 4, 3],

    },
}

WISDOM_CASTERS = ["Paladin", "Ranger", "Priest"]


def combine_minimums(minimums):
    minimum = {x: 0 for x in ABILITIES}
    for minima in minimums:
        for ability in minima:
            if minimum[ability] < minima[ability]:
                minimum[ability] = minima[ability]
    return minimum


def constitution_hp_modifier(con, class_group):
    con = int(con)
    if con <= 1:
        return -3
    elif con == 2 or con == 3:
        return -2
    elif con == 4 or con == 5 or con == 6:
        return -3
    elif con == 15:
        return 1
    elif con < 15:
        return 0
    if class_group != "Warrior" or con == 16:
        return 2
    elif con == 17:
        return 3
    elif con == 18:
        return 4
    elif con == 19 or con == 20:
        return 5
    elif con == 21 or con == 22 or con == 23:
        return 6
    else:
        return 7


def get_ability_priority(class_name):
    return CLASSES[class_name]["Primary"] + random.sample(
        CLASSES[class_name]["Secondary"], len(CLASSES[class_name]["Secondary"])
    )


def get_all_classes():
    return list(CLASSES.keys())

def get_caster_group(class_name):
    if class_name == "Paladin":
        caster = "Paladin"
    elif class_name == "Bard":
        caster = "Bard"
    else:
        caster = get_class_group(class_name)
    if caster in SPELL_PROGRESSION.keys():
        return caster

def get_class_group(class_name):
    return [x for x in CLASS_GROUPS if class_name in CLASS_GROUPS[x]["Classes"]][0]


def get_random_class():
    return random.choice(list(CLASSES.keys()))


def get_random_race_by_class(class_name):
    return random.choice(CLASSES[class_name]["Races"])


def get_spell_levels(caster_group, level, wisdom):
    wisdom = int(wisdom)
    spells = SPELL_PROGRESSION[caster_group][level]
    if caster_group in WISDOM_CASTERS:
        wisdom_spells = wisdom_bonus_spells(wisdom)
        try:
            for spell_level in range(0, len(spells)):
                spells[spell_level] += wisdom_spells[spell_level]
        except IndexError:
            pass
    if caster_group == "Priest":
        if wisdom < 17:
            spells = spells[:5]
        if wisdom < 18:
            spells = spells[:6]
    return spells

def wisdom_bonus_spells(wisdom):
    wisdom = int(wisdom)
    if wisdom < 13:
        return []
    elif wisdom == 13:
        return [1]
    elif wisdom == 14:
        return [2]
    elif wisdom == 15:
        return [2, 1]
    elif wisdom == 16:
        return [2, 2]
    elif wisdom == 17:
        return [2, 2, 1]
    elif wisdom == 18:
        return [2, 2, 1, 1]
    elif wisdom == 19:
        return [3, 2, 1, 2]
    elif wisdom == 20:
        return [3, 3, 1, 3]
    elif wisdom == 21:
        return [3, 3, 2, 3, 1]
    elif wisdom == 22:
        return [3, 3, 2, 4, 2]
    elif wisdom == 23:
        return [3, 3, 2, 4, 4]
    elif wisdom == 24:
        return [3, 3, 2, 4, 4, 2]
    elif wisdom == 25:
        return [3, 3, 2, 4, 4, 3, 1]

class Character(object):
    def __init__(self, char_class=None, abilities=None, race=None, level=1):
        self.char_class = char_class
        if not self.char_class:
            self.char_class = get_random_class()
        self.class_group = get_class_group(self.char_class)
        self.race = race
        if not self.race:
            self.race = get_random_race_by_class(self.char_class)
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
                tries=6 + int(self.level / 10),
                rolls=3 + int(self.level / 7),
                extrao_str=self.class_group == "Warrior" and self.race != "Halfling",
            )
        self.hitpoints = roll(
            CLASS_GROUPS[self.class_group]["Hit Dice"][self.level - 1][0],
            CLASS_GROUPS[self.class_group]["Hit Die"],
            CLASS_GROUPS[self.class_group]["Hit Dice"][self.level - 1][1]
            + self.level
            * constitution_hp_modifier(
                self.abilities["Constitution"], self.class_group
            ),
        )
        self.spell_levels = []
        self.spells = {}
        self.caster_group = get_caster_group(self.char_class)
        if self.caster_group:
            self.spell_levels = get_spell_levels(self.caster_group, self.level, self.abilities["Wisdom"])
            self.populate_spells()
        self.equipment = []

    def __str__(self):
        s = f"{'-'*10}\n"
        s += f"{self.race} {self.char_class} {self.level}\n"
        s += f"HP: {self.hitpoints}\n"
        for ability in self.abilities:
            s += f"{ability}: {self.abilities[ability]}\n"
        if self.spell_levels:
            s += "\n"
            s += f"Spells ({'/'.join([str(x) for x in self.spell_levels])}):\n"
            for spell_level in range(1, len(self.spell_levels)+1):
                s += f"{spell_level}: "
                cur_spells = []
                for spell in sorted(set(self.spells[spell_level])):
                    count = ""
                    if self.spells[spell_level].count(spell) > 1:
                        count = f" ({self.spells[spell_level].count(spell)})"
                    cur_spells.append(f"{spell}{count}")
                s += f"{'; '.join(cur_spells)}\n"
        s += "\n"
        s += "Equipment:\n" + "\n".join(self.equipment)
        s += f"\n{'-'*10}"
        return s

    def add_equipment(self, item):
        self.equipment.append(item)

    def populate_spells(self):
        for spell_level in range(1, len(self.spell_levels)+1):
            if spell_level not in self.spells:
                self.spells[spell_level] = []
            for _ in range(0, self.spell_levels[spell_level-1]):
                self.spells[spell_level].append(random_spell(spell_level, self.caster_group))
            #print(f"{spell_level}: {self.spell_levels[spell_level-1]}")

def main():
    parser = argparse.ArgumentParser(description="Create a character")
    # print(Character(get_random_class(), level=20))
    #for class_name in get_all_classes():
    #    print(Character(char_class=class_name, level=10))
    #print(get_spell_levels("Cleric", 8, 5))
    print(Character(char_class="Mage", level=15))

if __name__ == "__main__":
    main()
