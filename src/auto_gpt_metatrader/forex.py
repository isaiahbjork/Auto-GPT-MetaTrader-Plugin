import time
import schedule
import pandas as pd
from metaapi_cloud_sdk import MetaApi
import openai
import os
import requests
from dotenv import load_dotenv
import pytz
from datetime import datetime
load_dotenv()

# Set up OpenAI credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up MetaAPI credentials
token = os.getenv('META_API_TOKEN')
account_id = os.getenv('META_API_ACCOUNT_ID')

# Set time zone to New York
tz = pytz.timezone('America/New_York')

# Get current time in New York
now = datetime.now(tz)


def place_trade(account_id, symbol, signal, volume):
    signal = signal.upper()
    signal = signal.replace(".", "").strip()
    print(signal)
    # Get account information
    url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/account-information"
    headers = {
        "auth-token": token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response:
        response = response.json()
        global balance
        balance = response["balance"]
        global equity
        equity = response["equity"]
        global leverage
        leverage = response["leverage"]
        global margin
        margin = response["margin"]
        global free_margin
        free_margin = response["freeMargin"]

    else:
        print('Failed to get account information')
        return
    url2 = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/positions"
    headers = {
        "auth-token": token,
        "Content-Type": "application/json"
    }
    global positions
    positions = requests.get(url2, headers=headers)
    if positions:
        positions = positions.json()
    else:
        print('Failed to get positions')
        return

    # Check for existing open trade for the symbol
    matching_position = None
    for position in positions:
        if position['symbol'] == symbol:
            matching_position = position
            break

    if matching_position is not None:
        for position in positions:
            if position['symbol'] == symbol:
                if signal == 'BUY' and position['type'] == 'POSITION_TYPE_SELL':
                    # Close the existing trade
                    trade_data = {
                        'actionType': 'POSITION_CLOSE_ID',
                        'positionId': position['id']
                    }
                    url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
                    response = requests.post(
                        url, headers=headers, json=trade_data)
                    print(response.json())
                    if response:
                        print('Successfully closed existing trade')
                        # Place the new trade
                        trade_data = {
                            'symbol': symbol,
                            'actionType': 'ORDER_TYPE_BUY' if signal == 'BUY' else 'ORDER_TYPE_SELL',
                            'volume': volume,
                            'comment': 'TradeGPT',
                            'trailingStopLoss': {
                                'distance': {
                                    'distance': 40,
                                    'units': 'RELATIVE_POINTS'
                                },
                                'threshold': {
                                    'thresholds': [
                                        {
                                            'threshold': 0,
                                            'stopLoss': 0
                                        }
                                    ],
                                    'units': 'ABSOLUTE_PRICE',
                                    'stopPriceBase': 'CURRENT_PRICE'
                                }
                            }
                        }
                        headers = {
                            "auth-token": token,
                            "Content-Type": "application/json"
                        }
                        url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
                        response = requests.post(
                            url, headers=headers, json=trade_data)
                        if response:
                            print(
                                f"Successfully placed {signal} trade for {symbol}")
                        else:
                            print('Failed to place trade')

                    else:
                        print('Failed to close existing trade')
                        return
                elif signal == 'SELL' and position['type'] == 'POSITION_TYPE_BUY':
                    # Close the existing trade
                    trade_data = {
                        'actionType': 'POSITION_CLOSE_ID',
                        'positionId': position['id']
                    }
                    url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
                    headers = {
                        "auth-token": token,
                        "Content-Type": "application/json"
                    }
                    response = requests.post(
                        url, headers=headers, json=trade_data)
                    print(response.json())
                    if response:
                        print('Successfully closed existing trade')
                        # Place the new trade
                        trade_data = {
                            'symbol': symbol,
                            'actionType': 'ORDER_TYPE_BUY' if signal == 'BUY' else 'ORDER_TYPE_SELL',
                            'volume': volume,
                            'comment': 'TradeGPT',
                            'trailingStopLoss': {
                                'distance': {
                                    'distance': 40,
                                    'units': 'RELATIVE_POINTS'
                                },
                                'threshold': {
                                    'thresholds': [
                                        {
                                            'threshold': 0,
                                            'stopLoss': 0
                                        }
                                    ],
                                    'units': 'ABSOLUTE_PRICE',
                                    'stopPriceBase': 'CURRENT_PRICE'
                                }
                            }
                        }
                        headers = {
                            "auth-token": token,
                            "Content-Type": "application/json"
                        }
                        url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
                        response = requests.post(
                            url, headers=headers, json=trade_data)
                        print(response.json())
                        if response:
                            print(
                                f"Successfully placed {signal} trade for {symbol}")
                        else:
                            print('Failed to place trade')
                    else:
                        print('Failed to close existing trade')
                        return
                print("No trades need to be closed.")
    else:
        # Place the new trade
        trade_data = {
            'symbol': symbol,
            'actionType': 'ORDER_TYPE_BUY' if signal == 'BUY' else 'ORDER_TYPE_SELL',
            'volume': volume,
            'comment': 'TradeGPT',
            'trailingStopLoss': {
                'distance': {
                    'distance': 40,
                    'units': 'RELATIVE_POINTS'
                },
                'threshold': {
                    'thresholds': [
                        {
                            'threshold': 0,
                            'stopLoss': 0
                        }
                    ],
                    'units': 'ABSOLUTE_PRICE',
                    'stopPriceBase': 'CURRENT_PRICE'
                }
            }
        }
        headers = {
            "auth-token": token,
            "Content-Type": "application/json"
        }
        url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
        response = requests.post(url, headers=headers, json=trade_data)
        if response:
            print(f"Successfully placed {signal} trade for {symbol}")
        else:
            print('Failed to place trade')

# Define function to fetch candlestick data using requests library


def fetch_candlesticks(symbol, timeframe):
    url = f"https://mt-market-data-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/historical-market-data/symbols/{symbol}/timeframes/{timeframe}/candles?limit=15"
    headers = {
        "auth-token": token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response:
        candlesticks = response.json()
        return candlesticks
    else:
        return None


# Define OpenAI prompt template
prompt_template = "You are an expert hedge fund trader. You understand everything to make profitable trades based on OHLC data. Only using these 2 responses (BUY/SELL) do not give any other explanation or respond with numbers, You also know all the indicators and can calculate them based on the candlestick data provided that will help place winning trades. Should I open a trade based on the following candlestick data:\n{candlesticks}\n"

# Define pairs and timeframes to fetch
pairs = ["EURNZD", "EURUSD", "GBPUSD", "EURGBP",
         "USDCAD", "GBPNZD", "AUDCAD", "NZDUSD", "GBPJPY", "GBPCAD", "GBPAUD", "NZDJPY", "CADJPY", "EURCAD", "EURAUD"]
#
timeframe = "5m"

# Loop through each pair and timeframe


def run():
    try:
        url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/account-information"
        headers = {
            "auth-token": token,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response:
            response = response.json()
            global balance
            balance = response["balance"]
            global equity
            equity = response["equity"]
            global leverage
            leverage = response["leverage"]
            global margin
            margin = response["margin"]
            global free_margin
            free_margin = response["freeMargin"]
        url2 = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/positions"
        headers = {
            "auth-token": token,
            "Content-Type": "application/json"
        }
        global positions
        positions = requests.get(url2, headers=headers)
        if positions:
            positions = positions.json()
        else:
            print('Failed to get positions')
            return
        for pair in pairs:
            print(f"fetching {pair}")
            # Fetch candlestick data using requests library
            candlesticks = fetch_candlesticks(pair, timeframe)

            # If data was successfully fetched, process it and generate trade signal
            if candlesticks is not None:
                print(f"fetched candlestick data for {pair}")

                # Generate OpenAI prompt using template
                prompt = prompt_template.format(candlesticks=candlesticks)
                try:
                    # Call OpenAI API to generate response
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": f"You are TradeGPT, a sophisticated language model trained in the art of forex trading. You specialize in trading currency pairs on the foreign exchange market, using advanced technical analysis to make profitable trades that are in line with the prevailing trend. You understand that trading forex is a high-risk, high-reward endeavor, and you are experienced in managing risk and capitalizing on market opportunities. You have a proven track record of turning modest investments into substantial gains, using high leverage to maximize your returns. Currently, you are trading {pair} on the {timeframe} chart, constantly monitoring the market for trends and patterns that can help you make informed trading decisions. You know how to read candlestick OHLC data and use it to predict future price movements, and you are always on the lookout for new trading opportunities. When you open a trade on a symbol, you know that the opposite trade will be closed, and you rely on your knowledge and experience to make the right decisions at the right time. You do not use take profit or stop loss orders, preferring instead to manage your trades manually and adjust your positions as needed. Your current balance is {balance}, and you have ample margin and free margin to make profitable trades with a high degree of leverage. You understand that leverage is a double-edged sword, and you use it judiciously to maximize your profits while minimizing your risk. As a forex trading expert, you know that success in this market requires discipline, patience, and a deep understanding of market dynamics. You are always striving to improve your skills and refine your strategies, so that you can stay ahead of the curve and achieve your financial goals. Answer with only BUY or SELL when data is inputted nothing else. You have a current balance of {balance}, margin is {margin}, free margin is {free_margin}, leverage is {leverage} to 1. Here is the candle stick data: {candlesticks} \nCurrent date: 2023-04-03"},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=4,
                        stop=None,
                        n=1,
                        presence_penalty=0,
                        frequency_penalty=0
                    )
                    # Extract trading signal from API response
                    signal = response.choices[0].message.content
                except openai.Error as e:
                    print(f"OpenAI API Error: {e}")
                # Handle the error in an appropriate way
                except Exception as e:
                    print(f"Unexpected error: {e}")
                # Place trade based on signal
                if signal == "BUY":
                    place_trade(account_id, pair, "buy", 0.01)
                else:
                    place_trade(account_id, pair, "sell", 0.01)
    except:
        print("Error: rerunning...")
        run()


def close_all_trades():
    url2 = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/positions"
    headers = {
        "auth-token": token,
        "Content-Type": "application/json"
    }
    global positions

    positions = requests.get(url2, headers=headers)
    positions = positions.json()
    for position in positions:
        trade_data = {
            'actionType': 'POSITION_CLOSE_ID',
            'positionId': position['id']
        }
        url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
        response = requests.post(
            url, headers=headers, json=trade_data)
        if response:
            print(f"Successfully closed trade for {position['symbol']}")
        else:
            print(f"Failed to close trade for {position['symbol']}")


# Check if current time is within trading hours
if now.weekday() == 4 and now.hour == 15 and now.minute >= 50:
    # Run the function to close trades
    close_all_trades()
else:
    if now.weekday() < 5 and (now.hour >= 0 and now.hour < 16) and (now.hour < 15 or (now.hour == 15 and now.minute <= 55)):
        # Run the function
        run()
        # Schedule the function to run every 5 minutes
        schedule.every(5).minutes.do(run)
    else:
        print('Not within trading hours')


while True:
    schedule.run_pending()
    time.sleep(1)
