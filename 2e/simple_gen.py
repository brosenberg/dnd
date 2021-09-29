#!/usr/bin/env python3

import random

from dice import roll
from utils import plusify


def do_action(action, data):
    if action == "Choice":
        return random.choice(data)
    elif action.startswith("Choice_Unique_N"):
        count = int(action.split(" ")[1])
        results = []
        if count > len(data):
            return data
        for _ in range(0, count):
            result = random.choice(data)
            results.append(result)
            data.remove(result)
        return results
    elif action == "Choice Twice":
        return [random.choice(data), random.choice(data)]
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
        return roll(*data)
    elif action == "Table":
        return roll_table(data)
    elif action == "Table_Calc":
        new_data = {}
        last = 0
        for key, value in data:
            this = key + last
            new_data[str(this)] = value
            last = this
        return roll_table(new_data)
    elif action.startswith("Table_N_Roll"):
        roll_dice = (int(x) for x in action.split(" ")[1:])
        count = roll(*roll_dice)
        results = []
        for _ in range(0, count):
            result = roll_table(data)
            if type(result) is list:
                results += result
            else:
                results.append(result)
        return results
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
    join = kwargs.get("Join", None)
    math = kwargs.get("Math", None)
    action = kwargs["Action"].format(**kwargs)
    filters = kwargs.get("Filters", {})
    filter_options = kwargs.get("Filter Options", {})

    result = do_action(action, kwargs["Data"])

    # Generate sub sub_gens
    if type(result) is dict:
        result = gen(**result)
    # Generate sub sub_gens in lists
    elif type(result) is list:
        for index, entry in enumerate(result):
            if type(entry) is dict:
                result.remove(entry)
                sub_results = gen(**entry)
                if type(sub_results) is list:
                    result += sub_results
                else:
                    result.append(sub_results)

    if kwargs.get("Plusify", False):
        result = plusify(result)
    if kwargs.get("Sort", False):
        try:
            result = sorted(result)
        except:
            breakpoint()
    if math:
        for operator in math.split(" "):
            op = operator[0]
            number = int(operator[1:])
            if op == "+":
                result += number
            elif op == "-":
                result -= number
            elif op == "*":
                result *= number
            elif op == "/":
                result /= number
    if join:
        result = join.join(result)
    if str_format:
        return str_format.format(result=result, **kwargs)
    return result


def table_mutate_values(table, include=None, exclude=None):
    last = 0
    subtract = 0
    new_table = {}
    for key, value in table.items():
        if (include is not None and value not in include) or (
            exclude is not None and value in exclude
        ):
            subtract += int(key) - last
        else:
            last = int(key)
            new_table[str(int(key) - subtract)] = value
    return new_table


def roll_table(data):
    table = {int(x): data[x] for x in data}
    max_roll = max(table.keys())
    result = roll(1, max_roll, 0)
    for value in sorted(table):
        if value >= result:
            return table[value]
    return table[max_roll]
