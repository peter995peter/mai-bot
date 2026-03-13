import json
def get():
    with open("page.json") as file:
        return json.load(file)

def write(data):
    with open("page.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4,ensure_ascii=False)