import json

from pandas import DataFrame
from pybit.unified_trading import HTTP
import pandas as pd

def create_connection() -> HTTP:
    #main net
    # key = "1Ribli3TgGWq7qN5mG"
    # secret = "KlX1FIkiOuBdk0VWJnTXU0KqRCv8RtMzqyU5"
    #test net
    key = "ZKel6ndaPCuVJMlDuA"
    secret = "MGVSTNBQMLRaqN51XnxgfQ3ciNkkytCaziZd"
    session = HTTP(api_key=key, api_secret=secret, testnet=True)
    return session

def get_current_position() -> DataFrame:
    session = create_connection()
    response=session.get_positions(category="linear", settleCoin="USDT")
    print(response)
    result=format_data(response)
    print(result)
    return result

def format_data(response):
    if response.get('retCode') != 0:
        return
    result = response.get('result', None)
    if not result:
        return

    data = result.get('list', None)
    if not data:
        return

    data = pd.DataFrame(data,
        columns=[
            'symbol',
            'side',
            "createdTime",
            "leverage",
            "avgPrice",
            "markPrice",
            "positionValue",
            "unrealisedPnl"
        ],
        )

    return data
