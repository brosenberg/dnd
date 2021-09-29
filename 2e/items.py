#!/usr/bin/env python3

import json
import random
import re
import os

from dice import roll
from generate_scroll import generate_scroll
from simple_gen import gen
from spells import random_spell
from utils import choice_table_count_unique
from utils import intersect
from utils import load_table
from utils import mutate_data_if_equal_keys
from utils import plusify
from utils import table_keys_by_filter


AMMOS = load_table("weapons_ammos.json")
ARMOR = load_table("armor_master_list.json")
CLASSES = load_table("classes.json")
RODS = load_table("magic_item_rods.json")
SHIELDS = load_table("shields.json")
SPECIAL_MAGIC_ARMOR = load_table("magic_item_armor_special.json")
SPECIAL_MAGIC_WEAPONS = load_table("magic_item_weapons_special.json")
STAVES = load_table("magic_item_staves.json")
THROWN_WEAPONS = load_table("weapons_thrown.json")
WEAPONS = load_table("weapons_master_list.json")


def appropriate_ammo_type(weapon):
    try:
        return random.choice(WEAPONS[base_weapon(weapon)]["Ammo"])
    except KeyError:
        pass
    return None


def appropriate_armor_group(char_class):
    if char_class == "Druid":
        return "druid"
    if char_class in ["Thief", "Ranger"]:
        return "rogue"
    if char_class == "Bard":
        return "bard"
    if char_class in ["Fighter", "Cleric", "Paladin"]:
        return "warrior"
    return "none"


def appropriate_weapons_by_ammo(ammo):
    def in_ammo(item, ammo_list):
        for ammo_type in ammo_list:
            if ammo_type in item:
                return True
        return False

    weapons = []
    for weapon in WEAPONS:
        try:
            if in_ammo(ammo, WEAPONS[weapon]["Ammo"]):
                weapons.append(weapon)
        except KeyError:
            pass
    return weapons


def base_weapon(item):
    candidates = []
    for weapon in WEAPONS:
        if item.startswith(weapon):
            candidates.append(weapon)
    if candidates:
        return sorted(candidates, key=len)[-1]
    return None


def build_filters(**kwargs):
    filters = kwargs.get("filters", {})
    # FIXME: Should this really default to "Weapons"?
    item_type = kwargs.get("item_type", "Weapons")
    if "Source" not in filters:
        filters["Source"] = kwargs.get("sub_table", "standard")

    if "Usable By" not in filters:
        usable = kwargs.get("usable")
        if not usable and kwargs.get("classes"):
            usable = usable_by(kwargs.get("classes"))
        if usable:
            try:
                filters["Usable By"] = usable[item_type]
            except KeyError:
                pass
    return filters


def gen_table(table, **kwargs):
    return gen(**load_table(table, **kwargs), **kwargs)


def get_ac(item):
    if item == "Bracers of Defenselessness":
        return (10, None)
    remove_list = [" of Blending", " of Missile Attraction"]
    for remove in remove_list:
        item = item.replace(remove, "")
    bracers_of_defense = re.match(r"^Bracers of Defense \(AC ([0-9]+)\)$", item)
    if bracers_of_defense:
        return (int(bracers_of_defense.group(1)), None)
    item, adjustment = get_adjustment(item)
    item = item.capitalize()
    try:
        ac = ARMOR[item]["AC"]
    except KeyError:
        ac = None
    if ac:
        if ARMOR[item]["Category"] == "Shield":
            return (None, ac + adjustment)
        else:
            return (ac - adjustment, None)
    return (None, get_other_ac_bonus(item))


def get_adjustment(item):
    magic = re.match(r"^(.+?) ([+-][0-9]+)(, .+?)?$", item)
    if magic:
        return (magic.group(1), int(magic.group(2)))
    return (item, 0)


def get_other_ac_bonus(item):
    protection_items = ["Ring of Protection", "Cloak of Protection"]
    for protection_item in protection_items:
        if protection_item in item:
            _, adjustment = get_adjustment(item)
            return adjustment
    return None


