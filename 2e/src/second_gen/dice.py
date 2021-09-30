#!/usr/bin/env python3

import random


def roll(dice, sides, mod, drop=0):
    rolls = []
    for die in range(0, dice):
        rolls.append(random.randint(1, sides))
    return mod + sum(sorted(rolls)[drop:])
