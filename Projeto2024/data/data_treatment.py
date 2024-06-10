import json
from icecream import ic

with open("tipos.json", "r", encoding='utf-8') as file:
    tipos = json.load(file)

with open("2024-04-14-DRE_dump.json", "r", encoding='utf-8') as file:
    data = json.load(file)

flag = False

for d in data:
    for key in tipos.keys():
        tipo = tipos[key]
        for t in tipo:
            if d["doc_type"] == t and key != "outros":
                d["doc_class"] = key
                flag = True
            elif d["doc_type"] == t:
                d["doc_class"] = t
            if flag:
                break
        if flag:
            break         
    flag = False

print(json.dumps(data))
