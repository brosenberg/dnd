#!/usr/bin/env python3

import json
import random
import re
import os

from dice import roll
from generate_scroll import generate_scroll
from magic_item import MagicItemGen
from simple_gen import gen
from spells import random_spell
from utils import choice_table_count_unique
from utils import load_table
from utils import plusify
from utils import table_keys_by_filter


AMMOS = load_table("weapons_ammos.json")
ARMOR = load_table("armor_master_list.json")
ARMOR_STATS = load_table("armor_stats.json")
SHIELDS = load_table("shields.json")
SPECIAL_MAGIC_ARMOR = load_table("magic_item_armor_special.json")
SPECIAL_MAGIC_WEAPONS = load_table("magic_item_weapons_special.json")
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


def gen_table(table, **kwargs):
    return gen(**load_table(table), **kwargs)


def get_ac(item):
    ac = get_armor_ac(item)
    if ac:
        return (ac, None)
    ac = get_shield_ac_bonus(item)
    if ac:
        return (None, ac)
    return (None, get_other_ac_bonus(item))


def get_adjustment(item):
    magic = re.match(r"^(.+?) ([+-][0-9]+)(, .+?)?$", item)
    if magic:
        return (magic.group(1), int(magic.group(2)))
    return (item, 0)


def get_armor_ac(armor):
    if armor == "Bracers of Defenselessness":
        return 10
    remove_list = [" of Blending", " of Missile Attraction"]
    for remove in remove_list:
        armor = armor.replace(remove, "")
    bracers_of_defense = re.match(r"^Bracers of Defense \(AC ([0-9]+)\)$", armor)
    if bracers_of_defense:
        return int(bracers_of_defense.group(1))
    armor, adjustment = get_adjustment(armor)
    armor = armor.title()
    try:
        return ARMOR_STATS[armor]["AC"] - adjustment
    except KeyError:
        pass


def get_shield_ac_bonus(shield):
    if is_shield(shield):
        _, adjustment = get_adjustment(shield)
        return 1 + adjustment
    return None


def get_other_ac_bonus(item):
    protection_items = ["Ring of Protection", "Cloak of Protection"]
    for protection_item in protection_items:
        if protection_item in item:
            _, adjustment = get_adjustment(item)
            return adjustment
    return None


def intelligent_weapon(base_weapon, table="standard"):
    tables = load_table(f"magic_item_weapons_intelligent_{table}")
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
    if table == "standard":
        if intelligence > 16:  # Telepathic and Read magic ability
            ego_bonus += 4
        if intelligence > 15:  # Read language ability
            ego_bonus += 1
        ego_bonus += len(weapon_powers["Primary"])
        ego_bonus += len(weapon_powers["Languages"])
    elif table == "expanded":
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


def random_armor(expanded=False, table=None, classes=[], level=1):
    armors = []
    if table:
        armors = load_table(table)
    else:
        armor_groups = list(set([appropriate_armor_group(x) for x in classes]))
        if len(armor_groups) == 1:
            armor_group = armor_groups[0]
            if armor_group == "warrior":
                if level > 3:
                    armors = load_table("armor_high.json")
                else:
                    armors = load_table("armor_low.json")
            elif armor_group == "bard":
                if level > 2:
                    armors = load_table("armor_bard.json")
                else:
                    armors = load_table("armor_rogue.json")
            else:
                table = f"armor_{appropriate_armor_group(armor_group)}.json"
                armors = load_table(table)
        else:
            table = f"armor_{appropriate_armor_group(classes[0])}.json"
            armors = set(load_table(table))
            for class_name in classes[1:]:
                table = f"armor_{appropriate_armor_group(class_name)}.json"
                armors = armors.intersection(set(load_table(table)))
            armors = list(armors)
    try:
        return random.choice(armors)
    except IndexError:
        return None


def random_appropriate_ammo(weapon):
    try:
        ammo = appropriate_ammo_type(weapon)
        dice, die, mod = random_item_count(ammo)
        count = roll(dice, die, mod)
        return (ammo, count)
    except TypeError:
        return None


def random_item_count(item):
    try:
        return WEAPONS[base_weapon(item)]["Quantity"]
    # FIXME
    except:
        pass
    return None


def random_shield():
    return random.choice(SHIELDS)


def random_magic_armor(table="standard", base_item=None, filters={}):
    if not filters:
        filters["Source"] = table
    if not base_item:
        if table:
            base_item = gen_table(f"magic_item_armors_{table}")
        else:
            base_item = random.choice(table_keys_by_filter(ARMOR, filters))

    if base_item == "Special":
        return random_special_magic_armor(table=table, filters=filters)
    adjustment = gen(**load_table(f"magic_item_armor_adjustment_{table}"))
    base_item = f"{base_item} {plusify(adjustment)}"
    if adjustment < 0:
        base_item += " (Cursed)"
    return base_item


