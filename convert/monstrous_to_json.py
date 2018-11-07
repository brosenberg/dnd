#!/usr/bin/env python

# Consume the pages from http://dedpihto.narod.ru/games/Monsters1/MM00000.htm
#   and dump them to JSON

# TODO: Sanitize the data. Look for entries that are missing values.
#       Ex: Sheep's XP Value
# TODO: Extract XP lists like the Fire Giant, Treant, and Vampire have

import json
import sys

from bs4 import BeautifulSoup

def find_statblock(soup):
    for td in soup.find_all('td'):
        if "THAC0" in td.text:
            return td.parent.parent
    # Some monster pages don't list a THAC0 in the table (Mammal, Small)
    for td in soup.find_all('td'):
        if "XP" in td.text:
            return td.parent.parent

def parse_monsters_columns(stat_block, title):
    monsters = {}
    previous_statistic = None
    index_mod = 0
    for row in stat_block.find_all('tr'):
        cols = [x.text.strip() for x in row.find_all('td')]
        prefixes = [
                    "Bugbear leader",
                    "Bugbear chief",
                    "Bugbear shaman",
                    "Elder",
                    "Jaculi",
                   ]

        statistic = cols[0].strip(':')
        prefix = None
        if not cols[0].endswith(':'):
            statistic = u''
        if statistic in prefixes:
            prefix = statistic
            statistic = u'XP Value'
        if statistic == u'':
            if previous_statistic == None:
                statistic = "Name"
            # Not the greatest way to check for this being a new entry...
            # But if the last stat was the XP value and we have some blank
            # entries, this is probably the beginning of a new stat block.
            # See the Human entry for an example.
            elif previous_statistic == "XP Value":
                if [x for x in cols if x != u''] == []:
                    continue
                else:
                    index_mod = max(monsters.keys()) + 1
                    statistic = "Name"
            else:
                statistic = previous_statistic
        previous_statistic = statistic

        for index in range(0, len(cols[1:])):
            text = cols[index+1].strip()
            index += index_mod
            if index not in monsters:
                monsters[index] = {}
            if statistic in monsters[index]:
                if text != '':
                    if prefix:
                        monsters[index][statistic] += " %s: %s" % (prefix, text)
                    else:
                        monsters[index][statistic] += " %s" % (text,)
            else:
                monsters[index][statistic] = text

    return monsters

def parse_monsters_rows(stat_block, title):
    monsters = {}
    first_tr = stat_block.find('tr')
    headings = [x.text.strip() for x in first_tr.find_all('td')]
    headings[0] = "Name"
    previous_monster_index = 0
    for tr in first_tr.find_next_siblings('tr'):
        statistics = tr.find_all('td')
        monster_index = len(monsters.keys())
        if statistics[0].text.strip() == '':
            monster_index = previous_monster_index
        elif statistics[0].text.strip() == 'Mantis':
            monster_index = previous_monster_index
            monsters[monster_index]["Name"] = "Praying Mantis"
        elif previous_monster_index in monsters and monsters[previous_monster_index]["Name"][-1] == ',':
            monster_index = previous_monster_index
        else:
            previous_monster_index = monster_index
            monsters[monster_index] = {}
        for index in range(0, len(statistics)):
            if headings[index] in monsters[monster_index]:
                if statistics[index].text.strip() != '':
                    monsters[monster_index][headings[index]] += " %s" % (statistics[index].text.strip(),)
            else:
                monsters[monster_index][headings[index]] = statistics[index].text.strip()

    return monsters

