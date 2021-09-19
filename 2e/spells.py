#!/usr/bin/env python3

import json
import os
import random


class Spells(object):
    def __init__(self):
        self.spells = {
            "Wizard": load_spells("wizard-spells.json"),
            "School": load_spells("wizard-spells-school.json"),
            "Priest": load_spells("priest-spells.json"),
            "Sphere": load_spells("priest-spells-sphere.json"),
        }

    def random_spell(self, spell_level, caster_class):
        spell_level = str(spell_level)
        return random.choice(self.spells[caster_class][spell_level])

    def random_school_sphere_spell(self, spell_level, caster_class, school_sphere):
        spell_level = str(spell_level)
        if caster_class == "Wizard":
            return random.choice(self.spells["School"][school_sphere][spell_level])
        else:
            try:
                return random.choice(self.spells["Sphere"][school_sphere][spell_level])
            except KeyError:
                return None

    def random_exclude_school_sphere_spell(self, spell_level, caster_class, excludes):
        spell_level = str(spell_level)
        possible = []
        if caster_class == "Wizard":
            for school in list(set(self.spells["School"].keys() - set(excludes))):
                possible += self.spells["School"][school][spell_level]
            print("  ".join(sorted(possible)))
            return random.choice(list(set(possible)))
        else:
            for sphere in list(set(self.spells["Sphere"].keys() - set(excludes))):
                try:
                    possible += self.spells["Sphere"][sphere][spell_level]
                except KeyError:
                    return None
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
    print(spells.random_school_sphere_spell("4", "Wizard", "Necromancy"))
    print(spells.random_school_sphere_spell("4", "Priest", "Sun"))
    print(
        spells.random_exclude_school_sphere_spell(
            "3", "Wizard", ["Necromancy", "Evocation", "Conjuration"]
        )
    )


if __name__ == "__main__":
    main()
