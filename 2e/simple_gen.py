#!/usr/bin/env python3

import random

from dice import roll
from utils import plusify


def do_action(action, data):
    if action == "Choice":
        return random.choice(data)
    elif action.startswith("Key_"):
        key_action, key = action.split(" ", 1)
        key_action = key_action.replace("Key_", "")
        try:
            return do_action(key_action, data[key])
        except KeyError:
            return do_action(key_action, data["Default"])
    elif action == "Return":
        return data
    elif action == "Roll":
        return roll(data[0], data[1], data[2])
    elif action == "Table":
        return roll_table(data)
    elif action == "Table Twice":
        return [roll_table(data), roll_table(data)]

def dump_data(**kwargs):
    dump = []
    for data in kwargs["Data"]:
        if type(kwargs["Data"][data]) is dict:
            dump += dump_data(**kwargs["Data"][data])
        else:
            dump.append(kwargs["Data"][data])
    return dump


def gen(**kwargs):
    if not kwargs:
        return None
    str_format = kwargs.get("Format", None)
    action = kwargs["Action"].format(**kwargs)
    result = do_action(action, kwargs["Data"])
    if type(result) is dict:
        result = gen(**result)
    if kwargs.get("Plusify", False):
        result = plusify(result)
    if str_format:
        return str_format.format(result=result, **kwargs)
    return result


def roll_table(data):
    table = {int(x): data[x] for x in data}
    max_roll = max(table.keys())
    result = roll(1, max_roll, 0)
    for value in sorted(table):
        if value >= result:
            return table[value]
    return table[max_roll]
