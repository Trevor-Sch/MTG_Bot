import json
import pandas as pd
import re

raw_data = pd.read_json("JsonFiles/raw_decks.json", lines = True)
# Decklists = Commander: 7124, Standard: 6145, Modern: 3664

def mtg_search(decklist):

    with open("JsonFiles/AtomicCards.json", "r", encoding="utf-8") as f:
        data = json.load(f)


    cards = data["data"]
    enriched_decks = {
         "deckNum": deck_num,
         "cards": []
    }
        
        
    for n in decklist:
        card_num = int(n["amount"])
        card_name = n["name"]

        if card_name in cards:
            card_info = cards[card_name][0]

            manaCost = parse_mana_cost(card_info.get("manaCost", "N/A"))

            enriched_decksInfo = {
                "cardAmount": card_num,
                "cardName": card_info['name'],
                "cardInfo": {
                    "manaCost": manaCost,
                    "colorIdentity": card_info.get("colorIdentity"),
                    "text": card_info.get("text", ""),
                    "power": int(card_info.get("power")) if card_info.get("power") is not None else 0,
                    "toughness": int(card_info.get("toughness")) if card_info.get("toughness") is not None else 0,
                    "type": card_info.get("type", ""),
                    "loyalty": int(card_info.get("loyalty")) if card_info.get("loyalty") is not None else 0,
                    "relatedCards": card_info.get("relatedCards") or []
                }
            }


            enriched_decks["cards"].append(enriched_decksInfo)
    return enriched_decks
     

    

def parse_mana_cost(mana_cost):
    colors = ["W", "U", "B", "R", "G"]
    flags = {c: 0 for c in colors}
    flags["C"] = 0
    flags["generic"] = 0

    if mana_cost != "N/A":
        symbols = re.findall(r"{.*?}", mana_cost)

        for sym in symbols:
            sym = sym.strip("{}")

            if sym in colors:
                flags[sym] += 1

            elif sym == "C":
                flags["C"] += 1

            elif sym.isdigit():
                flags["generic"] += int(sym)

    return flags
            
    







card_commander = raw_data[raw_data["format"] == "Commander"]
decklist_name = card_commander["Decklist"]
alldecks = []

for deck_num, decklist in enumerate(decklist_name, start = 1):
    alldecks.append(mtg_search(decklist))
    percentage_left = 100 * (deck_num/7124)

    if deck_num % 100 == 0:
        print(f"Percentage remaining: {100 - percentage_left:.2f}%")
    
    #if deck_num > 5:
    #    break

    
with open("JsonFiles/enriched_decks.json", "a") as f:
        json.dump(alldecks, f, indent = 4)   


