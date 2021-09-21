#!/usr/bin/env python3

import json
import os
import random

def diff_lists(list_a, list_b):
    for level in list_a:
        for spell in list_a[level]:
            if spell not in list_b[level]:
                print(f"{spell} missing from level {level}!")

def flatten_schools(spell_list):
    spells = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': []}
    for school in spell_list:
        for level in spell_list[school]:
            spells[level] += spell_list[school][level]
    for level in spells:
        spells[level] = sorted(list(set(spells[level])))
    return spells

class Spells(object):
    def __init__(self, expanded=False):
        if expanded:
            pass
        else:
            self.spells = {
                "School": load_spells("wizard-spells.json"),
                "Sphere": load_spells("priest-spells.json"),
            }
            self.spells["Wizard"] = flatten_schools(self.spells["School"])
            self.spells["Priest"] = flatten_schools(self.spells["Sphere"])

    def random_spell(self, spell_level, caster_class):
        spell_level = str(spell_level)
        return random.choice(self.spells[caster_class][spell_level])

    def random_school_sphere_spell(self, spell_level, school_sphere, spell_list):
        spell_level = str(spell_level)
        try:
            return random.choice(self.spells[spell_list][school_sphere][spell_level])
        except KeyError:
            return None

    def random_include_school_sphere_spell(self, spell_level, spell_list, includes):
        spell_level = str(spell_level)
        possible = []
        for school_sphere in includes:
            try:
                possible += self.spells[spell_list][school_sphere][spell_level]
            except KeyError:
                pass
        return random.choice(list(set(possible)))

    def random_exclude_school_sphere_spell(self, spell_level, spell_list, excludes):
        spell_level = str(spell_level)
        possible = []
        for school_sphere in list(set(self.spells[spell_list].keys() - set(excludes))):
            try:
                possible += self.spells[spell_list][school_sphere][spell_level]
            except KeyError:
                pass
        return random.choice(list(set(possible)))

    def random_random_spell(self):
        caster_class = random.choice(["Wizard", "Priest"])
        if caster_class == "Wizard":
            return self.random_spell(random.randint(1, 9), caster_class)
        else:
            return self.random_spell(random.randint(1, 7), caster_class)


def load_spells(fname):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    return json.load(open(f"{base_dir}/spells/{fname}"))


def main():
    spells = Spells()
    spell_list = flatten_schools(spells.spells["Sphere"])
    #diff_lists(spells.spells["Wizard"], spell_list)
    diff_lists(spell_list, spells.spells["Priest"])
    breakpoint()


if __name__ == "__main__":
    main()
