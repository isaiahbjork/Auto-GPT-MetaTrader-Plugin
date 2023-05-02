import numpy as np
import pandas as pd
import requests
import os
from ta.utils import dropna
from ta.momentum import rsi, stoch_signal, tsi
from ta.trend import sma_indicator, ema_indicator, wma_indicator, macd_signal, adx
from ta.volume import acc_dist_index, money_flow_index

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
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            mfiv = []
            mfi_value = money_flow_index(
                df['high'], df['low'], df['close'], df['tickVolume'], window=int(period))
            mfi_value = pd.DataFrame(mfi_value)
            mfi_value = mfi_value.dropna()
            for v in mfi_value:
                mfiv.append(v)
            return mfiv

        if not candlesticks:
            return f'Failed to get candlesticks'

    def volume(candlesticks):
        if candlesticks:
            volumes = [float(candlestick['tickVolume']) for candlestick in candlesticks]
            return np.sum(volumes[-14:])
        else:
            return f'Failed to get candlesticks'

    def rsi(candlesticks, period):
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            rsiv = []
            rsi_value = rsi(df['close'], window=int(period))
            rsi_value = rsi_value.dropna()
            for v in rsi_value:
                rsiv.append(v)
            return rsiv

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Simple Moving Average (SMA)

    def sma(candlesticks, period):
        # Get the candlesticks data
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            smav = []
            sma_value = sma_indicator(df['close'], window=int(period))
            sma_value = sma_value.dropna()
            for v in sma_value:
                smav.append(v)
            return smav

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Exponential Moving Average (EMA)
    def ema(candlesticks, period):
        # Get the candlesticks data
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            emav = []
            ema_value = ema_indicator(df['close'], window=int(period))
            ema_value = ema_value.dropna()
            for v in ema_value:
                emav.append(v)
            return emav

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Weighted Moving Average (WMA)
    def wma(candlesticks, period):
        # Get the candlesticks data
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            wmav = []
            wma_value = wma_indicator(df['close'], window=int(period))
            wma_value = wma_value.dropna()
            for v in wma_value:
                wmav.append(v)
            return wmav

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Moving Average Convergence Divergence (MACD)
    def macd(candlesticks, fast_period, slow_period, signal_period):
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            macdv = []
            macd_value = macd_signal(df['close'], window_slow=int(
                slow_period), window_fast=int(fast_period), window_sign=int(signal_period))
            macd_value = macd_value.dropna()
            for v in macd_value:
                macdv.append(v)
            return macdv

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Average Directional Movement Index (ADX)
    def adx(candlesticks, period):
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            adxv = []
            adx_value = adx(df['high'], df['low'], df['close'], window=int(period))
            adx_value = adx_value.dropna()
            for v in adx_value:
                adxv.append(v)
            return adxv

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Accumulation/Distribution Index (ADI)
    def adi(candlesticks):
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            adiv = []
            adi_value = acc_dist_index(
                df['high'], df['low'], df['close'], df['tickVolume'])
            adi_value = adi_value.dropna()
            for v in adi_value:
                adiv.append(v)
            return adiv

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
        return retracements

     # Stochastic Oscillator
    def stochastic_oscillator(candlesticks, period, smooth_period):
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            stoch = []
            stoch_value = stoch_signal(
                df['high'], df['low'], df['close'], window=int(period), smooth_window=int(smooth_period))
            stoch_value = pd.DataFrame(stoch_value)
            stoch_value = stoch_value.dropna()
            for v in stoch_value:
                stoch.append(v)
            return stoch

        if not candlesticks:
            return f'Failed to get candlesticks'

    # True Strength Index
    def tsi(candlesticks, slow_period, fast_period):
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            tsiv = []
            tsi_value = tsi(
                df['close'], window_slow=int(slow_period), window_fast=int(fast_period))
            tsi_value = pd.DataFrame(tsi_value)
            tsi_value = tsi_value.dropna()
            for v in tsi_value:
                tsiv.append(v)
            return tsiv

        if not candlesticks:
            return f'Failed to get candlesticks'
