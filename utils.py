import yfinance as yf
import pandas as pd
import numpy as np
from itertools import product
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def fetch_stock_data(symbol, period='1y'):
    """
    Fetches historical stock data from Yahoo Finance.

    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT').
        period: Data period (e.g., '1y' for 1 year, '5y' for 5 years).

    Returns:
        pandas.DataFrame: Historical stock data.
    """
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data
