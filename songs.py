import requests
import json
from datetime import datetime

def off_ver(num):
    vl = {
    "100": "maimai",
    "110": "maimai PLUS",
    "120": "GreeN",
    "130": "GreeN PLUS",
    "140": "ORANGE",
    "150": "ORANGE PLUS",
    "160": "PiNK",
    "170": "PiNK PLUS",
    "180": "MURASAKi",
    "185": "MURASAKi PLUS",
    "190": "MiLK",
    "195": "MiLK PLUS",
    "199": "FiNALE",
    "200": "DX",
    "205": "DX PLUS",
    "210": "Splash",
    "215": "Splash PLUS",
    "220": "UNiVERSE",
    "225": "UNiVERSE PLUS",
    "230": "FESTiVAL",
    "235": "FESTiVAL PLUS",
    "240": "BUDDiES",
    "245": "BUDDiES PLUS",
    "250": "PRiSM",
    "255": "PRiSM PLUS",
    "260": "CiRCLE"
}
    return vl[int(num)//1000]


def version(date):
    nd = datetime.strptime(date, "%Y-%m-%d")
    vl = {
    "maimai": "2012-07-11",
    "maimai PLUS": "2012-12-13",
    "GreeN": "2013-07-11",
    "GreeN PLUS": "2014-02-26",
    "ORANGE": "2014-09-18",
    "ORANGE PLUS": "2015-03-19",
    "PiNK": "2015-12-09",
    "PiNK PLUS": "2016-06-30",
    "MURASAKi": "2016-12-15",
    "MURASAKi PLUS": "2017-06-22",
    "MiLK": "2017-12-14",
    "MiLK PLUS": "2018-06-21",
    "FiNALE": "2018-12-13",
    "DX": "2019-07-11",
    "DX PLUS": "2020-01-23",
    "Splash": "2020-09-17",
    "Splash PLUS": "2021-03-18",
    "UNiVERSE": "2021-09-16",
    "UNiVERSE PLUS": "2022-03-24",
    "FESTiVAL": "2022-09-15",
    "FESTiVAL PLUS": "2023-03-22",
    "BUDDiES": "2023-09-14",
    "BUDDiES PLUS": "2024-03-21",
    "PRiSM": "2024-09-12",
    "PRiSM PLUS": "2025-03-13",
    "CiRCLE": "2025-09-18",
    "CiRCLE PLUS": "2026-03-19"
}
    cv = "NaV"
    for i in vl:
        if nd >= datetime.strptime(vl[i], "%Y-%m-%d"):
            cv = i
        else:
            return cv

def update():
    ltll = {"BAS": "BASIC", "ADV": "ADVANCED", "EXP":"EXPERT", "MAS":"MASTER", "REMAS":"Re:MASTER"}
    songs = {}
    r = json.loads(requests.get("https://reiwa.f5.si/maimai_all.json").content.decode("utf-8-sig"))
    for i in r:
        name = i.get("meta").get("title")
        songs[name] = {
    "artist": i.get("meta").get("artist"),
    "genre": i.get("meta").get("genre"),
    "version": version(i.get("meta").get("release")),
    "img": f'{i["meta"]["img"]}.png',
    "const": {},
    "unknown": {},
    "region": {"JP": False,"INT": False,"CN": False}
    }
        songs[name]["const"] = {}
        for ds in i.get("data"):
            for lv in i.get("data").get(ds):
                songs[name]["const"][f'{ds.upper()}_{ltll.get(lv)}'] = i.get("data").get(ds).get(lv).get("const")
                songs[name]["unknown"][f'{ds.upper()}_{ltll.get(lv)}'] = i.get("data").get(ds).get(lv).get("is_const_unknown")
    r = json.loads(requests.get("https://reiwa.f5.si/maimai_official.json").content.decode("utf-8-sig"))
    for i in r:
        if i["title"] not in songs and i["catcode"] != "宴会場":
            print(f"日服發現新歌：{i['title']}")
            songs[i["title"]] = {}
        elif i["catcode"] != "宴会場":
            songs[i["title"]]["region"]["JP"] = True
    r = json.loads(requests.get("https://maimai.sega.com/assets/data/maimai_songs.json").content.decode("utf-8-sig"))
    for i in r:
        if i["title"] not in songs and i["catcode"] != "宴会場":
            print(f"國際版發現新歌：{i['title']}")
            songs[i["title"]] = {}
        elif i["catcode"] != "宴会場":
            songs[i["title"]]["region"]["INT"] = True
    r = json.loads(requests.get("https://raw.githubusercontent.com/CrazyKidCN/maimaiDX-CN-songs-database/refs/heads/main/maidata.json").content.decode("utf-8-sig"))
    for i in r:
        if i["title"] not in songs and i["title"] != "Bad Apple!! feat nomico":
            print(f"舞萌DX發現新歌：{i['title']}")
            songs[i["title"]] = {}
        elif i["title"] != "Bad Apple!! feat nomico":
            songs[i["title"]]["region"]["CN"] = True

    with open("songs.json", "w", encoding="utf-8") as file:
        json.dump(songs, file, indent=4,ensure_ascii=False)
    return songs

update()