def intelligent_weapon(base_weapon, sub_table="standard"):
    tables = load_table(f"magic_item_weapons_intelligent", sub_table=sub_table)
    (
        intelligence,
        primary_count,
        extraordinary_count,
        communication,
        reading_power,
    ) = gen(**tables["Intelligence"])
    weapon_powers = {
        "Ego": 0,
        "Primary": [],
        "Extraordinary": [],
        "Special Purpose": None,
        "Purpose Power": None,
        "Languages": [],
        "Alignment": gen(**tables["Alignment"]),
        "Communication": communication,
        "Intelligence": intelligence,
    }
    language_count = 0

    if reading_power is not None:
        weapon_powers["Primary"].append(reading_power)

    for _ in range(0, primary_count):
        power = gen(**tables["Primary"])
        if power == "Extraordinary Power":
            extraordinary_count += 1
        else:
            weapon_powers["Primary"].append(power)

    for _ in range(0, extraordinary_count):

        def special_powers():
            powers = "Special Purpose"
            if weapon_powers["Special Purpose"] is None:
                weapon_powers["Special Purpose"] = gen(**tables["Special Purpose"])
                weapon_powers["Purpose Power"] = gen(**tables["Special Purpose Powers"])
            while powers == "Special Purpose":
                powers = gen(**tables["Extraordinary"])
            handle_powers(powers)

        def handle_powers(powers):
            if powers == "Special Purpose":
                special_powers()
            elif type(powers) is list:
                for power in powers:
                    if power == "Special Purpose":
                        special_powers()
                    else:
                        weapon_powers["Extraordinary"].append(power)
            else:
                weapon_powers["Extraordinary"].append(powers)

        handle_powers(gen(**tables["Extraordinary"]))

    if intelligence > 13:
        language_count = 1 + gen(**tables["Languages"])
        weapon_powers["Languages"] = choice_table_count_unique(
            "languages", count=language_count
        )

    ego_bonus = 0
    if weapon_powers["Special Purpose"] is not None:
        ego_bonus += 5
    if sub_table == "standard":
        if intelligence > 16:  # Telepathic and Read magic ability
            ego_bonus += 4
        if intelligence > 15:  # Read language ability
            ego_bonus += 1
        ego_bonus += len(weapon_powers["Primary"])
        ego_bonus += len(weapon_powers["Languages"])
    elif sub_table == "expanded":
        if intelligence > 16:  # Telepathic ability
            ego_bonus += 2
        if intelligence > 16:  # Read magic ability
            ego_bonus += 2
        if intelligence > 15:  # Read language ability
            ego_bonus += 1
        ego_bonus += 2 * len(weapon_powers["Primary"])
        ego_bonus += int((len(weapon_powers["Languages"]) / 2) + 0.5)
    weapon_powers["Ego"] = (
        get_adjustment(base_weapon)[1]
        + 2 * len(weapon_powers["Extraordinary"])
        + ego_bonus
    )

    s = f"{base_weapon} (Intelligent) - "
    for key in [
        "Intelligence",
        "Ego",
        "Alignment",
        "Communication",
        "Languages",
        "Special Purpose",
        "Abilities",
    ]:
        if key == "Abilities":
            s += f"Abilities: {'; '.join(weapon_powers['Primary'] + weapon_powers['Extraordinary'])}  "
        elif key == "Special Purpose":
            if weapon_powers[key] is not None:
                s += f"Special Purpose: {weapon_powers[key]}  Purpose Power: {weapon_powers['Purpose Power']}  "
        elif type(weapon_powers[key]) is list:
            if key == "Languages":
                s += f"{key}: {', '.join(weapon_powers[key])}  "
        else:
            s += f"{key}: {weapon_powers[key]}  "
    return s.strip()


def is_cursed(item):
    return (
        re.search(r"-[0-9]+", item)
        or "ursed" in item
        or "Clumsiness" in item
        or "Contrariness" in item
        or "Delusion" in item
        or "Defenselessness" in item
        or "Stammering" in item
        or "Jewel of Attacks" in item
        or "Elixir of Madness" in item
        or "Ring of Weakness" in item
    )


def is_melee_weapon(item):
    return is_weapon_in_categories(item, ["Melee"])


