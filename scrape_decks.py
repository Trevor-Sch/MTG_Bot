import httpx
from selectolax.parser import HTMLParser
import re
import json
import time
import random

def scrape_decks(start_page, end_page, output_file):

    base_url = "https://www.mtggoldfish.com/deck/{page_num}"


    for page_num in range(start_page, end_page + 1):
        url = base_url.format(page_num=page_num)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }
    
        try:
            resp = httpx.get(url, headers=headers, timeout = 10)
            resp.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch page {page_num}: {e}")
            continue
    
        html = HTMLParser(resp.text)

        # Grabbing the format, number of cards and card names from website
        deckformat = html.css_first("div.deck-container p")
        raw_input_amount = html.css_first("input#deck_input_deck")

        if not raw_input_amount:
            print(f"Skipping page {page_num} - deck input element not found")
            continue

        raw_input_value = raw_input_amount.attributes.get("value", None)

        if raw_input_value is None:
            print(f"Skipping page {page_num} - 'value' attribute not found in deck input")
            continue
            
        raw_input_amount = raw_input_value.splitlines()

        if not deckformat or not raw_input_amount:
            print(f"Skipping page {page_num} - deck data not found")
            continue

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
        with open(output_file, "a") as f:
            f.write(json.dumps(raw_data) + "\n")

        time.sleep(random.uniform(1, 5))  # Pausing so it wont stress the servers

    with open(output_file, "r") as f:
        decks = [json.loads(line) for line in f]

    print(f"Scraped {len(decks)} decks and saved to {output_file}")

scrape_decks(start_page = 7286011, end_page = 7286011+1999, output_file = "raw_decks.json")