#!/usr/bin/env python3

import argparse
import json
import os
import random

from dice import roll
from items import get_ac
from spells import Spells
from roll_abilities import get_abilities
from utils import load_table


ABILITIES = load_table("abilities.json")
ABILITY_MODS = {
    "Strength": load_table("strength.json"),
    "Extrao Strength": load_table("extrao_strength.json"),
    "Dexterity": load_table("dexterity.json"),
    "Constitution": load_table("constitution.json"),
    "Intelligence": load_table("intelligence.json"),
    "Wisdom": load_table("wisdom.json"),
    "Charisma": load_table("charisma.json"),
}
ABILITY_ROLLS = load_table("ability_rolls.json")
ALIGNMENTS = load_table("alignments.json")
CLASSES = load_table("classes.json")
CLASS_GROUPS = load_table("class_groups.json")
CLASS_SPELLS = load_table("class_spells.json")
NWPS = load_table("nwps.json")
NWP_GROUPS = load_table("nwp_groups.json")
RACES = load_table("races.json")
SPELL_PROGRESSION = load_table("spell_progression.json")
THAC0 = load_table("thac0.json")
WISDOM_CASTERS = load_table("wisdom_casters.json")


def combine_minimums(minimums):
    minimum = {x: 0 for x in ABILITIES}
    for minima in minimums:
        for ability in minima:
            if minimum[ability] < minima[ability]:
                minimum[ability] = minima[ability]
    return minimum


def constitution_hp_modifier(con, class_group):
    if con <= 1:
        return -3
    elif con < 4:
        return -2
    elif con < 7:
        return -1
    elif con < 15:
        return 0
    elif con == 15:
        return 1
    elif class_group != "Warrior" or con == 16:
        return 2
    elif con == 17:
        return 3
    elif con == 18:
        return 4
    elif con < 21:
        return 5
    elif con < 24:
        return 6
    else:
        return 7


def convert_height(height):
    feet = int(height / 12)
    inches = height - (12 * feet)
    return f"{feet}'{inches}\""


def dexterity_mods(dexterity):
    return ABILITY_MODS["Dexterity"][str(dexterity)]


def dexterity_ac_mod(dexterity):
    return dexterity_mods(dexterity)[2]


def dexterity_to_hit(dexterity):
    return dexterity_mods(dexterity)[1]


def get_ability_priority(class_name):
    return CLASSES[class_name]["Primary"] + random.sample(
        CLASSES[class_name]["Secondary"], len(CLASSES[class_name]["Secondary"])
    )


def get_alignment_by_classes(classes):
    alignments = set(CLASSES[classes[0]]["Alignments"])
    for class_name in classes[1:]:
        alignments = alignments.intersection(set(CLASSES[class_name]["Alignments"]))
    return random.choice(alignments)


def get_all_classes():
    return list(CLASSES.keys())


def get_caster_group(class_name):
    if class_name == "Paladin":
        caster = "Paladin"
    elif class_name == "Ranger":
        caster = "Ranger"
    elif class_name == "Bard":
        caster = "Bard"
    else:
        caster = get_class_groups([class_name])[0]
    if caster in SPELL_PROGRESSION.keys():
        return caster
    return None


def get_caster_groups(classes):
    return [get_caster_group(x) for x in classes]


def get_class_group(class_name):
    return [x for x in CLASS_GROUPS if class_name in CLASS_GROUPS[x]["Classes"]][0]


def get_class_groups(classes):
    try:
        return list(set([get_class_group(x) for x in classes]))
    except:
        breakpoint()


def get_level_by_experience(class_name, experience):
    for index in range(0, len(CLASSES[class_name]["Levels"])):
        if experience < CLASSES[class_name]["Levels"][index]:
            return index
    return 20


def get_levels_by_experience(classes, experience):
    levels = []
    exp_per_class = int(experience / len(classes))
    for class_name in classes:
        levels.append(get_level_by_experience(class_name, exp_per_class))
    return levels


def get_level_limits(race, classes, abilities):
    limits = []
    for class_name in classes:
        limits.append(
            RACES[race]["Limits"][class_name] + level_limit_bonus(class_name, abilities)
        )
    return limits


