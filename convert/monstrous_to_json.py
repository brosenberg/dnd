#!/usr/bin/env python

# TODO: Sanitize the data. Look for entries that are missing values.
#       Ex: Sheep's XP Value
# TODO: Normalize the stat names. Mammals, Small has nonstandard namings, for example.

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

        statistic = cols[0].strip(":")
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
            if index+index_mod not in monsters:
                monsters[index+index_mod] = {}
            if statistic in monsters[index+index_mod]:
                if text != '':
                    monsters[index+index_mod][statistic] += " %s" % (text,)
            else:
                monsters[index+index_mod][statistic] = text

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
    title = soup.title.text.replace("(Monstrous Manual)", "").strip()
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

    for monster in monsters:
        if "Name" not in monsters[monster]:
            monsters[monster]["Name"] = title
        else:
            monsters[monster]["Name"] += " (%s)" % (title,)

    return monsters

def main():
    monsters = {}
    for fname in sys.argv[1:]:
        try:
            new_monsters = get_monsters(fname)
            for index in new_monsters:
                monster = new_monsters[index]
                # FIXME: This is caused by a bug. Fix it.
                if len(monster.keys()) < 3:
                    continue
                if monster["Name"] in monsters:
                    print "WARN: %s already exists! %s" % (monster["Name"], fname)
                    continue
                monsters[monster["Name"]] = monster
                del monsters[monster["Name"]]["Name"]
        except:
            print fname
            raise
    print json.dumps(monsters, sort_keys=True, indent=2)

if __name__ == '__main__':
    main()
