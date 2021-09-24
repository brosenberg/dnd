#!/usr/bin/env python3

import random

from dice import roll


def do_action(action, data):
    if action == "Choice":
        return random.choice(data)
    elif action.startswith("Key_Roll"):
        key = action.split(" ")[1]
        return roll(data[key][0], data[key][1], data[key][2])
    elif action == "Return":
        return data
    elif action == "Roll":
        return roll(data[0], data[1], data[2])
    elif action == "Table":
        table = {int(x): data[x] for x in data}
        max_roll = max(table.keys())
        result = roll(1, max_roll, 0)
        for value in sorted(table):
            if value >= result:
                return table[value]
        return table[max_roll]


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
    str_format = kwargs.get("Format", "{result}")
    action = kwargs["Action"].format(**kwargs)
    result = do_action(action, kwargs["Data"])
    if type(result) is dict:
        result = gen(**result)
    if kwargs.get("Plusify", False):
        result = plusify(result)
    return str_format.format(result=result, **kwargs)


def plusify(number):
    number = int(number)
    try:
        if number > 0:
            return f"+{number}"
        elif number < 0:
            return f"-{number}"
    except TypeError:
        pass
