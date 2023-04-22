# MetaTrader
import requests
import os
import numpy as np

account_id = os.getenv('META_API_ACCOUNT_ID')
token = os.getenv("META_API_TOKEN")

def fetch(symbol, timeframe):
        symbol = symbol.replace('/', '')
        symbol = symbol.upper()
        timeframe_map = {
            "1 minute": "1m",
            "1 min": "1m",
            "1min": "1m",
            "5 minutes": "5m",
            "5 min": "5m",
            "5min": "5m",
            "15 minutes": "15m",
            "15 min": "15m",
            "15min": "15m",
            "30 minutes": "30m",
            "30 min": "30m",
            "30min": "30m",
            "1 hour": "1h",
            "4 hours": "4h",
            "1 day": "1d",
            "1 week": "1w",
            "1 month": "1m"
        }
        # Check if the user input matches any of the keys in the dictionary
        if timeframe in timeframe_map:
            timeframe = timeframe_map[timeframe]
        else:
            # Assume that the user input is already in the correct format
            pass

        url = f"https://mt-market-data-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/historical-market-data/symbols/{symbol}/timeframes/{timeframe}/candles?limit=1000"
        headers = {
            "auth-token": token,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response:
            candlesticks = response.json()
            return candlesticks
        else:
            return 'Failed to get candlesticks.'