def is_missile_weapon(item):
    return is_weapon_in_categories(item, ["Ammo", "Ranged", "Thrown"])


def is_thrown_weapon(item):
    return is_weapon_in_categories(item, ["Thrown"])


def is_shield(item):
    for shield in SHIELDS:
        if item.startswith(shield):
            return True
    return False


def is_weapon_in_categories(item, categories):
    base = base_weapon(item)
    for weapon in WEAPONS:
        if WEAPONS[weapon]["Category"] in categories and base == weapon:
            return True
    return False


def is_two_handed_melee(weapon):
    base = base_weapon(weapon)
    return WEAPONS[base]["Hands"] == 2 and WEAPONS[base]["Category"] == "Melee"


def random_appropriate_ammo(weapon):
    try:
        ammo = appropriate_ammo_type(weapon)
        dice, die, mod = random_item_count(ammo)
        count = roll(dice, die, mod)
        return (ammo, count)
    except TypeError:
        return None


# FIXME: Wtf is this going to be used for?
def random_item_count(item):
    try:
        return WEAPONS[base_weapon(item)]["Quantity"]
    # FIXME
    except:
        pass
    return None


def random_shield():
    return random.choice(SHIELDS)


def random_magic_armor(**kwargs):
    base_item = kwargs.get("base_item")
    data = kwargs.get("data")
    sub_table = kwargs.get("sub_table", "standard")
    filters = build_filters(**kwargs)
    if kwargs.get("load_table") and data is None:
        data = load_table("magic_item_armor", sub_table=sub_table)
    if not filters.get("Usable By") and kwargs.get("classes"):
        filters["Usable By"] = usable_by(kwargs.get("classes"))

    if not base_item:
        if data is not None:
            base_item = gen(**data)
        else:
            base_item = random_item(item_type="Armor", filters=filters)

    if base_item == "Special":
        return random_special_magic_item(
            item_type="Armor", sub_table=sub_table, filters=filters
        )
    elif base_item == "Shield":
        filters["Category"] = "Shield"
        base_item = random.choice(table_keys_by_filter(ARMOR, filters))
    adjustment = gen(**load_table(f"magic_item_armor_adjustment", sub_table=sub_table))
    base_item = f"{base_item} {plusify(adjustment)}"
    if adjustment < 0:
        base_item += " (Cursed)"
    return base_item


