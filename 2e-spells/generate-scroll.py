#!/usr/bin/env python

import json
import random
import sys

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
        self.scroll = {}

    def __str__(self):
        s = ""
        if self.scroll_type:
            s += "%s Scroll\n" % (self.scroll_type)
        for level in sorted(self.scroll.keys()):
            s += "%s: %s\n" % (level, ', '.join(self.scroll[level]))
        s = s.rstrip('\n')
        return s

    def generate(self):
        for i in range(1, self.spell_count):
            spell_level = str(random.randint(self.min_level, self.max_level))
            if spell_level not in self.scroll.keys():
                self.scroll[spell_level] = []
            self.scroll[spell_level].append(self.spells.random_spell(spell_level))
        

def main():
    wizard_spells = Spells('wizard-spells.json')
    priest_spells = Spells('priest-spells.json')
    
    priest_scroll = Scroll(priest_spells, 7, 2, 7, scroll_type="Priest")
    priest_scroll.generate()
    print priest_scroll

if __name__ == '__main__':
    main()
