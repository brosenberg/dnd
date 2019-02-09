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

def percentile(table, roll_mod=0):
    roll = random.randint(1, 100)+roll_mod
    for row in table:
        if roll <= row[0]:
            return row[1]
    return table[-1][1]

class Hero(object):
    def __init__(self):
        self.origin = percentile(ORIGINS)

        ability_mod = 0

        if self.origin == "Alien":
            ability_mod = 10

        self.abilities = {
            "Fighting": percentile(MAJOR_ABILITY, ability_mod),
            "Agility": percentile(MAJOR_ABILITY, ability_mod),
            "Strength": percentile(MAJOR_ABILITY, ability_mod),
            "Endurance": percentile(MAJOR_ABILITY, ability_mod),
            "Reason": percentile(MAJOR_ABILITY, ability_mod),
            "Intuition": percentile(MAJOR_ABILITY, ability_mod),
            "Psyche": percentile(MAJOR_ABILITY, ability_mod)
        }

        # Do these at the end
        if self.origin == "Altered Human":
            self.notes = "Raise one rank of Major ability"
        elif self.origin == "Mutant":
            self.notes = "Increase one power by one rank"
            self.resources = "-1 CS"
            self.popularity = 0
        elif self.origin == "High-Tech":
            self.notes = "Max ASE = Remarkable"
            self.resources = "+1 CS"
            self.reason = "+1 CS"
        elif self.origin == "Robot":
            self.popularity = 0
        elif self.origin == "Alien":
            self.powers = -1

    def __str__(self):
        s = ""
        s += "Origin: %s\n" % (self.origin,)
        s += "\n"
        for ability in FASERIP:
            s += "%s: %s\n" % (ability, self.abilities[ability])
        return s

def main():
    hero = Hero()
    print hero


if __name__ == '__main__':
    main()
