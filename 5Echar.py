#!/usr/bin/env python

import re
import roll
import sys

class Character(object):
    def __init__(self, fh):
        self.stats   = {}
        self.attacks = {}
        self.name = fh.readline().strip()
        for line in fh:
            # Get stats
            for stat in ['str', 'dex', 'con', 'wis', 'int', 'cha']:
                try:
                    m = re.search('%s (\d+)' % (stat,), line, flags=re.I)
                    self.stats[stat] = int(m.group(1))
                except AttributeError:
                    pass

            # Get initiative
            try:
                m = re.search('^init\S* (\S+)\s*$', line, flags=re.I)
                self.init = m.group(1)
            except AttributeError:
                pass

            # Get attacks
            try:
                m = re.search('^(.+)\s+([-+]\d+)\s+(\d+d\d([-+/x]?\d+)?)(,.*)?$', line, flags=re.I)
                attack = m.group(1).strip().lower()
                self.attacks[attack] = {"attack": m.group(2), "damage": m.group(3)}
            except AttributeError:
                pass

    def __str__(self):
        s = self.name
        s += "\n"
        for stat in self.stats:
            s += "[%s] %d  " % (stat.title(), self.stats[stat])
        s += "\n\n[init]: %s\n\n" % (self.init,)
        s += "[attack]s\n"
        for attack in self.attacks:
            s += "%-15s %s %s\n" % ("[%s]" % (attack.title(),), self.attacks[attack]["attack"], self.attacks[attack]["damage"])
        return s

    def initiative(self):
        return roll.roll("1d20%s" % (self.init,))

    def do_attack(self, attack, show=False):
        try:
            attack = attack.lower()
            to_hit = roll.roll("1d20%s" % (self.attacks[attack]["attack"]),)
            damage = roll.roll(self.attacks[attack]["damage"])
            if show:
                print "%s hit AC %d for %d damage" % (attack.title(), to_hit, damage)
            return (to_hit, damage)
        except KeyError:
            print "Attack '%s' not available." % (attack.title(),)

    def roll_stat(self, stat, show=False):
        try:
            mod = (self.stats[stat]-10)/2
            if mod > 0:
                mod = "+%d" % (mod,)
            check = roll.roll("1d20%s" % (mod,))
            if show:
                print "%s rolled a %s for %s" % (self.name, stat.title(), check)
        except KeyError:
            print "Stat '%s' not available." % (stat.title(),)


def main():
    try:
        input_file = sys.argv[1]
    except:
        print "Usage: %s [path to character file]" % (sys.argv[0])
        return

    try:
        action = sys.argv[2]
    except IndexError:
        action = "show"

    try:
        c = Character(open(input_file, 'r'))
    except IOError:
        print "Bad filename: %s" % (input_file,)
        return

    if action == "show":
        print c

    if action == "init" or action == "initiative":
        print "%s initiative: %d" % (c.name, c.initiative())

    if action == "attack":
        try:
            attack = sys.argv[3]
        except IndexError:
            print "Usage: %s attack \"attack name\"" % (sys.argv[0],)
        print "%s attacks!" % (c.name)
        c.do_attack(attack, show=True)

    if action == "stat":
        try:
            stat = sys.argv[3]
            c.roll_stat(stat, show=True)
        except IndexError:
            print "Usage: %s stat \"stat name\"" % (sys.argv[0],)
        

if __name__ == '__main__':
    main()
