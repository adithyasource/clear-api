import requests
from flask import Flask, jsonify
from flask import request
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

authToken = os.getenv("AUTH_TOKEN")

print(authToken)


@app.route("/", methods=["GET", "POST"])
def handleRequest():
    if not any(request.args.values()):
        return "hey there, how'd you end up here? this is the main website: https://clear.adithya.zip"

    if request.args.get("version"):
        response = jsonify({"clearVersion": "0.19.0"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.args.get("update"):
        response = jsonify(
            {
                "version": "v0.19.2",
                "notes": "Test version",
                "platforms": {
                    "windows-x86_64": {
                        "signature": "dW50cnVzdGVkIGNvbW1lbnQ6IHNpZ25hdHVyZSBmcm9tIHRhdXJpIHNlY3JldCBrZXkKUlVRVExQaEtudkVWaTl4VmNVNC9PQUw0dk9wZ09ua1ZramZ1Y2pYZTBROG9VTkk3NlJ4aWYwRlI0TDF5aXJxV21ocC9vRFRZMmI3bTUyVkxJRko3aTBKK3p3YUdVQmlHa2dBPQp0cnVzdGVkIGNvbW1lbnQ6IHRpbWVzdGFtcDoxNzA0MTc1MjUwCWZpbGU6Y2xlYXJfMC4xOS4yX3g2NC1zZXR1cC5uc2lzLnppcAovQ2NqYkk1TFJsMlFWd1krVnl5REVzMkRzemFjcnBmRnBXUEcxNFVIZlZ3RVMvUmExcjVzWVZqMnRhNmdoL1NFQUhrNWQ1NnplRmY3V1dOY1VBaTJEZz09Cg==",
                        "url": "https://github.com/adithyasource/clear/releases/download/testing-beta/clear_0.19.2_x64-setup.nsis.zip",
                    },
                },
            }
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.args.get("gameName"):
        gameName = str(request.args.get("gameName"))

        gameData = requests.get(
            f"https://www.steamgriddb.com/api/v2/search/autocomplete/{gameName}",
            headers={"Authorization": f"Bearer {authToken}"},
            timeout=30,
        ).content

        response = jsonify(json.loads(gameData))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.args.get("steamID"):
        steamID = str(request.args.get("steamID"))

        gameData = requests.get(
            f"https://www.steamgriddb.com/api/v2/games/steam/{steamID}",
            headers={"Authorization": f"Bearer {authToken}"},
            timeout=30,
        ).content

        response = jsonify(json.loads(gameData))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.args.get("image"):
        link = str(request.args.get("image"))

        imageFile = requests.get(
            link,
            timeout=30,
        )

        imageFileBytes = list(imageFile.content)

        response = jsonify({"image": imageFileBytes})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.args.get("assets"):
        gameID = str(request.args.get("assets"))

        gridImageLinks = []
        heroImageLinks = []
        logoImageLinks = []
        iconImageLinks = []

        gridImageData = json.loads(
            requests.get(
                f"https://www.steamgriddb.com/api/v2/grids/game/{gameID}",
                headers={"Authorization": f"Bearer {authToken}"},
                timeout=30,
            ).content
        )

        for x in gridImageData["data"]:
            gridImageLinks.append(x["thumb"])

        heroImageData = json.loads(
            requests.get(
                f"https://www.steamgriddb.com/api/v2/heroes/game/{gameID}",
                headers={"Authorization": f"Bearer {authToken}"},
                timeout=30,
            ).content
        )

        for x in heroImageData["data"]:
            heroImageLinks.append(x["thumb"])

        logoImageData = json.loads(
            requests.get(
                f"https://www.steamgriddb.com/api/v2/logos/game/{gameID}",
                headers={"Authorization": f"Bearer {authToken}"},
                timeout=30,
            ).content
        )

        for x in logoImageData["data"]:
            logoImageLinks.append(x["thumb"])

        iconImageData = json.loads(
            requests.get(
                f"https://www.steamgriddb.com/api/v2/icons/game/{gameID}",
                headers={"Authorization": f"Bearer {authToken}"},
                timeout=30,
            ).content
        )

        for x in iconImageData["data"]:
            iconImageLinks.append(x["thumb"])

        allImages = {
            "grids": gridImageLinks,
            "heroes": heroImageLinks,
            "logos": logoImageLinks,
            "icons": iconImageLinks,
        }

        response = jsonify(allImages)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.args.get("limitedAssets"):
        gameID = str(request.args.get("limitedAssets"))

        gridImageLinks = []
        heroImageLinks = []
        logoImageLinks = []
        iconImageLinks = []

        gridImageFileBytes = []
        heroImageFileBytes = []
        logoImageFileBytes = []
        iconImageFileBytes = []

        gridImageData = json.loads(
            requests.get(
                f"https://www.steamgriddb.com/api/v2/grids/game/{gameID}",
                headers={"Authorization": f"Bearer {authToken}"},
                timeout=30,
            ).content
        )

        if gridImageData["data"] != []:
            for x in gridImageData["data"]:
                gridImageLinks.append(x["thumb"])

            gridImageFile = requests.get(
                gridImageLinks[0],
                timeout=30,
            )
            gridImageFileBytes = list(gridImageFile.content)

        heroImageData = json.loads(
            requests.get(
                f"https://www.steamgriddb.com/api/v2/heroes/game/{gameID}",
                headers={"Authorization": f"Bearer {authToken}"},
                timeout=30,
            ).content
        )

        if heroImageData["data"] != []:
            for x in heroImageData["data"]:
                heroImageLinks.append(x["thumb"])
            heroImageFile = requests.get(
                heroImageLinks[0],
                timeout=30,
            )
            heroImageFileBytes = list(heroImageFile.content)

        logoImageData = json.loads(
            requests.get(
                f"https://www.steamgriddb.com/api/v2/logos/game/{gameID}",
                headers={"Authorization": f"Bearer {authToken}"},
                timeout=30,
            ).content
        )

        if logoImageData["data"] != []:
            for x in logoImageData["data"]:
                logoImageLinks.append(x["thumb"])
            logoImageFile = requests.get(
                logoImageLinks[0],
                timeout=30,
            )
            logoImageFileBytes = list(logoImageFile.content)

        iconImageData = json.loads(
            requests.get(
                f"https://www.steamgriddb.com/api/v2/icons/game/{gameID}",
                headers={"Authorization": f"Bearer {authToken}"},
                timeout=30,
            ).content
        )

        if iconImageData["data"] != []:
            for x in iconImageData["data"]:
                iconImageLinks.append(x["thumb"])
            iconImageFile = requests.get(
                iconImageLinks[0],
                timeout=30,
            )
            iconImageFileBytes = list(iconImageFile.content)

        allImages = {
            "grid": gridImageFileBytes,
            "hero": heroImageFileBytes,
            "logo": logoImageFileBytes,
            "icon": iconImageFileBytes,
        }

        response = jsonify(allImages)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return "hey there, how'd you end up here? this is the main website: https://clear.adithya.zip"


# command to run python -m flask run --debug --port 5002
