import json
import difflib
from team_pick import dire_turn

f = open("jsonFile/heroes.json", "r")
data = json.load(f)

heroes_list = list(data.values())
hero_ids = dict()
IngameNameDict = {}
for hero in heroes_list:
    hero_name = hero["name"].split("hero_")[1]
    hero_name_ingame = hero["localized_name"]
    hero_name_ingame = hero_name_ingame.replace("-", "").upper()
    hero_name_ingame = hero_name_ingame.replace(" ", "").upper()
    IngameNameDict[hero_name_ingame] = hero_name


def get_true_hero_name(name, banList, pickList):
    if name in banList or name in pickList:
        return None
    ls = sorted(IngameNameDict.keys(), key= lambda x: len(x))
    closet_name = difflib.get_close_matches(name, ls)
    try:
        return IngameNameDict[closet_name[0]]
    except:
        return None


def fill_list(ls, status):
    new_ls = ls
    for i in range(len(ls), 7):
        new_ls.append(f"empty_{status}.png")
    return new_ls


def team_picking(num_picked, team_first):
    if team_first == "rad":
        if num_picked in dire_turn:
            return "rad"
        return "dire"
    else:
        if num_picked not in dire_turn:
            return "rad"
        return "dire"


def team_banning(num_banned, team_first):
    if team_first == "rad":
        if num_banned % 2 == 0:
            return "rad"
        return "dire"
    else:
        if num_banned % 2 == 1:
            return "rad"
        return "dire"


def process_return(i):
    if i < 10:
        return f"0{i}"
    return str(i)
