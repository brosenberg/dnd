#!/usr/bin/env python3

COINS = ["pp", "gp", "ep", "sp", "cp"]
COIN_VALUES = {"pp": 5, "gp": 1, "ep": 0.5, "sp": 0.1, "cp": 0.01}
# Integer version of COIN_VALUES to avoid floating point issues
MIN_COIN_VALUE = COIN_VALUES[min(COIN_VALUES, key=COIN_VALUES.get)]
COIN_MULT = int(1 / MIN_COIN_VALUE)
COIN_VALUES_MULT = {x: int(COIN_VALUES[x] * COIN_MULT) for x in COIN_VALUES}


def get_gold_value(coins):
    return sum([COIN_VALUES[x] * coins[x] for x in coins])


def gold_to_coins(gp_value):
    gp_value = int(
        (gp_value + MIN_COIN_VALUE * 0.99) * COIN_MULT
    )  # Avoid floating point issues
    coins = {}
    for coin in COINS:
        coin_count = int(gp_value / COIN_VALUES_MULT[coin])
        if coin_count:
            gp_value -= coin_count * COIN_VALUES_MULT[coin]
            coins[coin] = coin_count
    if gp_value > 1:
        coins["cp"] += 1
    return coins


def subtract_coins(coins, subtract, lazy=True):
    if lazy:
        return gold_to_coins(get_gold_value(coins) - get_gold_value(subtract))
    else:
        raise NotImplemented


def main():
    print(gold_to_coins(3.901))


if __name__ == "__main__":
    main()
