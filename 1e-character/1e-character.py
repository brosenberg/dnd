#!/usr/bin/env python

import random

STATS = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Wisdom",
    "Intelligence",
    "Charisma"
]

CLASSES = {
    "Fighter": {
        "stat": ["Strength"],
        "weapon_category": ["Fighter", "Cleric"],
        "spells": None,
        "armor": ["Metal", "Leather"],
        "hd": 10,
    },
    "Cleric": {
        "stat": ["Charisma", "Wisdom"],
        "weapon_category": ["Cleric"],
        "spells": "Divine",
        "armor": ["Metal", "Cloth"],
        "hd": 8,
    },
    "Mage": {
        "stat": ["Intelligence"],
        "weapon_category": ["Mage"],
        "spells": "Arcane",
        "armor": ["Cloth"],
        "hd": 4,
    },
    "Thief": {
        "stat": ["Dexterity"],
        "weapon_category": ["Thief"],
        "spells": None,
        "armor": ["Leather"],
        "hd": 6,
    },
    "Elf": {
        "stat": ["It's complicated"],
        "weapon_category": ["Fighter", "Mage", "Thief"],
        "spells": "Arcane",
        "armor": ["Leather", "Cloth"],
        "hd": 6,
    },
    "Dwarf": {
        "stat": ["Constitution"],
        "weapon_category": ["Fighter", "Thief"],
        "spells": None,
        "armor": ["Metal", "Leather"],
        "hd": 10,
    },
}

WEAPONS = {
    "Fighter": [
        "Longsword",
        "Broadsword",
        "Bastard Sword",
        "Two-handed Sword",
        "Scimitar",
        "Battle Axe",
        "War Axe",
        "Two-handed Axe",
        "Bearded Axe",
        "Pike",
        "Glaive",
        "Guisarme",
        "Halberd",
        "Spear",
        "Longbow",
        "Crossbow",
    ],
    "Cleric": [
        "Mace",
        "Hammer",
        "Morningstar",
        "Club",
        "Quarterstaff",
        "Flail",
    ],
    "Mage": [
        "Dagger",
        "Dart",
        "Quarterstaff",
        "Sling",
    ],
    "Thief": [
        "Dagger",
        "Shortsword",
        "Shortbow",
        "Stiletto",
        "Rapier",
        "Short Spear",
        "Shortbow",
        "Crossbow"
    ],
}

ARMOR = {
    "Metal": [
        "Chain Mail",
        "Banded Mail",
        "Ring Mail",
        "Splint Mail"
    ],
    "Leather": [
        "Leather Armor",
        "Studded Leather",
        "Raw Hide"
    ],
    "Cloth": [
        "Robes",
        "Tunic",
    ]
}

SPELLS = {
    "Arcane": [
        "Magic Missile",
        "Burning Hands",
        "Find Familiar",
        "Color Spray",
        "Sleep"
    ],
    "Divine": [
        "Cure Light Wounds",
        "Bless Water",
    ]
}


def roll(dice, sides):
    result = 0
    for die in range(0, dice):
        result += random.randint(0, sides-1) + 1
    return result

def roll_drop_lowest(dice, sides):
    rolls = []
    for die in range(0, dice):
        rolls.append(random.randint(0, sides-1) + 1)
    return sum(rolls[1:len(rolls)])

def mod(num):
    if num <4:
        return -3
    elif num < 6:
        return -2
    elif num < 9:
        return -1
    elif num < 12:
        return 0
    elif num < 16:
        return 1
    elif num < 18:
        return 2
    elif num >= 18:
        return 3
    else:
        return 0

class Character(object):
    def __init__(self):
        self.stats = {}

        for i in range(0, 6):
            self.stats[STATS[i]] = roll_drop_lowest(4, 6)

        max_stat = max(self.stats, key=self.stats.get)
        self.char_class = None
        if self.stats["Dexterity"] == self.stats["Intelligence"] or \
           self.stats["Strength"] == self.stats["Intelligence"]:
            self.char_class = "Elf"
        else:
            for c in CLASSES:
                if max_stat in CLASSES[c]["stat"]:
                    self.char_class = c
        if self.char_class is None:
            self.char_class = random.choice(CLASSES.keys())

        self.hp = roll(1, CLASSES[self.char_class]["hd"]) + mod(self.stats["Constitution"])
        if self.hp < 1:
            self.hp = 1

        weapons = []
        for weapon_type in CLASSES[self.char_class]["weapon_category"]:
            weapons += WEAPONS[weapon_type]
        self.weapon = random.choice(weapons)

        self.spell = None
        if CLASSES[self.char_class]["spells"] is not None:
            self.spell = random.choice(SPELLS[
                    CLASSES[self.char_class]["spells"]
                ]
            )

        armors = []
        for armor in CLASSES[self.char_class]["armor"]:
            armors += ARMOR[armor]
        self.armor = random.choice(armors)


    def __str__(self):
        s = "%s\n" % ("-" * 80,)
        s += "CHARACTER SHEET\n"
        s += "%s\n" % ("-" * 80,)
        s += "%s\n" % (self.char_class,)
        s += "Level 1\n\n"
        for stat in STATS:
            s += "%s: %s\n" % (stat, self.stats[stat])
        s += "\n"
        s += "HP: %s\n" % (self.hp,)
        s += "\n"
        s += "Weapon: %s\n" % (self.weapon,)
        s += "Armor: %s\n" % (self.armor,)
        if self.spell:
            s += "Spell: %s\n" % (self.spell,)
        s += "%s\n" % ("-" * 80,)
        return s


def main():
    c = Character()
    print c

if __name__ == '__main__':
    main()
