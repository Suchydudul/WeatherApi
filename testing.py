import json
with open("output.json") as file:
    content = json.load(file)
    print(content["weather"])