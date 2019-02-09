#!/usr/bin/env python

# TODO: Incorporate Ultimate Powers

# This uses the Advanced Rules

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

INITIAL_RANKS = {
    "Feeble": 1,
    "Poor": 3,
    "Typical": 5,
    "Good": 8,
    "Excellent": 16,
    "Remarkable": 26,
    "Incredible": 36,
    "Amazing": 46,
    "Monstrous": 63,
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

PRIMARY_ABILITY = {
    "Altered Human": [
        (5, "Feeble"),
        (10, "Poor"),
        (20, "Typical"),
        (40, "Good"),
        (60, "Excellent"),
        (80, "Remarkable"),
        (96, "Incredible"),
        (100, "Amazing")
    ],
    "Mutant": [
        (5, "Feeble"),
        (10, "Poor"),
        (20, "Typical"),
        (40, "Good"),
        (60, "Excellent"),
        (80, "Remarkable"),
        (96, "Incredible"),
        (100, "Amazing")
    ],
    "High-Tech": [
        (5, "Feeble"),
        (10, "Poor"),
        (40, "Typical"),
        (80, "Good"),
        (100, "Excellent"),
    ],
    "Robot": [
        (5, "Feeble"),
        (10, "Poor"),
        (15, "Typical"),
        (40, "Good"),
        (50, "Excellent"),
        (70, "Remarkable"),
        (90, "Incredible"),
        (98, "Amazing"),
        (100, "Monstrous")
    ],
    "Alien": [
        (10, "Feeble"),
        (20, "Poor"),
        (30, "Typical"),
        (40, "Good"),
        (60, "Excellent"),
        (70, "Remarkable"),
        (80, "Incredible"),
        (95, "Amazing"),
        (100, "Monstrous")
    ],
}

# Base table for Powers, Talents, and Contacts available
POWERS_TALENTS_CONTACTS = [
    (20, 2),
    (60, 3),
    (90, 4),
    (100, 5)
]

P_RESISTANCES = [
    (1, "Resistance to Fire and Heat"),
    (2, "Resistance to Cold"),
    (3, "Resistance to Electricity"),
    (4, "Resistance to Radiation"),
    (5, "Resistance to Toxins"),
    (6, "Resistance to Corrosives"),
    (7, "Resistance to Emotion Attacks"),
    (8, "Resistance to Mental Attacks"),
    (9, "Resistance to Magical Attacks"),
    (10, "Resistance to Disease Invulnerability *"),
]

P_SENSE = [
    (1, "Protected Senses"),
    (2, "Enhanced Senses"),
    (3, "Infravision"),
    (4, "Computer Links"),
    (5, "Emotion Detection"),
    (6, "Energy Detection"),
    (7, "Magnetic Detection"),
    (8, "Psionic Detection"),
    (9, "Astral Detection"),
    (10, "Tracking Ability"),
]

P_MOVEMENT = [
    (2, "Flight"),
    (3, "Gliding"),
    (4, "Leaping"),
    (6, "Wall-Crawling"),
    (7, "Lightning Speed Teleportation*"),
    (8, "Levitation"),
    (9, "Swimming"),
    (10, "Climbing"),
]

P_MATTER = [
    (2, "Earth Control"),
    (4, "Air Control"),
    (6, "Fire Control"),
    (8, "Water Control"),
    (10, "Weather Control"),
]

P_ENERGY = [
    (2, "Magnetic Manipulation"),
    (4, "Electrical Manipulation"),
    (6, "Light Manipulation"),
    (8, "Sound Manipulation"),
    (9, "Darkforce Manipulation"),
    (10, "Gravity Manipulation"),
]

P_BODY_CONTROL = [
    (1, "Growth"),
    (2, "Shrinking"),
    (3, "Invisibility"),
    (4, "Plasticity"),
    (5, "Shape-Shifting"),
    (6, "Body Transformation*"),
    (7, "Animal Transformation- Self"),
    (8, "Raise Lowest Ability"),
    (9, "Blending"),
    (10, "Alter Ego"),
]

P_RANGED_ATTACK = [
    (1, "Projectile Missile"),
    (2, "Ensnaring Missile"),
    (3, "Ice Generation"),
    (4, "Fire Generation"),
    (5, "Energy Generation"),
    (6, "Sound Generation"),
    (7, "Stunning Missile"),
    (8, "Corrosive Missile"),
    (9, "Slashing Missile"),
    (10, "Darkforce Generation"),
]

P_MENTAL = [
    (1, "Telepathy"),
    (2, "Image Generation*"),
    (3, "Telekinesis"),
    (4, "Force Field Generation"),
    (5, "Animal Communication and Control Mechanical Intuition"),
    (6, "Empathy"),
    (7, "Psi-Screen"),
    (8, "Mental Probe"),
    (9, "Astral Projection"),
    (10, "Psionic Attack"),
]

P_BODY_OFFENSE = [
    (3, "Extra Body Parts"),
    (4, "Extra Attacks"),
    (5, "Energy Touch"),
    (6, "Paralyzing Touch"),
    (8, "Claws"),
    (9, "Rotting Touch"),
    (10, "Corrosive Touch"),
]

P_BODY_DEFENSE = [
    (3, "Body Armor"),
    (4, "Water Breathing"),
    (5, "Absorption"),
    (6, "Regeneration"),
    (7, "Solar Regeneration"),
    (9, "Recovery"),
    (10, "Life Support"),
]

P_CATEGORIES = [
    (5, P_RESISTANCES),
    (10, P_SENSE),
    (15, P_MOVEMENT),
    (25, P_MATTER),
    (40, P_ENERGY),
    (55, P_BODY_CONTROL),
    (70, P_RANGED_ATTACK),
    (75, P_MENTAL),
    (90, P_BODY_OFFENSE),
    (100, P_BODY_DEFENSE),
]


def d10(table, roll_mod=0):
    roll = random.randint(1, 10)+roll_mod
    for row in table:
        if roll <= row[0]:
            return row[1]
    return table[-1][1]

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

def roll_primary_ability(origin, roll_mod=0):
     level = percentile(PRIMARY_ABILITY[origin], roll_mod)
     rank = INITIAL_RANKS[level]
     return (level, rank)

def column_shift(ability, shift, initial=False):
    new = POWER_LEVELS.index(ability)+shift
    if new < 0:
        new = 0
    if initial:
        return (POWER_LEVELS[new], INITIAL_RANKS[POWER_LEVELS[new]])
    return (POWER_LEVELS[new], POWER_RANKS[POWER_LEVELS[new]])

class Hero(object):
    def __init__(self):
        self.origin = percentile(ORIGINS)

        ability_mod = 0

        if self.origin == "Alien":
            ability_mod = 10

        self.abilities = {}
        for ability in FASERIP:
            self.abilities[ability] = roll_primary_ability(self.origin, ability_mod)

        self.resources = roll_ability()
        self.popularity = set_ability("Good")

        powers_available = percentile(POWERS_TALENTS_CONTACTS)
        self.talents = percentile(POWERS_TALENTS_CONTACTS)-1
        self.contacts = percentile(POWERS_TALENTS_CONTACTS)-2

        if self.origin == "Altered Human":
            self.notes = "Raise one primary ability by one rank"
        elif self.origin == "Mutant":
            self.notes = "Increase one power by one rank"
            self.resources = column_shift(self.resources[0], -1)
            self.popularity = set_ability("Shift 0")
            if powers_available < 5:
                powers_available += 1
            self.abilities["Endurance"] = column_shift(self.abilities["Endurance"][0], 1, True)
        elif self.origin == "High-Tech":
            self.notes = "Max ASE = Remarkable. One talent must be scientific or professional"
            self.resources = column_shift(self.resources[0], 1)
            self.abilities["Reason"] = column_shift(self.abilities["Reason"][0], 2, True)
            if self.contacts == 0:
                self.contacts = 1
        elif self.origin == "Robot":
            self.popularity = set_ability("Shift 0")
        elif self.origin == "Alien":
            self.resources = set_ability("Poor")
            self.contacts = 1
            if powers_available > 2:
                powers_available -= 1

        self.powers = []
        for _ in range(0, powers_available):
            self.powers.append(d10(percentile(P_CATEGORIES)))


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
        s += "\n"

        s += "Powers:\n"
        for power in self.powers:
            s += "%s\n" % (power,)
        s += "\n"

        s += "Talents: %d\n" % (self.talents,)
        s += "Contacts: %d\n" % (self.contacts,)
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
