#!/usr/bin/env python3

import json
import os


def intersect(list_a, list_b):
    if set(list_a).intersection(set(list_b)):
        return True
    return False


def load_table(fname, subdir="tables"):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    if not fname.endswith(".json"):
        fname += ".json"
    return json.load(open(f"{base_dir}/{subdir}/{fname}"))
