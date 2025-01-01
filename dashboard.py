import streamlit as st
import plotly.graph_objects as go
from utils import fetch_stock_data, preprocess_data, visualize_backtest_results
from backtester import Backtester
from strategies import (
    moving_average_crossover,
    rsi_strategy,
    macd_strategy,
    bollinger_bands_strategy,
    triple_ma_strategy,
    mean_reversion_strategy,
)

# Page configuration
st.set_page_config(
    page_title="Trading Strategy Dashboard",
    page_icon="📈",
    layout="wide"
)

def main():
    st.title("Trading Strategy Dashboard")

    # Configuration section
    st.subheader("Configuration")
    config_col1, config_col2, config_col3 = st.columns(3)

    with config_col1:
        ticker = st.text_input("Stock Symbol", value="AAPL")
    with config_col2:
        period = st.selectbox("Time Period", ["1y", "2y", "5y", "max"], index=0)
    with config_col3:
        strategy_type = st.selectbox(
            "Strategy Type",
            [
                "Moving Average Crossover",
                "RSI",
                "MACD",
                "Bollinger Bands",
                "Triple MA Crossover",
                "Mean Reversion",
            ],
            index=0,
        )

    # Strategy parameters section
    st.subheader("Strategy Parameters")
    col1, col2 = st.columns(2)

    strategy_params = {}

    if strategy_type == "Moving Average Crossover":
        with col1:
            short_window = st.slider("Short MA Window", 5, 50, 20)
        with col2:
            long_window = st.slider("Long MA Window", 20, 200, 50)
        strategy_params = {"short_window": short_window, "long_window": long_window}

    elif strategy_type == "RSI":
        with col1:
            rsi_period = st.slider("RSI Period", 5, 30, 14)
            oversold = st.slider("Oversold Threshold", 20, 40, 30)
        with col2:
            overbought = st.slider("Overbought Threshold", 60, 80, 70)
        strategy_params = {
            "window": rsi_period,
            "oversold": oversold,
            "overbought": overbought,
        }

    elif strategy_type == "MACD":
        with col1:
            fast_period = st.slider("Fast Period", 8, 20, 12)
            slow_period = st.slider("Slow Period", 20, 30, 26)
        with col2:
            signal_period = st.slider("Signal Period", 5, 15, 9)
        strategy_params = {
            "fast": fast_period,
            "slow": slow_period,
            "signal": signal_period,
        }

    elif strategy_type == "Bollinger Bands":
        with col1:
            bb_period = st.slider("Period", 10, 50, 20)
        with col2:
            std_dev = st.slider("Standard Deviation", 1.0, 3.0, 2.0, 0.1)
        strategy_params = {"window": bb_period, "std_dev": std_dev}

    elif strategy_type == "Triple MA Crossover":
        with col1:
            fast_window = st.slider("Fast MA Window", 3, 15, 5)
            medium_window = st.slider("Medium MA Window", 15, 50, 21)
        with col2:
            slow_window = st.slider("Slow MA Window", 50, 200, 63)
        strategy_params = {
            "short_window": fast_window,
            "mid_window": medium_window,
            "long_window": slow_window,
        }

    else:  # Mean Reversion
        with col1:
            lookback = st.slider("Lookback Period", 10, 100, 20)
        with col2:
            entry_threshold = st.slider("Entry Threshold", 1.0, 3.0, 2.0, 0.1)
        strategy_params = {"window": lookback, "std_dev": entry_threshold}

    # Load data
    raw_data = fetch_stock_data(ticker, period)
    if raw_data is not None:
        df = preprocess_data(raw_data)

        # Backtesting
        backtester = Backtester()
        
        if strategy_type == "Moving Average Crossover":
            signals = moving_average_crossover(df, **strategy_params)
        elif strategy_type == "RSI":
            signals = rsi_strategy(df, **strategy_params)
        elif strategy_type == "MACD":
            signals = macd_strategy(df, **strategy_params)
        elif strategy_type == "Bollinger Bands":
            signals = bollinger_bands_strategy(df, **strategy_params)
        elif strategy_type == "Triple MA Crossover":
            signals = triple_ma_strategy(df, **strategy_params)
        else:
            signals = mean_reversion_strategy(df, **strategy_params)

        results = backtester.backtest(df, signals)

        # Display Metrics and Visualizations
        st.subheader("Performance Metrics")
        metrics = backtester.calculate_metrics(results)
        st.write(metrics)

        st.subheader("Backtest Visualization")
        visualize_backtest_results(results)

if __name__ == "__main__":
    main()
