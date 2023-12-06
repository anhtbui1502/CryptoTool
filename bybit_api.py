import json
from pybit.unified_trading import HTTP

def create_connection() -> HTTP:
    #main net
    # key = "1Ribli3TgGWq7qN5mG"
    # secret = "KlX1FIkiOuBdk0VWJnTXU0KqRCv8RtMzqyU5"
    #test net
    key = "ZKel6ndaPCuVJMlDuA"
    secret = "MGVSTNBQMLRaqN51XnxgfQ3ciNkkytCaziZd"
    session = HTTP(api_key=key, api_secret=secret, testnet=True)
    return session

def get_current_position():
    session = create_connection()
    print(session.get_positions(category="linear", settleCoin="USDT"))