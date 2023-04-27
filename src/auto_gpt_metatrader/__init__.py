"""This is a plugin to use Auto-GPT with MetaTrader."""
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from auto_gpt_plugin_template import AutoGPTPluginTemplate

# MetaTrader
import requests
import os
import numpy as np
import ta
import myfxbook
import pandas as pd
from ta.utils import dropna
from ta.momentum import rsi, stoch_signal, tsi
from ta.trend import sma_indicator, ema_indicator, wma_indicator, macd_signal, adx
from ta.volume import acc_dist_index, money_flow_index
PromptGenerator = TypeVar("PromptGenerator")

account_id = os.getenv('META_API_ACCOUNT_ID')
token = os.getenv("META_API_TOKEN")
region = os.getenv("META_API_REGION")
lunarcrush_api = os.getenv('LUNAR_CRUSH_API_KEY')
myfxbook_username = os.getenv('MY_FX_BOOK_USERNAME')
myfxbook_password = os.getenv('MY_FX_BOOK_PASSWORD')
fcs_api = os.getenv('FCS_API_KEY')


class Message(TypedDict):
    role: str
    content: str


class AutoGPTMetaTraderPlugin(AutoGPTPluginTemplate):
    """
    This is a plugin to use Auto-GPT with MetaTrader.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-MetaTrader"
        self._version = "0.1.0"
        self._description = "This is a plugin for Auto-GPT-MetaTrader."

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        prompt.add_command(
            "Fetch Candlesticks",
            "fetch_candlesticks",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>"
            },
            self.fetch_candlesticks
        ),
        prompt.add_command(
            "Close All Trades",
            "close_all_trades",
            {},
            self.close_all_trades
        ),
        prompt.add_command(
            "Close A Trade",
            "close_trade",
            {
                "position_id": "<position_id>"
            },
            self.close_trade
        ),
        prompt.add_command(
            "Get Account Information",
            "get_account_information",
            {},
            self.get_account_information
        ),
        prompt.add_command(
            "Get Positions",
            "get_positions",
            {},
            self.get_positions
        ),
        prompt.add_command(
            "Place Trade",
            "place_trade",
            {
                "symbol": "<symbol>",
                "volume": "<volume>",
                "signal": "<signal>"
            },
            self.place_trade
        ),
        prompt.add_command(
            "Money Flow Index",
            "money_flow_index",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>"
            },
            self.money_flow_index
        ),
        prompt.add_command(
            "RSI",
            "rsi",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>"
            },
            self.rsi
        ),
        prompt.add_command(
            "Volume",
            "volume",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
            },
            self.volume
        ),
        prompt.add_command(
            "Simple Moving Average",
            "sma",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
            },
            self.sma
        ),
        prompt.add_command(
            "Exponential Moving Average",
            "ema",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
            },
            self.ema
        ),
        prompt.add_command(
            "MACD",
            "macd",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "fast_period": "<fast_period>",
                "slow_period": "<slow_period>",
                "signal_period": "<signal_period>",
            },
            self.macd
        ),
        prompt.add_command(
            "Accumulation/Distribution Index",
            "adi",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
            },
            self.adi
        ),
        prompt.add_command(
            "Weighted Moving Average",
            "wma",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",

            },
            self.wma
        ),
        prompt.add_command(
            "Average Directional Movement Index",
            "adx",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
            },
            self.adx
        ),
        prompt.add_command(
            "Fibonacci Retracement",
            "fib_retracements",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "high": "<high>",
                "low": "<low>",
            },
            self.fib_retracements
        ),
        prompt.add_command(
            "Stochastic Oscillator",
            "stochastic_oscillator",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
                "smooth_period": "<smooth_period>",
            },
            self.stochastic_oscillator
        ),
        prompt.add_command(
            "True Strength Index",
            "tsi",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period_slow": "<period_slow>",
                "period_fast": "<period_fast>",
            },
            self.tsi
        ),
        prompt.add_command(
            "Stock Of The Day",
            "get_stock_of_the_day",
            {},
            self.get_stock_of_the_day
        ),
        prompt.add_command(
            "Get Important Forex News",
            "get_important_forex_news",
            {},
            self.get_important_forex_news
        ),
        return prompt

    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.
        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True

    def can_handle_on_response(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_response method.
        Returns:
            bool: True if the plugin can handle the on_response method."""
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""
        pass

    def can_handle_on_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_planning method.
        Returns:
            bool: True if the plugin can handle the on_planning method."""
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        """This method is called before the planning chat completion is done.
        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """
        pass

    def can_handle_post_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_planning method.
        Returns:
            bool: True if the plugin can handle the post_planning method."""
        return False

    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completion is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_instruction method.
        Returns:
            bool: True if the plugin can handle the pre_instruction method."""
        return False

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        """This method is called before the instruction chat is done.
        Args:
            messages (List[Message]): The list of context messages.
        Returns:
            List[Message]: The resulting list of messages.
        """
        pass

    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.
        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return False

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        """This method is called when the instruction chat is done.
        Args:
            messages (List[Message]): The list of context messages.
        Returns:
            Optional[str]: The resulting message.
        """
        pass

    def can_handle_post_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_instruction method.
        Returns:
            bool: True if the plugin can handle the post_instruction method."""
        return False

    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_command method.
        Returns:
            bool: True if the plugin can handle the pre_command method."""
        return False

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """This method is called before the command is executed.
        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.
        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """
        pass

    def can_handle_post_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_command method.
        Returns:
            bool: True if the plugin can handle the post_command method."""
        return False

    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.
        Args:
            command_name (str): The command name.
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        """This method is called to check that the plugin can
          handle the chat_completion method.
        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
          Returns:
              bool: True if the plugin can handle the chat_completion method."""
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        """This method is called when the chat completion is done.
        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            str: The resulting response.
        """
        pass

    def fetch_candlesticks(self, symbol: str, timeframe: str) -> Optional[Dict[str, Any]]:
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

    def fetch(self, symbol, timeframe):
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

    def close_trade(self, position_id: str) -> None:
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

    def close_all_trades(self) -> Optional[Dict[str, Any]]:
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

    def get_positions(self) -> Optional[Dict[str, Any]]:
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

    def get_account_information(self) -> Optional[Dict[str, Any]]:
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

    def place_trade(self, symbol: str, volume: str, signal: str) -> None:
        signal = signal.upper()
        symbol = symbol.upper()
        # Place the new trade
        trade_data = {
            'symbol': symbol,
            'actionType': 'ORDER_TYPE_BUY' if signal == 'BUY' else 'ORDER_TYPE_SELL',
            'volume': float(volume),
            'comment': 'Auto-GPT MetaTrader Plugin'
        }
        headers = {
            "auth-token": token,
            "Content-Type": "application/json"
        }
        url = f"https://mt-client-api-v1.{region}.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
        response = requests.post(url, headers=headers, json=trade_data)
        if response:
            response = response.json()
            return response
        else:
            response = response.json()
            return response

    # Indicators

    def money_flow_index(self, symbol: str, timeframe: str, period: int = 14) -> Optional[float]:
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            mfi_value = money_flow_index(
                df['high'], df['low'], df['close'], df['tickVolume'], window=int(period))
            mfi_value = pd.DataFrame(mfi_value)
            mfiv = mfi_value.dropna()
            return mfiv.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'

    def volume(self, symbol: str, timeframe: str) -> Optional[float]:
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            volumes = [float(candlestick['tickVolume']) for candlestick in candlesticks]
            return np.sum(volumes[-14:])
        else:
            return f'Failed to get candlesticks'

    def rsi(self, symbol: str, timeframe: str, period: float = 14) -> Optional[float]:
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            rsi_value = rsi(df['close'], window=int(period))
            rsi_value = pd.DataFrame(rsi_value)
            rsiv = rsi_value.dropna()
            return rsiv.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Simple Moving Average (SMA)

    def sma(self, symbol: str, timeframe: str, period: int = 12) -> Optional[float]:
        # Get the candlesticks data
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            sma_value = sma_indicator(df['close'], window=int(period))
            sma_value = pd.DataFrame(sma_value)
            smav = sma_value.dropna()
            return smav.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Exponential Moving Average (EMA)
    def ema(self, symbol: str, timeframe: str, period: int = 14) -> Optional[float]:
        # Get the candlesticks data
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            ema_value = ema_indicator(df['close'], window=int(period))
            ema_value = pd.DataFrame(ema_value)
            emav = ema_value.dropna()
            return emav.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Weighted Moving Average (WMA)
    def wma(self, symbol: str, timeframe: str, period: int = 9) -> Optional[float]:
        # Get the candlesticks data
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            wma_value = wma_indicator(df['close'], window=int(period))
            wma_value = pd.DataFrame(wma_value)
            wmav = wma_value.dropna()
            return wmav.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Moving Average Convergence Divergence (MACD)
    def macd(self, symbol: str, timeframe: str, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Optional[Tuple[float, float, float]]:
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            macd_value = macd_signal(df['close'], window_slow=int(
                slow_period), window_fast=int(fast_period), window_sign=int(signal_period))
            macd_value = pd.DataFrame(macd_value)
            macdv = macd_value.dropna()
            return macdv.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Average Directional Movement Index (ADX)
    def adx(self, symbol: str, timeframe: str, period: str = 20) -> Optional[float]:
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            adx_value = adx(df['high'], df['low'], df['close'], window=int(period))
            adx_value = pd.DataFrame(adx_value)
            adxv = adx_value.dropna()
            return adxv.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'

    # Accumulation/Distribution Index (ADI)
    def adi(self, symbol: str, timeframe: str) -> Optional[float]:
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            adi_value = acc_dist_index(
                df['high'], df['low'], df['close'], df['tickVolume'])
            adi_value = pd.DataFrame(adi_value)
            adiv = adi_value.dropna()
            return adiv.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'

    def fib_retracements(self, high: float, low: float) -> List[float]:
        levels = [0.236, 0.382, 0.5, 0.618, 0.786]
        diff = high - low
        retracements = []
        for level in levels:
            retracements.append(high - level * diff)
        return retracements

     # Stochastic Oscillator
    def stochastic_oscillator(self, symbol: str, timeframe: str, period: int = 14, smooth_period: int = 3) -> Optional[float]:
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            stoch_value = stoch_signal(
                df['high'], df['low'], df['close'], window=int(period), smooth_window=int(smooth_period))
            stoch_value = pd.DataFrame(stoch_value)
            stochv = stoch_value.dropna()
            return stochv.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'

    # True Strength Index
    def tsi(self, symbol: str, timeframe: str, slow_period: int = 25, fast_period: int = 13) -> Optional[float]:
        candlesticks = self.fetch(symbol, timeframe)
        if candlesticks:
            df = pd.DataFrame(candlesticks)
            # Clean NaN values
            df = dropna(df)
            tsi_value = tsi(
                df['close'], window_slow=int(slow_period), window_fast=int(fast_period))
            tsi_value = pd.DataFrame(tsi_value)
            tsiv = tsi_value.dropna()
            return tsiv.to_json()

        if not candlesticks:
            return f'Failed to get candlesticks'
        
    # LunarCrush

    def get_stock_of_the_day(self) -> float:

        url = "https://lunarcrush.com/api3/stockoftheday"
        headers = {
            'Authorization': f'Bearer {lunarcrush_api}'
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            return response.text.encode('utf8')
        else:
            raise Exception(
                f"Failed to get Stock of the day from LunarCrush; status code {response.status_code}")

    # FCS API
    def get_important_forex_news(self) -> str:
        url = 'https://fcsapi.com/api-v3/forex/economy_cal'
        params = {
            'access_key': fcs_api
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception if the response status is not OK (2xx)

            json_data = response.json()
            important_events = []
            for item in json_data['response']:
                if item['importance'] == '2':
                    important_events.append(item)
            return important_events

        except requests.exceptions.RequestException as e:
            print('Error fetching data from FCS API:', e)
            return None
