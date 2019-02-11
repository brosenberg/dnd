#!/usr/bin/env python

# TODO: Add talents

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
    (26, ("Normal Human", "-")),
    (30, ("Mutant", "Induced")),
    (33, ("Mutant", "Random")),
    (35, ("Mutant", "Breed")),
    (38, ("Android", "-")),
    (46, ("Humanoid Race", "-")),
    (47, ("Surgical Composite", "-")),
    (49, ("Modified Human", "Organic")),
    (51, ("Modified Human", "Muscular")),
    (53, ("Modified Human", "Skeletal")),
    (57, ("Modified Human", "Extra Parts")),
    (58, ("Demihuman", "Centaur")),
    (59, ("Demihuman", "Equiman")),
    (60, ("Demihuman", "Faun")),
    (62, ("Demihuman", "Felinoid")),
    (64, ("Demihuman", "Lupinoid")),
    (66, ("Demihuman", "Avian-Angel")),
    (66, ("Demihuman", "Avian-Harpy")),
    (67, ("Demihuman", "Chiropteran")),
    (68, ("Demihuman", "Lamian")),
    (69, ("Demihuman", "Merhuman")),
    (70, ("Demihuman", "Other")),
    (72, ("Cyborg", "Artificial limbs/organs")),
    (74, ("Cyborg", "Exoskeleton")),
    (76, ("Cyborg", "Mechanical Body")),
    (79, ("Cyborg", "Mechanically Augmented")),
    (82, ("Robot", "Human Shape")),
    (84, ("Robot", "Usuform")),
    (86, ("Robot", "Metamorphic")),
    (87, ("Robot", "Computer")),
    (88, ("Angel/Demon", "-")),
    (89, ("Deity", "-")),
    (90, ("Animal", "-")),
    (91, ("Vegetable", "-")),
    (92, ("Abnormal Chemistry", "-")),
    (93, ("Mineral", "-")),
    (94, ("Gaseous", "-")),
    (95, ("Liquid", "-")),
    (96, ("Energy", "-")),
    (97, ("Ethereal", "-")),
    (98, ("Undead", "-")),
    (99, ("Compound", "-")),
    (100, ("Changeling", "-")),
]

MAJOR_ABILITY = [
    (5, "Feeble"),
    (10, "Poor"),
    (20, "Typical"),
    (40, "Good"),
    (60, "Excellent"),
    (80, "Remarkable"),
    (96, "Incredible"),
    (100, "Amazing")
]