def random_magic_item(**kwargs):
    sub_table = kwargs.get("sub_table", "standard")
    category = kwargs.get(
        "category", gen_table(f"magic_item_categories", sub_table=sub_table)
    )
    magic_items = load_table(f"magic_items", sub_table=sub_table)
    data = None
    subcategories = {
        "Armor or Weapon": {"Category": ["Armor and Shields", "Weapons"]},
        "Armor No Shields": {
            "Category": "Armor and Shields",
            "Data": f"magic_item_armor_only",
        },
        "Misc Magic": {
            "Category": [
                "Books and Tomes",
                "Jewels and Jewelry",
                "Cloaks and Robes",
                "Boots and Gloves",
                "Girdles and Helms",
                "Bags and Bottles",
                "Dusts and Stones",
                "Household Items and Tools",
                "Musical Instruments",
                "The Weird Stuff",
            ]
        },
        "Nonsword": {
            "Category": "Weapons",
            "Data": f"magic_item_weapon_nonsword",
        },
        "Nonweapon": {
            "Category": [
                "Potions and Oils",
                "Scrolls",
                "Rings",
                "Rods",
                "Staves",
                "Wands",
                "Books and Tomes",
                "Jewels and Jewelry",
                "Cloaks and Robes",
                "Boots and Gloves",
                "Girdles and Helms",
                "Bags and Bottles",
                "Dusts and Stones",
                "Household Items and Tools",
                "Musical Instruments",
                "The Weird Stuff",
                "Armor and Shields",
            ]
        },
        "Rod/Staff/Wand": {"Category": ["Rods", "Staves", "Wands"]},
        "Shields": {
            "Category": "Armor and Shields",
            "Data": f"magic_item_shields_only",
        },
        "Sword": {"Category": "Weapons", "Data": f"magic_item_weapon_sword"},
    }

    if category in subcategories:
        if type(subcategories[category]["Category"]) is list:
            category = random.choice(subcategories[category]["Category"])
        else:
            try:
                data = load_table(subcategories[category]["Data"], sub_table=sub_table)
            except:
                breakpoint()
            category = subcategories[category]["Category"]

    filters = build_filters(**kwargs, item_type=category)

    if category == "Weapons":
        return random_magic_weapon(sub_table=sub_table, data=data, filters=filters)
    elif category == "Armor and Shields":
        return random_magic_armor(sub_table=sub_table, data=data, filters=filters)
    elif category == "Rods":
        rods_data = load_table(f"magic_items", sub_table=sub_table)["Rods"]
        try:
            usable_rods = [
                x for x in RODS if intersect(filters["Usable By"], RODS[x]["Usable By"])
            ]
            mutate_data_if_equal_keys(rods_data, usable_rods)
        # If "Usable By" is empty, generate any rod
        except KeyError:
            pass
        item = gen(**rods_data)
        charges = roll(*RODS[item]["Charges"])
        return f"{item} ({charges} charges)"
    elif category == "Staves":
        staves_data = load_table(f"magic_items", sub_table=sub_table)["Staves"]
        try:
            usable_staves = [
                x
                for x in STAVES
                if intersect(filters["Usable By"], STAVES[x]["Usable By"])
            ]
            mutate_data_if_equal_keys(staves_data, usable_staves)
        except KeyError:
            pass
        return gen(**staves_data)
    else:
        item = gen(**magic_items[category])
        # Fill the Beaker
        if category == "Bags and Bottles" and item == "Beaker of Plentiful Potions":
            potions = []
            for _ in range(0, roll(1, 4, 1)):
                doses = roll(1, 4, 1)
                potion = random_magic_item(
                    category="Potions and Oils", sub_table=sub_table
                )
                potions.append(f"{potion} ({doses} doses)")
            item = f"{item} (Potions: {', '.join(potions)})"
        # Write the Robe of Useful Items' scrolls
        if (
            category == "Cloaks and Robes"
            and item.startswith("Robe of Useful Items")
            and "Scroll" in item
        ):
            scroll_count = len(re.findall("Scroll", item))
            scroll_match = re.match(r"^(.+?) (Scroll(, )?)+(, .+?)?$", item)
            if scroll_match:
                scrolls = [str(generate_scroll()) for x in range(0, scroll_count)]
                item = f"{scroll_match.group(1)} {', '.join(scrolls)}"
                if scroll_match.group(4):
                    item += scroll_match.group(4)
        # Write the scrolls
        elif category == "Scrolls" and item == "Spell Scroll":
            scroll_type = None
            scroll_data = load_table("scroll_types.json")
            # If this character can use scrolls, give them an appropriate one
            # Otherwise, give them something random
            if "Usable By" in filters and filters["Usable By"]:
                mutate_data_if_equal_keys(scroll_data, filters["Usable By"])
            scroll_type = gen(**scroll_data)
            item = str(generate_scroll(scroll_type=scroll_type))
        # Fill the Ring of Spell Storing with spells
        elif category == "Rings" and item == "Ring of Spell Storing":

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
                expanded = sub_table == "expanded"
                spells.append(
                    f"{spell_level}:{random_spell(spell_level, caster_class, expanded=expanded)}"
                )
            item = f"{item} ({caster_class}): {', '.join(spells)}"

        # Trap some wands
        if category == "Wands":
            if roll(1, 100, 0) == 1:
                item = f"{item} (Trapped)"

    return item


