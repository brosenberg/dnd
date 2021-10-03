#!/usr/bin/env python3

import argparse
import json
import os
import random
import re

from second_gen.currency import get_gold_value
from second_gen.currency import gold_to_coins
from second_gen.currency import subtract_coins
from second_gen.dice import roll
from second_gen.items import get_ac
from second_gen.spells import Spells
from second_gen.roll_abilities import get_abilities
from second_gen.treasure import generate_treasure
from second_gen.utils import load_table


ARMOR = load_table("armor_master_list.json")
ABILITIES = load_table("abilities.json")
ABILITY_MODS = {
    "Strength": load_table("strength.json"),
    "Extrao Strength": load_table("extrao_strength.json"),
    "Dexterity": load_table("dexterity.json"),
    "Constitution": load_table("constitution.json"),
    "Intelligence": load_table("intelligence.json"),
    "Wisdom": load_table("wisdom.json"),
    "Charisma": load_table("charisma.json"),
}
ABILITY_ROLLS = load_table("ability_rolls.json")
ALIGNMENTS = load_table("alignments.json")
CLASSES = load_table("classes.json")
CLASS_GROUPS = load_table("class_groups.json")
CLASS_SPELLS = load_table("class_spells.json")
MULTICLASSES = load_table("classes_multi.json")
NWPS = load_table("nwps.json")
NWP_GROUPS = load_table("nwp_groups.json")
RACES = load_table("races.json")
SPELL_PROGRESSION = load_table("spell_progression.json")
THAC0 = load_table("thac0.json")
THIEF_SKILLS = load_table("thief_skills.json")
THIEF_SKILLS_STANDARD = load_table("thief_skills_standard.json")
THIEF_SKILLS_HLA = load_table("thief_skills_hla.json")
WEAPONS = load_table("weapons_master_list.json")
WISDOM_CASTERS = load_table("wisdom_casters.json")


def combine_minimums(minimums):
    minimum = {x: 0 for x in ABILITIES}
    for minima in minimums:
        for ability in minima:
            if minimum[ability] < minima[ability]:
                minimum[ability] = minima[ability]
    return minimum


def constitution_hp_modifier(con, class_group):
    if con <= 1:
        return -3
    elif con < 4:
        return -2
    elif con < 7:
        return -1
    elif con < 15:
        return 0
    elif con == 15:
        return 1
    elif class_group != "Warrior" or con == 16:
        return 2
    elif con == 17:
        return 3
    elif con == 18:
        return 4
    elif con < 21:
        return 5
    elif con < 24:
        return 6
    else:
        return 7


def convert_height(height):
    feet = int(height / 12)
    inches = height - (12 * feet)
    return f"{feet}'{inches}\""


def dexterity_mods(dexterity):
    return ABILITY_MODS["Dexterity"][str(dexterity)]


def dexterity_ac_mod(dexterity):
    return dexterity_mods(dexterity)[2]


def dexterity_to_hit(dexterity):
    return dexterity_mods(dexterity)[1]


def get_ability_priority(classes):
    def get_minimum(attribute):
        try:
            return minimums[attribute]
        except KeyError:
            return 3

    primary = []
    secondary = []
    minimums = combine_minimums([CLASSES[x]["Minimums"] for x in classes])
    for class_name in classes:
        primary += CLASSES[class_name]["Primary"]
        secondary += CLASSES[class_name]["Secondary"]
    # Sort the primary list based on the combined minimums of the classes
    primary = sorted(list(set(primary)), key=get_minimum, reverse=True)
    secondary = list(set(secondary))
    random.shuffle(secondary)
    for ability in primary:
        if ability in secondary:
            secondary.remove(ability)
    return primary + secondary


def get_alignment_by_classes(classes):
    alignments = set(CLASSES[classes[0]]["Alignments"])
    for class_name in classes[1:]:
        alignments = alignments.intersection(set(CLASSES[class_name]["Alignments"]))
    return random.choice(list(alignments))


def get_all_classes():
    return list(CLASSES.keys())


def get_best_thac0(classes, levels):
    thac0 = 20
    for class_name, level in zip(classes, levels):
        # THAC0 stops improving past level 20
        if level > 20:
            level = 20
        if THAC0[get_class_group(class_name)][level - 1] < thac0:
            thac0 = THAC0[get_class_group(class_name)][level - 1]
    return thac0


def get_caster_group(class_name):
    if class_name == "Paladin":
        caster = "Paladin"
    elif class_name == "Ranger":
        caster = "Ranger"
    elif class_name == "Bard":
        caster = "Bard"
    else:
        caster = get_class_groups([class_name])[0]
    if caster in SPELL_PROGRESSION.keys():
        return caster
    return None


