import re
import requests
import random
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

channel_username = 'Pips_nations'
server_url = os.getenv("SERVER_URL")

async def pips_nations_handler(event):

# Extract text from the incoming message
    message_text = event.message.text
   # Define regular expressions to extract information
    pair_pattern = re.compile(r'PAIR :(.+)', re.IGNORECASE)
    position_pattern = re.compile(r'POSITION: (\w+)', re.IGNORECASE)
    entry_pattern = re.compile(r'ENTRY :(\d+)', re.IGNORECASE)
    sl_pattern = re.compile(r'S/L :(\d+)', re.IGNORECASE)
    tp1_pattern = re.compile(r'TP1 - (\d+)', re.IGNORECASE)
    tp2_pattern = re.compile(r'TP2 - (\d+)', re.IGNORECASE)
    tp3_pattern = re.compile(r'TP3 - (\d+)', re.IGNORECASE)
    tp4_pattern = re.compile(r'TP4 -(\d+)', re.IGNORECASE)

    # Use regular expressions to extract information from the message
    pair_match = pair_pattern.search(message_text)
    position_match = position_pattern.search(message_text)
    entry_match = entry_pattern.search(message_text)
    sl_match = sl_pattern.search(message_text)
    tp1_match = tp1_pattern.search(message_text)
    tp2_match = tp2_pattern.search(message_text)
    tp3_match = tp3_pattern.search(message_text)
    tp4_match = tp4_pattern.search(message_text)

    # Initialize action variable
    action = None

    # Check if matches are found and set the action variable
    if position_match and pair_match:
        print(f"New message in {event.chat_id}: {message_text}")
        position = position_match.group(1).lower()

        if 'short' in position:
            action = 'Sell'
        elif 'long' in position:
            action = 'Buy'
        else:
            action = "Unknown"

        # Print the extracted information
        if pair_match:
            print(f"Pair: {pair_match.group(1)}")
            pair = pair_match.group(1)
        if position_match:
            print(f"Position: {position_match.group(1)} (Action: {action})")
        if entry_match:
            print(f"Entry: {entry_match.group(1)}")
            entry = entry_match.group(1)
        if sl_match:
            print(f"S/L: {sl_match.group(1)}")
            sl = sl_match.group(1)
        if tp1_match:
            print(f"TP1: {tp1_match.group(1)}")
            tp1 = tp1_match.group(1)
        if tp2_match:
            print(f"TP2: {tp2_match.group(1)}")
            tp2 = tp2_match.group(1)
        if tp3_match:
            print(f"TP3: {tp3_match.group(1)}")
            tp3 = tp3_match.group(1)
        if tp4_match:
            print(f"TP4: {tp4_match.group(1)}")
            tp4 = tp4_match.group(1)

        # Generate a random 9-digit ID
        random_id = str(random.randint(100000000, 999999999))
        # Prepare JSON data
        json_data = {
            #'chat_id': event.chat_id,
            #'message_text': message_text,
            "id": random_id,
            "user_id": "1",
            "instrument": pair,
            "direction":action,
            "entry_type":"Market",
            "entry_value": entry,
            "stop_loss": sl,
            "take_profit":tp1,
            "take_profit2":tp2,
            "status":"1",
            "comment":f"Telegram tp3={tp3} tp4={tp4}"
        }

        # Send a POST request to the server
        response = requests.post(server_url, json=json_data)

        # Check the response status
        if response.status_code == 200:
            print("POST request successful")
        else:
            print(f"POST request failed with status code: {response.status_code}")

       # Send a POST request to the server for TP2
        json_data['take_profit'] = tp2
        tp2Request = requests.post(server_url, json=json_data)

        # Check the response status
        if tp2Request.status_code == 200:
            print("TP2 POST request successful")
        else:
            print(f"TP2 POST request failed with status code: {tp2Request.status_code}")

    else:
        print(f"New message in {event.chat_id}: {message_text}")
        print("No action detected")