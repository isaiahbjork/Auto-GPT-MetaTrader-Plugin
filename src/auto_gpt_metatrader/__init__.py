"""This is a plugin to use Auto-GPT with MetaTrader."""
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from auto_gpt_plugin_template import AutoGPTPluginTemplate

# MetaTrader
import requests
import os
import numpy as np
import ta
from candlesticks import fetch

PromptGenerator = TypeVar("PromptGenerator")

account_id = os.getenv('META_API_ACCOUNT_ID')
token = os.getenv("META_API_TOKEN")


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
                "timeframe": "<timeframe>"
            },
            self.money_flow_index
        ),
        prompt.add_command(
            "RSI",
            "rsi",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
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
                "period_fast": "<period_fast>",
                "period_slow": "<period_slow>",
                "period_signal": "<period_signal>",
            },
            self.macd
        ),
        prompt.add_command(
            "Moving Average of Oscillator (OsMA)",
            "osma",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period_fast": "<period_fast>",
                "period_slow": "<period_slow>",
                "period_signal": "<period_signal>",
            },
            self.osma
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
            "Moving Average Envelope",
            "mae",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
                "percentage": "<period>",
            },
            self.mae
        ),
        prompt.add_command(
            "Bollinger Bands",
            "bollinger_bands",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
                "deviation": "<deviation>",
            },
            self.bollinger_bands
        ), prompt.add_command(
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
        url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
        response = requests.post(
            url, headers=headers, json=trade_data)
        response = response.json()
        return response

    def close_all_trades(self) -> Optional[Dict[str, Any]]:
        url2 = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/positions"
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
            url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
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
        url2 = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/positions"
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
        url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/account-information"
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
        url = f"https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/{account_id}/trade"
        response = requests.post(url, headers=headers, json=trade_data)
        if response:
            response = response.json()
            return response
        else:
            response = response.json()
            return response

    # Indicators

    def money_flow_index(self, symbol: str, timeframe: str) -> Optional[float]:
        candlesticks = fetch(symbol, timeframe)
        if candlesticks:
            typical_prices = [(candlestick['high'] + candlestick['low'] +
                               candlestick['close']) / 3 for candlestick in candlesticks]

            positive_money_flow = [typical_prices[i] if typical_prices[i] >
                                   typical_prices[i-1] else 0 for i in range(1, len(typical_prices))]
            negative_money_flow = [typical_prices[i] if typical_prices[i] <
                                   typical_prices[i-1] else 0 for i in range(1, len(typical_prices))]
            positive_money_flow.insert(0, 0)
            negative_money_flow.insert(0, 0)

            positive_money_flow_sum = np.sum(positive_money_flow[-14:])
            negative_money_flow_sum = np.sum(negative_money_flow[-14:])
            money_ratio = positive_money_flow_sum / negative_money_flow_sum
            mfi = 100 - (100 / (1 + money_ratio))

            return mfi
        else:
            return 'Failed to get candlesticks.'

    def volume(self, symbol: str, timeframe: str) -> Optional[float]:
        candlesticks = fetch(symbol, timeframe)
        if candlesticks:
            candlesticks = candlesticks["candles"]
            volumes = [candlestick['tickVolume'] for candlestick in candlesticks]
            return np.sum(volumes[-14:])
        else:
            return f'Failed to get candlesticks'

    def rsi(self, symbol: str, timeframe: str) -> Optional[float]:
        # Get the tick volume data
        candlesticks = fetch(symbol, timeframe)
        if not candlesticks:
            return f'Failed to get candlesticks'

        rsi = ta.momentum.RSIIndicator(candlesticks['close'], window=14)

        return rsi

    # Simple Moving Average (SMA)
    def sma(self, symbol: str, timeframe: str, period: str) -> Optional[float]:
        # Get the tick volume data
        candlesticks = fetch(symbol, timeframe)
        if not candlesticks:
            return f'Failed to get candlesticks'
        return ta.trend.sma_indicator(candlesticks['close'], window=float(period))

    # Exponential Moving Average (EMA)
    def ema(self, symbol: str, timeframe: str, period: str) -> Optional[float]:
        # Get the tick volume data
        candlesticks = fetch(symbol, timeframe)
        if not candlesticks:
            return f'Failed to get candlesticks'
        return ta.trend.ema_indicator(candlesticks['close'], window=float(period))

    # Weighted Moving Average (WMA)
    def wma(self, symbol: str, timeframe: str, period: str) -> Optional[float]:
        # Get the tick volume data
        candlesticks = fetch(symbol, timeframe)
        if not candlesticks:
            return f'Failed to get candlesticks'
        return ta.trend.wma_indicator(candlesticks['close'], window=float(period))

    # Moving Average Convergence Divergence (MACD)
    def macd(self, symbol: str, timeframe: str, period_fast: str = 12, period_slow: str = 26, period_signal: str = 9) -> Optional[float]:
        # Get the tick volume data
        candlesticks = fetch(symbol, timeframe)
        if not candlesticks:
            return f'Failed to get candlesticks'
        return ta.trend.macd(candlesticks['close'], window_fast=float(period_fast), window_slow=float(period_slow), window_signal=float(period_signal))

    # Moving Average Envelope (MAE)
    def mae(self, symbol: str, timeframe: str, period: str = 20, percentage: str = 0.025) -> Optional[float]:
        # Get the tick volume data
        candlesticks = fetch(symbol, timeframe)
        if not candlesticks:
            return f'Failed to get candlesticks'
        return ta.volatility.bollinger_mavg(candlesticks['close'], window=float(period), percentage=float(percentage))

    # Moving Average of Oscillator (OsMA)
    def osma(self, symbol: str, timeframe: str, period_fast: int = 12, period_slow: int = 26, period_signal: int = 9) -> Optional[float]:
        # Get the candlestick data
        candlesticks = fetch(symbol, timeframe)
        if not candlesticks:
            return f'Failed to get candlesticks'

        # Calculate MACD
        macd_line, signal_line, histogram = ta.trend.macd(candlesticks['close'],
                                                          window_fast=period_fast,
                                                          window_slow=period_slow,
                                                          window_signal=period_signal)

        # Calculate OsMA
        osma = histogram - signal_line

        return osma

    def bollinger_bands(self, symbol: str, timeframe: str, period: int = 20, deviations: int = 2) -> Optional[Tuple[List[float], List[float], List[float]]]:
        candlesticks = fetch(symbol, timeframe)
        if candlesticks:
            candlesticks = candlesticks["candles"]
            closes = [candlestick['close'] for candlestick in candlesticks]
            sma = ta.SMA(np.array(closes), timeperiod=period)
            std = ta.STDDEV(np.array(closes), timeperiod=period)
            upper_band = sma + (deviations * std)
            lower_band = sma - (deviations * std)
            return upper_band.tolist(), sma.tolist(), lower_band.tolist()
        else:
            return None

    def fib_retracements(self, high: float, low: float) -> List[float]:
        levels = [0.236, 0.382, 0.5, 0.618, 0.786]
        diff = high - low
        retracements = []
        for level in levels:
            retracements.append(high - level * diff)
        return retracements
