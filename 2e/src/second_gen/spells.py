#!/usr/bin/env python3

import json
import os
import random

from second_gen.utils import load_table


def flatten_schools(spell_list):
    spells = {
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
        "7": [],
        "8": [],
        "9": [],
    }
    for school in spell_list:
        for level in spell_list[school]:
            spells[level] += spell_list[school][level]
    for level in spells:
        spells[level] = sorted(list(set(spells[level])))
    return spells


class Spells(object):
    def __init__(self, expanded=False):
        extension = ""
        if expanded:
            extension = "_expanded"
        self.spells = {
            "School": load_table(f"wizard_spells{extension}.json", subdir="spells"),
            "Sphere": load_table(f"priest_spells{extension}.json", subdir="spells"),
        }
        self.spells["Wizard"] = flatten_schools(self.spells["School"])
        self.spells["Priest"] = flatten_schools(self.spells["Sphere"])

    def random_spell(self, spell_level, caster_class):
        spell_level = str(spell_level)
        return random.choice(self.spells[caster_class][spell_level])

    def random_exclude_school_sphere_spell(self, spell_level, spell_list, excludes):
        spell_level = str(spell_level)
        possible = []
        for school_sphere in list(set(self.spells[spell_list].keys() - set(excludes))):
            try:
                possible += self.spells[spell_list][school_sphere][spell_level]
            except KeyError:
                pass
        return random.choice(list(set(possible)))

    def random_include_school_sphere_spell(self, spell_level, spell_list, includes):
        spell_level = str(spell_level)
        possible = []
        for school_sphere in includes:
            try:
                possible += self.spells[spell_list][school_sphere][spell_level]
            except KeyError:
                pass
        return random.choice(list(set(possible)))

    def random_school_sphere_spell(self, spell_level, school_sphere, spell_list):
        spell_level = str(spell_level)
        try:
            return random.choice(self.spells[spell_list][school_sphere][spell_level])
        except KeyError:
            return None

    def random_standard_school_sphere_spell(self, spell_level, spell_list, excludes=[]):
        schools_spheres = []
        if spell_list == "Wizard" or spell_list == "School":
            spell_list = "School"
            schools_spheres = load_table("standard_schools.json", subdir="spells")
        elif spell_list == "Priest" or spell_list == "Sphere":
            spell_list = "Sphere"
            schools_spheres = load_table("standard_spheres.json", subdir="spells")
        for exclude in excludes:
            try:
                schools_spheres.remove(exclude)
            except ValueError:
                pass
        return self.random_include_school_sphere_spell(
            spell_level, spell_list, schools_spheres
        )

    def random_random_spell(self):
        caster_class = random.choice(["Wizard", "Priest"])
        if caster_class == "Wizard":
            return self.random_spell(random.randint(1, 9), caster_class)
        else:
            return self.random_spell(random.randint(1, 7), caster_class)


def random_spell(spell_level, caster_class, expanded=False):
    return Spells(expanded=expanded).random_spell(spell_level, caster_class)


def random_random_spell(expanded=False):
    return Spells(expanded=expanded).random_random_spell()


def main():
    spells = Spells()
    print("\n".join(spells.spells["Sphere"]))


if __name__ == "__main__":
    main()