PRIMARY_ABILITY = {
    1: [
        (5, "Feeble"),
        (10, "Poor"),
        (20, "Typical"),
        (40, "Good"),
        (60, "Excellent"),
        (80, "Remarkable"),
        (96, "Incredible"),
        (100, "Amazing")
    ],
    2: [
        (5, "Feeble"),
        (25, "Poor"),
        (75, "Typical"),
        (95, "Good"),
        (100, "Excellent"),
    ],
    3: [
        (5, "Feeble"),
        (10, "Poor"),
        (40, "Typical"),
        (80, "Good"),
        (95, "Excellent"),
        (100, "Remarkable"),
    ],
    4: [
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
    5: [
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

# POWERS
P_AVAILABLE = [
    (12, (1, 3)),
    (26, (2, 4)),
    (41, (3, 5)),
    (55, (4, 6)),
    (66, (5, 7)),
    (75, (6, 8)),
    (83, (7, 9)),
    (89, (8, 10)),
    (94, (9, 12)),
    (97, (10, 12)),
    (99, (12, 14)),
    (100, (14, 18)),
]

P_DEFENSIVE = [
    (15, "Body Armor (D1)"),
    (20, "Force Field (D2)"),
    (23, "Force Field vs. Emotion (D3)"),
    (30, "Force Field vs. Energy (D4)"),
    (35, "Force Field vs. Magic (D5)"),
    (40, "Force Field vs. Mental (D6)"),
    (48, "Force Field vs. Physical (D7)"),
    (50, "Force Field vs. Power Manipulation (D8)"),
    (53, "Force Field vs. Vampirism (D9)"),
    (65, "Reflection (D10)"),
    (70, "Resist: Emotion (D11)"),
    (77, "Resist: Energy (D12)"),
    (82, "Resist: Magic (D13)"),
    (87, "Resist: Mental (D14)"),
    (94, "Resist: Physical (D15)"),
    (97, "Resist: Power Manipulation (D16)"),
    (100, "Resist: Vampirism (D17)"),
]

P_DETECTION = [
    (2, "Abnormal Sensitivity (DT1)"),
    (4, "Circular Vision (DT2)"),
    (10, "Energy Detection (DT3)"),
    (14, "Environmental Awareness (DT4)"),
    (20, "Extradimensional (DT5)"),
    (28, "Hyper-Hearing (DT6)"),
    (34, "Hyper-Olfactory (DT7)"),
    (40, "Hyper-Touch (DT8)"),
    (42, "Life Detection (DT9)"),
    (44, "Magic Detection (DT10)"),
    (50, "Microscopic Vision (DT11)"),
    (54, "Penetration Vision (DT12)"),
    (56, "Power Detection (DT13)"),
    (58, "Psionic Detection (DT14)"),
    (59, "Radarsense (DT15)"),
    (62, "Sonar (DT16)"),
    (69, "Telescopic Vision (DT17)"),
    (79, "Thermal Vision (DT18)"),
    (90, "Tracking (DT19)"),
    (94, "True Sight (DT20)"),
    (98, "UV Vision (DT21)"),
    (100, "Weakness Detection (DT22)"),
]

P_ENERGY_CONTROL = [
    (7, "Absorption Power (EC1)"),
    (10, "Catalytic Control (EC2)"),
    (15, "Coldshaping (EC3)"),
    (18, "Darkforce Manipulation (EC4)"),
    (25, "Electrical Control (EC5)"),
    (28, "Energy Conversion (EC6)"),
    (31, "Energy Solidification (EC7)"),
    (36, "Energy Sponge (EC8)"),
    (38, "Energy Vampirism (EC9)"),
    (45, "Fire Control (EC10)"),
    (49, "Gravity Manipulation (EC11)"),
    (53, "Hard Radiation Control (EC12)"),
    (59, "Kinetic Control (EC13)"),
    (66, "Light Control (EC14)"),
    (73, "Magnetic Manipulation (EC15)"),
    (77, "Plasma Control (EC16)"),
    (80, "Radiowave Control (EC17)"),
    (84, "Shadowshaping (EC18)"),
    (90, "Sound Manipulation (EC19)"),
    (97, "Thermal Control (EC20)"),
    (100, "Vibration Control (EC21)"),
]

P_ENERGY_EMISSION = [
    (10, "Cold Generation (EE1)"),
    (20, "Electrical Generation (EE2)"),
    (22, "Energy Doppelganger (EE3)"),
    (34, "Fire Generation (EE4)"),
    (37, "Hard Radiation (EE5)"),
    (42, "Heat (EE6)"),
    (52, "Kinetic Bolt (EE7)"),
    (62, "Light Emission (EE8)"),
    (72, "Magnetism (EE9)"),
    (75, "Plasma Generation (EE10)"),
    (78, "Radiowave Generation (EE11)"),
    (83, "Shadowcasting (EE12)"),
    (93, "Sonic Generation (EE13)"),
    (100, "Vibration (EE14)"),
]

P_FIGHTING = [
    (20, "Berserker (F1)"),
    (60, "Martial Supremacy (F2)"),
    (75, "Natural Weaponry (F3)"),
    (80, "Weapons Creation* (F4)"),
    (100, "Weapons Tinkering (F5)"),
]

P_ILLUSORY = [
    (15, "Animate Image (I1)"),
    (70, "Illusion-Casting* (I2)"),
    (85, "Illusory Invisibility (I3)"),
    (100, "Illusory Duplication (I4)"),
]

P_LIFEFORM_CONTROL = [
    (14, "Biophysical Control* (L1)"),
    (15, "Bio-Vampirism * (L2)"),
    (18, "Body Transformation-Others (L3)"),
    (26, "Emotion Control (L4)"),
    (32, "Exorcism (L5)"),
    (34, "Force Field vs. Hostiles (L6)"),
    (35, "Forced Reincarnation (L7)"),
    (39, "Grafting* (L8)"),
    (51, "Hypnotic Control (L9)"),
    (60, "Mind Control* (L10)"),
    (62, "Mind Transferral* (L11)"),
    (65, "Neural Manipulation (L12)"),
    (66, "Plague Carrier (L13)"),
    (69, "Plant Control (L14)"),
    (71, "Plant Growth (L15)"),
    (80, "Sense Alteration (L16)"),
    (83, "Shapechange-Others* (L17)"),
    (89, "Sleep-Induced (L18)"),
    (90, "Spirit Storage (L19)"),
    (95, "Summoning (L20)"),
    (100, "Undead Control (L21)"),
]

P_MAGICAL = [
    (8, "Enchantment* (MG1)"),
    (15, "Energy Source (MG2)"),
    (17, "Internal Limbo (MG3)"),
    (25, "Magic Control* (MG4)"),
    (28, "Magic Creation* (MG5)"),
    (33, "Magic Domination (MG6)"),
    (39, "Magic Transferral (MG7)"),
    (41, "Magic Vampirism (MG8)"),
    (71, "Power Simulation (MG9)"),
    (77, "Reality Alteration* (MG10)"),
    (79, "Spirit Vampirism* (MG11)"),
    (95, "Sympathetic Magic (MG12)"),
    (100, "Warding (MG13)"),
]

P_MATTER_CONTROL = [
    (5, "Bonding (MC1)"),
    (17, "Collection (MC2)"),
    (22, "Crystallization (MC3)"),
    (29, "Diminution (MC4)"),
    (39, "Disruption (MC5)"),
    (46, "Enlargement (MC6)"),
    (51, "Geoforce (MC7)"),
    (61, "Matter Animation* (MC8)"),
    (68, "Machine Animation* (MC9)"),
    (73, "Micro-Environment (MC10)"),
    (83, "Molding (MC11)"),
    (93, "Weather (MC12)"),
    (100, "Zombie Animation* (MC13)"),
]

P_MATTER_CONVERSION = [
    (10, "Coloration (MCo1)"),
    (25, "Combustion (MCo2)"),
    (45, "Disintegration (MCo3)"),
    (70, "Elemental Conversion* (MCo4)"),
    (80, "Ionization (MCo5)"),
    (100, "Molecular Conversion* (MCo6)"),
]

P_MATTER_CREATION = [
    (10, "Artifact Creation* (MCr1)"),
    (24, "Elemental Creation (MCr2)"),
    (29, "Lifeform Creation* (MCr3)"),
    (35, "Mechanical Creation* (MCr4)"),
    (59, "Missile Creation (MCr5)"),
    (69, "Molecular Creation (MCr6)"),
    (88, "Spray (MCr7)"),
    (100, "Webcasting (MCr8)"),
]

P_MENTAL_ENHANCEMENT = [
    (4, "Clairaudience (M1)"),
    (8, "Clairvoyance (M2)"),
    (11, "Communicate with Animals (M3)"),
    (12, "Communicate with Cybernetics (M4)"),
    (13, "Communicate with Non-Living (M5)"),
    (15, "Communicate with Plants (M6)"),
    (16, "Cosmic Awareness* (M7)"),
    (22, "Danger Sense (M8)"),
    (23, "Dreamtravel (M9)"),
    (26, "Empathy (M10)"),
    (27, "Free Spirit* (M11)"),
    (31, "Hallucinations* (M12)"),
    (40, "Hyper-Intelligence (M13)"),
    (47, "Hyper-Invention (M14)"),
    (48, "Incarnation Awareness (M15)"),
    (58, "Iron Will (M16)"),
    (65, "Linguistics (M17)"),
    (66, "Mental Duplication (M18)"),
    (67, "Mental Invisibility (M19)"),
    (69, "Mental Probe (M20)"),
    (72, "Mind Blast (M21)"),
    (73, "Mind Drain (M22)"),
    (74, "Postcognition (M23)"),
    (75, "Precognition* (M24)"),
    (76, "Psionic Vampirism* (M25)"),
    (78, "Remote Sensing (M26)"),
    (79, "Sensory Link (M27)"),
    (80, "Serial Immortality* (M28)"),
    (81, "Speechthrowing (M29)"),
    (85, "Telekinesis (M30)"),
    (86, "Telelocation (M31)"),
    (96, "Telepathy (M32)"),
    (100, "Total Memory (M33)"),
]

P_PHYSICAL_ENHANCEMENT = [
    (14, "Armor Skin (P1)"),
    (28, "Body Resistance (P2)"),
    (30, "Chemical Touch (P3)"),
    (33, "Digestive Adaptation (P4)"),
    (40, "Hyper-Speed (P5)"),
    (42, "Hypnotic Voice (P6)"),
    (45, "Lung Adaptability (P7)"),
    (47, "Pheromones (P8)"),
    (60, "Regeneration* (P9)"),
    (62, "Self-Revival* (P10)"),
    (67, "Self-Sustenance (P11)"),
    (71, "Stealth (P12)"),
    (76, "Suspended Animation (P13)"),
    (78, "True Invulnerability* (P14)"),
    (82, "Vocal Control (P15)"),
    (90, "Waterbreathing (P16)"),
    (100, "Water Freedom (P17)"),
]

P_POWER_CONTROL = [
    (8, "Control* (PC1)"),
    (12, "Creation (PC2)"),
    (18, "Domination* (PC3)"),
    (23, "Duplication (PC4)"),
    (37, "Energy Source (PC5)"),
    (39, "Energy Source Creation (PC6)"),
    (49, "Focus (PC7)"),
    (55, "Gestalt (PC8)"),
    (60, "Nemesis (PC9)"),
    (64, "Power Transferral (PC10)"),
    (73, "Power Vampirism * (PC11)"),
    (83, "Residual Absorption (PC12)"),
    (96, "Selection (PC13)"),
    (100, "Weakness Creation* (PC14)"),
]

P_SELF_ALTERATION = [
    (2, "Age-Shift (S1)"),
    (9, "Alter Ego (S2)"),
    (10, "Anatomical Separation (S3)"),
    (13, "Animal Transformation (S4)"),
    (19, "Animal Mimicry (S5)"),
    (21, "Blending (S6)"),
    (27, "Body Adaptation* (S7)"),
    (30, "Body Transformation* (S8)"),
    (33, "Body Coating (S9)"),
    (37, "Bouncing Ball (S10)"),
    (38, "Chemical Mimicry (S11)"),
    (42, "Elongation (S12)"),
    (44, "Energy Body* (S13)"),
    (49, "Energy Sheath (S14)"),
    (55, "Evolution (S15)"),
    (57, "Growth (S16)"),
    (58, "Imitation-Face Changer (S17)"),
    (60, "Imitation-Human Changeling (S18)"),
    (61, "Invisibility (S19)"),
    (62, "Mass Decrease (S20)"),
    (63, "Mass Increase (S21)"),
    (67, "Phasing (S22)"),
    (70, "Physical Gestalt (S23)"),
    (71, "Plant Mimicry (S24)"),
    (74, "Plasticity (S25)"),
    (78, "Prehensile Hair (S26)"),
    (81, "Self-Duplication* (S27)"),
    (84, "Self-Vegetation (S28)"),
    (90, "Shapeshifting (S29)"),
    (94, "Shrinking (S30)"),
    (99, "Spirit Gestalt (S31)"),
    (100, "Two-dimensionality (S32)"),
]

P_TRAVEL = [
    (2, "Astral Body (T1)"),
    (6, "Carrier Wave (T2)"),
    (10, "Dimension Travel (T3)"),
    (12, "Energy Path (T4)"),
    (14, "Floating Disc (T5)"),
    (20, "Gateway* (T6)"),
    (26, "Gliding (T7)"),
    (28, "Hyper-Digging (T8)"),
    (34, "Hyper-Leaping (T9)"),
    (42, "Hyper-Running (T10)"),
    (46, "Hyper-Swimming (T11)"),
    (52, "Levitation (T12)"),
    (56, "Rocket (T13)"),
    (58, "Skywalk (T14)"),
    (64, "Spiderclimb (T15)"),
    (72, "Teleport Self* (T16)"),
    (76, "Teleport Others* (T17)"),
    (78, "Telereformation (T18)"),
    (80, "Time Travel* (T19)"),
    (82, "Troubleseeker (T20)"),
    (93, "True Flight (T21)"),
    (97, "Water Walking (T22)"),
    (100, "Whirlwind (T23)"),
]

P_ORIGIN = [
    (10, "Natal"),
    (20, "Maturity"),
    (30, "Self-Achievement"),
    (35, "Endowment"),
    (50, "Technical Mishap"),
    (60, "Technical Procedure"),
    (65, "Creation"),
    (76, "Biological Exposure"),
    (87, "Chemical Exposure"),
    (98, "Energy Exposure"),
    (00, "Rebirth"),
]

P_CLASS = [
    (5, P_DEFENSIVE),
    (11, P_DETECTION),
    (16, P_ENERGY_CONTROL),
    (24, P_ENERGY_EMISSION),
    (29, P_FIGHTING),
    (31, P_ILLUSORY),
    (35, P_LIFEFORM_CONTROL),
    (40, P_MAGICAL),
    (47, P_MATTER_CONTROL),
    (53, P_MATTER_CONVERSION),
    (57, P_MATTER_CREATION),
    (71, P_MENTAL_ENHANCEMENT),
    (85, P_PHYSICAL_ENHANCEMENT),
    (88, P_POWER_CONTROL),
    (92, P_SELF_ALTERATION),
    (100, P_TRAVEL),
]

# WEAKNESS
W_STIMULUS = [
    (13, "Elemental Allergy"),
    (18, "Molecular Allergy"),
    (43, "Energy Allergy"),
    (68, "Energy Depletion"),
    (81, "Energy Dampening"),
    (94, "Finite Limit"),
    (100, "Psychological"),
]

W_EFFECT = [
    (50, "Power Negation"),
    (90, "Incapacitation"),
    (100, "Fatal"),
]

W_DURATION = [
    (40, "Continuous with Contact"),
    (60, "Limited Duration with Contact"),
    (90, "Limited Duration after Contact"),
    (100, "Permanent"),
]

# Talents
T_AVAILABLE = [
    (12, (0, 3)),
    (26, (1, 4)),
    (41, (1, 6)),
    (55, (2, 4)),
    (66, (2, 6)),
    (75, (2, 8)),
    (83, (3, 4)),
    (89, (3, 6)),
    (94, (4, 8)),
    (97, (4, 4)),
    (99, (5, 6)),
    (100, (6, 8)),
]

# Contacts
C_AVAILABLE = [
    (12, (0, 2)),
    (26, (0, 4)),
    (41, (1, 3)),
    (55, (2, 4)),
    (66, (2, 6)),
    (75, (3, 3)),
    (83, (3, 4)),
    (89, (3, 6)),
    (94, (4, 4)),
    (97, (4, 5)),
    (99, (5, 5)),
    (100, (6, 6)),
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

def roll_primary_ability(ability_column):
    level = percentile(PRIMARY_ABILITY[ability_column])
    rank = INITIAL_RANKS[level]
    return (level, rank)

def column_shift(rank, shift, initial=False):
    new = POWER_LEVELS.index(rank)+shift
    if new < 0:
        new = 0
    if initial:
        # Abilities can't start lower than Feeble
        if new < 1:
            new = 1
        # Abilities can't start higher than Monstrous
        if new > 9:
            new = 9
        return (POWER_LEVELS[new], INITIAL_RANKS[POWER_LEVELS[new]])
    return (POWER_LEVELS[new], POWER_RANKS[POWER_LEVELS[new]])

class Hero(object):
    def __init__(self, base_origin=None):
        if not base_origin:
            base_origin = percentile(ORIGINS)
        self.origin = base_origin[0]
        self.subform = base_origin[1]

        self.notes = []

        # Initial health multiplier
        self.health_mod = 1

        ability_column = self.get_ability_column()
        self.abilities = {}
        for ability in FASERIP:
            self.abilities[ability] = roll_primary_ability(ability_column)

        self.resources = roll_ability()
        self.popularity = set_ability("Good")

        self.powers_available, self.powers_max = percentile(P_AVAILABLE)
        self.talents, self.talents_max = percentile(T_AVAILABLE)
        self.contacts, self.contacts_max = percentile(C_AVAILABLE)

        self.postprocess_origin()
        if self.powers_available < 1:
            self.powers_available = 1

        self.weakness = {
            "Stimulus": percentile(W_STIMULUS),
            "Effect": percentile(W_EFFECT),
            "Duration": percentile(W_DURATION)
        }

        self.power_origin = percentile(P_ORIGIN)
        self.powers = []
        powers = []
        for _ in range(0, self.powers_available):
            new_power = percentile(percentile(P_CLASS))
            # Ignore duplicates
            while new_power in powers:
                new_power = percentile(percentile(P_CLASS))
            powers.append(new_power)

        for power in powers:
            self.powers.append((power, percentile(PRIMARY_ABILITY[4])))

    def __str__(self):
        s = ""
        s += "Origin: %s\n" % (self.origin,)
        s += "Subform: %s\n" % (self.subform,)
        s += "\n"

        for ability in FASERIP:
            s += "%s: %s\n" % (ability, self.abilities[ability])
        s += "\n"

        s += "Health: %d\n" % (self.get_health(),)
        s += "Karma: %d\n" % (self.get_karma(),)
        s += "Resources: %s\n" % (self.resources,)
        s += "Popularity: %s\n" % (self.popularity,)
        s += "\n"

        s += "Weakness:\n"
        for key in ["Stimulus", "Duration", "Effect"]:
            s += "%s: %s\n" % (key, self.weakness[key])
        s += "\n"

        s += "Power Origin: %s\n" % (self.power_origin,)
        s += "Powers (%d/%d):\n" % (self.powers_available, self.powers_max)
        for power in sorted(self.powers):
            s += "%s\n" % (power,)
        s += "\n"

        s += "Talents (%d/%d):\n" % (self.talents, self.talents_max)
        s += "Contacts (%d/%d):\n" % (self.contacts, self.contacts_max)
        s += "\n"

        if self.notes:
            s += "Notes:\n%s" % ('\n'.join(self.notes),)
        return s

    def _cs_primary(self, ability, shift):
        self.abilities[ability] = column_shift(self.abilities[ability][0], shift, True)

    def _note(self, note):
        self.notes.append(note)

    def get_health(self):
        health = 0
        for ability in ["Fighting", "Agility", "Strength", "Endurance"]:
            health += self.abilities[ability][1]
        return health*self.health_mod

    def get_karma(self):
        karma = 0
        for ability in ["Reason", "Intuition", "Psyche"]:
            karma += self.abilities[ability][1]
        return karma

    def get_ability_column(self):
        if self.origin == "Animal" or \
           self.origin == "Ethereal" or \
           self.subform == "Felinoid" or \
           self.origin == "Modified Human" or \
           self.origin == "Mutant" or \
           self.origin == "Undead" or \
           self.origin == "Vegetable":
            return 1
        elif self.origin == "Abnormal Chemistry" or \
             self.subform == "Artificial limbs/organs" or \
             self.subform == "Avian-Harpy" or \
             self.subform == "Chiropteran" or \
             self.origin == "Compound" or \
             self.subform == "Exoskeleton" or \
             self.subform == "Faun" or \
             self.subform == "Merhuman" or \
             self.origin == "Mineral" or \
             self.origin == "Normal Human" or \
             self.subform == "Other" or \
             self.origin == "Surgical Composite":
            return 2
        elif self.subform == "Avian-Angel" or \
             self.subform == "Equiman" or \
             self.subform == "Lamian" or \
             self.subform == "Mechanically Augmented":
            return 3
        elif self.origin == "Android" or \
             self.subform == "Lupinoid" or \
             self.subform == "Mechanical Body" or \
             self.origin == "Robot":
            return 4
        elif self.origin == "Alien" or \
             self.subform == "Alien" or \
             self.origin == "Angel/Demon" or \
             self.subform == "Centaur" or \
             self.origin == "Changeling" or \
             self.origin == "Deity" or \
             self.origin == "Energy" or \
             self.origin == "Gaseous" or \
             self.origin == "Humanoid Race" or \
             self.origin == "Liquid":
            return 5

    def postprocess_origin(self):
        if self.origin == "Normal Human":
            self.resources = column_shift(self.resources[0], 1)
        elif self.origin == "Mutant":
            if self.subform == "Induced":
                self._note("Raise any one Primary Ability +1CS")
            elif self.subform == "Random":
                self.powers_available += 1
                self.resources = column_shift(self.resources[0], -1)
                self._cs_primary("Endurance", 1)
                #self.abilities["Endurance"] = column_shift(self.abilities["Endurance"][0], 1, True)
            elif self.subform == "Breed":
                self._cs_primary("Endurance", 1)
                self._cs_primary("Intuition", 1)
                if self.contacts == 0:
                    self.contacts = 1
            #self.notes = "Increase one power by one rank"
            #self.popularity = set_ability("Shift 0")
            #if self.powers_available < 5:
                #self.powers_available += 1
            #self.abilities["Endurance"] = column_shift(self.abilities["Endurance"][0], 1, True)
        elif self.origin == "Android":
            self.popularity = column_shift(self.popularity[0], -1)
            self._note("Raise any one Primary Ability +1CS")
            self._note("One contact is your creator")
            self.powers_available += 1
            if self.contacts == 0:
                self.contacts = 1
        elif self.origin == "Humanoid Race":
            self._note("Raise any one Primary Ability +1CS")
            self._note("Contact must be your race")
            self.resources = set_ability("Poor")
            self.contacts = 1
        elif self.origin == "Surgical Composite":
            self._cs_primary("Strength", 1)
            self._cs_primary("Fighting", 1)
            self._cs_primary("Endurance", 1)
            self._note("Resistance to Mental Domination -1CS")
            self._note("Heal twice as quickly as Normal Humans")
            self.popularity = set_ability("Shift 0")
            self.resources = set_ability("Poor")
        elif self.origin == "Modified Human":
            if self.subform == "Organic":
                self._note("Heal twice as quickly as Normal Humans")
            elif self.subform == "Muscular":
                self._cs_primary("Strength", 1)
                self._cs_primary("Endurance", 1)
            elif self.subform == "Skeletal":
                self._note("+1CS Resistance to Physical Attacks")
            elif self.subform == "Extra Parts":
                self._cs_primary("Fighting", 1)
                self._note("Duplicate organs double Health")
                self._note("Tails give +1 attack per tail when using blunt attacks")
                self._note("Wings give Flight")
            self._note("One contact from organization responsible for modification")
            self.powers_available -= 1
        elif self.origin == "Demihuman":
            if self.subform == "Centaur":
                self._cs_primary("Strength", 1)
                self._note("Fast: Move 4 areas/turn horizontally")
                self._note("Can fight with hooves")
                self._note("Feeble Climbing ability")
            elif self.subform == "Equiman":
                self._note("Kicking does +1CS damage")
            elif self.subform == "Faun":
                self._note("Feeble Mental Domination over human(oid) females")
                self._note("Slow popularity progression")
                self.popularity = set_ability("Shift 0")
            elif self.subform == "Felinoid":
                self._note("Excellent night vision")
                self._note("+1CS Climbing")
            elif self.subform == "Lupinoid":
                self.popularity = column_shift(self.popularity[0], -1)
                self._note("Excellent sense of smell")
                self._note("Starting popularity is minimum")
            elif self.subform == "Avian-Angel":
                self.popularity = column_shift(self.popularity[0], 1)
            elif self.subform == "Avian-Harpy":
                self._cs_primary("Fighting", 1)
            elif self.subform == "Chiropteran":
                # TODO: Actually put this in as a power later
                self._note("Active Sonar Power at Good")
                self.popularity = set_ability("Feeble")
            elif self.subform == "Lamian":
                self.popularity = set_ability("Shift 0")
                if random.randint(0, 1):
                    self._note("You are venomous")
                self._note("+1CS to Escape")
            elif self.subform == "Merhuman":
                self.popularity = column_shift(self.popularity[0], 1)
                self._note("Dries out away from water")
                self._note("Limited to crawling on dry land")
                self._note("Can fascinate Normal Humans")
            elif self.subform == "Other":
                # This section effectively says "make it up"
                self._note("Work with the Judge to come up with stats")
        elif self.origin == "Cyborg":
            if self.subform == "Artificial limbs/organs":
                self._cs_primary("Intuition", -1)
            elif self.subform == "Exoskeleton":
                # Nothing to do here
                pass
            elif self.subform == "Mechanical Body":
                self._cs_primary("Intuition", -1)
                self._cs_primary("Psyche", -1)
                self.contacts = 1
                self._note("Monstrous Resistance to Disease and Poison")
                self._note("Vulnerable to Magnetic attacks and rust")
                self._note("Contact is the lab that created you")
            elif self.subform == "Mechanically Augmented":
                self.powers_available -= 1
        elif self.origin == "Robot":
            if self.subform == "Human Shape":
                self.popularity = column_shift(self.popularity[0], 1)
            elif self.subform == "Usuform":
                pass
            elif self.subform == "Metamorphic":
                # TODO: Actually roll this
                self._note("Two forms with different Abiltiies and Powers")
                self._note("Additional forms at -1CS to all Primary Abilities")
            elif self.subform == "Computer":
                self._note("Possess at least one remotely controlled industrial robot")
                self._cs_primary("Reason", 2)
                self._cs_primary("Fighting", -1)
                self.resources = column_shift(self.resources[0], 1)
                self._note("Decreased Resistance to Electrical, Magnetic, and Phasing attacks")
                self._note("Loss of electircal power causes loss of all Karma and -1CS to all Abilities and Powers")
        elif self.origin == "Angel/Demon":
            self.contacts = 0
            self._cs_primary("Fighting", 1)
            self._cs_primary("Agility", 1)
            self._cs_primary("Strength", 1)
            self._cs_primary("Endurance", 1)
            self._note("Psychological Weakness that Negates your Power")

            self.subform = "Angel"
            if random.randint(0, 1):
                self.subform = "Demon"
                self.popularity = column_shift(self.popularity[0], -2)
                # TODO: Add these as powers
                self._note("Power: Good Fire Generation")
                self._note("Power: Specific Invulnerability to Heat and Fire")
            else:
                self.popularity = column_shift(self.popularity[0], 2)
                self._note("Power: Artifact Creation - Create Excellent magical sword")
        elif self.origin == "Deity":
            self._cs_primary("Fighting", 2)
            self._cs_primary("Agility", 2)
            self._cs_primary("Strength", 2)
            self._cs_primary("Endurance", 2)
            self._cs_primary("Reason", 2)
            self._cs_primary("Intuition", 2)
            self._cs_primary("Psyche", 2)
            self.powers_available += 2
            # TODO: Actually roll this
            self._note("Bonus Travel Power")
            self._note("+2CS Popularity with public, Shift 0 popularity with religious organizations")
            self._note("Promoting a religion based on yourself causes -1CS on all Abilities and Powers")
        elif self.origin == "Animal":
            # TODO: Add a way to have Alien subform
            if self.subform == "Alien":
                pass
            self.powers_available -= 1
            self.resources = set_ability("Shift 0")
            self._note("Have to have a human Contact")
            # TODO: Add these as actual powers
            self._note("Two bonus Detection Powers at Good rank")
        elif self.origin == "Vegetable":
            self.resources = set_ability("Shift 0")
            self._cs_primary("Fighting", -2)
            self._cs_primary("Endurance", 2)
            self.contacts = 0
            # TODO: Add this as an actual power
            self._note("Power: Good rank Absorption Power")
            self._note("Light or water deprivation causes -1CS in Strength and Endurance per day after 3 days")
            self._note("You have no legal rights")
        elif self.origin == "Abnormal Chemistry":
            self._cs_primary("Endurance", 1)
            self._note("Blood is poisonous to those who consume it")
        elif self.origin == "Mineral":
            self.health_mod = 2
            self._note("Immune to normal Poisons and Diseases")
            self._note("-1CS Movement rate")
        elif self.origin == "Gaseous":
            self.resources = set_ability("Shift 0")
            self.contacts = 0
            self._note("Immobilized if turned into a liquid or solid")
            # TODO: Add this as an actual power
            self._note("Bonus Power: Phasing to penetrate solids")
        elif self.origin == "Liquid":
            self._note("If Endurance and Psyche are at least Excellent, can take a human form")
            self._note("If frozen, immobilized until melted, but immune to damage")
            self._note("Vaporization is fatal")
            self._note("Initial contacts can only be with same race")
            # TODO: Add this as an actual power
            self._note("Bonus Power: Phasing, for porous materials")
        elif self.origin == "Energy":
            self._note("-1CS vulnerability to Plasma C control")
            self._note("Can be immobilized in special storage batteries")
            self._note("Can only be destroyed by Negate or Solidify Energy")
            self._note("Physical contact caused Feeble damage")
            # TODO: Add this as sn actual power
            self._note("Bonus Power: Energy Emission")
            self._note("Optional Power: Energy Control")
        elif self.origin == "Ethereal":
            self._note("Immune to physical attacks lower than Monstrous")
            self._note("Vulnerable to Mental and Magical attacks")
            self._note("Completely destroyed by Spirit Vampirism")
            self._note("Turned into a Poltergeist by Psi-Vampirism")
            self._note("Fighting is Shift Zero unless fighting another Ethereal")
            self._note("Physical attacks are -9CS less effective")
            self._note("At least one contact can be a Spiritual Medium")
        elif self.origin == "Undead":
            self._cs_primary("Strength", 1)
            self._cs_primary("Endurance", 1)
            self._note("Requires a maintenance procedure unless you have Vampiric Power")
            self._note("Psychological Weakness: Power negated when within 10' of a religious symbol")
            self._note("If near religious symbol of own religion, suffer Excellent damage")
        # TODO: Make this work.
        elif self.origin == "Compound":
            self._note("Run this program multiple times and combine what you get")
        # TODO: Make this work.
        elif self.origin == "Changeling":
            self._note("You have complicated transformation abilities, consult the relevant section of the rules to learn more")
        else:
            raise(Exception("Invalid origin: %s" % (self.origin,)))


def test_origins():
    for origin in ORIGINS:
        print origin[1]
        hero = Hero(origin[1])

def test_gen_powers():
    for p_class in P_CLASS:
        percentile(p_class[1])

def main():
    hero = Hero()
    print hero


if __name__ == '__main__':
    main()
