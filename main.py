import requests
import pandas as pd
import os
import json

json_url = "https://raw.githubusercontent.com/the-fab-cube/flesh-and-blood-cards/develop/json/english/card.json"


def filter_card_json(card_data):
    card_list = []
    for card in card_data:
        card_data = {"name": "", "pitch": "", "images": []}
        card_data["name"] = card["name"]
        card_data["pitch"] = card["pitch"]
        for printing in card["printings"]:
            card_data["images"].append(printing["image_url"])

        card_list.append(card_data)

    return card_list


def download_card_json(json_url):
    # Download the file using requests
    response = requests.get(json_url)

    card_data = filter_card_json(response.json())

    # Check if download was successful (status code 200)
    if response.status_code == 200:
        # Open the file in write binary mode
        with open("card.json", "w") as f:
            json.dump(card_data, f)
        print("Download successful!")
    else:
        print(f"Download failed! Status code: {response.status_code}")


def get_card_json():
    # Check if the file exists
    if not os.path.isfile("card.json"):
        print("card.json not found. Downloading...")
        download_card_json(json_url)
    else:
        print("card.json already exists.")


def update_card_json():
    # Check if the file exists
    if os.path.isfile("card.json"):
        os.remove("card.json")

    download_card_json(json_url)


def testing():
    with open("card.json", "r", encoding="utf-8") as f:
        card_data = json.load(f)

    df = pd.json_normalize(card_data)

    print(df.head())


def testing1():
    with open("card.json", "r", encoding="utf-8") as f:
        card_data = json.load(f)

    card_list = []
    for card in card_data:
        card_data = {"name": "", "pitch": "", "images": []}
        card_data["name"] = card["name"]
        card_data["pitch"] = card["pitch"]
        for printing in card["printings"]:
            card_data["images"].append(printing["image_url"])

        card_list.append(card_data)
        break

    print(card_list)


download_card_json(json_url)
