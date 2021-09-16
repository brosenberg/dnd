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


def rods(mod=0):
    return load_and_roll("rods.json", mod=mod)


def staves(mod=0):
    return load_and_roll("staves.json", mod=mod)


def wands(mod=0):
    return load_and_roll("wands.json", mod=mod)


def books(mod=0):
    return load_and_roll("books.json", mod=mod)


def jewelry(mod=0):
    result = roll(1, 6, 0)
    base_jewelry = None
    if result < 4:
        base_jewelry = load_and_roll("jewelry_a.json", mod=mod)
    else:
        base_jewelry = load_and_roll("jewelry_b.json", mod=mod)
    return base_jewelry


def cloaks_robes(mod=0):
    return load_and_roll("cloaks_robes.json", mod=mod)


def boots_bracers_gloves(mod=0):
    return load_and_roll("boots_bracers_gloves.json", mod=mod)


def girdles_hats_helms(mod=0):
    return load_and_roll("girdles_hats_helms.json", mod=mod)


def containers(mod=0):
    return load_and_roll("containers.json", mod=mod)


def candles_dust_stones(mod=0):
    return load_and_roll("candles_dust_stones.json", mod=mod)


def household_tools(mod=0):
    return load_and_roll("household_tools.json", mod=mod)


def musical_instruments(mod=0):
    return load_and_roll("musical_instruments.json", mod=mod)


def weird(mod=0):
    result = roll(1, 6, 0)
    base_weird = None
    if result < 4:
        base_weird = load_and_roll("weird_a.json", mod=mod)
    else:
        base_weird = load_and_roll("weird_b.json", mod=mod)
    return base_weird


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
    category = load_and_roll("categories.json")[0]
    print(category)
    if category == 'Potions and Oils':
        print(potions_and_oils())
    elif category == 'Scrolls':
        print(scrolls())
    elif category == 'Rings':
        print(rings())
    elif category == 'Rods':
        print(rods())
    elif category == 'Staves':
        print(staves())
    elif category == 'Wands':
        print(wands())
    elif category == 'Books and Tomes':
        print(books())
    elif category == 'Jewels and Jewelry':
        print(jewelry())
    elif category == 'Cloaks and Robes':
        print(cloaks_robes())
    elif category == 'Boots and Gloves':
        print(boots_bracers_gloves())
    elif category == 'Girdles and Helms':
        print(girdles_hats_helms())
    elif category == 'Bags and Bottles':
        print(containers())
    elif category == 'Dusts and Stones':
        print(candles_dust_stones())
    elif category == 'Household Items and Tools':
        print(household_tools())
    elif category == 'Musical Instruments':
        print(musical_instruments())
    elif category == 'The Weird Stuff':
        print(weird())
    elif category == 'Armor and Shields':
        print(armor())
    elif category == 'Weapons':
        print(weapon())
    else:
        print(f"Unknown category '{category}'")


if __name__ == "__main__":
    main()
