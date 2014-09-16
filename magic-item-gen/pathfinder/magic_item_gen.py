#!/usr/bin/env python

import argparse
import json
import random
import re


def roll_table(table):
    table_max = sum(table.values())
    roll = random.randint(1, table_max)
    current = 0
    for i in table:
        current += table[i]
        if current >= roll:
            return i
    return None

# Why store your data in easily manipulated forms, when you can just parse the numbers out!?
def parse_item_bonuses(item_str):
    split_str = re.split('\s+with\s', item_str, maxsplit=1)
    base_bonus = split_str[0]
    abilities = []
    if len(split_str) > 1:
        for ability in re.split('\s+and\s+', split_str[1]):
            m = re.match(r'^(\S+)\s+(\+[0-9]+)\s+.*$', ability)
            count = 1 if m.group(1) == "one" else 2
            abilities.append( (count, m.group(2)) )
    bonus = re.match(r'^(\+[0-9]+)\s+.*$', base_bonus).group(1)
    return (bonus, abilities)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--category', choices=['minor', 'medium', 'major'], required=True)
    p.add_argument('-t', '--item-type', type=str)
    args = p.parse_args()
    category = args.category.title()

    base = {}
    with open('base.json', 'r') as f:
        base = json.load(f)
    print "Generating a %s magic item..." % (args.category,)
    if args.item_type:
        item_type = args.item_type
    else:
        item_type = roll_table(base['Item Types'][category])
    print "Item Type:", item_type
    # WHAT HAS HAPPENED HERE!?
    try:
        base_item = roll_table(base[item_type][category])
        print "Base Item:", base_item
        try:
            bonuses = parse_item_bonuses(base_item)
            #print "Base Item Bonuses:", bonuses
            abilities = []
            if item_type == 'Armor and shields':
                for ability in bonuses[1]:
                    for count in range(ability[0]):
                        abilities.append(roll_table(base['Armor abilities'][ability[1]]))
            ability_str = "%s " % (' and '.join(abilities),) if len(abilities) else ''
            print "%s%s %s" % (ability_str, item_type, bonuses[0])
        except AttributeError:
            pass
    except:
        pass

if __name__ == '__main__':
    main()
