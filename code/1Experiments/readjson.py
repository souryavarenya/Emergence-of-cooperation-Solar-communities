import json

with open("meta.json") as myjson:
    mydict = json.loads(myjson.read())

print(mydict)
print(mydict["min_x"])
print(type(mydict["min_x"]))