def cleanup_monsters(monsters, title):
    to_delete = []

    # Some pages are malformed, so some statistics don't get picked up properly.
    # Some monster entries are missing data or have strangely formatted data.
    # TODO: Automatically pull out Climates that span the entire width of the
    #       table and use it to populate everything in that table.
    if title == "Bird":
        for monster in monsters:
            monsters[monster]["Climate/Terrain"] = "Various"
    elif title == "Crocodile":
        monsters[1]["Climate/Terrain"] = "Subtropical and tropical/Saltwater swamps and rivers"
    elif title == "Elemental, Fire-Kin":
        monsters[0]["Frequency"] = "Rare"
        monsters[1]["Frequency"] = "Uncommon"
    elif title == "Elf":
        monsters[0]["Activity Cycle"] = "Any"
    elif title == "Elf, Drow":
        monsters[1]["Climate/Terrain"] = "Subterranean caves & cities"
        monsters[1]["Activity Cycle"] = "Any underground, night aboveground"
    elif title == "Fish":
        for monster in monsters:
            monsters[monster]["Climate/Terrain"] = "Water"
    elif title == "Gargoyle":
        monsters[1]["Climate/Terrain"] = "Any land, subterranean, ocean"
    elif title == "Giant, Cyclcops":
        monsters[1]["Climate/Terrain"] = "Temperate/Hills and mountains"
    elif title == "Horses":
        for monster in monsters:
            monsters[monster]["Climate/Terrain"] = "Any non-mountainous"
    elif title == "Human":
        for monster in monsters:
            monsters[monster]["Climate/Terrain"] = "Any"
    elif title == "Insect":
        for monster in monsters:
            monsters[monster]["Climate/Terrain"] = "Any"
    elif title == "Intellect Devourer":
        monsters[0]["Name"] = "Intellect Devourer, Adult"
        monsters[1]["Name"] = "Intellect Devourer, Larva"
    elif title == "Lamia":
        monsters[1]["Climate/Terrain"] = "Deserts, caves and ruined cities"
    elif title == "Lammasu":
        monsters[1]["Climate/Terrain"] = "Warm, with visits to other climes"
    elif title == "Leech":
        for monster in monsters:
            monsters[monster]["Climate/Terrain"] = "Temperate/Swamps and marshes"
    elif title == "Mammal":
        for monster in monsters:
            monsters[monster]["Climate/Terrain"] = "Various"
    elif title == "Mammal, Small":
        monsters[21]["Name"] = "Squirrel, Flying"
        monsters[22]["Name"] = "Squirrel, Giant black"
        for monster in monsters:
            monsters[monster]["Climate/Terrain"] = "Various"
            monsters[monster]["Frequency"] = "Common"
            monsters[monster]["Intelligence"] = "Animal (1)"
            monsters[monster]["Alignment"] = "Neutral"
            monsters[monster]["Magic Resistance"] = "Nil"
            monsters[monster]["Morale"] = "Unreliable to Average (2-9)"
            monsters[monster]["THAC0"] = "20"
        monsters[9]["THAC0"] = "19"
        monsters[14]["THAC0"] = "19"
        monsters[15]["THAC0"] = "19"
        monsters[17]["THAC0"] = "19"
        monsters[22]["THAC0"] = "19"
    elif title == "Mammal, Herd":
        monsters[3]["XP Value"] = "35"
        monsters[4]["XP Value"] = "35"
    elif title == "Mimic":
        monsters[1]["Climate/Terrain"] = "Subterranean"
    elif title == "Plant, Dangerous":
        monsters[5]["Name"] = "Tri-flower Frond"
        monsters[6]["Name"] = "Yellow Musk Creeper"
        monsters[7]["Name"] = "Yellow Musk Zombie"
    elif title == "Plant, Intelligent":
        monsters[7]["Name"] = "Thorny"
    elif title == "Ogre, Half-":
        monsters[0]["Name"] = "Half-Ogre"
        monsters[1]["Name"] = "Ogrillon"
    elif title == "Rat":
        monsters[0]["Name"] = "Rat, Giant"
        monsters[1]["Name"] = "Osquip"
    elif title == "Shedu":
        monsters[1]["Activity Cycle"] = "Hottest part of the day"
    elif title == "Swanmay":
        monsters[1]["Treasure"] = "See below"
    elif title == "Tabaxi":
        monsters[1]["Climate/Terrain"] = "Tropical or subtropical jungle"
        monsters[1]["Special Defenses"] = "Surprise, surprised only on a 1"
    elif title == "Tako":
        monsters[0]["Name"] = "Male Tako"
        monsters[1]["Name"] = "Female Tako"

    for monster in monsters:
        if [True for x in monsters[monster] if monsters[monster][x] != ''] == [True] or \
            [True for x in monsters[monster] if monsters[monster][x] != ''] == []:
            to_delete.append(monster)
    for monster in to_delete:
        del monsters[monster]

    normalize = {
                    "# AT": "No. of Attacks",
                    "# of Att": "No. of Attacks",
                    "#Att": "No. of Attacks",
                    "#AP": "No. Appearing",
                    "AC": "Armor Class",
                    "App.": "No. Appearing",
                    "Dmg/AT": "Damage/Attack",
                    "Dmg/Att": "Damage/Attack",
                    "HD": "Hit Dice",
                    "MV": "Movement",
                    "Mv": "Movement",
                    "XP": "XP Value"
    }

    for monster in monsters:
        if "Name" not in monsters[monster]:
            monsters[monster]["Name"] = title
        else:
            monsters[monster]["Name"] += " (%s)" % (title,)
        monsters[monster]["Name"] = monsters[monster]["Name"].strip()

        if monsters[monster].get("Frequency") == "Very Rare":
            monsters[monster]["Frequency"] = "Very rare"

        if "Notes" in monsters[monster] and monsters[monster]["Notes"] == '':
            del(monsters[monster]["Notes"])

        for normal in normalize:
            if normal in monsters[monster]:
                monsters[monster][ normalize[normal] ] = monsters[monster][normal]
                del monsters[monster][normal]

        for stat in monsters[monster]:
            monsters[monster][stat] = monsters[monster][stat].replace('/ ', '/') \
                                                             .replace('- ', '-') \
                                                             .replace('\n', '-') \
                                                             .replace(', -', ', ') \
                                                             .replace(' -', ' ') \

    return monsters

