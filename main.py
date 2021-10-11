import keyboard
import numpy as np
from PIL import ImageGrab
from win32gui import *
import cv2
import json
from team_pick import *
from image_to_text import *
from StringProcess import *
import time

window_handle = FindWindow(None, "Dota 2")
x_w, y_w, w_w, h_w = GetWindowRect(window_handle)
return_dict = {}
print("start")
pickListLast = []
hero_mini_list = []
banList = []
isPick = False
count_unpick = 0
pickList = ['monkey_king', 'jakiro', 'treant', 'legion_commander']
while True:
    if keyboard.is_pressed("g"):
        img = ImageGrab.grab(bbox=(x_w, y_w, w_w, h_w))
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if gray_frame[578][1639] > 100:
            pick_2_coords = pick_2_coords_rad_1st
            print("Rad 1st")
        else:
            pick_2_coords = pick_2_coords_dire_1st
            print("Dire 1st")
        break

n = len(pickList)

while True:
    img = ImageGrab.grab(bbox=(x_w, y_w, w_w, h_w))
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if list(frame[131][12]) == [179, 177, 175]:
        continue
    if gray_frame[281][68] < 50 or gray_frame[919][19] < 20:
        isPick = True
    else:
        isPick = False
    # else:
    #     isPick = False
    return_dict["isPick"] = isPick
    num_hero_picked = len(pickList)
    if isPick:
        hero_mini_list = pick_phase_2_coord(frame, hero_mini_list, pick_2_coords, len(pickList))
        if len(hero_mini_list) > 0:
            if get_true_hero_name(hero_mini_list[0], banList, pickList) in pickList:
                hero_mini_list = []
        if len(hero_mini_list) == 4:
            hero_append = get_true_hero_name(hero_mini_list[-1], banList, pickList)
            if hero_append not in pickList:
                print(hero_mini_list)
                pickList.append(hero_append)
                # time.sleep(1)
            hero_mini_list = []

        if len(pickList) > n:
            print(pickList)
            n = len(pickList)
            print("*" * 50)
            base_time = 27

    return_dict["isPick"] = isPick
    return_dict["listPick"] = pickList

    print(return_dict)
    json_object = json.dumps(return_dict)

    # Writing to sample.json
    for i in range(5):
        with open(f"testJsonFile/dota_status_{i}.json", "w+") as outfile:
            outfile.write(json_object)
