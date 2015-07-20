#!/usr/bin/env python

import random

def roll(die, sides):
    r = 0
    for i in range(die):
        r += random.randint(1,sides)
    return r

def main():
    print "Attacking with The Nightwatcher"
    base_damage = roll(1,8)
    large_damage = roll(1,12)
    bonus = 14
    to_hit = roll(1,20)
    if to_hit == 1:
        print "Critical miss!"
    else:
        if to_hit == 20:
            print "Critical hit!"
        to_hit += 8
        print "To hit: %d  AC: %d" % (to_hit, 12-to_hit)
        print "Medium Damage: %d" % (base_damage+bonus,)
        print " Large Damage: %d" % (large_damage+bonus,)
        print "ELarge Damage: %d" % (2*(.5+large_damage)+bonus,)

if __name__ == '__main__':
    main()
