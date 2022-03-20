#!/usr/bin/env python3

import random
import re
import sys


def parse_dice(dice_str):
    rolls = []
    dice_re = r"([0-9]+d[0-9]+)([-+*/][0-9](?!d))?([-+*/])?"
    matches = re.findall(dice_re, dice_str)
    print(matches)
    for match in matches:
        dice, sides = [int(x) for x in match[0].split("d")]
        try:
            bonus_sign = match[1][0]
            bonus = int(match[1][1:])
        except IndexError:
            bonus_sign = "+"
            bonus = 0
        except ValueError:
            bonus_sign = "+"
            bonus = 0
        next_sign = match[2]
        rolls.append([dice, sides, bonus_sign, bonus, next_sign])
    return rolls


def roll(dice, sides, bonus_sign, bonus):
    results = []
    s = f"{dice}d{sides}"
    if bonus_sign:
        s += f"{bonus_sign}{bonus}"
    s += " = "
    for _ in range(0, dice):
        results.append(random.randint(1, sides))
    s += "+".join([str(x) for x in results])
    result = sum(results)
    if bonus_sign:
        s += f"{bonus_sign}{bonus}"
        result = do_bonus(result, bonus_sign, bonus)
    s += f" = {result}"
    print(s)
    return result


def do_bonus(base, bonus_sign, bonus):
    if bonus_sign == "+":
        return base + bonus
    if bonus_sign == "-":
        return base - bonus
    if bonus_sign == "/":
        return base / bonus
    if bonus_sign == "*":
        return base * bonus


def main():
    dices = parse_dice(sys.argv[1])
    last_sign = ""
    result = 0
    for dice in dices:
        cur = roll(*dice[:4])
        if last_sign:
            result = do_bonus(result, last_sign, cur)
        else:
            result = cur
        if dice[4]:
            print(result)
            last_sign = dice[4]
            print(last_sign)
    print("=")
    print(result)


if __name__ == "__main__":
    main()
