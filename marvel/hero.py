#!/usr/bin/env python

import random

FASERIP = [
    "Fighting",
    "Agility",
    "Strength",
    "Endurance",
    "Reason",
    "Intuition",
    "Psyche"
]

POWER_LEVELS = [
    "Shift 0",
    "Feeble",
    "Poor",
    "Typical",
    "Good",
    "Excellent",
    "Remarkable",
    "Incredible",
    "Amazing",
    "Monstrous",
    "Unearthy",
    "Shift X",
    "Shift Y",
    "Shift Z",
    "Class 1000",
    "Class 3000",
    "Class 5000",
    #"Beyond"
]

POWER_RANKS = {
    "Shift 0": 0,
    "Feeble": 2,
    "Poor": 4,
    "Typical": 6,
    "Good": 10,
    "Excellent": 20,
    "Remarkable": 30,
    "Incredible": 40,
    "Amazing": 50,
    "Monstrous": 75,
    "Unearthy": 100,
    "Shift X": 150,
    "Shift Y": 250,
    "Shift Z": 500,
    "Class 1000": 1000,
    "Class 3000": 3000,
    "Class 5000": 5000,
    #"Beyond"
}

ORIGINS = [
    (30, 'Altered Human'),
    (60, 'Mutant'),
    (90, 'High-Tech'),
    (95, 'Robot'),
    (100, 'Alien')
]

MAJOR_ABILITY = [
    (5, "Feeble"),
    (10, "Poor"),
    (20, "Typical"),
    (40, "Good"),
    (60, "Excellent"),
    (80, "Remarkable"),
    (96, "Incredible"),
    (200, "Amazing")
]

POWERS_AVAILABLE = [
    (20, 2),
    (60, 3),
    (90, 4),
    (100, 5)
]

def percentile(table, roll_mod=0):
    roll = random.randint(1, 100)+roll_mod
    for row in table:
        if roll <= row[0]:
            return row[1]
    return table[-1][1]

def set_ability(level):
     rank = POWER_RANKS[level]
     return (level, rank)

def roll_ability(roll_mod=0):
     level = percentile(MAJOR_ABILITY, roll_mod)
     rank = POWER_RANKS[level]
     return (level, rank)

def column_shift(ability, shift):
    new = POWER_LEVELS.index(ability)+shift
    if new < 0:
        new = 0
    return (POWER_LEVELS[new], POWER_RANKS[POWER_LEVELS[new]])

class Hero(object):
    def __init__(self):
        self.origin = percentile(ORIGINS)

        ability_mod = 0

        if self.origin == "Alien":
            ability_mod = 10

        self.abilities = {}
        for ability in FASERIP:
            self.abilities[ability] = roll_ability(ability_mod)

        self.resources = roll_ability()
        self.popularity = set_ability("Good")

        powers_available = percentile(POWERS_AVAILABLE)

        if self.origin == "Altered Human":
            self.notes = "Raise one rank of Major ability"
        elif self.origin == "Mutant":
            self.notes = "Increase one power by one rank"
            self.resources = column_shift(self.resources[0], -1)
            self.popularity = set_ability("Shift 0")
        elif self.origin == "High-Tech":
            self.notes = "Max ASE = Remarkable"
            self.resources = column_shift(self.resources[0], 1)
            self.abilities["Reason"] = column_shift(self.abilities["Reason"][0], 1)
        elif self.origin == "Robot":
            self.popularity = set_ability("Shift 0")
        elif self.origin == "Alien":
            powers_available -= 1

    def __str__(self):
        s = ""
        s += "Origin: %s\n" % (self.origin,)
        s += "\n"
        for ability in FASERIP:
            s += "%s: %s\n" % (ability, self.abilities[ability])
        s += "\n"
        s += "Health: %d\n" % (self.get_health(),)
        s += "Karma: %d\n" % (self.get_karma(),)
        s += "Resources: %s\n" % (self.resources,)
        s += "Popularity: %s\n" % (self.popularity,)
        return s

    def get_health(self):
        health = 0
        for ability in ["Fighting", "Agility", "Strength", "Endurance"]:
            health += self.abilities[ability][1]
        return health

    def get_karma(self):
        karma = 0
        for ability in ["Reason", "Intuition", "Psyche"]:
            karma += self.abilities[ability][1]
        return karma

def main():
    hero = Hero()
    print hero


if __name__ == '__main__':
    main()
