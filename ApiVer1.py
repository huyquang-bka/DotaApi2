import pickle
from team_pick import *
from ReverseTime2 import *
from Timer import *
from StringProcess import *
import keyboard
import time
import numpy as np
from PIL import ImageGrab
from win32gui import *

ban_coords_dire_1st = {}
ban_coords_rad_1st = {}
ban_coords = {}

index = 0
with open("SpotFile/ban.csv", "r") as f:
    for line in f.read().split("\n")[:-1]:
        x, y, x2, y2 = list(map(int, line.split(",")))
        w = x2 - x
        h = y2 - y
        index += 1
        ban_coords_dire_1st[index] = [x, y, w, h]
        ban_coords[index] = [x, y, w, h]
        if index % 2 == 1:
            ban_coords_rad_1st[index+1] = [x, y, w, h]
        else:
            ban_coords_rad_1st[index-1] = [x, y, w, h]


with open("BanModel/clf.pkl", "rb") as f:
    clf = pickle.load(f)

reserve_time_coords = {}
with open("SpotFile/reserve_time.csv", "r") as f:
    for line in f.read().split("\n")[:-1]:
        x, y, w, h, index = map(int, line.split(","))
        reserve_time_coords[index] = [x, y, w, h]



window_handle = FindWindow(None, "Dota 2")
x_w, y_w, w_w, h_w = GetWindowRect(window_handle)

hero_mini_list = []
pickList = []
lastBanList = []
n = 0
print("start")

time_first = []
turn = 0
isBan = False
banList = []
present_time = 30
nums_ban = [4, 10, 14]
nums_pick = [4, 8, 10]
return_dict = {}
while True:
    if keyboard.is_pressed("g"):
        s = time.time()
        img = ImageGrab.grab(bbox=(x_w, y_w, w_w, h_w))
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        radiant_time_str, dire_time_str = reverse_time_rad(frame), reverse_time_dire(frame)
        # rv_time_ls = reverse_time(frame)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if gray_frame[578][1639] > 100:
            first_team = "rad"
            ban_coords = ban_coords_rad_1st
            pick_2_coords = pick_2_coords_rad_1st
            pick_coords = pick_coords_rad_1st
        else:
            first_team = "dire"
            ban_coords = ban_coords_dire_1st
            pick_2_coords = pick_2_coords_dire_1st
            pick_coords = pick_coords_dire_1st
        for index in range(1, 15):
            x, y, w, h = ban_coords[index]
            crop = frame[y:y + h, x:x + w]
            H, W, _ = crop.shape
            b, g, r = np.array(crop[5][W - 5], dtype=int)
            if b * g * r == 0:
                present_time = int(get_time_ban(crop))
                break
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            img = np.array(gray.flatten(), dtype=int)
            hero_name = clf.predict([img])[0]
            banList.append(hero_name.split("__")[0])
        print("After ban: ", present_time)
        if present_time != 30 and present_time != -1:
            isBan = True
        else:
            isBan = False
        print("isBan: ", isBan)
        print(time.time() - s)
        for i in range(10):
            hero_mini_list = pick_phase(frame, hero_mini_list, pick_coords, i)
            if len(hero_mini_list) > 0:
                print(hero_mini_list[-1])
                pickList.append(get_true_hero_name(hero_mini_list[-1], banList, pickList))
                hero_mini_list = []

        if not isBan:
            present_time = int(get_time_pick(frame, len(pickList), first_team))
        break