def random_magic_weapon(**kwargs):
    base_item = kwargs.get("base_item")
    data = kwargs.get("data")
    sub_table = kwargs.get("sub_table", "standard")
    filters = build_filters(**kwargs)
    if kwargs.get("load_table") and data is None:
        data = load_table("magic_item_weapons", sub_table=sub_table)

    if not base_item:
        if data is not None:
            base_item = gen(**data)
        else:
            base_item = random.choice(table_keys_by_filter(WEAPONS, filters))

    if base_item == "Special" or base_item in SPECIAL_MAGIC_WEAPONS:
        if base_item == "Special":
            base_item = None
        return special_magic_weapon(
            special=base_item,
            sub_table=sub_table,
            filters=filters,
        )

    # See if the item has a quantity specified on the random table
    quantity_match = re.match(r"^.*\((\d+)d(\d+)\)$", base_item)
    quantity = None
    if quantity_match:
        quantity = roll(int(quantity_match.group(1)), int(quantity_match.group(2)), 0)
        base_item = re.sub(r"\s*\(\d+d\d+\)$", "", base_item)

    if base_item in set([WEAPONS[x]["Base Type"] for x in WEAPONS]):
        base_item = random.choice(
            table_keys_by_filter(WEAPONS, {"Base Type": base_item, "Source": sub_table})
        )

    # If the item is supposed to have a quantity and it doesn't yet, give it one
    if quantity is None and "Quantity" in WEAPONS[base_item]:
        quantity = roll(*WEAPONS[base_item]["Quantity"])

    adjustment = gen_table(
        f"magic_item_weapon_adjustment",
        sub_table=sub_table,
        base_type=WEAPONS[base_item]["Base Type"],
    )

    weapon = f"{base_item} {plusify(adjustment)}"
    if quantity:
        weapon = f"{weapon} x{quantity}"

    # Check to see if weapon is intelligent
    if WEAPONS[base_item]["Category"] == "Melee":
        intelligent_chance = 5
        if WEAPONS[base_item]["Base Type"] == "Sword":
            intelligent_chance = 25
        if roll(1, 100, 0) <= intelligent_chance:
            weapon = intelligent_weapon(weapon, sub_table=sub_table)

    return weapon


# Use random item generation tables to choose random special magic weapon
def random_special_magic_item(**kwargs):
    sub_table = kwargs.get("sub_table", "standard")
    item_type = kwargs.get("item_type", "Weapons")
    filters = build_filters(**kwargs)

    random_table = f"magic_item_special_weapons"
    special_table = SPECIAL_MAGIC_WEAPONS
    if item_type == "Armor":
        random_table = f"magic_item_special_armor"
        special_table = SPECIAL_MAGIC_ARMOR

    allowed = table_keys_by_filter(special_table, filters)
    data = load_table(random_table, sub_table=sub_table)
    mutate_data_if_equal_keys(data, allowed)
    special = gen(**data)
    if item_type == "Armor":
        return special_magic_armor(
            special=special, sub_table=sub_table, filters=filters
        )
    else:
        return special_magic_weapon(
            special=special, sub_table=sub_table, filters=filters
        )


def random_item(**kwargs):
    item_list = kwargs.get("item_list")
    filters = kwargs.get("filters", {})
    item_type = kwargs.get("item_type", "Weapons")
    item_tables = {
        "Armor": ARMOR,
        "Weapons": WEAPONS,
    }

    filters = build_filters(**kwargs)

    items = table_keys_by_filter(item_tables[item_type], filters)
    if item_list:
        items = [x for x in items if x in item_list]
    return random.choice(items)


def special_magic_armor(**kwargs):
    special = kwargs.get("special")
    force_results = kwargs.get("force_results", {})
    sub_table = kwargs.get("sub_table", "standard")
    filters = build_filters(**kwargs, item_type="Armor")

    if special == None:
        special = random.choice(table_keys_by_filter(SPECIAL_MAGIC_ARMOR, filters))

    armor = special
    # Determine base item, if any
    if SPECIAL_MAGIC_ARMOR[special]["Random Armor"]:
        filters["Category"] = "Armor"
        armor = SPECIAL_MAGIC_ARMOR[special]["Format"].format(
            base_item=random.choice(table_keys_by_filter(ARMOR, filters))
        )

    adjustment = SPECIAL_MAGIC_ARMOR[special].get("Adjustment", None)
    if adjustment:
        armor = f"{armor} {gen(**adjustment)}"

    if SPECIAL_MAGIC_ARMOR[special].get("Cursed"):
        armor += " (Cursed)"
    return armor


