#!/usr/bin/env python3

import json
import random
import os

from dice import roll


def choice_table_count_unique(table_fname, subdir="tables", count=1):
    table = load_table(table_fname, subdir=subdir)
    results = []
    if len(table) <= count:
        return table
    for _ in range(0, count):
        result = random.choice(table)
        table.remove(result)
        results.append(result)
    return results


def intersect(list_a, list_b):
    if set(list_a).intersection(set(list_b)):
        return True
    return False


def load_table(fname, subdir="tables"):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    if not fname.endswith(".json"):
        fname += ".json"
    return json.load(open(f"{base_dir}/{subdir}/{fname}"))


def plusify(number):
    number = int(number)
    try:
        if number > 0:
            return f"+{number}"
        elif number < 0:
            return f"{number}"
    except TypeError:
        pass
