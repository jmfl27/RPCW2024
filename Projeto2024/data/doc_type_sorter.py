import json
from icecream import ic

with open("2024-04-14-DRE_dump.json", "r", encoding='utf-8') as file:
    content = json.load(file)

types = set()

for c in content:
    types.add(c["doc_type"])

types = list(types)
types.sort()

print({"types": types})
#ic(len(types))