def get_class_group(class_name):
    return [x for x in CLASS_GROUPS if class_name in CLASS_GROUPS[x]["Classes"]][0]


def get_class_groups(classes):
    return list(set([get_class_group(x) for x in classes]))


def get_hitpoints(class_groups, levels, constitution):
    con_mod = constitution_hp_modifier(constitution, class_groups)
    hitpoints = 0
    for class_group, level in zip(class_groups, levels):
        hit_dice, additional_hp = CLASS_GROUPS[class_group]["Hit Dice"][level - 1]
        class_hp = 0
        for die in range(0, hit_dice):
            result = roll(1, CLASS_GROUPS[class_group]["Hit Die"], con_mod)
            if result < 1:
                result = 1
            class_hp += result
        hitpoints += int((class_hp + additional_hp) / len(levels))
    return hitpoints


def get_level_by_experience(
    class_name, experience, experience_penalty=[1, 1], level_limit=None
):
    if level_limit is None:
        level_limit = 99
    for level, requirement in enumerate(CLASSES[class_name]["Levels"]):
        penalty = (
            experience_penalty[0] if level <= level_limit else experience_penalty[1]
        )
        if experience <= requirement * penalty:
            return level
    return 30


def get_levels_by_experience(
    classes, experience, experience_penalty=[1, 1], level_limits=None
):
    levels = []
    if level_limits is None:
        level_limits = [None for x in classes]
    for class_name, xp, level_limit in zip(classes, experience, level_limits):
        levels.append(
            get_level_by_experience(
                class_name,
                xp,
                experience_penalty=experience_penalty,
                level_limit=level_limit,
            )
        )
    return levels


def get_level_limits(race, classes, abilities):
    limits = []
    for class_name in classes:
        limits.append(
            RACES[race]["Limits"][class_name] + level_limit_bonus(class_name, abilities)
        )
    return limits


def get_nwp_slots(class_groups, level, intelligence):
    base_nwps = 0
    nwp_rate = 99
    for class_group in class_groups:
        if CLASS_GROUPS[class_group]["Proficiencies"]["Nonweapon"][0] > base_nwps:
            base_nwps = CLASS_GROUPS[class_group]["Proficiencies"]["Nonweapon"][0]
        if CLASS_GROUPS[class_group]["Proficiencies"]["Nonweapon"][1] < nwp_rate:
            nwp_rate = CLASS_GROUPS[class_group]["Proficiencies"]["Nonweapon"][1]
    return (
        base_nwps
        + int(level / nwp_rate)
        + intelligence_bonus_proficiencies(intelligence)
    )


# TODO: Make this return multiclasses sometimes
def get_random_classes(
    class_group=None, alignment=None, can_multiclass=True, multiclass_chance=20
):
    classes = set(CLASSES.keys())
    if alignment:
        alignment_classes = set()
        for class_name in CLASSES:
            if alignment in CLASSES[class_name]["Alignments"]:
                alignment_classes.add(class_name)
        classes = classes.intersection(alignment_classes)
    if can_multiclass and roll(1, 100, 0) <= multiclass_chance:
        classes = classes.intersection(
            set([y for x in MULTICLASSES for y in x.split("/")])
        )
        base_class = None
        if class_group:
            base_class = random.choice(
                list(classes.intersection(set(CLASS_GROUPS[class_group]["Classes"])))
            )
        else:
            base_class = random.choice(list(classes))
        possible_multiclasses = [x for x in MULTICLASSES if base_class in x]
        if alignment:
            possible_multiclasses = [
                x
                for x in possible_multiclasses
                if alignment in MULTICLASSES[x]["Alignments"]
            ]
        return random.choice(possible_multiclasses).split("/")
    else:
        if class_group:
            classes = classes.intersection(set(CLASS_GROUPS[class_group]["Classes"]))
        return [random.choice(list(classes))]


def get_random_experience_by_level(class_name, level, penalty=1):
    if level < 30:
        return random.randint(
            CLASSES[class_name]["Levels"][level - 1] * penalty,
            CLASSES[class_name]["Levels"][level] * penalty,
        )
    else:
        xp = CLASSES[class_name]["Levels"][29] * penalty
        return xp + random.randint(0, xp / 10)


def get_random_experiences_by_level(classes, level, penalty=1):
    base_experience = CLASSES[classes[0]]["Levels"][level - 1]
    base_class = classes[0]
    for class_name in classes[1:]:
        if base_experience > CLASSES[class_name]["Levels"][level - 1]:
            base_experience = CLASSES[class_name]["Levels"][level - 1]
            base_class = class_name
    experience = get_random_experience_by_level(base_class, level, penalty=penalty)
    return [experience for x in classes]


