import re
import requests
import random
import time
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

server_url = os.getenv("SERVER_URL")
channel_username = 'Olymp_Trade_Trading_Signals'


async def olymp_trade_trading_signals_handler(event):

 # Extract the text from the message
    message_text = event.message.text

    # Define a regular expression pattern to match "And we're gonna put" and "DOWN" or "UP"
    pattern = re.compile(r'And we\'re gonna put[\s\S]*?(DOWN|UP)')

    #over the counter
    otc_pattern = re.compile(r'\(OTC\)')

    # Search for the pattern in the message text
    match = pattern.search(message_text)
    otc_match = otc_pattern.search(message_text)

    # Check if a match is found
    if match and not otc_match:
        action = match.group(1)
        print(f"New message in {event.chat_id}: {message_text}")
        print(f"Action: {action}")

          # Translate "UP" to "Buy" and "DOWN" to "Sell"
        if action == "UP":
            translated_action = "Buy"
        elif action == "DOWN":
            translated_action = "Sell"
        else:
            translated_action = "Unknown"

        print(f"Translated Action: {translated_action}")
        # Generate a random 9-digit ID
        random_id = str(random.randint(100000000, 999999999))
        # Prepare JSON data
        json_data = {
            #'chat_id': event.chat_id,
            #'message_text': message_text,
            "id": random_id,
            "user_id": "1",
            "instrument":"EURUSD",
            "direction":translated_action,
            "entry_type":"Market",
            "status":"1",
            "comment":"Telegram"
        }

        # Send a POST request to the server
        response = requests.post(server_url, json=json_data)

        # Check the response status
        if response.status_code == 200:
            print("POST request successful")

             # Introduce a 5-minute delay (300 seconds)
            time.sleep(300)

            # Send a PUT request after the delay
            json_data['status'] = '0'
            put_response = requests.put(server_url + f'/{random_id}', json=json_data)  # Modify the endpoint as needed

            # Check the PUT request status
            if put_response.status_code == 200:
                print("PUT request successful")
            else:
                print(f"PUT request failed with status code: {put_response.status_code}")
        else:
            print(f"POST request failed with status code: {response.status_code}")

    else:
        print(f"New message in {event.chat_id}: {message_text}")
        print("No action detected")