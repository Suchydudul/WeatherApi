import json
with open("output.json") as file:
    content = json.load(file)
    weather_type = content["weather"][0]
    print(weather_type)