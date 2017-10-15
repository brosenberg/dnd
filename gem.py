#!/usr/bin/env python

import sys
import random


def main():
    gems = [0, 0, 0, 0, 0, 0]
    try:
        count = int(sys.argv[1])
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
        print "%d 10gp gems" % (gems[0],)
        print "%d 50gp gems" % (gems[1],)
        print "%d 100gp gems" % (gems[2],)
        print "%d 500gp gems" % (gems[3],)
        print "%d 1000gp gems" % (gems[4],)
        print "%d 5000gp gems" % (gems[5],)

    except IndexError:
        print "Usage: %s [number of gems]" % (sys.argv[0],)
        sys.exit(1)


if __name__ == '__main__':
    main()