print(first_team)
print(present_time)
present_time = present_time - (time.time() - s)
first_count = True
isPick = False
banned = 0
count_unpick = 0
print(banList)
print(pickList)
print(radiant_time_str, dire_time_str, present_time)
exit()
# print(rv_time_ls)
isRadiant = True
while True:
    start = time.time()
    rad_ban = []
    dire_ban = []
    rad_pick = []
    dire_pick = []
    img = ImageGrab.grab(bbox=(x_w, y_w, w_w, h_w))
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if list(frame[131][12]) == [179, 177, 175]:
        continue
    if gray_frame[281][68] < 60 or gray_frame[919][19] < 30:
        isPick = True
    else:
        isPick = False

    if isBan and banned < 14:
        banList = []
        count_ban = 0
        for index in range(1, 15):
            x, y, w, h = ban_coords[index]
            crop = frame[y:y + h, x:x + w]
            H, W, _ = crop.shape
            b, g, r = np.array(crop[5][W-5], dtype=int)
            if b * g * r == 0:
                break
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            img = np.array(gray.flatten(), dtype=int)
            hero_name = clf.predict([img])[0]
            banList.append(hero_name.split("__")[0])
    if banList != lastBanList:
        print(banList)
        lastBanList = banList
        base_time = 30


    if not isPick:
        hero_mini_list = pick_phase(frame, hero_mini_list, pick_coords, len(pickList))
        if len(hero_mini_list) > 0:
            if get_true_hero_name(hero_mini_list[0], banList, pickList) in pickList:
                hero_mini_list = []
        if len(hero_mini_list) == 2:
            print(hero_mini_list[-1])
            hero_append = get_true_hero_name(hero_mini_list[-1], banList, pickList)
            hero_mini_list = []
            if hero_append not in pickList and hero_append is not None:
                pickList.append(hero_append)
        if len(pickList) > n:
            print(pickList)
            n = len(pickList)
            print("*" * 50)
            base_time = 24


    banned = len(banList)
    picked = len(pickList)
    if banned in nums_ban:
        isBan = False
    if picked in nums_pick and isBan is False:
        if nums_ban.index(banned) == nums_pick.index(picked):
            isBan = True
    if first_count:
        base_time = present_time
        first_count = False
    team1 = []
    team2 = []
    for i in range(10):
        if i in dire_turn:
            try:
                team1.append(pickList[i] + ".png")
            except:
                pass
        else:
            try:
                team2.append(pickList[i] + ".png")
            except:
                pass
    if first_team == "rad":
        rad_pick = team1
        dire_pick = team2
    else:
        rad_pick = team2
        dire_pick = team1
    for i in range(len(banList)):
        if first_team == "rad":
            if i % 2 == 0:
                rad_ban.append(banList[i] + ".jpg")
            else:
                dire_ban.append(banList[i] + ".jpg")
        else:
            if i % 2 == 1:
                rad_ban.append(banList[i] + ".jpg")
            else:
                dire_ban.append(banList[i] + ".jpg")
    if isBan and len(banList) < 14:
        teamBanning = team_banning(banned, first_team)
        if teamBanning == "dire":
            isRadiant = False
            dire_ban.append("banning.mov")
        else:
            isRadiant = True
            rad_ban.append("banning.mov")
    else:
        teamPicking = team_picking(picked, first_team)
        if teamPicking == "dire":
            isRadiant = False
            dire_pick.append("picking.mov")
        else:
            isRadiant = True
            rad_pick.append("picking.mov")
    rad_ban = fill_list(rad_ban, "ban")
    dire_ban = fill_list(dire_ban, "ban")
    rad_pick = fill_list(rad_pick, "pick")
    dire_pick = fill_list(dire_pick, "pick")
    for i in range(7):
        return_dict[f"turn_{process_return(i+1)}"] = dire_ban[i]
        return_dict[f"turn_{process_return(i+8)}"] = rad_ban[i]
        if i < 5:
            return_dict[f"turn_{process_return(i + 15)}"] = dire_pick[i]
            return_dict[f"turn_{process_return(i + 20)}"] = rad_pick[i]
    if base_time > 0:
        base_time -= time.time() - start
    else:
        if not isPick:
            if isRadiant:
                radiant_time_str = reverse_time_rad(frame)
            else:
                dire_time_str = reverse_time_dire(frame)
        base_time = 0
    return_dict["RT_radiant"] = radiant_time_str
    return_dict["RT_dire"] = dire_time_str
    return_dict["timeBP"] = "0:" + str(int(base_time)) if base_time//10 >= 1 else "0:0" + str(int(base_time))
    if len(pickList) == 10:
        return_dict["RT_radiant"] = ""
        return_dict["RT_dire"] = ""
        return_dict["timeBP"] = ""
    print(int(base_time), radiant_time_str, dire_time_str, "isBan: ", isBan, "isPick: ", isPick, "isRadiant: ", isRadiant)
    print(banList, pickList)
    # Writing to sample.json
    json_object = json.dumps(return_dict)
    for i in range(5):
        with open(f"ApiFile/dota_status_{i}.json", "w+") as outfile:
            outfile.write(json_object)
    print(time.time() - start)
    if len(pickList) == 10:
        break
