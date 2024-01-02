import os
from dotenv import load_dotenv
from telethon import events
from telethon.sync import TelegramClient
from telethon.tl.types import InputChannel
from olymp_trade_trading_signals import olymp_trade_trading_signals_handler, channel_username as olymp_channel_username
from pips_nations import pips_nations_handler, channel_username as pips_channel_username

# Load environment variables from the .env file
load_dotenv()

with TelegramClient('session_name', os.getenv("API_ID"), os.getenv("API_HASH")) as client:
    # Ensure you are logged in
    if not client.is_user_authorized():
        client.send_code_request(os.getenv("PHONE_NUMBER"))
        client.sign_in(os.getenv("PHONE_NUMBER"), input('Enter the code: '))

    # EUR/USD
    # Get the channel entity
    olymp_channel_entity = client.get_entity(olymp_channel_username)
    # Add an event handler for NewMessage events
    client.add_event_handler(olymp_trade_trading_signals_handler, events.NewMessage(chats=[olymp_channel_entity]))


    # GOLD
    # Get the channel entity
    pips_channel_entity = client.get_entity(pips_channel_username)
    # Add an event handler for NewMessage events
    client.add_event_handler(pips_nations_handler, events.NewMessage(chats=[pips_channel_entity]))

    # Run the client to listen for events
    client.run_until_disconnected()