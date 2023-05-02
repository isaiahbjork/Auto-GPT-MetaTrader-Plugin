"""This is a plugin to use Auto-GPT with MetaTrader."""
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from auto_gpt_plugin_template import AutoGPTPluginTemplate

# MetaTrader
import requests
import os
import numpy as np
import ta
from myfxbook import myfxbook
import pandas as pd
from .indicators import Indicators
from .fcs import Fcs
from .lunarcrush import LunarCrush
from .trading import Trading

PromptGenerator = TypeVar("PromptGenerator")


myfxbook_username = os.getenv('MY_FX_BOOK_USERNAME')
myfxbook_password = os.getenv('MY_FX_BOOK_PASSWORD')


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
        self.fx = myfxbook.myfxbook(myfxbook_username, myfxbook_password)

        def login():
            self.fx.login()
        login()

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
        # prompt.add_command(
        #     "Get Sentiment",
        #     "get_sentiment",
        #     {
        #         "symbol": "<symbol>"
        #     },
        #     self.get_sentiment
        # ),
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
        data = Trading.fetch_candlesticks(symbol, timeframe)
        return data

    def close_trade(self, position_id: str) -> None:
        data = Trading.close_trade(position_id)
        return data

    def close_all_trades(self) -> Optional[Dict[str, Any]]:
        data = Trading.close_all_trades()
        return data

    def get_positions(self) -> Optional[Dict[str, Any]]:
        data = Trading.get_positions()
        return data

    def get_account_information(self) -> Optional[Dict[str, Any]]:
        data = Trading.get_account_information()
        return data

    def place_trade(self, symbol: str, volume: str, signal: str) -> None:
        data = Trading.place_trade(symbol, volume, signal)
        return data

    # Indicators
    def money_flow_index(self, symbol: str, timeframe: str, period: int = 14) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.money_flow_index(candlesticks, period)
        return data

    def volume(self, symbol: str, timeframe: str) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.volume(candlesticks)
        return data

    def rsi(self, symbol: str, timeframe: str, period: float = 14) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.rsi(candlesticks, period)
        return data

    def sma(self, symbol: str, timeframe: str, period: int = 12) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.sma(candlesticks, period)
        return data

    def ema(self, symbol: str, timeframe: str, period: int = 14) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.ema(candlesticks, period)
        return data

    def wma(self, symbol: str, timeframe: str, period: int = 9) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.wma(candlesticks, period)
        return data

    def macd(self, symbol: str, timeframe: str, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Optional[Tuple[float, float, float]]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.macd(candlesticks, fast_period,
                               slow_period, signal_period)
        return data

    def adx(self, symbol: str, timeframe: str, period: str = 20) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.adx(candlesticks, period)
        return data

    def adi(self, symbol: str, timeframe: str) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.adi(candlesticks, symbol, timeframe)
        return data

    def fib_retracements(self, symbol: str, timeframe: str, high: float, low: float) -> List[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.fib_retracements(candlesticks,high, low)
        return data

    def stochastic_oscillator(self, symbol: str, timeframe: str, period: int = 14, smooth_period: int = 3) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.stochastic_oscillator(candlesticks, period, smooth_period)
        return data

    def tsi(self, symbol: str, timeframe: str, slow_period: int = 25, fast_period: int = 13) -> Optional[float]:
        candlesticks = Indicators.fetch(symbol, timeframe)
        data = Indicators.tsi(candlesticks, slow_period, fast_period)
        return data

    # LunarCrush
    def get_stock_of_the_day(self) -> float:
        data = LunarCrush.get_stock_of_the_day(indicators)
        return data

    # FCS API
    def get_important_forex_news(self) -> str:
        data = Fcs.get_important_forex_news(indicators)
        return data

    # MyFxBook
    # def get_sentiment(self, symbol: str) -> str:
    #     data = self.fx.get_community_outlook()
    #     symbol = symbol.replace('/', '')
    #     symbol = symbol.upper()
    #     for d in data["symbols"]:
    #         if d["name"] == symbol:
    #             short_percentage = d["shortPercentage"]
    #             long_percentage = d["longPercentage"]
    #             return f"Shorts: {short_percentage}%, Longs: {long_percentage}%"
    #     # Symbol name not found in data
    #     return f'Symbol Not Found'
