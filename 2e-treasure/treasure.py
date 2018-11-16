#!/usr/bin/env python

import random
import sys

ORDER = ['cp', 'sp', 'gp', 'pp', 'gems', 'art', 'potions', 'scrolls', 'magic']

TREASURE = {
    'B': {
        'cp': [50, 1000, 6000],
        'sp': [25, 1000, 3000],
        'gp': [25, 200, 2000],
        'pp': [25, 100, 1000],
        'gems': [30, 1, 8],
        'art': [20, 1, 4],
        'magic': [10, 'Armor Weapon']
    },
    'Q': {
        'gems': [100, 1, 4],
    },
    'R': {
        'gp': [100, 2, 20],
        'pp': [100, 10, 60],
        'gems': [100, 2, 8],
        'art': [100, 1, 3],
    },
    'S': {
        'magic': [100, 1, 8, 'potions'],
    },
    'T': {
        'magic': [100, 1, 8, 'scrolls'],
    },
}

def percentile_check(check_val):
    if random.randint(1, 100) <= check_val:
        return True
    else:
        return False

def roll_treasure(ttypes):
    treasure = {}
    for ttype in ttypes:
        if ttype in TREASURE:
            for thing in ORDER:
                if thing not in treasure:
                    if thing == "magic":
                        treasure["magic"] = []
                    else:
                        treasure[thing] = 0
                if thing not in TREASURE[ttype]:
                    continue
                if percentile_check(TREASURE[ttype][thing][0]):
                    if thing == "magic":
                        if len(TREASURE[ttype][thing]) == 2:
                            treasure["magic"].append(TREASURE[ttype][thing][1])
                        else:
                            amount = random.randint(TREASURE[ttype][thing][1],
                                                    TREASURE[ttype][thing][2])
                            treasure[TREASURE[ttype][thing][3]] += amount
                    else:
                        amount = random.randint(TREASURE[ttype][thing][1],
                                                TREASURE[ttype][thing][2])
                        treasure[thing] += amount
        else:
            print "Unknown treasure type: %s" % (ttype,)
    return treasure

def print_treasure(treasure):
    valuables = []
    for thing in ORDER:
        if thing in treasure:
            if not treasure[thing]:
                continue
            if thing == "magic":
                continue
            else:
                valuables.append("%s %s" % ('{:,}'.format(treasure[thing]), thing))
    print ', '.join(valuables)
    if treasure.get("magic"):
        print 'Magic Items: ' + ', '.join(treasure[thing])

def main():
    t = roll_treasure(sys.argv[1:])
    print_treasure(t)

if __name__ == '__main__':
    main()
