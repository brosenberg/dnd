#!/usr/bin/env python

import sys
import random


def main():
    gems = [0, 0, 0, 0, 0, 0]
    values = (10, 50, 100, 500, 1000, 5000)
    try:
        count = int(sys.argv[1])
        total = 0
        while count:
            roll = random.randint(1, 100)
            if roll == 100:
                gems[5] += 1
            elif roll >= 91:
                gems[4] += 1
            elif roll >= 71:
                gems[3] += 1
            elif roll >= 51:
                gems[2] += 1
            elif roll >= 26:
                gems[1] += 1
            else:
                gems[0] += 1

            count = count - 1
        for i in range(0, 6):
            if gems[i]:
                print "%d %s gp gems" % (gems[i], values[i])
                total += gems[i] * values[i]
        print "%d gp total" % (total,)

    except IndexError:
        print "Usage: %s [number of gems]" % (sys.argv[0],)
        sys.exit(1)


if __name__ == '__main__':
    main()
