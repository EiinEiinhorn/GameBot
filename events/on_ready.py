import os
import json


def removeRequests():

    for filename in os.listdir("serverData"):
        with open(f"serverData/{filename}", "r", encoding="UTF-8") as file:
            serverFile = json.load(file)

            if "currentRequests" in serverFile:
                del serverFile["currentRequests"]
            serverFile["CurrentRequests"] = {}

            with open(f"serverData/{filename}", "w", encoding="UTF-8") as file:
                file.write(json.dumps(serverFile))


def run():
    removeRequests()