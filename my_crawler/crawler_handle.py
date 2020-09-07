# headers
a = """"""
import json
tmp = {}
for i in a.split("\n"):
    tmp[i.split(":")[0].strip()] = i.split(":")[1].strip()
print(json.dumps(tmp, indent=True))
