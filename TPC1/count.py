import json

f = open("plantas.json")
bd = json.load(f)
f.close()

print(bd.len())