#!/usr/bin/env python

import argparse
import json
import random

def roll_table(table):
    table_max = sum(table.values())
    roll = random.randint(1, table_max)
    current = 0
    for i in table:
        current += table[i]
        if current >= roll:
            return i
    return None

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--category', choices=['minor', 'medium', 'major'], required=True)
    args = p.parse_args()

    base = {}
    with open('base.json', 'r') as f:
        base = json.load(f)
    print "Generating a %s magic item..." % (args.category,)
    item_type = roll_table(base['Item Type'][args.category.title()])
    print "Item Type:", item_type

if __name__ == '__main__':
    main()