def get_random_race_by_classes(classes):
    table = CLASSES
    class_name = classes[0]
    if len(classes) > 1:
        table = MULTICLASSES
        class_name = "/".join(classes)
    return random.choice(list(table[class_name]["Races"]))


def get_saving_throw(class_group, level):
    return get_score_from_table(CLASS_GROUPS[class_group]["Saves"], level)


def get_saving_throws(class_groups, levels, race, constitution):
    saving_throws = [20, 20, 20, 20, 20]
    for class_group, level in zip(class_groups, levels):
        saving_throws = [
            min(x) for x in zip(saving_throws, get_saving_throw(class_group, level))
        ]
    # Dwarves, gnomes, and halflings get a bonus to their saves against
    # Rod, Staves, Wands, and Spells based on their Constitution score.
    if race in ["Dwarf", "Gnome", "Halfling"]:
        saving_throws[1] -= int(constitution / 3.5)
        saving_throws[4] -= int(constitution / 3.5)
    return saving_throws


def get_score_from_table(table, value):
    return table[[x for x in table if value >= int(x)][-1]]


def get_spell_levels(class_name, level, wisdom):
    caster_group = get_caster_group(class_name)
    level = str(level)
    spells = SPELL_PROGRESSION[caster_group][level]
    # Specialists get a bonus spell per level
    if get_spell_specialization(class_name):
        spells = [x + 1 for x in spells]
    if caster_group in WISDOM_CASTERS:
        wisdom_spells = wisdom_bonus_spells(wisdom)
        try:
            for spell_level in range(0, len(spells)):
                spells[spell_level] += wisdom_spells[spell_level]
        except IndexError:
            pass
    if caster_group == "Priest":
        if wisdom < 17:
            spells = spells[:5]
        if wisdom < 18:
            spells = spells[:6]
    return spells


def get_spell_includes(class_name):
    try:
        return CLASS_SPELLS[class_name]["Include"]
    except KeyError:
        return None


def get_spell_excludes(class_name):
    try:
        return CLASS_SPELLS[class_name]["Exclude"]
    except KeyError:
        return None


def get_spell_subtype(class_name):
    try:
        return CLASS_SPELLS[class_name]["Subtype"]
    except KeyError:
        pass
    caster = get_class_groups([class_name])[0]
    if caster == "Priest":
        return "Sphere"
    elif caster == "Wizard":
        return "School"
    return None


def get_spell_specialization(class_name):
    try:
        return CLASS_SPELLS[class_name]["Specialization"]
    except KeyError:
        return None


def generate_characteristics(race, level):
    race_chars = RACES[race]["Characteristics"]
    characteristics = {"Gender": random.choice(["Female", "Male"])}
    gender_index = 0
    if characteristics["Gender"] == "Female":
        gender_index = 1
    characteristics["Height"] = roll(
        race_chars["Height"][2],
        race_chars["Height"][3],
        race_chars["Height"][gender_index],
    )
    characteristics["Weight"] = roll(
        race_chars["Weight"][2],
        race_chars["Weight"][3],
        race_chars["Weight"][gender_index],
    )
    characteristics["Age"] = roll(
        race_chars["Age"][1], race_chars["Age"][2], race_chars["Age"][0]
    )
    characteristics["Age"] += roll(level, race_chars["Age"][3], -level)
    if characteristics["Age"] >= race_chars["Age"][4]:
        characteristics["Age"] -= roll(2, race_chars["Age"][3], 0)
    return characteristics


def intelligence_mods(intelligence):
    return ABILITY_MODS["Intelligence"][str(intelligence)]


def intelligence_bonus_proficiencies(intelligence):
    return intelligence_mods(intelligence)[0]


def level_limit_bonus(class_name, abilities):
    prime_reqs = CLASSES[class_name]["Requisite"]
    lowest = 99
    for prime_req in prime_reqs:
        prime_req_score = abilities[prime_req]
        if prime_req_score < lowest:
            lowest = prime_req_score
    if lowest > 18:
        return 4
    elif lowest > 17:
        return 3
    elif lowest > 15:
        return 2
    elif lowest > 13:
        return 1
    return 0


def strength_mods(strength, extrao_str):
    if extrao_str:
        if extrao_str < 51:
            extrao_str = "50"
        elif extrao_str < 76:
            extrao_str = "75"
        elif extrao_str < 91:
            extrao_str = "90"
        elif extrao_str < 100:
            extrao_str = "99"
        else:
            extrao_str = "100"
        return ABILITY_MODS["Extrao Strength"][extrao_str]
    else:
        return ABILITY_MODS["Strength"][str(strength)]


