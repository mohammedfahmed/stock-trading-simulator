import streamlit as st
from data_loader import fetch_stock_data
from utils import preprocess_data, configure_strategy_parameters
from visualize import visualize_backtest_results
from simulator import Simulator
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
    layout="wide"
)

def main():
    st.title("Trading Strategy Dashboard")

    # Sidebar: Configuration section
    st.header("Configuration")
    ticker = st.text_input("Stock Symbol", value="AAPL")
    period = st.selectbox("Time Period", ["1y", "2y", "5y", "max"], index=0)
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

    # Sidebar: Strategy parameters section
    # st.sidebar.header("Strategy Parameters")
    strategy_params = configure_strategy_parameters(strategy_type)

    # Load and preprocess data
    raw_data = fetch_stock_data(ticker, period)
    if raw_data is None or raw_data.empty:
        st.error(f"No data available for {ticker}. Please check the stock symbol.")
        return

    df = preprocess_data(raw_data)
    simulator = Simulator()
    signals = select_strategy(strategy_type, df, strategy_params)
    results = simulator.execute_trade(df, signals)

    # Display metrics and visualizations
    st.subheader("Performance Metrics")
    metrics = simulator.calculate_metrics(results)
    st.write(metrics)

    st.subheader("Backtest Visualization")
    st.altair_chart(visualize_backtest_results(results))


def select_strategy(strategy_type, df, strategy_params):
    """Selects and applies the appropriate strategy based on user input."""
    strategies = {
        "Moving Average Crossover": moving_average_crossover,
        "RSI": rsi_strategy,
        "MACD": macd_strategy,
        "Bollinger Bands": bollinger_bands_strategy,
        "Triple MA Crossover": triple_ma_strategy,
        "Mean Reversion": mean_reversion_strategy,
    }
    strategy_function = strategies.get(strategy_type)
    if strategy_function:
        return strategy_function(df, **strategy_params)
    else:
        raise ValueError(f"Unknown strategy type: {strategy_type}")

if __name__ == "__main__":
    main()
