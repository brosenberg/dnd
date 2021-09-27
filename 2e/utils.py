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


def table_keys_by_filter(table, filter_dict, do_extra=True, inverse=False):
    results = []
    for entry in table:
        match = False
        for key in filter_dict.keys():

            def default_match():
                if type(filter_dict[key]) is list:
                    return intersect(table[entry][key], filter_dict[key])
                return table[entry][key] == filter_dict[key]

            if do_extra:
                if key == "Source" and filter_dict[key] == "expanded":
                    if table[entry][key] in ["standard", "expanded"]:
                        match = True
                elif key == "Cost":
                    if table[entry][key] <= filter_dict[key]:
                        match = True
                elif default_match():
                    match = True
            elif default_match():
                match = True
        if match and not inverse:
            results.append(entry)
        elif not match and inverse:
            results.append(entry)

    return results
