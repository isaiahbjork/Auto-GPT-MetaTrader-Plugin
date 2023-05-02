import requests
import os

account_id = os.getenv('META_API_ACCOUNT_ID')
token = os.getenv("META_API_TOKEN")
region = os.getenv("META_API_REGION")

class Trading():
    def fetch_candlesticks(symbol, timeframe):
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

        url = f"https://mt-market-data-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/historical-market-data/symbols/{symbol}/timeframes/{timeframe}/candles?limit=15"
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

    

    def close_trade(position_id) -> None:
        trade_data = {
            'actionType': 'POSITION_CLOSE_ID',
            'positionId': position_id
        }
        headers = {
            "auth-token": token,
            "Content-Type": "application/json"
        }
        url = f"https://mt-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
        response = requests.post(
            url, headers=headers, json=trade_data)
        response = response.json()
        return response

    def close_all_trades():
        url2 = f"https://mt-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/positions"
        headers = {
            "auth-token": token,
            "Content-Type": "application/json"
        }
        positions = requests.get(url2, headers=headers)
        positions = positions.json()
        responses = []
        for position in positions:
            trade_data = {
                'actionType': 'POSITION_CLOSE_ID',
                'positionId': position['id']
            }
            url = f"https://mt-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
            response = requests.post(
                url, headers=headers, json=trade_data)
            if response:
                print(f"Successfully closed trade for {position['symbol']}")
            else:
                print(f"Failed to close trade for {position['symbol']}")
            if response:
                responses.append(f"Successfully closed trade for {position['symbol']}")
            else:
                responses.append(f"Failed to close trade for {position['symbol']}")

        if responses:
            return responses
        else:
            return f'No trades to close.'

    def get_positions():
        url2 = f"https://mt-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/positions"
        headers = {
            "auth-token": token,
            "Content-Type": "application/json"
        }
        positions = requests.get(url2, headers=headers)
        if positions:
            positions = positions.json()
            return positions
        else:
            return f'Failed to get positions'

    def get_account_information():
        url = f"https://mt-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/account-information"
        headers = {
            "auth-token": token,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response:
            response = response.json()
            return response
        else:
            return f'Failed to get account information'

    def place_trade(symbol, volume, signal) -> None:
        signal = signal.upper()
        symbol = symbol.upper()
        # Place the new trade
        if signal == 'BUY':
            trade_data = {
                'symbol': symbol,
                'actionType': 'ORDER_TYPE_BUY',
                'volume': float(volume),
                'comment': 'Auto-GPT MetaTrader Plugin'
            }
            headers = {
                "auth-token": token,
                "Content-Type": "application/json"
            }
            url = f"https://mt-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
            response = requests.post(url, headers=headers, json=trade_data)

            response = response.json()
            return response

        elif signal == 'SELL':
            trade_data = {
                'symbol': symbol,
                'actionType': 'ORDER_TYPE_SELL',
                'volume': float(volume),
                'comment': 'Auto-GPT MetaTrader Plugin'
            }
            headers = {
                "auth-token": token,
                "Content-Type": "application/json"
            }
            url = f"https://mt-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
            response = requests.post(url, headers=headers, json=trade_data)

            response = response.json()
            return response