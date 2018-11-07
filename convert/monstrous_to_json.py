#!/usr/bin/env python

# Consume the pages from http://dedpihto.narod.ru/games/Monsters1/MM00000.htm
#   and dump them to JSON

# TODO: Sanitize the data. Look for entries that are missing values.
#       Ex: Sheep's XP Value
# TODO: Normalize the stat names. Mammals, Small has nonstandard namings, for example.
# TODO: Extract XP lists like the Fire Giant has

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
            statistic = u''
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
        elif previous_monster_index in  monsters and monsters[previous_monster_index]["Name"][-1] == ',':
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

    # Some pages are malformed, so some statistics don't get picked up properly.
    if title == "Cat, Great":
        del(monsters[9])
    if title == "Giant, Fire":
        del(monsters[1])
        del(monsters[2])
    elif title == "Intellect Devourer":
        monsters[0]["Name"] = "Intellect Devourer, Adult"
        monsters[1]["Name"] = "Intellect Devourer, Larva"
    elif title == "Plant, Dangerous":
        monsters[5]["Name"] = "Tri-flower Frond"
        monsters[6]["Name"] = "Yellow Musk Creeper"
        monsters[7]["Name"] = "Yellow Musk Zombie"
    elif title == "Plant, Intelligent":
        monsters[7]["Name"] = "Thorny"
    elif title == "Ogre, Half-":
        monsters[0]["Name"] = "Half-Ogre"
        monsters[1]["Name"] = "Ogrillon"
    elif title == "Ooze/Slime/Jelly II":
        del(monsters[5])
    elif title == "Rat":
        monsters[0]["Name"] = "Rat, Giant"
        monsters[1]["Name"] = "Osquip"
    elif title == "Tako":
        monsters[0]["Name"] = "Male Tako"
        monsters[1]["Name"] = "Female Tako"

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

        for normal in normalize:
            if normal in monsters[monster]:
                monsters[monster][ normalize[normal] ] = monsters[monster][normal]
                del monsters[monster][normal]

    return monsters

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
            print fname
            raise
    keys = set()
    for monster in monsters:
        keys.update(monsters[monster].keys())
    for key in sorted(keys):
        print key
    #print json.dumps(monsters, sort_keys=True, indent=2)

if __name__ == '__main__':
    main()
