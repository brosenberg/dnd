#!/usr/bin/env python3

import json
import os
import random


class Spells(object):
    def __init__(self, spell_file):
        self.spell_list = json.load(open(spell_file))

    def random_spell(self, spell_level):
        return random.choice(self.spell_list[spell_level])


class Scroll(object):
    def __init__(self, spells, spell_count, min_level, max_level, scroll_type=None):
        self.spells = spells
        self.spell_count = spell_count
        self.min_level = min_level
        self.max_level = max_level
        self.scroll_type = scroll_type
        self.scroll_capacity = 25
        self.scroll = {}

    def __str__(self):
        s = ""
        if self.scroll_type:
            s += "%s Scroll: " % (self.scroll_type)
        for level in sorted(self.scroll.keys()):
            s += "%s - %s; " % (level, ", ".join(sorted(self.scroll[level])))
        s = s.rstrip("; ")
        # s = "%s\nCapacity = %d" % (s, self.scroll_capacity)
        return s

    def generate(self):
        for i in range(0, self.spell_count):
            spell_level = random.randint(self.min_level, self.max_level)

            self.scroll_capacity -= spell_level

            spell_level = str(spell_level)
            if spell_level not in self.scroll.keys():
                self.scroll[spell_level] = []
            new_spell = self.spells.random_spell(spell_level)
            # If the spell is already on the scroll, increase its count, rather
            # than duplicating it in the list.
            if [x for x in self.scroll[spell_level] if x.startswith(new_spell)]:
                spell_index = self.scroll[spell_level].index(new_spell)
                cur_spell = self.scroll[spell_level][spell_index]
                # Assume that no spells contain "(" in their name
                # TODO: r'^.*(\([0-9]\))$'
                if "(" in cur_spell:
                    count = int(cur_spell.split("(")[1][:-1]) + 1
                    cur_spell = "%s (%d)" % (new_spell, count)
                else:
                    cur_spell = "%s (2)" % (new_spell,)
                self.scroll[spell_level][spell_index] = cur_spell
            else:
                self.scroll[spell_level].append(new_spell)


def random_spell_scroll(wizard_spells, priest_spells):
    scroll_roll = random.randint(1, 19)
    type_roll = random.randint(1, 100)
    scroll_type = "Wizard"
    spell_list = wizard_spells
    spell_count = 1
    min_level = 1
    max_level = 4
    if type_roll > 70:
        scroll_type = "Priest"
        spell_list = priest_spells

    if scroll_roll == 7 or scroll_roll == 8:
        spell_count = 2
    elif scroll_roll == 9 or scroll_roll == 10:
        spell_count = 3
    elif scroll_roll == 11 or scroll_roll == 12:
        spell_count = 4
    elif scroll_roll == 13 or scroll_roll == 14:
        spell_count = 5
    elif scroll_roll == 15 or scroll_roll == 16:
        spell_count = 6
    elif scroll_roll > 16:
        spell_count = 7

    if scroll_roll in [4, 5, 11, 13, 15]:
        max_level = 6
    elif scroll_roll in [6, 8, 10, 18]:
        min_level = 2
        max_level = 9
    elif scroll_roll in [12, 14, 17]:
        max_level = 8
    elif scroll_roll == 16:
        min_level = 3
        max_level = 8
    elif scroll_roll == 19:
        min_level = 4
        max_level = 9

    if scroll_type == "Priest" and max_level > 7:
        max_level = 7

    scroll = Scroll(
        spell_list, spell_count, min_level, max_level, scroll_type=scroll_type
    )
    scroll.generate()
    return scroll


def random_spell(spell_level, caster_class):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    spells = None
    if caster_class == "Wizard":
        spells = Spells(f"{base_dir}/spells/wizard-spells.json")
    else:
        spells = Spells(f"{base_dir}/spells/priest-spells.json")
    return spells.random_spell(str(spell_level))


def random_random_spell():
    caster_class = random.choice(["Wizard", "Priest"])
    if caster_class == "Wizard":
        return random_spell(random.randint(1, 9), caster_class)
    else:
        return random_spell(random.randint(1, 7), caster_class)


def generate_scroll():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    wizard_spells = Spells(f"{base_dir}/spells/wizard-spells.json")
    priest_spells = Spells(f"{base_dir}/spells/priest-spells.json")
    return random_spell_scroll(wizard_spells, priest_spells)


def main():
    scroll = generate_scroll()
    print(scroll)


if __name__ == "__main__":
    main()
