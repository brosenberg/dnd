#!/usr/bin/env python3

import json
import random
import os

from dice import roll


def do_action(action, options):
    if action == "Choice":
        return random.choice(options)
    elif action.startswith("Key_Roll"):
        key = action.split(" ")[1]
        return roll(options[key][0], options[key][1], options[key][2])
    elif action == "Roll":
        return roll(options[0], options[1], options[2])
    elif action == "Table":
        table = {int(x): options[x] for x in options}
        max_roll = max(table.keys())
        result = roll(1, max_roll, 0)
        for value in sorted(table):
            if value >= result:
                return table[value]
        return table[max_roll]


def intersect(list_a, list_b):
    if set(list_a).intersection(set(list_b)):
        return True
    return False


def load_table(fname, subdir="tables"):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    if not fname.endswith(".json"):
        fname += ".json"
    return json.load(open(f"{base_dir}/{subdir}/{fname}"))
