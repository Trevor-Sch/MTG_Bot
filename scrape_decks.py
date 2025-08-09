import httpx
from selectolax.parser import HTMLParser
import re
import json

url = "https://www.mtggoldfish.com/archetype/standard-izzet-cauldron-woe#paper"
headers = {"User-Agent": ""}

resp = httpx.get(url, headers=headers)
html = HTMLParser(resp.text)

# Grabbing the format, number of cards and card names from website
deckformat = html.css_first("div.deck-container p")
raw_input_amount = html.css_first("input#deck_input_deck")

raw_input_amount = raw_input_amount.attributes.get("value", "").splitlines()

# Formatting text for deck format
deck_format_text = deckformat.text(strip=True)
deck_format_text = deck_format_text.replace("Format:", "").strip()                       
deck_format_text = re.findall(r'[A-Z][a-z]*', deck_format_text)[0]        # reads tbe groupings of words with CAPITAL LETTERs then removes all but the first word

mainboard = []
sideboard = []
current = mainboard

# strips each line of text then splits the numbers and names up to pair them back (that way the stored data will be easier to read)
for line in raw_input_amount:
    line = line.strip()

    if not line:
        continue
    if line.lower() == "sideboard":
        current = sideboard
        continue

    parts = line.split()
    amount = int(parts[0])
    name = " ".join(parts[1:])
    current.append({"amount": amount, "name": name})


# Stores the raw data in a json file
raw_data = {
    "format": deck_format_text,
    "Decklist": mainboard,
    "SideBoard": sideboard
}

# Sends raw data to json file for sorting later
with open("raw_decks.json", "w") as f:
    json.dump(raw_data, f, indent=2)
