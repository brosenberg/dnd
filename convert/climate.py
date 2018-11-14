#!/usr/bin/env python
# -*- coding: utf-8 -*-


import copy
import json
import re
import sys

# TODO: Transform non* climates into sane lists of terrains or climates.
CLIMATES = set([
    "any",
    "arctic",
    "arid",
    "cold",
    "freshwater",
    "nonarctic",
    "nonmountainous",
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
        return ('nonarctic')
        #return (CLIMATES.difference(['any', 'arctic']), None)
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
        'coast': (
            ['coastal'],
            []
        ),
        'coastal marine': (
            ['aquatic', 'coastal'],
            ['saltwater']
        ),
        'deep ocean': (
            ['aquatic', 'deep sea'],
            ['saltwater']
        ),
        'deep waters': (
            ['deep aquatic'],
            []
        ),
        'fresh': (
            ['aquatic'],
            ['freshwater']
        ),
        'fresh water': (
            ['aquatic'],
            ['freshwater']
        ),
        'forest with oaks': (
            ['oak forests'],
            []
        ),
        'forest': (
           ['forests'],
           []
        ),
        'lake shore': (
           ['aquatic'],
           ['freshwater']
        ),
        'large areas of water': (
           ['aquatic'],
           []
        ),
        'magical cloud islands': (
           ['cloud islands'],
           []
        ),
        'marine': (
           ['aquatic'],
           ['saltwater']
        ),
        'mountain': (
           ['mountains'],
           []
        ),
        'mountainous': (
           ['mountains'],
           []
        ),
        'ocean': (
           ['aquatic'],
           ['saltwater']
        ),
        'oceans': (
           ['aquatic'],
           ['saltwater']
        ),
        'plain': (
           ['plains'],
           []
        ),
        'river': (
           ['aquatic', 'rivers'],
           ['freshwater']
        ),
        'salt water': (
            ['aquatic'],
            ['saltwater']
        ),
        'salt water depths': (
            ['aquatic', 'deep sea'],
            ['saltwater']
        ),
        'sea bed': (
            ['aquatic'],
            ['saltwater']
        ),
        'sea coasts': (
           ['aquatic', 'coastal'],
           ['saltwater']
        ),
        'sea shore': (
           ['aquatic', 'coastal'],
           ['saltwater']
        ),
        'seacoast': (
           ['aquatic', 'coastal'],
           ['saltwater']
        ),
        'seashore': (
           ['aquatic', 'coastal'],
           ['saltwater']
        ),
        'shallow salt water': (
           ['aquatic', 'coastal'],
           ['saltwater']
        ),
        'swamp': (
           ['swamps'],
           []
        ),
        'very deep oceans': (
           ['aquatic', 'very deep sea'],
           ['saltwater']
        ),
        'water': (
           ['aquatic'],
           []
        ),
        'waters': (
           ['aquatic'],
           []
        ),
        'woodlands': (
           ['forests'],
           []
        )
    }
    new_terrains = set()
    new_climates = set()
    for terrain in terrains:
        if terrain in normalize:
            new_terrains.update(normalize[terrain][0])
            new_climates.update(normalize[terrain][1])
        else:
            new_terrains.add(terrain)
    return (new_climates, new_terrains)

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
        (climates, terrains) = read_climates(climate)
        (new_climates, terrains) = normalize_terrain(terrains)
        climates.update(new_climates)
        if True in [x.startswith('non') for x in climates]:
            climates.discard('any')
        #print monster.encode('utf-8'), climates, terrains
        monsters[monster]["Normalized Climates"] = list(climates)
        monsters[monster]["Normalized Terrains"] = list(terrains)

    print json.dumps(monsters, sort_keys=True, indent=2)

    ###
    #    climates.update(normalized[0])
    #    terrains.update(normalized[1])
    #(new_climates, terrains) = normalize_terrain(terrains)
    #climates.update(new_climates)
    #print '\n'.join(sorted(climates))
    #print '\n\n'
    #print '\n'.join(sorted(terrains))
    ###

def main():
    monsters = json.load(open(sys.argv[1]))
    doit(monsters)

if __name__ == '__main__':
    main()