def get_nwp_slots(class_groups, level, intelligence):
    base_nwps = 0
    nwp_rate = 99
    for class_group in class_groups:
        if CLASS_GROUPS[class_group]["Proficiencies"]["Nonweapon"][0] > base_nwps:
            base_nwps = CLASS_GROUPS[class_group]["Proficiencies"]["Nonweapon"][0]
        if CLASS_GROUPS[class_group]["Proficiencies"]["Nonweapon"][1] < nwp_rate:
            nwp_rate = CLASS_GROUPS[class_group]["Proficiencies"]["Nonweapon"][1]
    return (
        base_nwps
        + int(level / nwp_rate)
        + intelligence_bonus_proficiencies(intelligence)
    )


# TODO: Make this return multiclasses sometimes
def get_random_classes(class_group=None, alignment=None):
    classes = set(CLASSES.keys())
    if alignment:
        alignment_classes = set()
        for class_name in CLASSES:
            if alignment in CLASSES[class_name]["Alignments"]:
                alignment_classes.add(class_name)
        classes = classes.intersection(alignment_classes)
    if class_group:
        classes = classes.intersection(set(CLASS_GROUPS[class_group]["Classes"]))
    return [random.choice(list(classes))]


def get_random_experience_by_level(class_name, level):
    if level < 20:
        return random.randint(
            CLASSES[class_name]["Levels"][level - 1],
            CLASSES[class_name]["Levels"][level],
        )
    else:
        xp = CLASSES[class_name]["Levels"][19]
        return xp + random.randint(0, xp / 10)


# TODO: Have this return an array instead
def get_random_experience_by_levels(classes, level):
    experience = 0
    for class_name in classes:
        experience += get_random_experience_by_level(class_name, level)
    return experience


def get_random_race_by_classes(classes):
    races = set()
    races = set(CLASSES[classes[0]]["Races"])
    for class_name in classes[1:]:
        races = races.intersection(set(CLASSES[class_name]["Races"]))
    return random.choice(list(races))


def get_spell_levels(class_name, level, wisdom):
    caster_group = get_caster_group(class_name)
    level = str(level)
    spells = SPELL_PROGRESSION[caster_group][level]
    # Specialists get a bonus spell per level
    if get_spell_specialization(class_name):
        spells = [x + 1 for x in spells]
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


def get_spell_includes(class_name):
    try:
        return CLASS_SPELLS[class_name]["Include"]
    except KeyError:
        return None


def get_spell_excludes(class_name):
    try:
        return CLASS_SPELLS[class_name]["Exclude"]
    except KeyError:
        return None


def get_spell_subtype(class_name):
    try:
        return CLASS_SPELLS[class_name]["Subtype"]
    except KeyError:
        pass
    caster = get_class_groups([class_name])[0]
    if caster == "Priest":
        return "Sphere"
    elif caster == "Wizard":
        return "School"
    return None


def get_spell_specialization(class_name):
    try:
        return CLASS_SPELLS[class_name]["Specialization"]
    except KeyError:
        return None


def generate_characteristics(race, level):
    race_chars = RACES[race]["Characteristics"]
    characteristics = {"Gender": random.choice(["Female", "Male"])}
    gender_index = 0
    if characteristics["Gender"] == "Female":
        gender_index = 1
    characteristics["Height"] = roll(
        race_chars["Height"][2],
        race_chars["Height"][3],
        race_chars["Height"][gender_index],
    )
    characteristics["Weight"] = roll(
        race_chars["Weight"][2],
        race_chars["Weight"][3],
        race_chars["Weight"][gender_index],
    )
    characteristics["Age"] = roll(
        race_chars["Age"][1], race_chars["Age"][2], race_chars["Age"][0]
    )
    characteristics["Age"] += roll(level, race_chars["Age"][3], -level)
    if characteristics["Age"] >= race_chars["Age"][4]:
        characteristics["Age"] -= roll(2, race_chars["Age"][3], 0)
    return characteristics


def intelligence_mods(intelligence):
    return ABILITY_MODS["Intelligence"][str(intelligence)]


def intelligence_bonus_proficiencies(intelligence):
    return intelligence_mods(intelligence)[0]


def level_limit_bonus(class_name, abilities):
    prime_reqs = CLASSES[class_name]["Requisite"]
    lowest = 99
    for prime_req in prime_reqs:
        prime_req_score = abilities[prime_req]
        if prime_req_score < lowest:
            lowest = prime_req_score
    if lowest > 18:
        return 4
    elif lowest > 17:
        return 3
    elif lowest > 15:
        return 2
    elif lowest > 13:
        return 1
    return 0


