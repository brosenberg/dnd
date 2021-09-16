#!/usr/bin/env python3

import json
import random


def roll(dice, sides, mod):
    total = mod
    for die in range(0, dice):
        total += random.randint(1, sides)
    return total


def roll_table(table, mod=0):
    max_roll = sorted([int(x) for x in table.keys()])[-1]
    result = roll(1, max_roll, mod)
    for value in sorted([int(x) for x in table.keys()]):
        if value >= result:
            return (table[str(value)], result)
    return (table[str(max_roll)], result)


def load_table(fname):
    return json.load(open(fname))


def load_and_roll(fname, mod=0):
    return roll_table(load_table(fname), mod=mod)


def potions_and_oils(mod=0):
    result = roll(1, 6, 0)
    base_potion = None
    if result < 3:
        base_potion = load_and_roll("potions_oils_a.json", mod=mod)
    if result < 5:
        base_potion = load_and_roll("potions_oils_b.json", mod=mod)
    else:
        base_potion = load_and_roll("potions_oils_c.json", mod=mod)

    if base_potion[0] == "Animal Control":
        animal_control = load_and_roll("animal_control.json")[0]
        base_potion = (f"{base_potion[0]} ({animal_control})", base_potion[1])
    elif base_potion[0] == "Dragon Control":
        dragon_control = load_and_roll("dragon_control.json")[0]
        base_potion = (f"{base_potion[0]} ({dragon_control})", base_potion[1])
    elif base_potion[0] == "Giant Control":
        giant_control = load_and_roll("giant_control.json")[0]
        base_potion = (f"{base_potion[0]} ({giant_control})", base_potion[1])
    elif base_potion[0] == "Giant Strength":
        giant_strength = load_and_roll("giant_strength.json")[0]
        base_potion = (f"{base_potion[0]} ({giant_strength})", base_potion[1])
    elif base_potion[0] == "Oil of Elemental Invulnerability":
        elemental_invuln = load_and_roll("elemental_invuln.json")[0]
        base_potion = (f"{base_potion[0]} ({elemental_invuln})", base_potion[1])
    elif base_potion[0] == "Undead Control":
        undead_control = load_and_roll("undead_control.json")[0]
        base_potion = (f"{base_potion[0]} ({undead_control})", base_potion[1])

    return base_potion


def scrolls(mod=0):
    result = roll(1, 6, 0)
    if result < 5:
        return load_and_roll("scrolls_a.json", mod=mod)
    else:
        return load_and_roll("scrolls_b.json", mod=mod)


def rings(mod=0):
    result = roll(1, 6, 0)
    base_ring = None
    if result < 5:
        base_ring = load_and_roll("rings_a.json", mod=mod)
    else:
        base_ring = load_and_roll("rings_b.json", mod=mod)

    if base_ring[0] == "Clumsiness":
        clumsiness = load_and_roll("clumsiness.json")[0]
        base_ring = (f"{base_ring[0]} {clumsiness}", base_ring[1])
    elif base_ring[0] == "Contrariness":
        contrariness = load_and_roll("contrariness.json")[0]
        base_ring = (f"{base_ring[0]} {contrariness}", base_ring[1])
    elif base_ring[0] == "Protection":
        ring_protection = load_and_roll("ring_protection.json")[0]
        base_ring = (f"{base_ring[0]} {ring_protection}", base_ring[1])

    return base_ring


def armor(mod=0):
    base_armor = load_and_roll("armor_type.json", mod=mod)
    adjustment = load_and_roll("armor_adjustment.json")
    if base_armor[0] == "Special":
        return load_and_roll("special_armor.json")
    else:
        return (f"{base_armor[0]} {adjustment[0]}", (base_armor[1], adjustment[1]))


def weapon(mod=0):
    result = roll(1, 6, 0)
    base_weapon = None
    adjustment = None
    if result < 3:
        base_weapon = load_and_roll("weapon_type_a.json", mod=mod)
    else:
        base_weapon = load_and_roll("weapon_type_b.json", mod=mod)
    if base_weapon[0] == "Special":
        result = roll(1, 10, 0)
        if result < 4:
            return load_and_roll("special_weapons_a.json")
        elif result < 7:
            return load_and_roll("special_weapons_b.json")
        elif result < 10:
            return load_and_roll("special_weapons_c.json")
        else:
            return load_and_roll("special_weapons_c.json")
    elif base_weapon[0] == "Sword" or base_weapon[0] == "Scimitar":
        adjustment = load_and_roll("sword_adjustment.json")
    else:
        adjustment = load_and_roll("weapon_adjustment.json")
    return (f"{base_weapon[0]} {adjustment[0]}", (base_weapon[1], adjustment[1]))


def main():
    categories = load_table("categories.json")
    print(roll_table(categories))
    print(potions_and_oils())
    print(scrolls())
    print(rings())
    print(armor())
    print(weapon())


if __name__ == "__main__":
    main()
