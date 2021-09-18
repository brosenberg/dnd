#!/usr/bin/env python3

import argparse
import json
import os
import random

from dice import roll
from generate_scroll import generate_scroll
from generate_scroll import random_spell
from generate_scroll import random_random_spell


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
    base_wand = load_and_roll("wands.json", mod=mod)
    charges = roll(1, 20, 80)
    trapped = False
    if roll(1, 100, 0) == 1:
        trapped = True

    if base_wand == "Wand of Earth and Stone":
        if roll(1, 100, 0) <= 50:
            base_wand = f"{base_wand} (transmute mud to rock and transmute rock to mud)"

    base_wand = f"{base_wand} ({charges} charges)"
    if trapped:
        base_wand = f"{base_wand} (trapped)"
    return base_wand


def books(mod=0):
    base_book = load_and_roll("books.json", mod=mod)
    if base_book == "Book of Infinite Spells":
        pages = (1, 8, 22)
        base_book = f"{base_book} ({pages} pages)"
    elif base_book == "Manual of Golems":
        manual_of_golems = load_and_roll("manual_of_golems.json")
        base_book = f"{base_book} ({manual_of_golems})"
    return base_book


def jewelry(mod=0):
    result = roll(1, 6, 0)
    base_jewelry = None
    if result < 4:
        base_jewelry = load_and_roll("jewelry_a.json", mod=mod)
    else:
        base_jewelry = load_and_roll("jewelry_b.json", mod=mod)

    if base_jewelry == "Amulet Versus Undead":
        amulet_versus_undead = load_and_roll("amulet_versus_undead.json")
        base_jewelry = f"{base_jewelry} ({amulet_versus_undead} level)"
    elif base_jewelry == "Medallion of ESP":
        medallion_of_esp = load_and_roll("medallion_of_esp.json")
        base_jewelry = f"{base_jewelry} ({medallion_of_esp})"
    elif base_jewelry == "Necklace of Missiles":
        necklace_of_missiles = load_and_roll("necklace_of_missiles.json")
        base_jewelry = f"{base_jewelry} ({necklace_of_missiles})"
    elif base_jewelry == "Necklace of Prayer Beads":
        beads = []
        for _ in range(0, roll(1, 4, 2)):
            beads.append(load_and_roll("prayer_beads.json"))
        base_jewelry = f"{base_jewelry} (Beads: {', '.join(sorted(beads))}"
    elif base_jewelry == "Pearl of Power":
        pearl_of_power = load_and_roll("pearl_of_power.json")
        if pearl_of_power == "two spells":
            levels = [roll(1, 6, 0), roll(1, 6, 0)]
            pearl_of_power = f"{pearl_of_power} ({', '.join(levels)})"
        base_jewelry = f"{base_jewelry} ({pearl_of_power})"
        if roll(1, 20, 0) == 20:
            base_jewelry = f"{base_jewelry} (cursed)"
    elif base_jewelry == "Periapt of Proof Against Poison":
        proof_against_poison = load_and_roll("proof_against_poison.json")
        base_jewelry = f"{base_jewelry} ({proof_against_poison})"
    elif base_jewelry == "Phylactery of Long Years":
        if roll(1, 20, 0) == 20:
            base_jewelry = f"{base_jewelry} (cursed)"
    elif base_jewelry == "Scarab of Enraging Enemies":
        base_jewelry = f"{base_jewelry} ({roll(1, 6, 18)} charges)"
    elif base_jewelry == "Scarab of Insanity":
        base_jewelry = f"{base_jewelry} ({roll(1, 8, 8)} charges)"
    elif base_jewelry == "Scarab of Protection":
        if roll(1, 20, 0) == 20:
            base_jewelry = f"{base_jewelry} (cursed)"
    elif base_jewelry == "Scarab Versus Golems":
        scarab_versus_golems = load_and_roll("scarab_versus_golems.json")
        base_jewelry = f"{base_jewelry} ({scarab_versus_golems})"

    return base_jewelry


