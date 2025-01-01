import yfinance as yf
import pandas as pd
import numpy as np

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

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
  """
  Calculates the Sharpe Ratio.

  Args:
      returns: Series of portfolio returns.
      risk_free_rate: Annual risk-free rate.

  Returns:
      float: Sharpe Ratio.
  """
  excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
  return np.sqrt(252) * excess_returns.mean() / excess_returns.std()

def calculate_max_drawdown(returns):
  """
  Calculates the maximum drawdown of a portfolio.

  Args:
      returns: Series of portfolio returns.

  Returns:
      float: Maximum drawdown percentage.
  """
  cumulative_returns = (1 + returns).cumprod()
  rolling_max = cumulative_returns.cummax()
  drawdown = (cumulative_returns - rolling_max) / rolling_max
  return drawdown.min() * 100

def calculate_sortino_ratio(returns, target_return=0.0):
  """
  Calculates the Sortino Ratio.

  Args:
      returns: Series of portfolio returns.
      target_return: Target return for the portfolio.

  Returns:
      float: Sortino Ratio.
  """
  downside_deviation = np.sqrt(np.mean((np.minimum(returns - target_return, 0)) ** 2))
  if downside_deviation == 0:
    return np.inf
  return (returns.mean() - target_return) / downside_deviation

def calculate_calmar_ratio(returns, period='1y'):
  """
  Calculates the Calmar Ratio.

  Args:
      returns: Series of portfolio returns.
      period: Time period for calculating annualized return.

  Returns:
      float: Calmar Ratio.
  """
  annualized_return = (1 + returns).prod() ** (252 / len(returns)) - 1
  max_drawdown = calculate_max_drawdown(returns)
  return annualized_return / (max_drawdown / 100) 




import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

def preprocess_data(data):
  """
  Preprocesses the stock data.

  Args:
      data: pandas.DataFrame containing stock data.

  Returns:
      pandas.DataFrame: Preprocessed stock data.
  """
  # Fill missing values (if any)
  data = data.fillna(method='ffill') 

  # Normalize data (optional)
  # data = (data - data.mean()) / data.std() 

  return data

def visualize_backtest_results(results):
  """
  Visualizes backtesting results.

  Args:
      results: pandas.DataFrame containing backtesting results.
  """
  plt.figure(figsize=(12, 6))

  # Plot cumulative returns
  plt.subplot(2, 1, 1)
  plt.plot(results['Cumulative_Returns'], label='Benchmark')
  plt.plot(results['Strategy_Cumulative_Returns'], label='Strategy')
  plt.title('Cumulative Returns')
  plt.legend()

  # Plot equity curve
  plt.subplot(2, 1, 2)
  plt.plot(results['Portfolio_Value'])
  plt.title('Equity Curve')

  plt.tight_layout()
  plt.show()

def optimize_portfolio(returns, risk_free_rate=0.01, target_return=0.0):
  """
  Optimizes portfolio weights using the Efficient Frontier.

  Args:
      returns: DataFrame of asset returns.
      risk_free_rate: Risk-free rate of return.
      target_return: Target return for the portfolio.

  Returns:
      dict: Dictionary containing optimal weights and portfolio statistics.
  """
  from scipy.optimize import minimize

  def portfolio_return(weights):
    return np.sum(returns.mean() * weights) * 252

  def portfolio_volatility(weights):
    return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

  def min_variance(weights):
    return portfolio_volatility(weights)

  def neg_sharpe_ratio(weights):
    return -((portfolio_return(weights) - risk_free_rate) / portfolio_volatility(weights))

  # Constraints: weights must sum to 1
  constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

  # Bounds: weights must be between 0 and 1
  bounds = tuple((0, 1) for x in range(len(returns.columns)))

  # Initial guess: equal weights
  initial_weights = np.array(len(returns.columns) * [1. / len(returns.columns)])

  # Minimize variance
  min_variance_weights = minimize(min_variance, initial_weights, bounds=bounds, constraints=constraints)

  # Maximize Sharpe Ratio
  max_sharpe_weights = minimize(neg_sharpe_ratio, initial_weights, bounds=bounds, constraints=constraints)

  # Target return portfolio
  def target_return_portfolio(weights):
    return portfolio_return(weights) - target_return

  target_return_weights = minimize(min_variance, initial_weights, bounds=bounds, constraints=(constraints, {'type': 'eq', 'fun': target_return_portfolio}))

  return {
      'min_variance': {'weights': min_variance_weights.x, 'volatility': portfolio_volatility(min_variance_weights.x)},
      'max_sharpe': {'weights': max_sharpe_weights.x, 'volatility': portfolio_volatility(max_sharpe_weights.x)},
      'target_return': {'weights': target_return_weights.x, 'volatility': portfolio_volatility(target_return_weights.x)}
  }



import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

