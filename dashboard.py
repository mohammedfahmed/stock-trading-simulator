import streamlit as st
# from data_loader import fetch_stock_data
from simulator import Simulator, Strategy
from visualize import visualize_backtest_results


st.set_page_config(
    page_title="Trading Strategy Dashboard",
    layout="wide"
)

def main():

    st.title("Trading Strategy Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker = st.text_input("Stock Symbol", value="AAPL")
    with col2:
        period = st.selectbox("Time Period", ["1y", "2y", "5y", "max"], index=0)
    with col3:
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

    simulator = Simulator()
    strategy = Strategy()

    strategy_params = strategy.configure_strategy_parameters(strategy_type)

    raw_data = simulator.fetch_stock_data(ticker, period)
    if raw_data is None or raw_data.empty:
        st.error(f"No data available for {ticker}. Please check the stock symbol.")
        return

    signals = strategy.generate_signals(strategy_type, raw_data, strategy_params)
    results = simulator.execute_trade(raw_data, signals)

    st.subheader("Performance Metrics")
    metrics = simulator.calculate_metrics(results)
    st.write(metrics)

    st.subheader("Backtest Visualization")
    st.altair_chart(visualize_backtest_results(results))
    st.dataframe(results)



if __name__ == "__main__":
    main()
