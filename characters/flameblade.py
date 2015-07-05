#!/usr/bin/env python

import random

def roll(die, sides):
    r = 0
    for i in range(die):
        r += random.randint(1,sides)
    return r

def main():
    base_damage = roll(1,8)+4
    large_damage = roll(1,12)+4
    to_hit = roll(1,20+2)
    print "To hit: %d  AC: %d" % (to_hit, 12-to_hit)
    print "Medium Damage: %d" % (base_damage+roll(1,6),)
    print " Large Damage: %d" % (large_damage+roll(1,6),)

if __name__ == '__main__':
    main()
