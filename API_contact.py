from pprint import pprint
import json
import requests


def getinfo(call):
    r = requests.get(call)
    return r.json()


name = "baseballaholic"
uuid = "14552d0d4cb949b59d4f7d1875b0ad94"
uuid_dashed = "14552d0d-4cb9-49b5-9d4f-7d1875b0ad94"
API_KEY = "deb9e086-d418-42f8-9de5-03676d1f98d9"

name_link = f"https://api.hypixel.net/player?key={API_KEY}&name={name}"
uuid_link = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid_dashed}"

pprint(getinfo(name_link))