def preprocess_data(data):
  """
  Preprocesses the stock data.

  Args:
      data: pandas.DataFrame containing stock data.

  Returns:
      pandas.DataFrame: Preprocessed stock data.
  """
  # Fill missing values (if any)
  data = data.fillna(method='ffill') 

  # Normalize data (optional)
  # data = (data - data.mean()) / data.std() 

  return data

def visualize_backtest_results(results):
  """
  Visualizes backtesting results.

  Args:
      results: pandas.DataFrame containing backtesting results.
  """
  plt.figure(figsize=(12, 6))

  # Plot cumulative returns
  plt.subplot(2, 1, 1)
  plt.plot(results['Cumulative_Returns'], label='Benchmark')
  plt.plot(results['Strategy_Cumulative_Returns'], label='Strategy')
  plt.title('Cumulative Returns')
  plt.legend()

  # Plot equity curve
  plt.subplot(2, 1, 2)
  plt.plot(results['Portfolio_Value'])
  plt.title('Equity Curve')

  plt.tight_layout()
  plt.show()

def optimize_portfolio(returns, risk_free_rate=0.01, target_return=0.0):
  """
  Optimizes portfolio weights using the Efficient Frontier.

  Args:
      returns: DataFrame of asset returns.
      risk_free_rate: Risk-free rate of return.
      target_return: Target return for the portfolio.

  Returns:
      dict: Dictionary containing optimal weights and portfolio statistics.
  """
  from scipy.optimize import minimize

  def portfolio_return(weights):
    return np.sum(returns.mean() * weights) * 252

  def portfolio_volatility(weights):
    return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

  def min_variance(weights):
    return portfolio_volatility(weights)

  def neg_sharpe_ratio(weights):
    return -((portfolio_return(weights) - risk_free_rate) / portfolio_volatility(weights))

  # Constraints: weights must sum to 1
  constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

  # Bounds: weights must be between 0 and 1
  bounds = tuple((0, 1) for x in range(len(returns.columns)))

  # Initial guess: equal weights
  initial_weights = np.array(len(returns.columns) * [1. / len(returns.columns)])

  # Minimize variance
  min_variance_weights = minimize(min_variance, initial_weights, bounds=bounds, constraints=constraints)

  # Maximize Sharpe Ratio
  max_sharpe_weights = minimize(neg_sharpe_ratio, initial_weights, bounds=bounds, constraints=constraints)

  # Target return portfolio
  def target_return_portfolio(weights):
    return portfolio_return(weights) - target_return

  target_return_weights = minimize(min_variance, initial_weights, bounds=bounds, constraints=(constraints, {'type': 'eq', 'fun': target_return_portfolio}))

  return {
      'min_variance': {'weights': min_variance_weights.x, 'volatility': portfolio_volatility(min_variance_weights.x)},
      'max_sharpe': {'weights': max_sharpe_weights.x, 'volatility': portfolio_volatility(max_sharpe_weights.x)},
      'target_return': {'weights': target_return_weights.x, 'volatility': portfolio_volatility(target_return_weights.x)}
  }

def analyze_drawdown(results):
  """
  Analyzes drawdown of the backtesting results.

  Args:
      results: pandas.DataFrame containing backtesting results.

  Returns:
      float: Maximum drawdown.
  """
  cumulative_returns = results['Strategy_Cumulative_Returns']
  rolling_max = cumulative_returns.cummax()
  drawdown = (cumulative_returns - rolling_max) / rolling_max
  max_drawdown = drawdown.min() * 100
  return max_drawdown

def analyze_win_rate(results):
  """
  Analyzes win rate of the backtesting results.

  Args:
      results: pandas.DataFrame containing backtesting results.

  Returns:
      float: Win rate percentage.
  """
  winning_trades = (results['Strategy_Returns'] > 0).sum()
  total_trades = (results['Position'].diff() != 0).sum()
  win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
  return win_rate

def apply_stop_loss(results, stop_loss_pct=0.05):
  """
  Applies stop-loss to the backtesting results.

  Args:
      results: pandas.DataFrame containing backtesting results.
      stop_loss_pct: Stop-loss percentage.

  Returns:
      pandas.DataFrame: Backtesting results with stop-loss applied.
  """
  results['Stop_Loss_Price'] = results['Close'] * (1 - stop_loss_pct)

  for i in range(1, len(results)):
    if results.iloc[i]['Position'] == 1:  # Long position
      if results.iloc[i]['Close'] < results.iloc[i]['Stop_Loss_Price']:
        results.at[results.index[i], 'Signal'] = -1  # Sell signal
        results.at[results.index[i], 'Stop_Loss_Triggered'] = True
      else:
        results.at[results.index[i], 'Stop_Loss_Triggered'] = False

  return results

# You can add more utility functions here, such as:
# - Backtesting result analysis functions (e.g., Calmar Ratio, Sortino Ratio)
# - Risk management functions (e.g., trailing stop-loss)