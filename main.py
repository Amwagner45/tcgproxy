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


def parse_decklist():
    ## need to parse the given decklist and download each image
    decklist_json = {"Hero": "", "Weapons": [], "Equipment": [], "Deck": []}
    with open("example_decklist.txt", "r", encoding="UTF-8") as file:
        for line in file:
            line_stripped = line.strip()
            # print(line_stripped)
            if line_stripped.startswith("Hero"):
                decklist_json["Hero"] = line_stripped.split("Hero: ")[1]
            if line_stripped.startswith("Weapons"):
                decklist_json["Weapons"] = line_stripped.split("Weapons: ")[1].split(
                    ","
                )
            if line_stripped.startswith("Equipment"):
                decklist_json["Equipment"] = line_stripped.split("Equipment: ")[
                    1
                ].split(",")
            if line_stripped.startswith("("):
                deck_card_name = line_stripped.split(") ")[1].split(" (")[0]
                deck_card_pitch_name = (
                    line_stripped.split(") ")[1].split(" (")[1].split(")")[0]
                )
                if deck_card_pitch_name == "red":
                    deck_card_pitch = "1"
                elif deck_card_pitch_name == "yellow":
                    deck_card_pitch = "2"
                elif deck_card_pitch_name == "blue":
                    deck_card_pitch = "3"
                else:
                    deck_card_pitch = "error"

                decklist_json["Deck"].append(f"{deck_card_name} - {deck_card_pitch}")
    return decklist_json


if __name__ == "__main__":
    # download_card_json(json_url)
    decklist = parse_decklist()
    print(decklist)
    pass
