#!/usr/bin/env python

import sys
import random

BASE_JEWELRY = [
    # (Min value, Max value), ['materials']
    ((1,10), ['ivory', 'wrought silver']),
    ((2,12), ['wrought silver and gold']),
    ((3,18), ['wrought gold']),
    ((5,30), ['jade', 'coral', 'wrought platinum']),
    ((10,60), ['silver with gems']),
    ((20,80), ['gold with gems']),
    ((20,120), ['platinum with gems']),
]

JEWELRY_TYPES = [
    "anklet",
    "armband",
    "belt",
    "box (small)",
    "bracelet",
    "broach",
    "buckle",
    "chain",
    "chalice",
    "choker",
    "clasp",
    "coffer",
    "collar",
    "comb",
    "coronet",
    "crown",
    "decanter",
    "diadem",
    "earring",
    "fob",
    "goblet",
    "headband (fillet)",
    "idol",
    "locket",
    "medal",
    "medallion",
    "necklace",
    "pendant",
    "pin",
    "orb",
    "ring",
    "scepter",
    "seal",
    "statuette",
    "tiara",
]


class Jewelry(object):
    def __init__(self):
        index = 0
        roll = random.randint(1, 100)
        if roll >= 91:
            index = 6
        elif roll >= 71:
            index = 5
        elif roll >= 51:
            index = 4
        elif roll >= 41:
            index = 3
        elif roll >= 21:
            index = 2
        elif roll >= 11:
            index = 1
        self. value = 100 * random.randint(BASE_JEWELRY[index][0][0],
                                           BASE_JEWELRY[index][0][1])
        self.description = "%s %s" % (random.choice(BASE_JEWELRY[index][1]),
                                      random.choice(JEWELRY_TYPES))

    def __str__(self):
        return "%s (%s gp)" % (self.description, self.value)

    def _quality(self, rollmin=1, rollmax=10):
        roll = random.randint(rollmin, rollmax)
        if roll == 1:
            self.value = self.value * 2
            self._quality(rollmax=8)
        elif roll == 2:
            self.value = self.value * 2
        elif roll == 3:
            self.value = self.value * (1+float(random.randint(1, 6))/10)
        elif roll == 9:
            self.value = self.value * (1-float(random.randint(1, 4))/10)
        elif roll == 10:
            self.value = self.value / 2
            self._quality(rollmin=4)

def main():
    try:
        count = int(sys.argv[1])
        total = 0
        while count:
            jewelry = Jewelry()
            print jewelry
            total = total + jewelry.value
            count = count - 1
        print "%s gp total" % (total,)
    except IndexError:
        print "Usage: %s [pieces of jewelry]" % (sys.argv[0],)
        sys.exit(1)

if __name__ == '__main__':
    main()
