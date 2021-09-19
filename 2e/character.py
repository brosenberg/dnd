#!/usr/bin/env python3

import argparse
import json
import os
import random

from dice import roll
from spells import Spells
from roll_abilities import get_abilities


def load_table(fname):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    return json.load(open(f"{base_dir}/tables/{fname}"))


ABILITIES = load_table("abilities.json")
RACES = load_table("races.json")
CLASSES = load_table("classes.json")
CLASS_GROUPS = load_table("class_groups.json")
CLASS_SPELLS = load_table("class_spells.json")
SPELL_PROGRESSION = load_table("spell_progression.json")
WISDOM_CASTERS = load_table("wisdom_casters.json")


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
    elif class_name == "Ranger":
        caster = "Ranger"
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


def get_spell_levels(class_name, level, wisdom):
    caster_group = get_caster_group(class_name)
    level = str(level)
    wisdom = int(wisdom)
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


def get_spell_list(class_name):
    try:
        return CLASS_SPELLS[class_name]["List"]
    except KeyError:
        pass
    caster = get_class_group(class_name)
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
            self.spell_levels = get_spell_levels(
                self.char_class, self.level, self.abilities["Wisdom"]
            )
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
            for spell_level in range(1, len(self.spell_levels) + 1):
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
        def add_spell(spell_level, spell):
            self.spells[spell_level].append(spell)

        spell_gen = Spells()
        specialization = get_spell_specialization(self.char_class)
        includes = get_spell_includes(self.char_class)
        excludes = get_spell_excludes(self.char_class)
        spell_list = get_spell_list(self.char_class)
        for spell_level in range(1, len(self.spell_levels) + 1):
            if spell_level not in self.spells:
                self.spells[spell_level] = []
            spell_count = self.spell_levels[spell_level - 1]
            if specialization:
                add_spell(
                    spell_level,
                    spell_gen.random_school_sphere_spell(
                        spell_level, specialization, spell_list
                    ),
                )
                spell_count -= 1
            if excludes is not None:
                for _ in range(0, spell_count):
                    add_spell(
                        spell_level,
                        spell_gen.random_exclude_school_sphere_spell(
                            spell_level, spell_list, excludes
                        ),
                    )
            elif includes is not None:
                for _ in range(0, spell_count):
                    add_spell(
                        spell_level,
                        spell_gen.random_include_school_sphere_spell(
                            spell_level, spell_list, includes
                        ),
                    )
            else:
                caster_class = self.caster_group
                for _ in range(0, spell_count):
                    add_spell(
                        spell_level, spell_gen.random_spell(spell_level, caster_class)
                    )


def main():
    parser = argparse.ArgumentParser(description="Create a character")
    # print(Character(get_random_class(), level=20))
    # for class_name in get_all_classes():
    #    print(Character(char_class=class_name, level=10))
    # print(get_spell_levels("Cleric", 8, 5))
    for char_class in [
        "Mage",
        "Abjurer",
        "Ranger",
        "Paladin",
        "Bard",
        "Cleric",
        "Diviner",
    ]:
        print(Character(char_class=char_class, level=15))


if __name__ == "__main__":
    main()
