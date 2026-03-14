import requests
import json
from datetime import datetime

def off_ver(num): #由官方版本號轉換版本名稱
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
    return vl[str(int(num)//100)]


def version(date): #由日期推算版本名稱
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

def update(): #更新歌曲資料庫
    ltll = {"BAS": "BASIC", "ADV": "ADVANCED", "EXP":"EXPERT", "MAS":"MASTER", "REMAS":"Re:MASTER"} #短名到完整名稱對照表
    songs = {}
    r = json.loads(requests.get("https://reiwa.f5.si/maimai_all.json").content.decode("utf-8-sig"))
    for i in r:
        name = i.get("meta").get("title") #抓取歌曲名稱
        songs[name] = {
    "artist": i.get("meta").get("artist"), #抓取作曲者資料
    "genre": i.get("meta").get("genre"), #抓取歌曲分類
    "version": version(i.get("meta").get("release")), #由推出日期推算版本名稱
    "img": f'{i["meta"]["img"]}.png', #圖片保存位置
    "const": {}, #定數列表
    "unknown": {}, #是否未知定數
    "region": {"JP": False,"INT": False,"CN": False} #各版本收錄情況
    }
        for ds in i.get("data"):
            for lv in i.get("data").get(ds):
                songs[name]["const"][f'{ds.upper()}_{ltll.get(lv)}'] = i.get("data").get(ds).get(lv).get("const") #抓取類型_難度的定數
                songs[name]["unknown"][f'{ds.upper()}_{ltll.get(lv)}'] = i.get("data").get(ds).get(lv).get("is_const_unknown") #檢查是否未知定數
    off_lv = {"dx_lev_bas": "DX_BASIC","dx_lev_adv": "DX_ADVANCED","dx_lev_exp": "DX_EXPERT","dx_lev_mas": "DX_MASTER","dx_lev_remas": "DX_Re:MASTER","lev_bas": "STD_BASIC","lev_adv": "STD_ADVANCED","lev_exp": "STD_EXPERT","lev_mas": "STD_MASTER","lev_remas": "STD_Re:MASTER"} #官網資料與儲存資料對照表
    r = json.loads(requests.get("https://reiwa.f5.si/maimai_official.json").content.decode("utf-8-sig")) #抓取日版官網資料
    for i in r:
        if i["catcode"] != "宴会場": #不抓宴譜
            if i["title"] not in songs: #檢查有沒有沒有缺的歌
                print(f"日服發現新歌：{i['title']}")
                songs[i["title"]] = {
        "artist": i.get("artist"), #作曲者
        "genre": i.get("genre"), #類別
        "version": off_ver(i.get("version")), #由官方版本號轉換為版本名稱
        "img": i.get("image_url"), #圖片保存位置
        "const": {}, #定數
        "unknown": {}, #是否未知
        "region": {"JP": False,"INT": False,"CN": False} #各版本收錄情況
        }
                for lv in i:
                    if lv.startswith("lev_") or lv.startswith("dx_lev_"): #抓歌曲難度
                        if i[lv].endswith("+"): #如果是+就默認.6
                            flv = float(i[lv][:-1])+0.6
                        else: #如果沒有就默認.0
                            flv = float(i[lv])
                        songs[i["title"]]["const"][off_lv[lv]] = flv
                        songs[i["title"]]["unknown"][off_lv[lv]] = 1 #官網抓取資料一律認定未知
                        print(f"{off_lv[lv]}: {i[lv]}")
            songs[i["title"]]["region"]["JP"] = True #標示日服有這首歌
    r = json.loads(requests.get("https://maimai.sega.com/assets/data/maimai_songs.json").content.decode("utf-8-sig")) #抓取國際版官網資料
    for i in r:
        if i["catcode"] != "宴会場": #不抓宴譜
            if i["title"] not in songs and i["catcode"] != "宴会場": #檢查有沒有沒有缺的歌
                print(f"國際版發現新歌：{i['title']}")
                songs[i["title"]] = {
        "artist": i.get("artist"), #作曲者
        "genre": i.get("genre"), #類別
        "version": off_ver(i.get("version")), #由官方版本號轉換為版本名稱
        "img": i.get("image_url"), #圖片保存位置
        "const": {}, #定數
        "unknown": {}, #是否未知
        "region": {"JP": False,"INT": False,"CN": False} #各版本收錄情況
        }
                for lv in i:
                    if lv.startswith("lev_") or lv.startswith("dx_lev_"): #抓歌曲難度
                        if i[lv].endswith("+"): #如果是+就默認.6
                            flv = float(i[lv][:-1])+0.6
                        else: #如果沒有就默認.0
                            flv = float(i[lv])
                        songs[i["title"]]["const"][off_lv[lv]] = flv
                        songs[i["title"]]["unknown"][off_lv[lv]] = 1 #官網抓取資料一律認定未知
                        print(f"{off_lv[lv]}: {i[lv]}")
            songs[i["title"]]["region"]["INT"] = True #標示國際版有這首歌
    r = json.loads(requests.get("https://raw.githubusercontent.com/CrazyKidCN/maimaiDX-CN-songs-database/refs/heads/main/maidata.json").content.decode("utf-8-sig")) #抓取中國版官網資料
    for i in r:
        if i["title"] != "Bad Apple!! feat nomico": #不抓重複曲
            if i["title"] not in songs: #檢查有沒有沒有缺的歌
                print(f"舞萌DX發現新歌：{i['title']}")
                songs[i["title"]] = {
        "artist": i.get("artist"), #作曲者
        "genre": i.get("category"), #類別
        "version": i.get("version"), #由官方版本號轉換為版本名稱
        "img": i.get("image_file"), #圖片保存位置
        "const": {}, #定數
        "unknown": {}, #是否未知
        "region": {"JP": False,"INT": False,"CN": False} #各版本收錄情況
        }
                for lv in i:
                    if lv.startswith("lev_") or lv.startswith("dx_lev_"): #抓歌曲難度
                        if i[lv].endswith("+"): #如果是+就默認.6
                            flv = float(i[lv][:-1])+0.6
                        else: #如果沒有就默認.0
                            flv = float(i[lv])
                        songs[i["title"]]["const"][off_lv[lv]] = flv
                        songs[i["title"]]["unknown"][off_lv[lv]] = 1 #官網抓取資料一律認定未知
                        print(f"{off_lv[lv]}: {i[lv]}")
            songs[i["title"]]["region"]["CN"] = True #標示中國版有這首歌
    with open("data/songs.json", "w", encoding="utf-8") as file:
        json.dump(songs, file, indent=4,ensure_ascii=False)
    return songs

def get():
    with open("data/songs.json") as file:
        return json.load(file)
