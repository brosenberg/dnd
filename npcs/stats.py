#!/usr/bin/env python

import random


class NPC(object):
    def __init__(self, level=1):
        self.stats = roll_stats(level=level)
        self.stats.reverse()

    def __str__(self):
        s = ""
        for stat in self.stats:
            s += '%d' % (stat[0],)
            if stat[1]:
                s += '/%02d' % (stat[1],)
            s += '\n'
        return s.rstrip()


def roll_stat(drop=1):
    stat = sum(sorted([random.randint(1,6) for x in range(0,3+drop)])[drop:])
    percentile = random.randint(1,100) if stat == 18 else 0
    return (stat, percentile)

def roll_stats(level=1):
    drop = level+3
    count = (level/2)
    stats = []
    for i in range(0,6+count):
        stats.append(roll_stat(drop=drop))
        if drop > 0:
            drop /= 2
    return sorted(stats)[count:]

def main():
    npc = NPC(level=10)
    print npc

if __name__ == '__main__':
    main()
