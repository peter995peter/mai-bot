import json

def Get():
    with open("data/link.json") as file:
        return json.load(file)

def Write(data):
    with open("data/link.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4,ensure_ascii=False)

def DidToMid(Did): #Discord ID 轉換為 maimai DX NET 好友代碼
    data = Get()
    if str(Did) in data:
        return data[str(Did)]
    else:
        return None
