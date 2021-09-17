#!/usr/bin/env python3

import argparse
import json
import os
import random

from generate_scroll import generate_scroll
from generate_scroll import random_spell


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
            return table[str(value)]
    return table[str(max_roll)]


def load_table(fname):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    path = f"{base_dir}/magic_items/{fname}"
    return json.load(open(path))


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

    if base_potion == "Potion of Animal Control":
        animal_control = load_and_roll("animal_control.json")
        base_potion = f"{base_potion} ({animal_control})"
    elif base_potion == "Potion of Dragon Control":
        dragon_control = load_and_roll("dragon_control.json")
        base_potion = f"{base_potion} ({dragon_control})"
    elif base_potion == "Potion of Giant Control":
        giant_control = load_and_roll("giant_control.json")
        base_potion = f"{base_potion} ({giant_control})"
    elif base_potion == "Potion of Giant Strength":
        giant_strength = load_and_roll("giant_strength.json")
        base_potion = f"{base_potion} ({giant_strength})"
    elif base_potion == "Potion of Human Control":
        potion_human_control = load_and_roll("potion_human_control.json")
        base_potion = f"{base_potion} ({potion_human_control})"
    elif base_potion == "Oil of Elemental Invulnerability":
        elemental_invuln = load_and_roll("elemental_invuln.json")
        base_potion = f"{base_potion} ({elemental_invuln})"
    elif base_potion == "Potion of Undead Control":
        undead_control = load_and_roll("undead_control.json")
        base_potion = f"{base_potion} ({undead_control})"

    return base_potion


def scrolls(mod=0):
    result = roll(1, 6, 0)
    if result < 5:
        return str(generate_scroll())
    base_scroll = load_and_roll("scrolls_b.json", mod=mod)
    if base_scroll == "Scroll of Protection - Elementals":
        scroll_elementals = load_and_roll("scroll_elementals.json")
        base_scroll = f"{base_scroll} ({scroll_elementals})"
    elif base_scroll == "Scroll of Protection - Lycanthropes":
        scroll_lycanthropes = load_and_roll("scroll_lycanthropes.json")
        base_scroll = f"{base_scroll} ({scroll_lycanthropes})"

    return base_scroll


def rings(mod=0):
    result = roll(1, 6, 0)
    base_ring = None
    if result < 5:
        base_ring = load_and_roll("rings_a.json", mod=mod)
    else:
        base_ring = load_and_roll("rings_b.json", mod=mod)

    if base_ring == "Ring of Clumsiness":
        clumsiness = load_and_roll("clumsiness.json")
        base_ring = f"{base_ring} ({clumsiness})"
    elif base_ring == "Ring of Contrariness":
        contrariness = load_and_roll("contrariness.json")
        base_ring = f"{base_ring} ({contrariness})"
    elif base_ring == "Ring of Elemental Command":
        element = random.choice(["Air", "Earth", "Fire", "Water"])
        base_ring = f"{base_ring} ({element})"
    elif base_ring == "Ring of Protection":
        ring_protection = load_and_roll("ring_protection.json")
        base_ring = f"{base_ring} {ring_protection}"
    elif base_ring == "Ring of Regeneration":
        if roll(1, 100, 0) >= 90:
            base_ring = "Vampiric Ring of Regeneration"
    elif base_ring == "Ring of Spell Storing":

        def spell_storing_level(caster_class):
            if caster_class == "Wizard":
                spell_level = roll(1, 8, 0)
                if spell_level == 8:
                    spell_level = roll(1, 6, 0)
            else:
                spell_level = roll(1, 6, 0)
                if spell_level == 6:
                    spell_level = roll(1, 4, 0)
            return spell_level

        caster_class = "Wizard"
        if roll(1, 100, 0) > 70:
            caster_class = "Priest"
        spell_levels = sorted(
            [spell_storing_level(caster_class) for x in range(0, roll(1, 4, 1))]
        )
        spells = []
        for spell_level in spell_levels:
            spells.append(f"{spell_level}:{random_spell(spell_level, caster_class)}")
        base_ring = f"{base_ring} ({caster_class}): {', '.join(spells)}"
    elif base_ring == "Ring of Telekinesis":
        telekinesis = load_and_roll("telekinesis.json")
        base_ring = f"{base_ring} ({telekinesis})"
    elif base_ring == "Ring of Multiple Wishes":
        wishes = roll(2, 4, 0)
        base_ring = f"{base_ring} ({wishes} wishes)"
    elif base_ring == "Ring of Three Wishes":
        if roll(1, 100, 0) <= 25:
            base_ring = f"{base_ring} (limited wish)"
    elif base_ring == "Ring of Wizardry":
        ring_of_wizardry = load_and_roll("ring_of_wizardry.json")
        base_ring = f"{base_ring} ({ring_of_wizardry})"

    return base_ring


def rods(mod=0):
    return load_and_roll("rods.json", mod=mod)


def staves(mod=0):
    base_staff = load_and_roll("staves.json", mod=mod)
    no_charge = ["Staff-Mace", "Staff-Spear", "Staff of the Serpent"]
    has_charges = True
    charges = roll(1, 6, 19)
    if base_staff in no_charge:
        has_charges = False

    if base_staff == "Staff-Spear":
        staff_spear = load_and_roll("staff_spear.json")
        base_staff = f"{base_staff} {staff_spear}"
    elif base_staff == "Staff of the Serpent":
        snake = "Python"
        if roll(1, 100, 0) > 60:
            snake = "Adder"
        base_staff = f"{base_staff} ({snake})"
    elif base_staff == "Staff of Swarming Insects":
        charges = roll(1, 6, 44)

    if has_charges:
        base_staff = f"{base_staff} ({charges} charges)"

    return base_staff


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
    if base_armor == "Special":
        return load_and_roll("special_armor.json")
    else:
        return f"{base_armor} {adjustment}"