def strength_mods(strength, extrao_str):
    if extrao_str:
        if extrao_str < 51:
            extrao_str = "50"
        elif extrao_str < 76:
            extrao_str = "75"
        elif extrao_str < 91:
            extrao_str = "90"
        elif extrao_str < 100:
            extrao_str = "99"
        else:
            extrao_str = "100"
        return ABILITY_MODS["Extrao Strength"][extrao_str]
    else:
        return ABILITY_MODS["Strength"][str(strength)]


def strength_damage(strength, extrao_str=None):
    return strength_mods(strength, extrao_str)[1]


def strength_to_hit(strength, extrao_str=None):
    return strength_mods(strength, extrao_str)[0]


def wisdom_bonus_spells(wisdom):
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
    def __init__(
        self,
        classes=[],
        class_group=None,
        abilities=None,
        race=None,
        level=1,
        alignment=None,
        experience=None,
        expanded=False,
    ):
        self.expanded = expanded
        self.classes = [classes]

        # Determine a class
        if not self.classes:
            self.classes = get_random_classes(
                class_group=class_group, alignment=alignment
            )
        self.class_groups = get_class_groups(self.classes)

        # Choose a race
        self.race = race
        if not self.race:
            self.race = get_random_race_by_classes(self.classes)

        # Assign alignment
        self.alignment = alignment
        if not self.alignment:
            self.alignment = get_alignment_by_classes(self.classes)

        # Calculate experience
        if experience is not None:
            self.experience = experience
            self.levels = get_levels_by_experience(self.classes, experience)
        else:
            self.levels = [level for x in self.classes]
            self.experience = get_random_experience_by_levels(self.classes, self.levels)

        # Roll abilities if necessary
        self.abilities = abilities
        if not self.abilities:
            minimums = combine_minimums(
                [CLASSES[x]["Minimums"] for x in classes]
                + [RACES[self.race]["Minimums"]]
            )
            ability_rolls = ABILITY_ROLLS[str(self.level)]
            self.abilities = get_abilities(
                get_ability_priority(self.classes),
                minimums,
                RACES[self.race]["Maximums"],
                RACES[self.race]["Ability Modifiers"],
                order=ability_rolls,
                extrao_str="Warrior" in self.class_groups and self.race != "Halfling",
            )

        # Apply level limits
        self.level_limits = get_level_limits(self.race, self.classes, self.abilities)
        for index in range(0, len(self.levels)):
            if self.levels[index] > self.level_limit[index]:
                self.levels[index] = self.level_limit[index]

        # Calculate hitpoints
        # FIXME: The Con mod is being applied per level, not per HD
        hps = []
        for index in range(0, len(self.levels)):
            class_group = self.class_groups[index]
            level = self.levels[index]
            hps.append(
                roll(
                    CLASS_GROUPS[class_group]["Hit Dice"][level - 1][0],
                    CLASS_GROUPS[class_group]["Hit Die"],
                    CLASS_GROUPS[class_group]["Hit Dice"][level - 1][1]
                    + level
                    * constitution_hp_modifier(
                        self.abilities["Constitution"], self.class_groups
                    ),
                )
            )
        self.hp = int(sum(hps) / len(self.levels))

        # Determine if this character can cast spells, and assign them if so
        self.spell_levels = {}
        self.spells = {}
        self.caster_groups = get_caster_groups(self.classes)
        if self.caster_groups:
            for index in range(0, len(self.classes)):
                self.spell_levels[class_name] = get_spell_levels(
                    self.classes[index], self.levels[index], self.abilities["Wisdom"]
                )
            self.populate_spells()

        # Assign proficiencies
        self.nwp_slots = get_nwp_slots(
            self.class_groups, self.level, self.abilities["Intelligence"]
        )
        self.profs = {"NWP": [], "Weapon": [], "Languages": ["Common"]}
        if "Thief" in self.classes:
            self.profs["Languages"].append("Thieves' Cant")
        elif "Druid" in self.classes:
            self.druid_lang_known = 0
        self.assign_nwps()

        # Determine misc. stats
        self.thac0 = THAC0[self.class_group][self.level - 1]
        self.ac = 10 + dexterity_ac_mod(self.abilities["Dexterity"])
        self.equipment = []
        self.characteristics = generate_characteristics(self.race, max(self.levels))

    def __str__(self):
        self.update_ac()
        dex_hit_mod = dexterity_to_hit(self.abilities["Dexterity"])
        str_hit_mod = strength_to_hit(
            self.abilities["Strength"], self.abilities["Extrao Strength"]
        )
        s = f"{'-'*10}\n"

        ### Race, Class, Alignment, HP, AC, THAC0
        classes_str = "/".join(self.classes)
        levels_str = "/".join(self.levels)
        s += f"{self.alignment} {self.race} {classes_str} {levels_str}"
        s += f"XP: {self.experience:,} - "
        if self.level_limit > 98:
            s += "Unlimited level limit\n"
        else:
            level_limits_str = "/".join(self.level_limits)
            s += f"Level limit: {level_limits_str}\n"
        s += f"HP: {self.hitpoints}  AC: {self.ac}  THAC0: {self.thac0} (Melee:{self.thac0-str_hit_mod}/Ranged:{self.thac0-dex_hit_mod})\n"

        ### Abilities
        for ability in ABILITIES:
            details = ""
            ability_val = str(self.abilities[ability])
            if ability == "Strength":
                hit_mod = str_hit_mod
                dmg_mod = strength_damage(
                    self.abilities["Strength"], self.abilities["Extrao Strength"]
                )
                if self.abilities["Extrao Strength"]:
                    ability_val += f'/{self.abilities["Extrao Strength"]}'
                if hit_mod >= 0:
                    hit_mod = f"+{hit_mod}"
                if dmg_mod >= 0:
                    dmg_mod = f"+{dmg_mod}"
                details = f"{hit_mod} to hit/{dmg_mod} damage"
            elif ability == "Dexterity":
                hit_mod = dex_hit_mod
                ac_mod = dexterity_ac_mod(self.abilities["Dexterity"])
                if hit_mod >= 0:
                    hit_mod = f"+{hit_mod}"
                if ac_mod > 0:
                    ac_mod = f"+{ac_mod}"
                details = f"{hit_mod} to hit/{ac_mod} AC"
            elif ability == "Intelligence":
                bonus_nwps = intelligence_bonus_proficiencies(
                    self.abilities["Intelligence"]
                )
                details = f"{bonus_nwps} bonus NWPs"
            if details:
                details = f" ({details})"
            s += f"{ability+':':13} {ability_val:>5} {details}\n"
        s += "\n"

        ### Characteristics
        s += f"{self.characteristics['Gender']}  {convert_height(self.characteristics['Height'])}  {self.characteristics['Weight']} lbs.  {self.characteristics['Age']} years old\n"
        s += "\n"

        ### Proficiencies
        s += f"Proficiencies ({self.nwp_slots}):\n"
        for nwp in self.profs["NWP"]:
            modifier = "N/A"
            ability = NWPS[nwp][1]
            if ability != "N/A":
                modifier = self.abilities[ability] + NWPS[nwp][2]
                if "Ranger" in self.classes and nwp == "Tracking":
                    modifier += int(self.level / 3)
            s += f"\t{nwp:20} {ability:12}  Mod: {modifier:2}  Slots: {NWPS[nwp][0]}\n"

        ### Languages
        s += f"Languages known: {', '.join(self.profs['Languages'])}\n"

        ### Spells
        if self.spell_levels:
            s += "\nSpells:"
            for class_name in self.spell_levels:
                s += f"{class_name} ({'/'.join([str(x) for x in self.spell_levels[class_name]])}):\n"
                for spell_level in range(1, len(self.spell_levels[class_name]) + 1):
                    s += f"\t{spell_level}: "
                    cur_spells = []
                    for spell in sorted(set(self.spells[class_name][spell_level])):
                        count = ""
                        if self.spells[class_name][spell_level].count(spell) > 1:
                            count = f" ({self.spells[class_name][spell_level].count(spell)})"
                        cur_spells.append(f"{spell}{count}")
                    s += f"{'; '.join(cur_spells)}\n"

        ### Equipment
        if self.equipment:
            items = []
            for item in self.equipment:
                ac, ac_bonus = get_ac(item)
                if ac is not None:
                    item = f"{item} (AC: {ac})"
                elif ac_bonus is not None:
                    if ac_bonus >= 0:
                        item = f"{item} (AC +{ac_bonus})"
                    else:
                        item = f"{item} (AC {ac_bonus})"
                items.append(item)
            s += "\n"
            s += "Equipment:\n\t" + "\n\t".join(items)
        s += f"\n{'-'*10}"
        return s

    def add_equipment(self, item):
        self.equipment.append(item)

    def assign_nwps(self):
        slots = self.nwp_slots
        possible_nwps = []
        if "Bard" in self.classes:
            self.profs["NWP"].append("Local History")
            self.profs["NWP"].append("Reading/Writing")
        elif "Ranger" in self.classes:
            self.profs["NWP"].append("Tracking")
        for class_name in self.classes:
            for group in CLASSES[class_name]["Proficiency Groups"]:
                possible_nwps += NWP_GROUPS[group]
        possible_nwps = list(set(possible_nwps))
        while slots:
            # 50% chance for each slot to give demi-humans their racial language
            if (
                self.race not in ["Human", "Half-Elf"]
                and roll(1, 100, 0) > 50
                and RACES[self.race]["Languages"][0] not in self.profs["Languages"]
            ):
                self.profs["Languages"].append(RACES[self.race]["Languages"][0])
                slots -= 1
            # 20% - 2*(Number of Languages) chance for each slot to learn a language
            elif roll(1, 100, 0) < 20 - 2 * len(self.profs["Languages"]):
                languages = []
                if self.race != "Human":
                    if self.race != "Half-Elf":
                        if (
                            RACES[self.race]["Languages"][0]
                            not in self.profs["Languages"]
                        ):
                            self.profs["Languages"].append(
                                RACES[self.race]["Languages"][0]
                            )
                            slots -= 1
                            continue
                    languages = RACES[self.race]["Languages"]
                else:
                    languages = load_table("languages.json")
                if "Druid" in self.classes and self.druid_lang_known / self.level > 1:
                    languages += load_table("druid_languages.json")
                languages = list(set(languages) - (set(self.profs["Languages"])))
                # Make sure this character hasn't learned all of their possible languages
                if languages:
                    self.profs["Languages"].append(random.choice(languages))
                    slots -= 1
            else:
                new_nwp = random.choice(possible_nwps)
                while NWPS[new_nwp][0] > slots:
                    new_nwp = random.choice(possible_nwps)
                self.profs["NWP"].append(new_nwp)
                slots -= NWPS[new_nwp][0]
                possible_nwps.remove(new_nwp)

    def populate_spells(self):
        spell_gen = Spells(expanded=self.expanded)
        for class_name in self.spell_levels:

            def add_spell(spell_level, spell):
                if spell is None:
                    raise TypeError("Can't assign None as spell")
                self.spells[class_name][spell_level].append(spell)

            specialization = get_spell_specialization(class_name)
            includes = get_spell_includes(class_name)
            excludes = get_spell_excludes(class_name)
            spell_subtype = get_spell_subtype(class_name)
            for spell_level in range(1, len(self.spell_levels[class_name]) + 1):
                if spell_level not in self.spells[class_name]:
                    self.spells[class_name][spell_level] = []
                spell_count = self.spell_levels[class_name][spell_level - 1]
                if specialization:
                    add_spell(
                        spell_level,
                        spell_gen.random_school_sphere_spell(
                            spell_level, specialization, spell_subtype
                        ),
                    )
                    spell_count -= 1
                if excludes is not None:
                    for _ in range(0, spell_count):
                        add_spell(
                            spell_level,
                            spell_gen.random_standard_school_sphere_spell(
                                spell_level, spell_subtype, excludes=excludes
                            ),
                        )
                elif includes is not None:
                    for _ in range(0, spell_count):
                        add_spell(
                            spell_level,
                            spell_gen.random_include_school_sphere_spell(
                                spell_level, spell_subtype, includes
                            ),
                        )
                else:
                    caster_class = get_caster_group(class_name)
                    for _ in range(0, spell_count):
                        add_spell(
                            spell_level,
                            spell_gen.random_spell(spell_level, caster_class),
                        )

    def update_ac(self):
        if "Bracers of Defenselessness" in self.equipment:
            self.ac = 10
            return
        mods = [dexterity_ac_mod(self.abilities["Dexterity"])]
        base_ac = 10
        for item in self.equipment:
            ac, ac_bonus = get_ac(item)
            if ac is not None:
                if ac < base_ac:
                    base_ac = ac
            elif ac_bonus is not None:
                mods.append(-ac_bonus)
        self.ac = base_ac + sum(mods)


def main():
    parser = argparse.ArgumentParser(description="Create a character")
    parser.add_argument(
        "-x",
        "--expanded",
        default=False,
        action="store_true",
        help="use expanded generation tables",
    )
    args = parser.parse_args()
    for class_name in get_all_classes():
        print(Character(classes=[class_name], level=15, expanded=args.expanded))


if __name__ == "__main__":
    main()
