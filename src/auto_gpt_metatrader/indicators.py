import numpy as np
import pandas as pd
import requests
import os
from ta.utils import dropna
from ta.momentum import RSIIndicator, StochasticOscillator, TSIIndicator
from ta.trend import SMAIndicator, EMAIndicator, WMAIndicator, MACD, ADXIndicator
from ta.volume import AccDistIndexIndicator, MFIIndicator

account_id = os.getenv('META_API_ACCOUNT_ID')
token = os.getenv("META_API_TOKEN")
region = os.getenv("META_API_REGION")


class Indicators():
    def fetch(symbol, timeframe):
        symbol = symbol.replace('/', '')
        symbol = symbol.upper()
        timeframe_map = {
            "1 minute": "1m",
            "1 min": "1m",
            "1min": "1m",
            "M1": "1m",
            "5 minutes": "5m",
            "5 min": "5m",
            "5min": "5m",
            "M5": "1m",
            "15 minutes": "15m",
            "15 min": "15m",
            "15min": "15m",
            "M15": "15m",
            "30 minutes": "30m",
            "30 min": "30m",
            "30min": "30m",
            "M30": "30m",
            "1 hour": "1h",
            "1hour": "1h",
            "1hr": "1h",
            "H1": "1h",
            "4 hours": "4h",
            "4hours": "4h",
            "4 hrs": "4h",
            "H4": "4h",
            "1 day": "1d",
            "1day": "1d",
            "D1": "1d",
            "1 week": "1w",
            "1week": "1w",
            "W1": "1w",
            "1 month": "1mn",
            "1month": "1mn",
            "M1": "1mn"

        }
        # Check if the user input matches any of the keys in the dictionary
        if timeframe in timeframe_map:
            timeframe = timeframe_map[timeframe]
        else:
            # Assume that the user input is already in the correct format
            pass

        url = f"https://mt-market-data-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/historical-market-data/symbols/{symbol}/timeframes/{timeframe}/candles?limit=100"
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

    def money_flow_index(candlesticks, period):
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['high', 'low', 'close', 'tickVolume'])
            # Clean NaN values
            df = dropna(df)
            
            mfi = MFIIndicator(df['high'], df['low'], df['close'], volume=df['tickVolume'], window=int(20))
            return f'Current MFI Value: {mfi.money_flow_index().iloc()[-1]}'
        else:
            return f'Failed to get candlesticks'

    def volume(candlesticks):
        if candlesticks:
            volumes = [float(candlestick['tickVolume']) for candlestick in candlesticks]
            return np.sum(volumes[-14:])
        else:
            return f'Failed to get candlesticks'

    def rsi(candlesticks, period):
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['close'])
            # Clean NaN values
            df = dropna(df)
            rsi_indicator = RSIIndicator(df['close'], window=float(period))
            current_rsi = rsi_indicator.rsi().iloc[-1]
            return f'Current RSI Value: {current_rsi}'

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Simple Moving Average (SMA)

    def sma(candlesticks, period):
        # Get the candlesticks data
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['close'])
            df = dropna(df)
            sma = SMAIndicator(df['close'], window=float(period))
            return f'Current Simple Moving Average Value: {sma.sma_indicator().iloc()[-1]}'

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Exponential Moving Average (EMA)
    def ema(candlesticks, period):
        # Get the candlesticks data
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['close'])
            df = dropna(df)
            ema = EMAIndicator(df['close'], window=float(period))
            return f'Current Exponential Moving Average Value: {ema.ema_indicator().iloc()[-1]}'

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Weighted Moving Average (WMA)
    def wma(candlesticks, period):
        # Get the candlesticks data
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['close'])
            df = dropna(df)
            wma = WMAIndicator(df['close'], window=float(period))
            return f'Current Weighted Moving Average Value: {wma.wma_indicator().iloc()[-1]}'

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Moving Average Convergence Divergence (MACD)
    def macd(candlesticks, fast_period, slow_period, signal_period):
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['close'])
    # Clean NaN values
            df = dropna(df)
            # Calculate the RSI values
            macd = MACD(df['close'], window_slow=int(
                        12), window_fast=int(26), window_sign=int(9))
            signal_line = macd.macd_signal().iloc()[-1]
            macd_line = macd.macd().iloc()[-1]
            macd_diff = macd.macd_diff().iloc()[-1]
            macd_values = {"macd_line": macd_line, 'macd_diff': macd_diff, 'signal_line': signal_line}
            return f'Current MACD Values: {macd_values}'
        
        if not candlesticks:
            return f'Failed to get candlesticks'

    # Average Directional Movement Index (ADX)
    def adx(candlesticks, period):
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['high', 'low', 'close'])
            # Clean NaN values
            df = dropna(df)
            # Calculate the RSI values
            adx = ADXIndicator(df['high'], df['low'], df['close'], window=int(period))
            return f' Current Average Directional Movement Index Value: {adx.adx().iloc()[-1]}'

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Accumulation/Distribution Index (ADI)
    def adi(candlesticks):
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['high', 'low', 'close', 'tickVolume'])
            # Clean NaN values
            df = dropna(df)
            adi = AccDistIndexIndicator(df['high'], df['low'], df['close'], volume=df['tickVolume'])
            return f'Current Accumulation/Distribution Index: {adi.acc_dist_index().iloc()[-1]}'

        if not candlesticks:
            return f'Failed to get candlesticks'

    def fib_retracements(candlesticks, high, low):
        high = float(high)
        low = float(low)
        levels = [0.236, 0.382, 0.5, 0.618, 0.786]
        diff = high - low
        retracements = []
        for level in levels:
            retracements.append(high - level * diff)
        return f'Current Fibonacci Retracements are: {retracements}'

    # Stochastic Oscillator
    def stochastic_oscillator(candlesticks, period, smooth_period):
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['high', 'low', 'close'])
            # Clean NaN values
            df = dropna(df)
            # Calculate the RSI values
            stotch = StochasticOscillator(
                df['high'], df['low'], df['close'], window=int(period), smooth_window=int(smooth_period))
            return f'Current Stochastic Oscillator value is: {stotch.stoch().iloc()[-1]}'

        if not candlesticks:
            return f'Failed to get candlesticks'

    # True Strength Index
    def tsi(candlesticks, slow_period, fast_period):
        if candlesticks:
            df = pd.DataFrame(candlesticks, columns=['close'])
            # Clean NaN values
            df = dropna(df)
            # Calculate the RSI values
            tsi = TSIIndicator(df['close'], window_slow=int(slow_period), window_fast=int(fast_period))
            return f'Current True Strength Index value is: {tsi.tsi().iloc()[-1]}'

        if not candlesticks:
            return f'Failed to get candlesticks'