def armor_no_shields():
    base_armor = load_and_roll("armor_no_shield.json")
    adjustment = load_and_roll("armor_adjustment.json")
    return f"{base_armor} {adjustment}"


def shields():
    base_armor = load_and_roll("shields.json")
    adjustment = load_and_roll("armor_adjustment.json")
    return f"{base_armor} {adjustment}"


def weapon(mod=0):
    result = roll(1, 6, 0)
    base_weapon = None
    adjustment = None
    if result < 3:
        base_weapon = load_and_roll("weapon_type_a.json", mod=mod)
    else:
        base_weapon = load_and_roll("weapon_type_b.json", mod=mod)
    if base_weapon == "Special":
        result = roll(1, 10, 0)
        if result < 4:
            return load_and_roll("special_weapons_a.json")
        elif result < 7:
            return load_and_roll("special_weapons_b.json")
        elif result < 10:
            return load_and_roll("special_weapons_c.json")
        else:
            return load_and_roll("special_weapons_c.json")
    elif base_weapon == "Sword" or base_weapon == "Scimitar":
        if base_weapon == "Sword":
            base_weapon = load_and_roll("sword_types.json")
        adjustment = load_and_roll("sword_adjustment.json")
    else:
        if base_weapon == "Pole Arm":
            base_weapon = load_and_roll("polearms.json")
        adjustment = load_and_roll("weapon_adjustment.json")
    return f"{base_weapon} {adjustment}"


def sword():
    base_weapon = load_and_roll("sword_types.json")
    adjustment = load_and_roll("sword_adjustment.json")
    return f"{base_weapon} {adjustment}"


def non_sword():
    base_weapon = load_and_roll("non_sword_weapons.json")
    adjustment = load_and_roll("weapon_adjustment.json")
    return f"{base_weapon} {adjustment}"


def armor_or_weapon():
    category = load_and_roll("armor_or_weapon.json")
    return roll_category(category)


def misc_magic():
    category = load_and_roll("misc_magic.json")
    return roll_category(category)


def random_magic_item():
    category = load_and_roll("categories.json")
    return roll_category(category)


def roll_nonweapon():
    results = []
    categories = list(load_table("categories.json").values())
    categories.remove("Weapons")
    category = random.choice(categories)
    return roll_category(category)


def roll_category(category):
    if category == "Potions and Oils":
        return potions_and_oils()
    elif category == "Scrolls":
        return scrolls()
    elif category == "Rings":
        return rings()
    elif category == "Rods":
        return rods()
    elif category == "Staves":
        return staves()
    elif category == "Wands":
        return wands()
    elif category == "Rod/Staff/Wand":
        category = random.choice(["Rods", "Staves", "Wands"])
        roll_category(category)
    elif category == "Books and Tomes":
        return books()
    elif category == "Jewels and Jewelry":
        return jewelry()
    elif category == "Cloaks and Robes":
        return cloaks_robes()
    elif category == "Boots and Gloves":
        return boots_bracers_gloves()
    elif category == "Girdles and Helms":
        return girdles_hats_helms()
    elif category == "Bags and Bottles":
        return containers()
    elif category == "Dusts and Stones":
        return candles_dust_stones()
    elif category == "Household Items and Tools":
        return household_tools()
    elif category == "Musical Instruments":
        return musical_instruments()
    elif category == "The Weird Stuff":
        return weird()
    elif category == "Armor and Shields":
        return armor()
    elif category == "Armor No Shields":
        return armor_no_shields()
    elif category == "Shields":
        return shields()
    elif category == "Weapons":
        return weapon()
    elif category == "Sword":
        return sword()
    elif category == "Nonsword":
        return non_sword()
    elif category == "Misc Magic":
        return misc_magic()
    else:
        print(f"Unknown category '{category}'")
        return None


def roll_all_categories():
    results = []
    categories = load_table("categories.json").values()
    for category in categories:
        results.append(roll_category(category))
    return results


def print_all_categories():
    categories = load_table("categories.json")
    for category in categories.values():
        print(category)


def main():
    parser = argparse.ArgumentParser(description="Generate random magic items.")
    parser.add_argument(
        "-a", "--all", action="store_true", help="generate an item in every category"
    )
    parser.add_argument(
        "-c",
        "--category",
        action="store",
        help="generate a magic item from a specific category",
    )
    parser.add_argument(
        "-i", "--item", action="store_true", help="generate a random magic item"
    )
    parser.add_argument(
        "-m", "--misc", action="store_true", help="generate a misc. magic item"
    )
    parser.add_argument(
        "-n",
        "--nonweapon",
        action="store_true",
        help="generate a non-weapon magic item",
    )
    parser.add_argument(
        "-p", "--print", action="store_true", help="print all valid categories"
    )

    args = parser.parse_args()
    if args.all:
        print("\n".join(roll_all_categories()))
    if args.category:
        print(roll_category(args.category))
    if args.item:
        print(random_magic_item())
    if args.misc:
        print(roll_category("Misc Magic"))
    if args.nonweapon:
        print(roll_nonweapon())
    if args.print:
        print_all_categories()


if __name__ == "__main__":
    main()