def get_monsters(fname):
    soup = BeautifulSoup(open(fname).read(), 'html.parser')
    stat_block = find_statblock(soup)
    title = soup.title.text.replace("(Monstrous Manual)", "").replace("--", ",").strip()
    monsters = {}

    # Detect if the monsters on this page are arranged in rows or columns.
    # Column example: Satyr
    # Row example: Mammals
    # u'AC', u'# of Att', u'THAC0', u'#AP', u'Morale', u'MV', u'Dmg/Att', u'XP Value', u'HD'
    row_page_headings = set([u'ac', u'mv', u'hd'])
    if row_page_headings.issubset(set([x.text.strip().lower() for x in stat_block.find('tr').find_all('td')])):
        monsters = parse_monsters_rows(stat_block, title)
    else:
        monsters = parse_monsters_columns(stat_block, title)

    monsters = cleanup_monsters(monsters, title)

    return monsters

def get_unique_statistics(monsters):
    stats = set()
    for monster in monsters:
        stats.update(monsters[monster].keys())
    return stats

def monsters_with_empty_stats(monsters):
    for monster in monsters:
        for stat in monsters[monster].keys():
            if monsters[monster][stat] == '':
                print "%s %s == ''" % (monster, stat)

def monsters_with_no_stat(monsters, stat):
    for monster in monsters:
        if monsters[monster].get(stat) is None:
            print "%s has no %s" % (monster, stat)

def monsters_missing_important_stats(monsters):
    stats = [
        'Activity Cycle',
        'Alignment',
        'Armor Class',
        'Climate/Terrain',
        'Damage/Attack',
        'Diet',
        'Frequency',
        'Hit Dice',
        'Intelligence',
        'Magic Resistance',
        'Morale',
        'Movement',
        'No. Appearing',
        'No. of Attacks',
        'Organization',
        'Size',
        'Special Attacks',
        'Special Defenses',
        'THAC0',
        'Treasure',
        'XP Value'
    ]
    for stat in stats:
        monsters_with_no_stat(monsters, stat)

def main():
    monsters = {}
    for fname in sys.argv[1:]:
        try:
            new_monsters = get_monsters(fname)
            #print json.dumps(new_monsters, indent=2)
            for index in new_monsters:
                monster = new_monsters[index]
                # FIXME: This is caused by a bug. Fix it.
                if len(monster.keys()) < 3:
                    continue
                if monster["Name"] in monsters:
                    sys.stderr.write("WARN: %s already exists! %s\n" % (monster["Name"], fname))
                    continue
                monsters[monster["Name"]] = monster
                del monsters[monster["Name"]]["Name"]
        except:
            print "Problem parsing %s" % (fname,)
            raise
    print json.dumps(monsters, sort_keys=True, indent=2)

if __name__ == '__main__':
    main()
