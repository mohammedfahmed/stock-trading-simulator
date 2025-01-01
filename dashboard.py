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
    st.sidebar.header("Configuration")
    ticker = st.sidebar.text_input("Stock Symbol", value="AAPL")
    period = st.sidebar.selectbox("Time Period", ["1y", "2y", "5y", "max"], index=0)
    strategy_type = st.sidebar.selectbox(
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
    st.sidebar.header("Strategy Parameters")
    strategy_params = configure_strategy_parameters(strategy_type)

    # Load data
    raw_data = fetch_stock_data(ticker, period)
    if raw_data is None or raw_data.empty:
        st.error(f"No data available for {ticker}. Please check the stock symbol.")
        return

    df = preprocess_data(raw_data)

    # Backtesting
    backtester = Backtester()
    signals = select_strategy(strategy_type, df, strategy_params)
    results = backtester.backtest(df, signals)

    # Display Metrics and Visualizations
    st.subheader("Performance Metrics")
    metrics = backtester.calculate_metrics(results)
    st.write(metrics)

    st.subheader("Backtest Visualization")
    visualize_backtest_results(results)

def configure_strategy_parameters(strategy_type):
    """Configures parameters based on the selected strategy type."""
    params = {}

    if strategy_type == "Moving Average Crossover":
        params["short_window"] = st.sidebar.slider("Short MA Window", 5, 50, 20)
        params["long_window"] = st.sidebar.slider("Long MA Window", 20, 200, 50)
    elif strategy_type == "RSI":
        params["window"] = st.sidebar.slider("RSI Period", 5, 30, 14)
        params["oversold"] = st.sidebar.slider("Oversold Threshold", 20, 40, 30)
        params["overbought"] = st.sidebar.slider("Overbought Threshold", 60, 80, 70)
    elif strategy_type == "MACD":
        params["fast"] = st.sidebar.slider("Fast Period", 8, 20, 12)
        params["slow"] = st.sidebar.slider("Slow Period", 20, 30, 26)
        params["signal"] = st.sidebar.slider("Signal Period", 5, 15, 9)
    elif strategy_type == "Bollinger Bands":
        params["window"] = st.sidebar.slider("Period", 10, 50, 20)
        params["std_dev"] = st.sidebar.slider("Standard Deviation", 1.0, 3.0, 2.0, 0.1)
    elif strategy_type == "Triple MA Crossover":
        params["short_window"] = st.sidebar.slider("Fast MA Window", 3, 15, 5)
        params["mid_window"] = st.sidebar.slider("Medium MA Window", 15, 50, 21)
        params["long_window"] = st.sidebar.slider("Slow MA Window", 50, 200, 63)
    elif strategy_type == "Mean Reversion":
        params["window"] = st.sidebar.slider("Lookback Period", 10, 100, 20)
        params["std_dev"] = st.sidebar.slider("Entry Threshold", 1.0, 3.0, 2.0, 0.1)

    return params

def select_strategy(strategy_type, df, strategy_params):
    """Selects and applies the appropriate strategy based on user input."""
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

if __name__ == "__main__":
    main()
