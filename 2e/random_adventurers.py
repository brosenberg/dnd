#!/usr/bin/env python3

import random
import magic_item

LEVEL_RANGE = {
    "Low": (1, 3, 0),
    "Medium": (1, 4, 3),
    "High": (1, 6, 6),
    "Very high": (1, 12, 8),
}
MAGIC_ITEMS = {
    "Fighter": ["Armor No Shields", "Shields", "Sword", "Nonsword", "Potions and Oils"],
    "Wizard": ["Scrolls", "Rings", "Rod/Staff/Wand", "Misc Magic"],
    "Cleric": ["Armor No Shields", "Shields", "Nonsword", "Potions and Oils", "Scrolls", "Misc Magic"],
    "Thief": ["Shields", "Sword", "Nonsword", "Potions and Oils", "Rings", "Misc Magic"],
}


def roll(dice, sides, mod):
    total = mod
    for die in range(0, dice):
        total += random.randint(1, sides)
    return total


class Adventurer(object):
    def __init__(self, level_range):
        class_roll = roll(1, 10, 0)
        self.char_class = "Fighter"
        if class_roll > 8:
            self.char_class = "Wizard"
        elif class_roll > 6:
            self.char_class = "Thief"
        elif class_roll > 4:
            self.char_class = "Cleric"
        self.level = roll(
            LEVEL_RANGE[level_range][0],
            LEVEL_RANGE[level_range][1],
            LEVEL_RANGE[level_range][2],
        )
        self.equipment = []
        has_armor = False
        has_shield = False
        for category in MAGIC_ITEMS[self.char_class]:
            if roll(1, 100, 0) <= self.level * 5:
                if category == "Armor No Shields":
                    has_armor = True
                elif category == "Shields":
                    has_shield = True
                self.equipment.append(str(magic_item.roll_category(category)[0]))
        if self.level > 7 and (
            self.char_class == "Cleric" or self.char_class == "Fighter"
        ):
            if not has_armor:
                self.equipment.append("plate mail")
            if not has_shield:
                self.equipment.append("medium shield")
            self.equipment.append("unbarded medium warhorse")

    def __str__(self):
        s = f"{self.char_class} {self.level}\n"
        s += "Equipment:\n" + "\n".join(self.equipment)
        return s


def main():
    no_appearing = roll(1, 8, 0)
    level_range = random.choice(list(LEVEL_RANGE.keys()))
    print(f"{level_range} level Adventurer Party ({no_appearing} adventurers)")
    print()
    for adventurer in range(0, no_appearing):
        print(Adventurer(level_range))
        print()


if __name__ == "__main__":
    main()