def random_magic_item(category, table="standard", expanded=False):
    magic_items = load_table(f"magic_items_{table}")
    data = None
    subcategories = {
        "Armor No Shields": {
            "Category": "Armor and Shields",
            "Data": f"magic_item_armor_only_{table}"
        },
        "Sword": {
            "Category": "Weapons",
            "Data": f"magic_item_weapon_sword_{table}"
        },
        "Nonsword": {
            "Category": "Weapons",
            "Data": f"magic_item_weapon_nonsword_{table}"
        },
    }

    if category in subcategories:
        data = subcategories[category]["Data"]
        category = subcategories[category]["Category"]

    if category == "Weapons":
        return random_magic_weapon(table=table)
    elif category == "Armor and Shields":
        return random_magic_armor(table=table)
    else:
        item = gen(**magic_items[category])
        # Fill the Beaker
        if category == "Bags and Bottles" and item == "Beaker of Plentiful Potions":
            potions = []
            for _ in range(0, roll(1, 4, 1)):
                doses = roll(1, 4, 1)
                potion = random_magic_item(
                    "Potions and Oils", table=table, expanded=expanded
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
            scrolls = [str(generate_scroll()) for x in range(0, scroll_count)]
            item = f"{m.group(1)} {', '.join(scrolls)}"
            if m.group(4):
                item += m.group(4)
        # Write the scrolls
        elif category == "Scrolls" and item == "Spell Scroll":
            item = str(generate_scroll())
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
                spells.append(
                    f"{spell_level}:{random_spell(spell_level, caster_class, expanded=expanded)}"
                )
            item = f"{base_ring} ({caster_class}): {', '.join(spells)}"

        # Trap some wands
        if category == "Wands":
            if roll(1, 100, 0) == 1:
                item = f"{item} (Trapped)"

    return item


def random_magic_weapon(**kwargs):
    base_item = kwargs.get("base_item")
    data = kwargs.get("data")
    table = kwargs.get("table", "standard")
    filters = kwargs.get("filters", {"Source": table})
    if kwargs.get("load_table") and data is None:
        data = load_table("magic_item_weapons_{table}")

    if not base_item:
        if data is not None:
            base_item = gen(**data)
        else:
            base_item = random.choice(table_keys_by_filter(WEAPONS, filters))

    if base_item == "Special":
        return random_special_magic_weapon(table=table, filters=filters)

    quantity_match = re.match(r"^.*\((\d+)d(\d+)\)$", base_item)
    quantity = None
    if quantity_match:
        quantity = roll(int(quantity_match.group(1)), int(quantity_match.group(2)), 0)
        base_item = re.sub(r"\s*\(\d+d\d+\)$", "", base_item)

    # Assume this is a weapon category first
    try:
        base_item = random.choice(
            table_keys_by_filter(WEAPONS, {"Base Type": base_item, "Source": table})
        )
    except IndexError:
        pass

    adjustment = gen_table(
        f"magic_item_weapon_adjustment_{table}",
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
            weapon = intelligent_weapon(weapon, table=table)

    return weapon


def random_special_magic_armor(table="standard", usable=None, filters={}):
    return special_magic_armor(
        special=gen_table(f"magic_item_special_armor_{table}"),
        table=table,
        usable=usable,
    )


def random_special_magic_weapon(table="standard", filters={}):
    return special_magic_weapon(
        special=gen_table(f"magic_item_special_weapons_{table}"), table=table
    )


# TODO: Update or remove this
def random_weapon(
    expanded=False, classes=[], class_groups=[], table=None, weapon_filter=None, level=1
):
    mig = MagicItemGen(expanded)
    weapon = None
    if table:
        weapons = load_table(table)
    else:
        if "Cleric" in classes:
            weapons = load_table("weapons_cleric.json")
        elif "Druid" in classes:
            weapons = load_table("weapons_druid.json")
        elif "Warrior" in class_groups or "Bard" in classes:
            if level > 1:
                weapons = load_table("weapons_warrior.json")
            else:
                weapons = load_table("weapons_generic.json")
        elif "Rogue" in classes:
            weapons = load_table("weapons_rogue.json")
        else:
            weapons = load_table("weapons_wizard.json")
    if weapon_filter:
        weapons = [x for x in weapons if weapon_filter(x)]
    return mig.diversify_weapon(random.choice(weapons))


def special_magic_armor(special=None, force_results={}, table="standard", usable=None):
    if special == None:
        special = random.choice(list(SPECIAL_MAGIC_ARMOR))

    armor = special
    # Determine base item, if any
    if SPECIAL_MAGIC_ARMOR[special]["Random Armor"]:
        filters = {"Source": table, "Category": "Armor"}
        if usable:
            filters["Usable By"] = usable
        armor = SPECIAL_MAGIC_ARMOR[special]["Format"].format(
            base_item=random.choice(table_keys_by_filter(ARMOR, filters))
        )

    adjustment = SPECIAL_MAGIC_ARMOR[special].get("Adjustment", None)
    if adjustment:
        armor = f"{armor} {gen(**adjustment)}"

    if SPECIAL_MAGIC_ARMOR[special].get("Cursed"):
        armor += " (Cursed)"
    return armor


def special_magic_weapon(special=None, force_results={}, table="standard"):
    gen_output_order = ["Adjustment", "Details", "Charges", "Quantity"]
    if special == None:
        special = random.choice(list(SPECIAL_MAGIC_WEAPONS))

    # Determine base item, if any
    base_item = None
    if not SPECIAL_MAGIC_WEAPONS[special].get("Generic Item", False):
        try:
            base_item = random.choice(SPECIAL_MAGIC_WEAPONS[special]["Base Items"])
        except KeyError:
            base_item = random.choice(
                table_keys_by_filter(
                    WEAPONS,
                    {
                        "Base Type": SPECIAL_MAGIC_WEAPONS[special]["Base Type"],
                        "Source": table,
                    },
                )
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


def weapons_by_type(weapon_type):
    return [x for x in WEAPONS if WEAPONS[x]["Base Type"] == weapon_type]


def main():
    import simple_gen

    def gen_all_special_weapons():
        for weapon in simple_gen.dump_data(
            **load_table("magic_item_special_weapons_standard.json")
        ):
            print(special_magic_weapon(special=weapon))

    def gen_all_categories():
        for category in simple_gen.dump_data(
            **load_table("magic_item_categories_standard.json")
        ):
            print(random_magic_item(category))

    gen_all_special_weapons()
    gen_all_categories()


if __name__ == "__main__":
    main()
