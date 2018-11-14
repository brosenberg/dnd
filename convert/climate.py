#!/usr/bin/env python
# -*- coding: utf-8 -*-


import copy
import json
import re
import sys


CLIMATES = set([
    "any",
    "arctic",
    "arid",
    "cold",
    "freshwater",
    "nonarctic",
    "nontropical",
    "saltwater",
    "subarctic",
    "subterranean",
    "subtropical",
    "temperate",
    "tropical",
    "warm"
])

# Returns (climates, terrains)
def handle_separates(separate):
    climates = set([])
    if separate in CLIMATES:
        return (set([separate]), None)
    if separate == 'any except arctic':
        return (CLIMATES.difference(['any', 'arctic']), None)
    subseparates = separate.split()
    terrain = copy.deepcopy(subseparates)
    for subseparate in subseparates:
        if subseparate in CLIMATES:
            climates.add(subseparate)
            terrain.remove(subseparate)
    if terrain != subseparates and terrain:
        if terrain[0] in CLIMATES:
            if len(terrain) > 1:
                sys.stderr.write("Something went wrong with handles_separates()\n")
                sys.stderr.write(str(terrain) + "\n")
            climates.add(terrain[0])
            terrain = []
    if climates:
        if terrain == []:
            return (climates, None)
        else:
            return (climates, ' '.join(terrain))
    return (None, separate)

def normalize_terrain(terrains):
    normalize = {
        'coastal marine': 'sea coast',
        'deep ocean': 'deep sea',
        'deep waters': 'deep aquatic',
        'forest with oaks': 'oak forests',
        'forest': 'forests',
        'lake shore': 'lake shores',
        'large areas of water': 'aquatic',
        'magical cloud islands': 'cloud islands',
        'marine': 'aquatic',
        'mountain': 'mountains',
        'mountainous': 'mountains',
        'ocean': 'sea',
        'oceans': 'sea',
        'plain': 'plains',
        'river': 'rivers',
        'sea coast': 'sea coasts',
        'sea shore': 'sea shores',
        'seacoast': 'sea coasts',
        'seashore': 'sea shores',
        'swamp': 'swamps',
        'very deep oceans': 'very deep sea',
        'waters': 'aquatic',
        'woodlands': 'forests'
    }
    new_terrains = set()
    for terrain in terrains:
        if terrain in normalize:
            new_terrains.add(normalize[terrain])
        else:
            new_terrains.add(terrain)
    return new_terrains

def read_climates(raw_climate):
    climates = set()
    terrains = set()
    SEPS = [
            ', and ',
            ' and ',
            ', or ',
            ' or ',
            ' to ',
            ', ',
            ' & ',
            '/',
           ]
    separated = re.split(r'|'.join(SEPS), raw_climate)
    for separate in separated:
        handled = handle_separates(separate)
        if handled[0] is not None:
            climates.update(handled[0])
        if handled[1] is not None:
            if handled[1] in CLIMATES:
                print [separate, handled[1]]
                
            terrains.add(handled[1])
    #print monster, climates, terrains
    return (climates, terrains)

def doit(monsters):
    raw_climates = set()
    climates = set()
    terrains = set()
    for monster in monsters:
        # Cleanup input
        climate = monsters[monster]["Climate/Terrain"].lower() \
                                                      .replace('-', '') \
                                                      .replace('artic', 'arctic') \
                                                      .replace(', any terrain', '') \
                                                      .replace('hills,and', 'hills, and') \
                                                      .replace('hill and mountain caverns', 'hill caverns and mountain caverns') \
                                                      .replace(', with visits to other climes', '') \
                                                      .replace('any ruins', 'ruins') \
                                                      .replace('any underground', 'subterranean') \
                                                      .replace('any pool', 'any, pools') \
                                                      .replace('below ground', 'subterranean') \
                                                      .replace('terrain', 'land') \
                                                      .replace(', in wilderness areas', '') \
                                                      .replace('temperature', 'temperate') \
                                                      .replace('demiplane of shadow', 'plane of shadow') \
                                                      .replace(' (preferred)', '') \
                                                      .replace('(rarely temperate ', ' and ') \
                                                      .replace('and forests.)', 'and forests')
        #print monster.encode('utf-8'), norm_climate(climate)
        normalized = read_climates(climate)
        climates.update(normalized[0])
        terrains.update(normalized[1])
    terrains = normalize_terrain(terrains)
    print '\n'.join(sorted(climates))
    print '\n\n'
    print '\n'.join(sorted(terrains))

def main():
    monsters = json.load(open(sys.argv[1]))
    doit(monsters)

if __name__ == '__main__':
    main()
