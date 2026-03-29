import requests
import os
from bs4 import BeautifulSoup
import time
import json
headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36'}
session = requests.Session()

def loginSid(): #使用帳號密碼登入
    r = session.get("https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/",headers=headers) #先取得JSESSIONID
    up = {"retention":1,"sid":os.getenv("MaiNet_User"),"password":os.getenv("MaiNet_Pass")} #設定帳號密碼
    r = session.post("https://lng-tgk-aime-gw.am-all.net/common_auth/login/sid",data=up, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    sc = r.status_code
    if sc == 200:
        print(f"已成功使用帳號密碼登入帳號{soup.select_one('div.name_block.f_l.f_16').text}")
        return True
    elif sc == 500:
        print("登入失敗，請檢查帳號密碼是否正確")
        return False
    else:
        print(sc)
        return False

def loginUid(): #使用clal登入
    r = session.get("https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/",headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.text
    if title == "Login":
        print("登入失敗，嘗試使用帳號密碼登入")
        return loginSid()
    elif title == "maimai DX NET－Home－":
        print(f"已成功使用clal登入帳號{soup.select_one('div.name_block.f_l.f_16').text}")
        return True
    else:
        print(title)
        return False

def get(url):
    r = session.get(f"https://maimaidx-eng.com/maimai-mobile/{url}",headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.text
    if title == "Login|maimai DX NET" or title == "maimai DX NET－Error－":
        print("取得網頁失敗，嘗試抓取clal登入")
        if loginUid():
            r = session.get(f"https://maimaidx-eng.com/maimai-mobile/{url}",headers=headers)
        else:
            return False
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.text
    if title == "Login|maimai DX NET" or title == "maimai DX NET－Error－":
        return False
    else:
        return soup

def addFriend(friend_code):
    if not(get("playerData")):
        return False
    token = session.cookies.get("_t",domain="maimaidx-eng.com")
    r = session.post("https://maimaidx-eng.com/maimai-mobile/friend/search/invite/",headers=headers,data={"idx": str(friend_code),"token": token})
    return True

def getInfo(friend_code):
    soup = get(f"friend/friendGenreVs/?idx={friend_code}")
    if soup:
        if soup.title.text == "maimai DX NET－All Friend's－":
            return None
        else:
            icon = soup.select('img.h_55.f_l')[1]["src"]
            return {"name": soup.select('div.p_l_5.t_l.f_l.f_12.f_b')[1].text, "rating": int(soup.select('div.rating_block')[1].text),"icon": icon}
    else:
        return {"name": "未知", "rating": -1,"icon": "https://http.cat/404"}

def newCache(name,data,et):
    data = {"start": time.time(), "expired": time.time()+et, "data": data}
    with open(f"data/cache/{name}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4,ensure_ascii=False)

def getScore(id,diff):
    print(f"開始抓取{id} {diff}")
    diff = {"BASIC":0,"ADVANCED":1,"EXPERT":2,"MASTER":3,"Re:MASTER":4}[diff]
    if os.path.exists(f"data/cache/{id}_{diff}.json"):
        print("發現cache")
        with open(f"data/cache/{id}_{diff}.json") as file:
            data = json.load(file)
        if time.time() > data["expired"]:
            print("cache已過期，繼續抓取網頁")
            os.remove(f"data/cache/{id}_{diff}.json")
        else:
            print("cache未過期，使用cache")
            return data["data"]
    soup = get(f"friend/friendGenreVs/battleStart/?scoreType=2&genre=99&diff={diff}&idx={id}")
    if not soup:
        return False
    else:
        data = {}
        diff2 = ["basic","advanced","expert","master","remaster"][diff]
        for i in soup.select(f"div.music_{diff2}_score_back"):
            music_name = i.select_one("div.music_name_block").text
            data[music_name] = []
            dx = i.select_one("img.music_kind_icon")["src"] == "https://maimaidx-eng.com/maimai-mobile/img/music_dx.png"
            acc = i.select(f"td.{diff2}_score_label")[1].get_text(strip=True).replace("%", "")
            if acc != "― ":
                data[music_name].append({"dx":dx,"acc": float(acc)})
        newCache(f"{id}_{diff}",data,3600) #緩存1小時
        print(f"完成抓取{id} {diff}")
        return data
