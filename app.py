from flask import Flask, jsonify
import json
import requests
import concurrent

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = True


with open("jsonFile/hero_ids.json", "rb") as f:
    hero_ids = json.load(f)


with open("jsonFile/item_ids.json", "rb") as f:
    item_ids = json.load(f)


@app.route("/")
def first_page():
    return "This is for Dota Api"


@app.route("/dota_status")
def dota_status():
    for i in range(5):
        try:
            with open(f"ApiFile/dota_status_{i}.json", "rb") as f:
                return jsonify(json.load(f))
        except:
            pass
    return "No file"


@app.route("/test_status")
def test_status():
    for i in range(5):
        try:
            with open(f"testJsonFile/dota_status_{i}.json", "rb") as f:
                return jsonify(json.load(f))
        except:
            pass
    return "No file"


@app.route("/match_info/<match_id>")
def match_info(match_id):
    r = requests.get(f"https://api.opendota.com/api/matches/{match_id}/")
    data = json.loads(r.content)
    match_dict = []
    for player in data["players"]:
        hero_info = {}
        account_id = player["account_id"]
        account_name = json.loads(requests.get(f"https://api.opendota.com/api/players/{account_id}/").content)["profile"]["name"]
        hero_info[f"playername"] = account_name
        hero_id = player["hero_id"]
        hero_info[f"heroname"] = hero_ids[str(hero_id)]
        hero_info["heroani"] =  hero_ids[str(hero_id)] + ".jpg"
        hero_info[f"level"] = player["level"]
        hero_info[f"networth"] = player["net_worth"]
        hero_info[f"kills"] = player["kills"]
        hero_info[f"deaths"] = player["deaths"]
        hero_info[f"assists"] = player["assists"]
        hero_info[f"damage"] = player["hero_damage"]
        # hero_info[f"items"] = []
        for i in range(6):
            hero_info[f"item{i}"] = item_ids[str(player[f"item_{i}"])] + ".jpg"
        match_dict.append(hero_info)

    return jsonify(match_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
