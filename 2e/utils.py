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


def load_table(fname, **kwargs):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    subdir = kwargs.get("subdir", "tables")
    sub_table = kwargs.get("sub_table")
    if sub_table:
        fname = fname.replace(".json", "")
        if not sub_table.startswith("_"):
            sub_table = f"_{sub_table}"
        try:
            return load_table(f"{fname}{sub_table}", subdir=subdir)
        except FileNotFoundError:
            sub_table = "_standard"
            return load_table(f"{fname}{sub_table}", subdir=subdir)
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


def mutate_data_if_equal_keys(table, keys):
    data = []
    for entry in table["Data"]:
        if type(entry[1]) is dict:
            if entry[1]["Base Item"] in keys:
                data.append(entry)
        elif entry[1] in keys:
            data.append(entry)
    # data = [x for x in table["Data"] if x[1] in keys]
    table["Data"] = data


def table_keys_by_filter(table, filter_dict, do_extra=True, inverse=False):
    results = []
    for entry in table:
        match = True
        for key in filter_dict.keys():

            def default_match():
                if type(filter_dict[key]) is list:
                    if type(table[enty][key]) is list:
                        return intersect(table[entry][key], filter_dict[key])
                    return table[entry][key] in filter_dict[key]
                elif type(table[entry][key]) is list:
                    return filter_dict[key] in table[entry][key]
                return table[entry][key] == filter_dict[key]

            if do_extra:
                if key == "Source" and filter_dict[key] == "expanded":
                    if table[entry][key] not in ["standard", "expanded"]:
                        match = False
                elif key == "Cost":
                    if table[entry][key] > filter_dict[key]:
                        match = False
                elif not default_match():
                    match = False
            elif not default_match():
                match = False
        if match and not inverse:
            results.append(entry)
        elif not match and inverse:
            results.append(entry)

    return results