def special_magic_weapon(**kwargs):
    special = kwargs.get("special")
    force_results = kwargs.get("force_results", {})
    sub_table = kwargs.get("sub_table", "standard")
    filters = build_filters(**kwargs, item_type="Weapons")

    gen_output_order = ["Adjustment", "Details", "Charges", "Quantity"]
    if special == None:
        special = random.choice(table_keys_by_filter(SPECIAL_MAGIC_WEAPONS, filters))

    # Determine base item, if any
    base_item = None
    if not SPECIAL_MAGIC_WEAPONS[special].get("Generic Item", False):
        try:
            base_item = random_item(
                item_list=SPECIAL_MAGIC_WEAPONS[special]["Base Items"], filters=filters
            )
        except KeyError:
            base_item = random_item(
                filters={
                    **{"Base Type": SPECIAL_MAGIC_WEAPONS[special]["Base Type"]},
                    **filters,
                }
            )

    weapon = base_item
    sub_gens = SPECIAL_MAGIC_WEAPONS[special].get("Gens", {})
    gen_results = {}
    for sub_gen in sub_gens:
        if sub_gen not in force_results:
            gen_results[sub_gen] = gen(**sub_gens[sub_gen], base_item=base_item)
    # Force some gen_results
    for sub_gen in force_results:
        gen_results = force_results[sub_gen]

    # Reformat name as specified
    weapon = SPECIAL_MAGIC_WEAPONS[special]["Format"].format(base_item=base_item)
    weapon = " ".join(
        [weapon]
        + sorted(
            [gen_results[x] for x in gen_results],
            key=lambda y: gen_output_order.index(y)
            if y in gen_output_order
            else len(gen_output_order) + 1,
        )
    )
    if SPECIAL_MAGIC_WEAPONS[special].get("Cursed"):
        weapon += " (Cursed)"
    return weapon


def usable_by(classes):
    usable_priority = {
        "Armor": [
            "Heavy",
            "Bard",
            "Elf Fighter/Mage",
            "Druid",
            "Ranger",
            "Rogue",
            "Mage",
        ],
        "Weapons": ["Warrior", "Rogue", "Druid", "Cleric", "Mage"],
    }

    def best_option(priority_group, options):
        return usable_priority[priority_group][
            min([usable_priority[priority_group].index(x) for x in options])
        ]

    exclusive_weapon_groups = set(["Druid", "Cleric"])
    usable_lists = {"Armor": [], "Rods": [], "Scrolls": [], "Staves": [], "Weapons": []}
    usable = {
        "Armor": "Mage",
        "Rods": [],
        "Scrolls": [],
        "Staves": [],
        "Weapons": "Mage",
    }

    for class_name in classes:
        # These categories aren't lists, so just append them
        for category in ["Armor", "Rods", "Weapons"]:
            usable_lists[category].append(CLASSES[class_name]["Usable By"][category])
        # THese categories are lists, so add them
        for category in ["Scrolls", "Staves"]:
            try:
                usable_lists[category] += list(
                    CLASSES[class_name]["Usable By"][category]
                )
            except KeyError:
                pass

    for category_best in ["Armor", "Weapons"]:
        usable[category_best] = best_option(category_best, usable_lists[category_best])
    for category in ["Rods", "Scrolls", "Staves"]:
        usable[category] = list(set(usable_lists[category]))

    has_exclusive = list(
        set(usable_lists["Weapons"]).intersection(exclusive_weapon_groups)
    )
    if has_exclusive:
        usable["Weapons"] = has_exclusive[-1]
    return usable


def weapons_by_type(weapon_type):
    return [x for x in WEAPONS if WEAPONS[x]["Base Type"] == weapon_type]


def main():
    import simple_gen

    def gen_all_special_weapons():
        for weapon in simple_gen.dump_data(
            **load_table("magic_item_special_weapons_standard.json")
        ):
            print(special_magic_weapon(special=weapon))

    def gen_all_categories(**kwargs):
        for category in simple_gen.dump_data(
            **load_table("magic_item_categories_standard.json")
        ):
            print(f"{category:25}  {random_magic_item(category=category, **kwargs)}")

    gen_all_categories(classes=["Fighter"], sub_table="expanded")


if __name__ == "__main__":
    main()
