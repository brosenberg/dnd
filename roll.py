#!/usr/bin/env python3

import random
import re
import sys


def do_bonus(base, bonus_sign, bonus):
    if bonus_sign == "+":
        return base + bonus
    if bonus_sign == "-":
        return base - bonus
    if bonus_sign == "/":
        return base / bonus
    if bonus_sign == "*":
        return base * bonus


def parse_dice(dice_str):
    rolls = []
    dice_re = r"([0-9]+d[0-9]+)([-+*/][0-9](?!d))?([-+*/])?"
    matches = re.findall(dice_re, dice_str)
    for match in matches:
        dice, sides = [int(x) for x in match[0].split("d")]
        try:
            bonus_sign = match[1][0]
            bonus = int(match[1][1:])
        except IndexError:
            bonus_sign = None
        except ValueError:
            bonus_sign = None
        next_sign = match[2]
        rolls.append([dice, sides, bonus_sign, bonus, next_sign])
    return rolls


def roll(dice, sides, bonus_sign, bonus):
    results = []
    s = f"{dice}d{sides}"
    if bonus_sign:
        s += f"{bonus_sign}{bonus}"
    s += ": "
    for _ in range(0, dice):
        results.append(random.randint(1, sides))
    s += "("
    s += "+".join([str(x) for x in results])
    s += ")"
    result = sum(results)
    if bonus_sign:
        s += f"{bonus_sign}{bonus}"
        result = do_bonus(result, bonus_sign, bonus)
    s += f" = {result}"
    print(s)
    return result


def roll_dices(dices, quiet=False):
    last_sign = ""
    result = 0
    for dice in dices:
        cur = roll(*dice[:4])
        if last_sign:
            result = do_bonus(result, last_sign, cur)
        else:
            result = cur
        if dice[4]:
            if not quiet:
                print(result)
            last_sign = dice[4]
            if not quiet:
                print(f"{last_sign} ", end="")
    if len(dices) == 1:
        return
    if not quiet:
        print("=")
        print(result)
    return result


def print_usage():
    print(f"Usage: {sys.argv[0]} [dice_str] ([dice_str] ...)")
    print(f"   Ex: {sys.argv[0]} 3d6")
    print(f"   Ex: {sys.argv[0]} '1d4+2+2d8-3d6+1*1d5/1d20'")


def main():
    dice_str = re.sub(r"\s*", "", "".join(sys.argv[1:]))
    dices = parse_dice(dice_str)
    if not dice_str:
        print_usage()
        sys.exit(1)
    if not dices:
        print(f"Unknown dice string: {dice_str}")
        print_usage()
        sys.exit(2)
    roll_dices(dices)


if __name__ == "__main__":
    main()