def strength_damage(strength, extrao_str=None):
    return strength_mods(strength, extrao_str)[1]


def strength_to_hit(strength, extrao_str=None):
    return strength_mods(strength, extrao_str)[0]


def wisdom_bonus_spells(wisdom):
    if wisdom < 13:
        return []
    elif wisdom == 13:
        return [1]
    elif wisdom == 14:
        return [2]
    elif wisdom == 15:
        return [2, 1]
    elif wisdom == 16:
        return [2, 2]
    elif wisdom == 17:
        return [2, 2, 1]
    elif wisdom == 18:
        return [2, 2, 1, 1]
    elif wisdom == 19:
        return [3, 2, 1, 2]
    elif wisdom == 20:
        return [3, 3, 1, 3]
    elif wisdom == 21:
        return [3, 3, 2, 3, 1]
    elif wisdom == 22:
        return [3, 3, 2, 4, 2]
    elif wisdom == 23:
        return [3, 3, 2, 4, 4]
    elif wisdom == 24:
        return [3, 3, 2, 4, 4, 2]
    elif wisdom == 25:
        return [3, 3, 2, 4, 4, 3, 1]


class Character(object):
    def __init__(
        self,
        classes=[],
        class_name=None,
        class_group=None,
        abilities=None,
        race=None,
        level=1,
        levels=[],
        alignment=None,
        experience=None,
        expanded=False,
        slow_advancement=False,
        starting_money=True,
        demi_experience_penalty=[2, 3],
        **kwargs,
    ):
        self.expanded = expanded

        ### Determine classes
        if not classes and class_name:
            self.classes = class_name.split("/")
        else:
            self.classes = classes
        if not self.classes:
            self.classes = get_random_classes(
                class_group=class_group, alignment=alignment
            )
        self.class_groups = get_class_groups(self.classes)

        ### Assign or choose a race and subrace
        self.race = race
        if not self.race:
            self.race = get_random_race_by_classes(self.classes)
        self.race_stats = RACES[self.race]
        self.subrace = kwargs.get("subrace", None)
        if not self.subrace:
            try:
                self.subrace = random.choice(list(self.race_stats["Subraces"]))
                for stat in self.race_stats["Subraces"][self.subrace]:
                    self.race_stats[stat] = self.race_stats["Subraces"][self.subrace][
                        stat
                    ]
            except KeyError:
                pass

        self.slow_advancement = slow_advancement
        self.experience_penalty = [1, 1]  # No penalty
        if slow_advancement and self.race != "Human":
            self.experience_penalty = demi_experience_penalty
            try:
                self.experience_penalty *= 1 + self.race_stats["Experience Penalty"]
            except KeyError:
                pass

        ### Assign alignment
        self.alignment = alignment
        if not self.alignment:
            self.alignment = get_alignment_by_classes(self.classes)

        ### Calculate experience
        if experience is not None:
            # Divide experience evenly across classes for multiclass characters
            if type(experience) is int:
                self.experience = [
                    int(experience / len(self.classes)) for x in self.classes
                ]
            else:
                self.experience = experience
            self.levels = get_levels_by_experience(
                self.classes,
                self.experience,
                experience_penalty=self.experience_penalty,
            )
        elif levels:
            self.levels = levels
            self.experience = [
                get_random_experience_by_level(
                    class_name, level, penalty=self.experience_penalty[0]
                )
                for class_name, level in zip(self.classes, self.levels)
            ]
        else:
            self.experience = get_random_experiences_by_level(
                self.classes, level, penalty=self.experience_penalty[0]
            )
            self.levels = get_levels_by_experience(
                self.classes,
                self.experience,
                experience_penalty=self.experience_penalty,
            )

        ### Roll abilities if necessary
        self.abilities = abilities
        if not self.abilities:
            minimums = combine_minimums(
                [CLASSES[x]["Minimums"] for x in classes]
                + [self.race_stats["Minimums"]]
            )
            # TODO: Calculate the level here a little better for multiclass
            ability_rolls = ABILITY_ROLLS[str(max(self.levels))]
            self.abilities = get_abilities(
                get_ability_priority(self.classes),
                minimums,
                self.race_stats["Maximums"],
                self.race_stats["Ability Modifiers"],
                order=ability_rolls,
                extrao_str="Warrior" in self.class_groups and self.race != "Halfling",
            )

        ### Apply level limits
        self.level_limits = get_level_limits(self.race, self.classes, self.abilities)
        if slow_advancement:
            self.levels = get_levels_by_experience(
                self.classes,
                self.experience,
                experience_penalty=self.experience_penalty,
                level_limits=self.level_limits,
            )
        else:
            for index, (level, limit) in enumerate(zip(self.levels, self.level_limits)):
                if level > limit:
                    self.levels[index] = limit

        ### Calculate hitpoints
        self.hitpoints = get_hitpoints(
            self.class_groups, self.levels, self.abilities["Constitution"]
        )

        ### Calculate saving throws
        self.saving_throws = get_saving_throws(
            self.class_groups, self.levels, self.race, self.abilities["Constitution"]
        )

        ### Determine if this character can cast spells, and assign them if so
        self.spell_levels = {}
        self.spells = {}
        for class_name, level in zip(self.classes, self.levels):
            caster_group = get_caster_group(class_name)
            if caster_group:
                self.spell_levels[class_name] = get_spell_levels(
                    class_name, level, self.abilities["Wisdom"]
                )
                self.spells[class_name] = {}
        if self.spell_levels:
            self._populate_spells()

        ### Assign thief skills
        self.thief_skills = {}
        self._assign_thief_skills()

        ### Assign proficiencies
        self.nwp_slots = get_nwp_slots(
            self.class_groups, max(self.levels), self.abilities["Intelligence"]
        )
        self.profs = {"NWP": [], "Weapon": [], "Languages": ["Common"]}
        if "Thief" in self.classes:
            self.profs["Languages"].append("Thieves' Cant")
        elif "Druid" in self.classes:
            self.druid_lang_known = 0
        self._assign_nwps()

        ### Determine misc. stats
        self.thac0 = get_best_thac0(self.classes, self.levels)
        self.ac = 10 + dexterity_ac_mod(self.abilities["Dexterity"])
        self.equipment = []
        self.currency = {"pp": 0, "gp": 0, "ep": 0, "sp": 0, "cp": 0}
        if starting_money:
            funds_roll = (1, 4, 1)
            if "Rogue" in self.class_groups:
                funds_roll = (2, 6, 0)
            if "Priest" in self.class_groups:
                fund_roll = (3, 6, 0)
            if "Warrior" in self.class_groups:
                funds_roll = (5, 4, 0)
            self.currency["gp"] = 10 * roll(*funds_roll)
        self.characteristics = generate_characteristics(self.race, max(self.levels))

    def __str__(self):
        self.update_ac()
        dex_hit_mod = dexterity_to_hit(self.abilities["Dexterity"])
        str_hit_mod = strength_to_hit(
            self.abilities["Strength"], self.abilities["Extrao Strength"]
        )
        s = f"{'-'*80}\n"

        ### Race, Class, Alignment, HP, AC, THAC0
        classes_str = "/".join(self.classes)
        levels_str = "/".join([str(x) for x in self.levels])
        xp_str = "/".join([f"{x:,}" for x in self.experience])
        if self.subrace:
            s += f"{self.alignment} {self.subrace} {classes_str} {levels_str}\n"
        else:
            s += f"{self.alignment} {self.race} {classes_str} {levels_str}\n"
        s += f"XP: {xp_str} - "
        level_limits_str = "/".join(
            ["U" if x > 98 else str(x) for x in self.level_limits]
        )
        if level_limits_str == "U":
            s += "Unlimited level limit\n"
        else:
            limit_str = "Soft level limit" if self.slow_advancement else "Level limit"
            s += f"{limit_str}: {level_limits_str}\n"
        s += f"HP: {self.hitpoints}  AC: {self.ac}  THAC0: {self.thac0} (Melee:{self.thac0-str_hit_mod}/Ranged:{self.thac0-dex_hit_mod})\n"

        ### Saving Throws
        save_names = ["PPD", "RSW", "PP", "BW", "S"]
        s += "Saving Throws: " + "  ".join(
            [f"{x[0]}: {x[1]}" for x in zip(save_names, self.saving_throws)]
        )
        s += "\n"
        s += "\n"

        ### Abilities
        for ability in ABILITIES:
            details = ""
            ability_val = str(self.abilities[ability])
            if ability == "Strength":
                hit_mod = str_hit_mod
                dmg_mod = strength_damage(
                    self.abilities["Strength"], self.abilities["Extrao Strength"]
                )
                if self.abilities["Extrao Strength"]:
                    ability_val += f'/{self.abilities["Extrao Strength"]}'
                if hit_mod >= 0:
                    hit_mod = f"+{hit_mod}"
                if dmg_mod >= 0:
                    dmg_mod = f"+{dmg_mod}"
                details = f"{hit_mod} to hit/{dmg_mod} damage"
            elif ability == "Dexterity":
                hit_mod = dex_hit_mod
                ac_mod = dexterity_ac_mod(self.abilities["Dexterity"])
                if hit_mod >= 0:
                    hit_mod = f"+{hit_mod}"
                if ac_mod > 0:
                    ac_mod = f"+{ac_mod}"
                details = f"{hit_mod} to hit/{ac_mod} AC"
            elif ability == "Constitution":
                con_mod = constitution_hp_modifier(
                    self.abilities["Constitution"], self.class_groups
                )
                if con_mod > 1:
                    con_mod = f"+{con_mod}"
                details = f"{con_mod} HP adj"
            elif ability == "Intelligence":
                bonus_nwps = intelligence_bonus_proficiencies(
                    self.abilities["Intelligence"]
                )
                details = f"{bonus_nwps} bonus NWPs"
            if details:
                details = f" ({details})"
            s += f"{ability+':':13} {ability_val:>5} {details}\n"
        s += "\n"

        ### Characteristics
        s += f"{self.characteristics['Gender']}  {convert_height(self.characteristics['Height'])}  {self.characteristics['Weight']} lbs.  {self.characteristics['Age']} years old\n"
        s += "\n"

        ### Attacks per round
        if "Warrior" in self.class_groups:
            level = self.get_level(None, class_group="Warrior")
            spr = "3/2"
            apr = 1
            if level > 12:
                apr = 2
                spr = "5/2"
            elif level > 6:
                apr = "3/2"
                spr = 2
            s += f"Melee Attacks Per Round: {apr}\n"
            s += f"Specialist Attacks Per Round: {spr}\n\n"

        ### Backstab
        if "Thief" in self.classes:
            backstab = int((self.get_level("Thief") - 1) / 4) + 2
            if backstab > 5:
                backstab = 5
            s += f"Backstab Multiplier: x{backstab}\n"

        ### Thief skills
        if self.thief_skills:
            skill_str = "  ".join(
                [
                    f"{re.sub(r'[^A-Z]', '', x)}: {self.thief_skills[x]}"
                    for x in self.thief_skills
                ]
            )
            s += f"Thief Skills: {skill_str}\n\n"

        ### Proficiencies
        s += f"Non-Weapon Proficiencies ({self.nwp_slots}):\n"
        for nwp in sorted(self.profs["NWP"]):
            modifier = "N/A"
            ability = NWPS[nwp][1]
            if ability != "N/A":
                modifier = self.abilities[ability] + NWPS[nwp][2]
                if "Ranger" in self.classes and nwp == "Tracking":
                    modifier += int(self.get_level("Ranger") / 3)
            s += f"\t{nwp:20} {ability:12}  Mod: {modifier:3}  Slots: {NWPS[nwp][0]}\n"

        ### Languages
        s += f"Languages known: {', '.join(self.profs['Languages'])}\n"

        ### Spells
        if self.spells:
            s += "\nSpells:\n"
            for class_name in self.spell_levels:
                if not self.spell_levels[class_name]:
                    continue
                s += f"    {class_name} ({'/'.join([str(x) for x in self.spell_levels[class_name]])}):\n"
                for spell_level in range(1, len(self.spell_levels[class_name]) + 1):
                    s += f"\t{spell_level}: "
                    cur_spells = []
                    for spell in sorted(set(self.spells[class_name][spell_level])):
                        count = ""
                        if self.spells[class_name][spell_level].count(spell) > 1:
                            count = f" ({self.spells[class_name][spell_level].count(spell)})"
                        cur_spells.append(f"{spell}{count}")
                    s += f"{'; '.join(cur_spells)}\n"

        ### Currency
        funds_str = ", ".join(
            [f"{self.currency[x]:,}{x}" for x in self.currency if self.currency[x]]
        )
        if funds_str:
            s += f"\nCurrency: {funds_str}\n"

        ### Equipment
        if self.equipment:
            items = []
            for item in self.equipment:
                ac, ac_bonus = get_ac(item)
                if ac is not None:
                    item = f"{item} (AC: {ac})"
                elif ac_bonus is not None:
                    if ac_bonus >= 0:
                        item = f"{item} (AC +{ac_bonus})"
                    else:
                        item = f"{item} (AC {ac_bonus})"
                items.append(item)
            s += "\n"
            s += "Equipment:\n\t" + "\n\t".join(items)
        s += f"\n{'-'*80}"
        return s

    def _assign_nwps(self):
        slots = self.nwp_slots
        classgroups_nwps = []

        if "Bard" in self.classes:
            self.profs["NWP"].append("Local History")
            self.profs["NWP"].append("Reading/Writing")
        elif "Ranger" in self.classes:
            self.profs["NWP"].append("Tracking")

        for class_name in self.classes:
            groups = CLASSES[class_name]["Proficiency Groups"]
            try:
                groups.remove("General")
            except ValueError:
                pass
            for group in groups:
                classgroups_nwps += NWP_GROUPS[group]
        classgroups_nwps = list(set(classgroups_nwps))
        general_nwps = list(NWP_GROUPS["General"])
        while slots:
            classgroups_nwps = [x for x in classgroups_nwps if NWPS[x][0] <= slots]
            general_nwps = [x for x in general_nwps if NWPS[x][0] <= slots]
            # 50% chance for each slot to give demi-humans their racial language
            if (
                self.race not in ["Human", "Half-Elf"]
                and roll(1, 100, 0) > 50
                and self.race_stats["Languages"][0] not in self.profs["Languages"]
            ):
                self.profs["Languages"].append(self.race_stats["Languages"][0])
                slots -= 1
            # 60% chance to assign a non-general NWP if there's enough slots
            elif classgroups_nwps and roll(1, 100, 0) > 40:
                new_nwp = random.choice(classgroups_nwps)
                self.profs["NWP"].append(new_nwp)
                slots -= NWPS[new_nwp][0]
                classgroups_nwps.remove(new_nwp)
            # 20% chance to assign a non-general NWP if there's enough slots
            elif general_nwps and roll(1, 100, 0) > 80:
                new_nwp = random.choice(general_nwps)
                self.profs["NWP"].append(new_nwp)
                slots -= NWPS[new_nwp][0]
                general_nwps.remove(new_nwp)
            # Otherwise, learn a language
            else:
                languages = []
                if self.race != "Human":
                    if self.race != "Half-Elf":
                        if (
                            self.race_stats["Languages"][0]
                            not in self.profs["Languages"]
                        ):
                            self.profs["Languages"].append(
                                self.race_stats["Languages"][0]
                            )
                            slots -= 1
                            continue
                    languages = self.race_stats["Languages"]
                else:
                    languages = load_table("languages.json")
                if (
                    "Druid" in self.classes
                    and self.druid_lang_known / self.get_level("Druid") > 1
                ):
                    languages += load_table("druid_languages.json")
                languages = list(set(languages) - (set(self.profs["Languages"])))
                # Make sure this character hasn't learned all of their possible languages
                if languages:
                    self.profs["Languages"].append(random.choice(languages))
                    slots -= 1

    def _assign_thief_skills(self):
        def apply_race_dex_mods(skills):
            for skill in skills:
                if self.race in THIEF_SKILLS[skill]["Races"]:
                    self.thief_skills[skill] += THIEF_SKILLS[skill]["Races"][self.race]
                if "Dexterity" in THIEF_SKILLS[skill]:
                    self.thief_skills[skill] += get_score_from_table(
                        THIEF_SKILLS[skill]["Dexterity"], self.abilities["Dexterity"]
                    )

        if "Bard" in self.classes:
            self.thief_skills["Climb Walls"] = 50
            self.thief_skills["Detect Noise"] = 20
            self.thief_skills["Pick Pockets"] = 10
            self.thief_skills["Read Languages"] = 5
        if "Ranged" in self.classes:
            self.thief_skills = CLASSES["Ranger"]["Skills"][
                str(self.get_level("Ranger"))
            ]
        if "Thief" in self.classes:
            for skill in THIEF_SKILLS_STANDARD:
                self.thief_skills[skill] = THIEF_SKILLS[skill]["Base"]

        apply_race_dex_mods(self.thief_skills)

        # Assign thief skills points after modifiers are applied, so that
        # skills can hit 95 and not be reduced.
        # TODO: Assign Bard points in here, too
        if "Thief" in self.classes:

            def assign_points(points):
                max_points = points / 2
                skills = list(self.thief_skills)
                assigned = {x: 0 for x in skills}
                for skill in skills:
                    if self.thief_skills[skill] >= 95:
                        skills.remove(skill)
                for point in range(0, points):
                    try:
                        skill = random.choice(skills)
                    except IndexError:
                        # This thief has maxed their skills. Good for them!
                        return
                    self.thief_skills[skill] += 1
                    assigned[skill] += 1
                    if assigned[skill] == max_points or self.thief_skills[skill] == 95:
                        skills.remove(skill)

            assign_points(60)
            thief_level = self.get_level("Thief")
            for level in range(1, thief_level + 1)[:20]:
                assign_points(30)
            if thief_level > 20:
                for skill in THIEF_SKILLS_HLA:
                    self.thief_skills[skill] = THIEF_SKILLS[skill]["Base"]
                apply_race_dex_mods(THIEF_SKILLS_HLA)
                for level in range(20, thief_level + 1):
                    assign_points(30)

    def _populate_spells(self):
        spell_gen = Spells(expanded=self.expanded)
        for class_name in self.spell_levels:

            def add_spell(spell_level, spell):
                if spell is None:
                    raise TypeError("Can't assign None as spell")
                self.spells[class_name][spell_level].append(spell)

            specialization = get_spell_specialization(class_name)
            includes = get_spell_includes(class_name)
            excludes = get_spell_excludes(class_name)
            spell_subtype = get_spell_subtype(class_name)
            for spell_level in range(1, len(self.spell_levels[class_name]) + 1):
                if spell_level not in self.spells[class_name]:
                    self.spells[class_name][spell_level] = []
                spell_count = self.spell_levels[class_name][spell_level - 1]
                if specialization:
                    add_spell(
                        spell_level,
                        spell_gen.random_school_sphere_spell(
                            spell_level, specialization, spell_subtype
                        ),
                    )
                    spell_count -= 1
                if excludes is not None:
                    for _ in range(0, spell_count):
                        add_spell(
                            spell_level,
                            spell_gen.random_standard_school_sphere_spell(
                                spell_level, spell_subtype, excludes=excludes
                            ),
                        )
                elif includes is not None:
                    for _ in range(0, spell_count):
                        add_spell(
                            spell_level,
                            spell_gen.random_include_school_sphere_spell(
                                spell_level, spell_subtype, includes
                            ),
                        )
                else:
                    caster_class = get_caster_group(class_name)
                    for _ in range(0, spell_count):
                        add_spell(
                            spell_level,
                            spell_gen.random_spell(spell_level, caster_class),
                        )

    def add_equipment(self, item):
        if item is not None:
            self.equipment.append(item)

    def buy_item(self, item, **kwargs):
        item_table = kwargs.get("item_table")
        if not item_table:
            item_type = kwargs.get("item_type")
            if item_type == "Armor":
                item_table = ARMOR
            elif item_type == "Weapons":
                item_table = WEAPONS
        price = item_table[item]["Cost"]
        if price > get_gold_value(self.currency):
            return False
        self.currency = subtract_coins(self.currency, gold_to_coins(price))
        self.add_equipment(item)
        return True

    def get_level(self, class_name, class_group=None):
        if class_group:
            return self.levels[self.class_groups.index(class_group)]
        else:
            return self.levels[self.classes.index(class_name)]

    def give_treasure(self, treasure_types):
        treasure = generate_treasure(treasure_types)
        for currency in treasure["Currency"]:
            self.currency[currency] += treasure["Currency"][currency]
        for category in treasure.keys() - ["Currency"]:
            for item in treasure[category]:
                self.add_equipment(item)

    def update_ac(self):
        if "Bracers of Defenselessness" in self.equipment:
            self.ac = 10
            return
        mods = [dexterity_ac_mod(self.abilities["Dexterity"])]
        base_ac = 10
        for item in self.equipment:
            ac, ac_bonus = get_ac(item)
            if ac is not None:
                if ac < base_ac:
                    base_ac = ac
            elif ac_bonus is not None:
                mods.append(-ac_bonus)
        self.ac = base_ac + sum(mods)


def main():
    parser = argparse.ArgumentParser(description="Create a character")
    parser.add_argument(
        "-s",
        "--slow",
        default=False,
        action="store_true",
        help="use slow advancement but removed level limits for demi-humans",
    )
    parser.add_argument(
        "-x",
        "--expanded",
        default=False,
        action="store_true",
        help="use expanded generation tables",
    )
    args = parser.parse_args()
    for class_name in get_all_classes():
        print(
            Character(
                class_name=class_name,
                level=15,
                expanded=args.expanded,
                slow_advancement=args.slow,
            )
        )
    for class_name in get_all_classes():
        print(
            Character(
                class_name=class_name,
                level=30,
                race="Human",
                expanded=args.expanded,
                slow_advancement=args.slow,
            )
        )
    for class_name in MULTICLASSES:
        print(
            Character(
                class_name=class_name,
                experience=15000000,
                expanded=args.expanded,
                slow_advancement=args.slow,
            )
        )


if __name__ == "__main__":
    main()
