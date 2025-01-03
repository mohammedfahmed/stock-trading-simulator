import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def moving_average_crossover(data, short_window, long_window):
    short_ma = SMAIndicator(close=data['Close'], window=short_window).sma_indicator()
    long_ma = SMAIndicator(close=data['Close'], window=long_window).sma_indicator()

    signal = pd.Series(0.0, index=data.index)
    signal[short_ma > long_ma] = 1.0  # Buy
    signal[short_ma < long_ma] = -1.0  # Sell

    return signal

def rsi_strategy(data, window=14, overbought=70, oversold=30):
    rsi = RSIIndicator(close=data['Close'], window=window).rsi()

    signal = pd.Series(0.0, index=data.index)
    signal[rsi < oversold] = 1.0  # Buy
    signal[rsi > overbought] = -1.0  # Sell

    return signal

def macd_strategy(data, fast=12, slow=26, signal=9):
    macd = MACD(close=data['Close'], window_fast=fast, window_slow=slow, window_sign=signal)
    macd_line = macd.macd()
    signal_line = macd.macd_signal()

    signal = pd.Series(0.0, index=data.index)
    signal[macd_line > signal_line] = 1.0  # Buy
    signal[macd_line < signal_line] = -1.0  # Sell

    return signal

def bollinger_bands_strategy(data, window=20, std_dev=2):
    bb = BollingerBands(close=data['Close'], window=window, window_dev=std_dev)

    signal = pd.Series(0.0, index=data.index)
    signal[data['Close'] < bb.bollinger_lband()] = 1.0  # Buy
    signal[data['Close'] > bb.bollinger_hband()] = -1.0  # Sell

    return signal

def triple_ma_strategy(data, short_window=5, mid_window=21, long_window=63):
    short_ma = SMAIndicator(close=data['Close'], window=short_window).sma_indicator()
    mid_ma = SMAIndicator(close=data['Close'], window=mid_window).sma_indicator()
    long_ma = SMAIndicator(close=data['Close'], window=long_window).sma_indicator()

    signal = pd.Series(0.0, index=data.index)
    signal[(short_ma > mid_ma) & (mid_ma > long_ma)] = 1.0  # Buy
    signal[(short_ma < mid_ma) & (mid_ma < long_ma)] = -1.0  # Sell

    return signal

def mean_reversion_strategy(data, window=20, std_dev=2):
    ma = SMAIndicator(close=data['Close'], window=window).sma_indicator()
    std = data['Close'].rolling(window=window).std()

    upper_band = ma + (std * std_dev)
    lower_band = ma - (std * std_dev)

    signal = pd.Series(0.0, index=data.index)
    signal[data['Close'] < lower_band] = 1.0  # Buy
    signal[data['Close'] > upper_band] = -1.0  # Sell

    return signal