def cloaks_robes(mod=0):
    base_item = load_and_roll("cloaks_robes.json", mod=mod)
    if base_item == "Cloak of Displacement":
        size = "normal sized"
        if roll(1, 100, 0) > 75:
            size = "small sized"
        base_item = f"{base_item} ({size})"
    elif base_item == "Cloak of Elvenkind":
        size = "normal sized"
        if roll(1, 100, 0) > 90:
            size = "small sized"
        base_item = f"{base_item} ({size})"
    elif base_item == "Cloak of Protection":
        cloak_of_protection = load_and_roll("cloak_of_protection.json")
        base_item = f"{base_item} {cloak_of_protection}"
    elif base_item == "Robe of the Archmagi":
        robe_archmagi = load_and_roll("robe_archmagi.json")
        base_item = f"{base_item} ({robe_archmagi})"
    elif base_item == "Robe of Useful Items":
        item_count = roll(4, 4, 0)
        items = []
        while item_count > 0:
            item = load_and_roll("useful_items.json")
            if item == "Scroll":
                item = f"{item} - {random_random_spell()}"
            if item == "Roll twice":
                item_count += 2
            else:
                items.append(item)
            item_count -= 1
        base_item = f"{base_item} (Items: {', '.join(sorted(items))})"
    return base_item


def boots_bracers_gloves(mod=0):
    base_item = load_and_roll("boots_bracers_gloves.json", mod=mod)

    if base_item == "Boots of Levitation":
        weight = 280 + (14 * roll(1, 20, 0))
        base_item = f"{base_item} ({weight} lbs.)"
    elif base_item == "Boots of Varied Tracks":

        def get_track_type():
            table_roll = roll(1, 6, 0)
            if table_roll < 4:
                return load_and_roll("varied_tracks_a.json")
            else:
                return load_and_roll("varied_tracks_b.json")

        track_types = []
        while len(track_types) < 4:
            new_track_type = get_track_type()
            if new_track_type not in track_types:
                track_types.append(new_track_type)
        base_item = f"{base_item} (Track Types: {', '.join(track_types)})"
    elif base_item == "Winged Boots":
        winged_boots = load_and_roll("winged_boots.json")
        base_item = f"{base_item} ({winged_boots})"
    elif base_item == "Bracers of Defense":
        bracers_of_defense = load_and_roll("bracers_of_defense.json")
        base_item = f"{base_item} ({bracers_of_defense})"

    return base_item


def girdles_hats_helms(mod=0):
    base_item = load_and_roll("girdles_hats_helms.json", mod=mod)
    if base_item == "Girdle of Giant Strength":
        girdle_giant_strength = load_and_roll("girdle_giant_strength.json")
        base_item = f"{base_item} ({girdle_giant_strength})"
    return base_item


def containers(mod=0):
    base_container = load_and_roll("containers.json", mod=mod)
    if base_container == "Bag of Beans":
        beans = roll(3, 4, 0)
        base_container = f"{base_container} ({beans} beans)"
    elif base_container == "Bag of Holding":
        bag_of_holding = load_and_roll("bag_of_holding.json")
        base_container = f"{base_container} ({bag_of_holding})"
    elif base_container == "Bag of Tricks":
        bag_of_tricks = load_and_roll("bag_of_tricks.json")
        base_container = f"{base_container} ({bag_of_tricks})"
    elif base_container == "Beaker of Plentiful Potions":
        potions = []
        for _ in range(0, roll(1, 4, 1)):
            doses = roll(1, 4, 1)
            potions.append(f"{potions_and_oils()} ({doses} doses)")
        base_container = f"{base_container} (Potions: {', '.join(potions)})"
    elif base_container == "Bucknard's Everfull Purse":
        everfull_purse = load_and_roll("everfull_purse.json")
        base_container = f"{base_container} ({everfull_purse})"
    elif base_container == "Iron Flask":
        iron_flask = load_and_roll("iron_flask.json")
        base_container = f"{base_container} ({iron_flask})"
    return base_container


