import json
import pandas as pd
import time

raw_data = pd.read_json("JsonFiles/raw_decks.json", lines = True)
# Decklists = Commander: 7124, Standard: 6145, Modern: 3664

def mtg_search(deck_num, card_num, card_name):

    with open("JsonFiles/AtomicCards.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data["data"]

    if deck_num > 0:
        print(f"Deck {deck_num}")


    if card_name in cards:
        card_info = cards[card_name][0]
        print(card_num)
        print(card_info['name'])
        print(card_info.get("manaCost", "N/A"))
        print(card_info.get("colorIdentity"))
        print(card_info.get("text", ""))
        print(card_info.get("power"))
        print(card_info.get("toughness"))
        print(card_info.get("type"))
        print(card_info.get("loyalty"))
        print(card_info.get("relatedCards"))
        
    else:
        print("Not Found")
    


card_commander = raw_data[raw_data["format"] == "Commander"]
decklist_name = card_commander["Decklist"]


for deck_num, value in enumerate(decklist_name, start = 1): 
    for n in value:
        card_num = int(n["amount"])
        card_name = n["name"]
        
            
        mtg_search(deck_num, card_num, card_name)  
        deck_num = 0  
        time.sleep(1)

    
    


