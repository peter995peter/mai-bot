import requests
import os
from bs4 import BeautifulSoup

clal = {'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36'}
userId = {'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36'}
def loginSid(): #使用帳號密碼登入
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36'}
    r = requests.get("https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/",headers=headers) #先取得JSESSIONID
    up = {"retention":1,"sid":os.getenv("MaiNet_User"),"password":os.getenv("MaiNet_Pass")} #設定帳號密碼
    headers["Cookie"] = r.headers["Set-Cookie"] #把獲取的JSESSIONID存進Cookie
    r = requests.post("https://lng-tgk-aime-gw.am-all.net/common_auth/login/sid/",data=up, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.text
    if title == "Login|maimai DX NET":
        print("登入失敗，請檢查帳號密碼是否正確")
        return False
    elif title == "maimai DX NET－Home－":
        print(f"已成功使用帳號密碼登入帳號{soup.select_one('div.name_block.f_l.f_16').text}")
        global clal, userId
        clal["Cookie"] = r.history[0].headers.get("Set-Cookie")
        userId = r.request.headers
        return True
    else:
        print(title)
        return False

def loginUid(): #使用clal登入
    r = requests.get("https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/",headers=clal)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.text
    if title == "Login|maimai DX NET":
        print("登入失敗，嘗試使用帳號密碼登入")
        return loginSid()
    elif title == "maimai DX NET－Home－":
        print(f"已成功使用clal登入帳號{soup.select_one('div.name_block.f_l.f_16').text}")
        global userId
        userId = r.request.headers
        return True
    else:
        print(title)
        return False

def get(url):
    r = requests.get(f"https://maimaidx-eng.com/maimai-mobile/{url}",headers=userId)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.text
    if title == "Login|maimai DX NET" or title == "maimai DX NET－Error－":
        print("取得網頁失敗，嘗試抓取clal登入")
        if loginUid():
            #print(userId)
            r = requests.get(f"https://maimaidx-eng.com/maimai-mobile/{url}",headers=userId)
        else:
            return False
    with open("out.html","w") as file:
        file.write(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.text
    if title == "Login|maimai DX NET" or title == "maimai DX NET－Error－":
        return False
    else:
        return soup

def addFriend(friend_code):
    if not(get("playerData")):
        return False
    for i in userId["Cookie"].split(";"):
        if i.startswith("_t"):
            token = i.split("=",1)[1]
    r = requests.post("https://maimaidx-eng.com/maimai-mobile/friend/search/invite/",headers=userId,data={"idx": str(friend_code),"token": token})
    return True

def getInfo(friend_code):
    soup = get(f"friend/friendGenreVs/?idx={friend_code}")
    if soup:
        if soup.title.text == "maimai DX NET－All Friend's－":
            return None
        else:
            return {"name": soup.select('div.p_l_5.t_l.f_l.f_12.f_b')[1].text, "rating": int(soup.select('div.rating_block')[1].text)}
    else:
        return None