def candles_dust_stones(mod=0):
    base_item = load_and_roll("candles_dust_stones.json", mod=mod)
    if base_item == "Dust of Dryness":
        pinches = roll(1, 6, 4)
        base_item = f"{base_item} ({pinches} pinches)"
    elif base_item == "Dust of Illusion":
        pinches = roll(1, 10, 10)
        base_item = f"{base_item} ({pinches} pinches)"
    elif base_item == "Dust of Tracelessness":
        pinches = roll(1, 12, 12)
        base_item = f"{base_item} ({pinches} pinches)"
    elif base_item == "Incense of Meditation":
        pieces = roll(2, 4, 0)
        base_item = f"{base_item} ({pieces} pieces)"
    elif base_item == "Incense of Obsession":
        pieces = roll(2, 4, 0)
        base_item = f"{base_item} ({pieces} pieces)"
    elif base_item == "Ioun Stone":
        ioun_stones = load_and_roll("ioun_stones.json")
        if ioun_stones == "dull gray":
            shape = random.choice(
                ["rhomboid", "sphere", "prism", "spindle", "ellipsoid"]
            )
            ioun_stones = f"{ioun_stone} {shape}"
        base_item = f"{base_item} ({ioun_stones})"
    elif base_item == "Keoghtom's Ointment":
        jars = roll(1, 3, 0)
        base_item = f"{base_item} ({jars} jars)"
    elif base_item == "Smoke Powder":
        charges = roll(3, 6, 0)
        base_item = f"{base_item} ({charges} charges)"
    elif base_item == "Sovereign Glue":
        ounces = roll(1, 10, 0)
        base_item = f"{base_item} ({ounces} ounces)"
    return base_item


def household_tools(mod=0):
    base_item = load_and_roll("household_tools.json", mod=mod)
    if base_item == "Carpet of Flying":
        carpet_of_flying = load_and_roll("carpet_of_flying.json")
        base_item = f"{base_item} ({carpet_of_flying})"
    return base_item


def musical_instruments(mod=0):
    base_item = load_and_roll("musical_instruments.json", mod=mod)
    if base_item == "Horn of Valhalla":
        horn_of_valhalla = load_and_roll("horn_of_valhalla.json")
        base_item = f"{base_item} ({horn_of_valhalla})"
    return base_item


def weird(mod=0):
    result = roll(1, 6, 0)
    base_weird = None
    if result < 4:
        base_weird = load_and_roll("weird_a.json", mod=mod)
    else:
        base_weird = load_and_roll("weird_b.json", mod=mod)

    if base_weird == "Crystal Ball":
        crystal_ball = load_and_roll("crystal_ball.json")
        base_weird = f"{base_weird} {crystal_ball}"
    elif base_weird == "Figurine of Wondrous Power":
        figurine_of_power = load_and_roll("figurine_of_power.json")
        if figurine_of_power == "Marble elephant":
            if roll(1, 100, 0) > 90:
                figurine_of_power = f"{figurine_of_power} - Prehistoric Elephant"
            else:
                figurine_of_power = f"{figurine_of_power} - Normal Elephant"
        base_weird = f"{base_weird} ({figurine_of_power})"
    elif base_weird == "Quaal's Feather Token":
        feather_token = load_and_roll("feather_token.json")
        base_weird = f"{base_weird} ({feather_token})"

    return base_weird


def armor(mod=0):
    base_armor = load_and_roll("armor_type.json", mod=mod)
    adjustment = load_and_roll("armor_adjustment.json")
    if base_armor == "Special":
        base_armor = load_and_roll("special_armor.json")
        if base_armor == "Elven Chain Mail":
            elven_chain_size = load_and_roll("elven_chain_size.json")
            base_armor = f"{base_armor} (Size: {elven_chain_size})"
        return base_armor
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
    intelligent = False
    is_sword = False
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
        is_sword = True
        if base_weapon == "Sword":
            base_weapon = load_and_roll("sword_types.json")
        adjustment = load_and_roll("sword_adjustment.json")
    else:
        if base_weapon == "Pole Arm":
            base_weapon = load_and_roll("polearms.json")
        adjustment = load_and_roll("weapon_adjustment.json")

    if is_sword:
        if roll(1, 100, 0) <= 25:
            return intelligent_weapon(base_weapon, adjustment)
    elif can_be_intelligent(base_weapon):
        if roll(1, 100, 0) <= 5:
            return intelligent_weapon(base_weapon, adjustment)

    return f"{base_weapon} {adjustment}"


