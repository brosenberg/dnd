#!/usr/bin/env python

import random

PREFIX = [
    'B',
    'Bal',
    'Bel',
    'Bof',
    'Bol',
    'D',
    'Dal',
    'Dor',
    'Dw',
    'Far',
    'Gil',
    'Gim',
    'Kil',
    'Mor',
    'Nal',
    'Nor',
    'Ov',
    'Th',
    'Thor',
    'Thr',
]

F_SUFFIX = [
    'a',
    'ala',
    'ana',
    'ip',
    'ia',
    'ila',
    'ina',
    'on',
    'ola',
    'ona',
]

M_SUFFIX = [
    'aim',
    'ain',
    'ak',
    'ar',
    'i',
    'im',
    'in',
    'o',
    'or',
    'ur',
]

S_SUFFIX = [
    'ack',
    'arr',
    'bek',
    'dal',
    'duum',
    'dukr',
    'eft',
    'est',
    'fik',
    'gak',
    'hak',
    'hig',
    'jak',
    'kak',
    'lode',
    'malk',
    'mek',
    'rak',
    'tek',
    'zak',
]

FILLER = 'bdfgkmtvz'
VOWELS = 'aeiouy'

def gen_stronghold():
    parts = []
    for i in range(0, random.randint(1,4)):
        parts.append(random.choice(PREFIX))
    parts.append(random.choice(S_SUFFIX))
    for i in range(0, len(parts)):
        try:
            if parts[i][-1] not in VOWELS and parts[i+1][0] not in VOWELS:
                parts.insert(i+1, random.choice(VOWELS))
            if parts[i][-1] in VOWELS and parts[i+1][0] in VOWELS:
                parts.insert(i+1, random.choice(FILLER))
        except IndexError:
            break
    return (''.join(parts)).title()

def gen_firstname(gender="female"):
    name = random.choice(PREFIX)
    suffix = ''
    if gender == "female":
        suffix = random.choice(F_SUFFIX)
    else:
        suffix = random.choice(M_SUFFIX)

    if name[-1].lower() in VOWELS and random.randint(1,3) == 3:
        name = "%s%s%s" % (name, random.choice(FILLER), suffix)
    else:
        name = "%s%s" % (name, suffix)
    return name

def main():
    print "Female Dwarf Name:", gen_firstname()
    print "  Male Dwarf Name:", gen_firstname(gender="male")
    print "  Stronghold Name:", gen_stronghold()

if __name__ == '__main__':
    main()
