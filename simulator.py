import pandas as pd
import numpy as np
import streamlit as st

from strategies import (
    moving_average_crossover,
    rsi_strategy,
    macd_strategy,
    bollinger_bands_strategy,
    triple_ma_strategy,
    mean_reversion_strategy,
)

import yfinance as yf

import pandas as pd
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands



class Simulator:




    def moving_average_crossover(self, data, short_window, long_window):
        short_ma = SMAIndicator(close=data['Close'], window=short_window).sma_indicator()
        long_ma = SMAIndicator(close=data['Close'], window=long_window).sma_indicator()

        signal = pd.Series(0.0, index=data.index)
        signal[short_ma > long_ma] = 1.0  # Buy
        signal[short_ma < long_ma] = -1.0  # Sell

        return signal

    def rsi_strategy(self, data, window=14, overbought=70, oversold=30):
        rsi = RSIIndicator(close=data['Close'], window=window).rsi()

        signal = pd.Series(0.0, index=data.index)
        signal[rsi < oversold] = 1.0  # Buy
        signal[rsi > overbought] = -1.0  # Sell

        return signal

    def macd_strategy(self, data, fast=12, slow=26, signal=9):
        macd = MACD(close=data['Close'], window_fast=fast, window_slow=slow, window_sign=signal)
        macd_line = macd.macd()
        signal_line = macd.macd_signal()

        signal = pd.Series(0.0, index=data.index)
        signal[macd_line > signal_line] = 1.0  # Buy
        signal[macd_line < signal_line] = -1.0  # Sell

        return signal

    def bollinger_bands_strategy(self, data, window=20, std_dev=2):
        bb = BollingerBands(close=data['Close'], window=window, window_dev=std_dev)

        signal = pd.Series(0.0, index=data.index)
        signal[data['Close'] < bb.bollinger_lband()] = 1.0  # Buy
        signal[data['Close'] > bb.bollinger_hband()] = -1.0  # Sell

        return signal

    def triple_ma_strategy(self, data, short_window=5, mid_window=21, long_window=63):
        short_ma = SMAIndicator(close=data['Close'], window=short_window).sma_indicator()
        mid_ma = SMAIndicator(close=data['Close'], window=mid_window).sma_indicator()
        long_ma = SMAIndicator(close=data['Close'], window=long_window).sma_indicator()

        signal = pd.Series(0.0, index=data.index)
        signal[(short_ma > mid_ma) & (mid_ma > long_ma)] = 1.0  # Buy
        signal[(short_ma < mid_ma) & (mid_ma < long_ma)] = -1.0  # Sell

        return signal

    def mean_reversion_strategy(self, data, window=20, std_dev=2):
        ma = SMAIndicator(close=data['Close'], window=window).sma_indicator()
        std = data['Close'].rolling(window=window).std()

        upper_band = ma + (std * std_dev)
        lower_band = ma - (std * std_dev)

        signal = pd.Series(0.0, index=data.index)
        signal[data['Close'] < lower_band] = 1.0  # Buy
        signal[data['Close'] > upper_band] = -1.0  # Sell

        return signal








    def fetch_stock_data(self, symbol, period='1y'):
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        data.columns = [col if isinstance(col, str) else col[0] for col in data.columns]
        return data



    def __init__(self, initial_balance=10000, transaction_cost=10):
        self.initial_balance = initial_balance
        self.transaction_cost = transaction_cost

    def execute_trade(self, df, signals, take_profit=0.05, stop_loss=0.02):
        results = signals.to_frame(name="Signal").copy()
        results["Close"] = df["Close"]
        results["Shares"] = 0.0
        results["Balance"] = self.initial_balance
        results["Transaction_Cost"] = 0.0
        results["Portfolio_Value"] = self.initial_balance
        results["Position"] = 0
        results["Buy_Price"] = np.nan

        # Initialize state variables
        position_open = False
        buy_price = 0.0

        for date in results.index:
            if results.at[date, "Signal"] == 1 and not position_open:
                # Execute buy action
                shares = int((results.at[date, "Balance"] - self.transaction_cost) / results.at[
                    date, "Close"])
                results.at[date, "Shares"] = shares
                results.at[date, "Transaction_Cost"] = self.transaction_cost
                results.at[date, "Balance"] -= (
                    shares * results.at[date, "Close"] + self.transaction_cost
                )
                results.at[date, "Position"] = 1
                results.at[date, "Buy_Price"] = results.at[date, "Close"]
                buy_price = results.at[date, "Close"]
                position_open = True

            elif position_open:
                # Evaluate exit conditions
                current_price = results.at[date, "Close"]
                price_change = (current_price - buy_price) / buy_price

                if price_change >= take_profit or price_change <= -stop_loss:
                    # Execute sell action
                    previous_date = results.index[results.index.get_loc(date) - 1]
                    shares = results.at[previous_date, "Shares"]
                    results.at[date, "Balance"] += int(shares * current_price - self.transaction_cost)

                    results.at[date, "Transaction_Cost"] = self.transaction_cost
                    results.at[date, "Shares"] = 0
                    results.at[date, "Position"] = 0
                    position_open = False

            # Carry forward values for non-trading days
            if date != results.index[0]:  # Skip the first date
                previous_date = results.index[results.index.get_loc(date) - 1]
                if results.at[date, "Shares"] == 0:
                    results.at[date, "Shares"] = results.at[previous_date, "Shares"]
                if results.at[date, "Balance"] == self.initial_balance:
                    results.at[date, "Balance"] = results.at[previous_date, "Balance"]
                results.at[date, "Position"] = results.at[previous_date, "Position"]
        
        # Calculate portfolio value
        results["Portfolio_Value"] = results["Balance"] + (results["Shares"] * results["Close"])

        # Calculate cumulative returns
        results['Daily_Return'] = results['Portfolio_Value'].pct_change().fillna(0)
        results['Cumulative_Returns'] = (1 + results['Daily_Return']).cumprod() - 1


        
        return results

    def calculate_metrics(self, results):
        if "Portfolio_Value" not in results.columns:
            return {
                "total_return": 0,
                "sharpe_ratio": 0,
                "max_drawdown": 0,
                "win_rate": 0,
            }

        # Total Return
        metrics = {
            "total_return": (results["Portfolio_Value"].iloc[-1] - self.initial_balance)
            / self.initial_balance
            * 100
        }

        # Sharpe Ratio (assuming risk-free rate of 0.01)
        risk_free_rate = 0.01
        daily_returns = results["Portfolio_Value"].pct_change().fillna(0)
        excess_returns = daily_returns - risk_free_rate / 252
        metrics["sharpe_ratio"] = (
            (np.sqrt(252) * excess_returns.mean() / excess_returns.std())
            if excess_returns.std() > 0
            else 0
        )

        # Maximum Drawdown
        rolling_max = results["Portfolio_Value"].expanding().max()
        drawdowns = (results["Portfolio_Value"] - rolling_max) / rolling_max
        metrics["max_drawdown"] = drawdowns.min() * 100

        # Win Rate
        winning_trades = (daily_returns > 0).sum()
        total_trades = len(daily_returns[daily_returns != 0])
        metrics["win_rate"] = (
            (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        )

        return metrics 


    def generate_signals(self, strategy_type, df, strategy_params):
        if strategy_type == "Moving Average Crossover":
            return moving_average_crossover(df, **strategy_params)
        elif strategy_type == "RSI":
            return rsi_strategy(df, **strategy_params)
        elif strategy_type == "MACD":
            return macd_strategy(df, **strategy_params)
        elif strategy_type == "Bollinger Bands":
            return bollinger_bands_strategy(df, **strategy_params)
        elif strategy_type == "Triple MA Crossover":
            return triple_ma_strategy(df, **strategy_params)
        elif strategy_type == "Mean Reversion":
            return mean_reversion_strategy(df, **strategy_params)
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

    def configure_strategy_parameters(self, strategy_type):

        params = {}

        if strategy_type == "Moving Average Crossover":
            params["short_window"] = st.slider("Short MA Window", 5, 50, 20)
            params["long_window"] = st.slider("Long MA Window", 20, 200, 50)
        elif strategy_type == "RSI":
            params["window"] = st.slider("RSI Period", 5, 30, 14)
            params["oversold"] = st.slider("Oversold Threshold", 20, 40, 30)
            params["overbought"] = st.slider("Overbought Threshold", 60, 80, 70)
        elif strategy_type == "MACD":
            params["fast"] = st.slider("Fast Period", 8, 20, 12)
            params["slow"] = st.slider("Slow Period", 20, 30, 26)
            params["signal"] = st.slider("Signal Period", 5, 15, 9)
        elif strategy_type == "Bollinger Bands":
            params["window"] = st.slider("Period", 10, 50, 20)
            params["std_dev"] = st.slider("Standard Deviation", 1.0, 3.0, 2.0, 0.1)
        elif strategy_type == "Triple MA Crossover":
            params["short_window"] = st.slider("Fast MA Window", 3, 15, 5)
            params["mid_window"] = st.slider("Medium MA Window", 15, 50, 21)
            params["long_window"] = st.slider("Slow MA Window", 50, 200, 63)
        elif strategy_type == "Mean Reversion":
            params["window"] = st.slider("Lookback Period", 10, 100, 20)
            params["std_dev"] = st.slider("Entry Threshold", 1.0, 3.0, 2.0, 0.1)

        return params
