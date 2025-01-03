import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
import streamlit as st



def configure_strategy_parameters(strategy_type):
    """Configures parameters based on the selected strategy type."""
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


def calculate_portfolio_value(cash, shares, current_price):
    return cash + (shares * current_price)

def calculate_returns(initial_value, final_value):
    return ((final_value - initial_value) / initial_value) * 100


def format_currency(value):
    return f"${value:,.2f}"


def preprocess_data(data):
    return data.ffill()


# def visualize_backtest_results(results):
#     """
#     Visualize cumulative returns and the equity curve.
    
#     Args:
#         results (pandas.DataFrame): Backtesting results.
#     """
#     plt.figure(figsize=(12, 6))

#     # Plot cumulative returns
#     plt.subplot(2, 1, 1)
#     plt.plot(results['Cumulative_Returns'], label='Benchmark', color='blue')
#     plt.plot(results['Strategy_Cumulative_Returns'], label='Strategy', color='orange')
#     plt.title('Cumulative Returns')
#     plt.legend()

#     # Plot equity curve
#     plt.subplot(2, 1, 2)
#     plt.plot(results['Portfolio_Value'], color='green')
#     plt.title('Equity Curve')

#     plt.tight_layout()
#     plt.show()


# def execute_trade(cash, shares, price, action, quantity, transaction_cost=0):
#     """Execute a trade with transaction costs and return updated cash and shares."""
#     if action == 'buy' and cash >= price * quantity + transaction_cost:
#         cash -= price * quantity + transaction_cost
#         shares += quantity
#     elif action == 'sell' and shares >= quantity:
#         cash += price * quantity - transaction_cost
#         shares -= quantity
#     return cash, shares



def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    """
    Calculate the Sharpe Ratio.
    
    Args:
        returns (pandas.Series): Portfolio returns.
        risk_free_rate (float): Annual risk-free rate.
    
    Returns:
        float: Sharpe Ratio.
    """
    excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()


def calculate_max_drawdown(returns):
    """
    Calculate the maximum drawdown of a portfolio.
    
    Args:
        returns (pandas.Series): Portfolio returns.
    
    Returns:
        float: Maximum drawdown percentage.
    """
    cumulative_returns = (1 + returns).cumprod()
    rolling_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - rolling_max) / rolling_max
    return drawdown.min() * 100


def calculate_sortino_ratio(returns, target_return=0.0):
    """
    Calculate the Sortino Ratio.
    
    Args:
        returns (pandas.Series): Portfolio returns.
        target_return (float): Target return for the portfolio.
    
    Returns:
        float: Sortino Ratio.
    """
    downside_deviation = np.sqrt(np.mean(np.minimum(returns - target_return, 0) ** 2))
    return (returns.mean() - target_return) / downside_deviation if downside_deviation > 0 else np.inf


def calculate_calmar_ratio(returns):
    """
    Calculate the Calmar Ratio.
    
    Args:
        returns (pandas.Series): Portfolio returns.
    
    Returns:
        float: Calmar Ratio.
    """
    annualized_return = (1 + returns).prod() ** (252 / len(returns)) - 1
    max_drawdown = calculate_max_drawdown(returns)
    return annualized_return / (max_drawdown / 100) if max_drawdown != 0 else np.inf


def optimize_portfolio(returns, risk_free_rate=0.01, target_return=0.0):
    """
    Optimize portfolio weights using the Efficient Frontier.
    
    Args:
        returns (pandas.DataFrame): Asset returns.
        risk_free_rate (float): Risk-free rate of return.
        target_return (float): Target return for the portfolio.
    
    Returns:
        dict: Optimal weights and portfolio statistics.
    """
    def portfolio_return(weights):
        return np.sum(returns.mean() * weights) * 252

    def portfolio_volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

    def min_variance(weights):
        return portfolio_volatility(weights)

    def neg_sharpe_ratio(weights):
        return -((portfolio_return(weights) - risk_free_rate) / portfolio_volatility(weights))

    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    bounds = tuple((0, 1) for _ in range(returns.shape[1]))
    initial_weights = np.full(returns.shape[1], 1.0 / returns.shape[1])

    min_variance_weights = minimize(min_variance, initial_weights, bounds=bounds, constraints=constraints)
    max_sharpe_weights = minimize(neg_sharpe_ratio, initial_weights, bounds=bounds, constraints=constraints)

    return {
        'min_variance': {'weights': min_variance_weights.x, 'volatility': portfolio_volatility(min_variance_weights.x)},
        'max_sharpe': {'weights': max_sharpe_weights.x, 'volatility': portfolio_volatility(max_sharpe_weights.x)}
    }


def analyze_drawdown(results):
    """
    Analyze drawdown of the backtesting results.
    
    Args:
        results (pandas.DataFrame): Backtesting results.
    
    Returns:
        float: Maximum drawdown.
    """
    cumulative_returns = results['Strategy_Cumulative_Returns']
    rolling_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - rolling_max) / rolling_max
    return drawdown.min() * 100


def analyze_win_rate(results):
    """
    Analyze win rate of the backtesting results.
    
    Args:
        results (pandas.DataFrame): Backtesting results.
    
    Returns:
        float: Win rate percentage.
    """
    winning_trades = (results['Strategy_Returns'] > 0).sum()
    total_trades = results['Position'].diff().ne(0).sum()
    return (winning_trades / total_trades) * 100 if total_trades > 0 else 0


def apply_stop_loss(results, stop_loss_pct=0.05):
    """
    Apply stop-loss to the backtesting results.
    
    Args:
        results (pandas.DataFrame): Backtesting results.
        stop_loss_pct (float): Stop-loss percentage.
    
    Returns:
        pandas.DataFrame: Backtesting results with stop-loss applied.
    """
    results['Stop_Loss_Price'] = results['Close'] * (1 - stop_loss_pct)

    for i in range(1, len(results)):
        if results.iloc[i]['Position'] == 1 and results.iloc[i]['Close'] < results.iloc[i]['Stop_Loss_Price']:
            results.at[results.index[i], 'Signal'] = -1  # Sell signal
            results.at[results.index[i], 'Stop_Loss_Triggered'] = True
        else:
            results.at[results.index[i], 'Stop_Loss_Triggered'] = False

    return results
