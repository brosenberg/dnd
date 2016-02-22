#!/usr/bin/env python

import sys
import random
import re

def roll(input_dice, verbose=True):
    r = re.match('^([0-9]+)\s*d\s*([0-9]+)\s*([-+\/*x])?\s*([0-9]+)?\s*$', input_dice)
    result = 0
    rolls = []
    try:
        dice     = int(r.group(1))
        sides    = int(r.group(2))
    except AttributeError:
        raise "Unknown dice input!"
    try:
        mod_type = r.group(3)
        mod      = int(r.group(4))
    except AttributeError:
        mod_type = "+"
        mod = 0
    except TypeError:
        mod_type = "+"
        mod = 0
    old_dice = dice

    while dice > 0:
        roll = random.randint(1, sides)
        rolls.append(roll)
        result += roll
        dice -= 1

    if mod_type == '+':
        result += mod
    if mod_type == '*' or mod_type == 'x':
        result *= mod
    if mod_type == '/':
        result /= mod

    if verbose:
        print "%dd%d%s%d = (%s)%s%d = %d" % (old_dice, sides, mod_type, mod, '+'.join(str(x) for x in rolls), mod_type, mod, result)

    return result

def main():
    print roll(sys.argv[1])

if __name__ == '__main__':
    main()