def sword():
    base_weapon = load_and_roll("sword_types.json")
    adjustment = load_and_roll("sword_adjustment.json")
    if roll(1, 100, 0) > 25:
        return f"{base_weapon} {adjustment}"
    else:
        return intelligent_weapon(base_weapon, adjustment)


def non_sword():
    base_weapon = load_and_roll("non_sword_weapons.json")
    adjustment = load_and_roll("weapon_adjustment.json")
    if roll(1, 100, 0) > 5 and can_be_intelligent(base_weapon):
        return f"{base_weapon} {adjustment}"
    else:
        return intelligent_weapon(base_weapon, adjustment)


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


def can_be_intelligent(base_weapon):
    if (
        "Arrow" in base_weapon
        or "Bolt" in base_weapon
        or "Bullet" in base_weapon
        or "Dart" in base_weapon
        or "Javelin" in base_weapon
    ):
        return False
    else:
        return True


def intelligent_weapon(base_weapon, adjustment):
    intelligence = load_and_roll("weapon_intelligence.json")
    alignment = load_and_roll("weapon_alignment.json")
    communication = "speech"
    primary_abilities = 3
    extraordinary_abilities = 0
    has_special_purpose = False
    special_purpose = "None"
    abilities = []
    languages_spoken = load_and_roll("weapon_languages.json")
    ego = int(adjustment) + int(languages_spoken)
    if intelligence == 12:
        communication = "semi-empathy"
        primary_abilities = 1
    elif intelligence == 13:
        communication = "empathy"
        primary_abilities = 2
    elif intelligence == 14:
        primary_abilities = 2
    elif intelligence == 16:
        abilities.append("read nonmagical languages/maps")
        ego += 1
    elif intelligence == 17:
        communication = "speech and telepathy"
        extraordinary_abilities = 1
        abilities.append("read magical languages/maps/writings")
        ego += 4

    for _ in range(0, primary_abilities):
        ability = load_and_roll("weapon_primary_abilities.json")
        while ability in abilities:
            ability = load_and_roll("weapon_primary_abilities.json")
        if ability == "Roll Twice":
            def roll_twice_primary():
                ability = load_and_roll("weapon_primary_abilities_nrt.json")
                while ability in abilities:
                    ability = load_and_roll("weapon_primary_abilities_nrt.json")
                if ability == "Extraordinary Powers":
                    primary_abilities -= 1
                    extraordinary_abilities += 1
                else:
                    abilities.append(ability)
            roll_twice_primary()
            roll_twice_primary()
        elif ability == "Extraordinary Powers":
            primary_abilities -= 1
            extraordinary_abilities += 1
        else:
            abilities.append(ability)

    def special_purpose_roll():
        has_special_purpose = True
        ability = load_and_roll("weapon_extraordinary_abilities_nsp.json")
        while ability in abilities:
            ability = load_and_roll("weapon_extraordinary_abilities_nsp.json")
        return ability

    for _ in range(0, extraordinary_abilities):
        ability = load_and_roll("weapon_extraordinary_abilities.json")
        while ability in abilities:
            ability = load_and_roll("weapon_extraordinary_abilities.json")
        if ability == "Roll Twice":
            def roll_twice_extra():
                ability = load_and_roll("weapon_extraordinary_abilities_nrt.json")
                while ability in abilities:
                    ability = load_and_roll("weapon_extraordinary_abilities_nrt.json")
                if ability == "Special Purpose":
                    ability = special_purpose_roll()
                abilties.append(ability)
            roll_twice_extra()
            roll_twice_extra()
        elif ability == "Special Purpose":
            abilities.append(special_purpose_roll())
        else:
            abilities.append(ability)

    if has_special_purpose:
        special_purpose = load_and_roll("weapon_special_purpose.json")
        special_power = load_and_roll("weapon_special_power.json")
        abilities.append(f"Special Purpose: {special_power}")
        ego += 5

    ego += primary_abilities + extraordinary_abilities * 2

    return f"{base_weapon} {adjustment} (Intelligent) - Int:{intelligence}  Ego:{ego}  Alignment:{alignment}  Communication:{communication} Languages:{languages_spoken}  Special Purpose:{special_purpose}  Abilities:{', '.join(sorted(abilities))}"


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
