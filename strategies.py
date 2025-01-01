import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def moving_average_crossover(data, short_window, long_window):
    """
    Calculates the moving average crossover signal.

    Args:
        data: Pandas DataFrame containing the stock data with a 'Close' column.
        short_window: Window size for the short moving average.
        long_window: Window size for the long moving average.

    Returns:
        Pandas Series with signal values:
            1.0: Buy signal
            -1.0: Sell signal
            0.0: Hold
    """
    short_ma = SMAIndicator(close=data['Close'], window=short_window).sma_indicator()
    long_ma = SMAIndicator(close=data['Close'], window=long_window).sma_indicator()

    signal = pd.Series(0.0, index=data.index)
    signal[short_ma > long_ma] = 1.0  # Buy
    signal[short_ma < long_ma] = -1.0  # Sell

    return signal

def rsi_strategy(data, window=14, overbought=70, oversold=30):
    """
    Calculates the RSI-based trading signal.

    Args:
        data: Pandas DataFrame containing the stock data with a 'Close' column.
        window: Window size for RSI calculation.
        overbought: RSI level indicating overbought condition.
        oversold: RSI level indicating oversold condition.

    Returns:
        Pandas Series with signal values:
            1.0: Buy signal
            -1.0: Sell signal
            0.0: Hold
    """
    rsi = RSIIndicator(close=data['Close'], window=window).rsi()

    signal = pd.Series(0.0, index=data.index)
    signal[rsi < oversold] = 1.0  # Buy
    signal[rsi > overbought] = -1.0  # Sell

    return signal

def macd_strategy(data, fast=12, slow=26, signal=9):
    """
    Calculates the MACD-based trading signal.

    Args:
        data: Pandas DataFrame containing the stock data with a 'Close' column.
        fast: Fast period for MACD calculation.
        slow: Slow period for MACD calculation.
        signal: Signal period for MACD calculation.

    Returns:
        Pandas Series with signal values:
            1.0: Buy signal
            -1.0: Sell signal
            0.0: Hold
    """
    macd = MACD(close=data['Close'], window_fast=fast, window_slow=slow, window_sign=signal)
    macd_line = macd.macd()
    signal_line = macd.macd_signal()

    signal = pd.Series(0.0, index=data.index)
    signal[macd_line > signal_line] = 1.0  # Buy
    signal[macd_line < signal_line] = -1.0  # Sell

    return signal

def bollinger_bands_strategy(data, window=20, std_dev=2):
    """
    Calculates the Bollinger Bands-based trading signal.

    Args:
        data: Pandas DataFrame containing the stock data with a 'Close' column.
        window: Window size for Bollinger Bands calculation.
        std_dev: Number of standard deviations for Bollinger Bands.

    Returns:
        Pandas Series with signal values:
            1.0: Buy signal
            -1.0: Sell signal
            0.0: Hold
    """
    bb = BollingerBands(close=data['Close'], window=window, window_dev=std_dev)

    signal = pd.Series(0.0, index=data.index)
    signal[data['Close'] < bb.bollinger_lband()] = 1.0  # Buy
    signal[data['Close'] > bb.bollinger_hband()] = -1.0  # Sell

    return signal

def triple_ma_strategy(data, short_window=5, mid_window=21, long_window=63):
    """
    Calculates the Triple Moving Average crossover signal.

    Args:
        data: Pandas DataFrame containing the stock data with a 'Close' column.
        short_window: Window size for the short moving average.
        mid_window: Window size for the mid moving average.
        long_window: Window size for the long moving average.

    Returns:
        Pandas Series with signal values:
            1.0: Buy signal
            -1.0: Sell signal
            0.0: Hold
    """
    short_ma = SMAIndicator(close=data['Close'], window=short_window).sma_indicator()
    mid_ma = SMAIndicator(close=data['Close'], window=mid_window).sma_indicator()
    long_ma = SMAIndicator(close=data['Close'], window=long_window).sma_indicator()

    signal = pd.Series(0.0, index=data.index)
    signal[(short_ma > mid_ma) & (mid_ma > long_ma)] = 1.0  # Buy
    signal[(short_ma < mid_ma) & (mid_ma < long_ma)] = -1.0  # Sell

    return signal

def mean_reversion_strategy(data, window=20, std_dev=2):
    """
    Calculates the Mean Reversion trading signal.

    Args:
        data: Pandas DataFrame containing the stock data with a 'Close' column.
        window: Window size for moving average and standard deviation calculation.
        std_dev: Number of standard deviations for the bands.

    Returns:
        Pandas Series with signal values:
            1.0: Buy signal
            -1.0: Sell signal
            0.0: Hold
    """
    ma = SMAIndicator(close=data['Close'], window=window).sma_indicator()
    std = data['Close'].rolling(window=window).std()

    upper_band = ma + (std * std_dev)
    lower_band = ma - (std * std_dev)

    signal = pd.Series(0.0, index=data.index)
    signal[data['Close'] < lower_band] = 1.0  # Buy
    signal[data['Close'] > upper_band] = -1.0  # Sell

    return signal
