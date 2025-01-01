# Quantitative Trading Strategies and Backtesting Framework

This Python framework provides tools for developing, testing, and optimizing quantitative trading strategies. It includes utility functions for:

- **Fetching Stock Data**: Retrieves historical stock data from Yahoo Finance.
- **Data Preprocessing**: Handles missing values and optional normalization of stock data.
- **Strategy Implementation**: Allows you to implement and backtest trading strategies based on technical indicators or other signals.
- **Backtesting Analysis**:
  - Calculates key performance metrics such as Sharpe Ratio, Maximum Drawdown, and Win Rate.
  - Analyzes the equity curve and cumulative returns.
- **Portfolio Optimization**: Optimizes asset allocation using the Efficient Frontier and other metrics.
- **Risk Management**: Implements basic risk management features like stop-loss mechanisms.

---

## Features

- **Data Collection**: Fetches stock data from Yahoo Finance for any stock ticker.
- **Preprocessing**: Cleans and normalizes stock data.
- **Backtesting**: Tests trading strategies and evaluates them with financial metrics.
- **Visualization**: Generates graphs for backtest results, showing cumulative returns and drawdowns.
- **Optimization**: Provides tools for portfolio optimization based on historical asset returns.

---

## Installation

To get started, clone the repository and install the required dependencies.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/quantitative-trading-backtesting.git
   cd quantitative-trading-backtesting

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Make sure you have the following Python libraries:
   - `yfinance` (for fetching stock data)
   - `pandas` (for data manipulation)
   - `numpy` (for numerical operations)
   - `matplotlib` (for plotting results)
   - `scipy` (for optimization)

---

## Usage Examples

### 1. Import Libraries

```python
import yfinance as yf
import pandas as pd
from utils import fetch_stock_data, preprocess_data, visualize_backtest_results, \
                   calculate_sharpe_ratio, calculate_max_drawdown, analyze_win_rate, \
                   apply_stop_loss, analyze_drawdown, optimize_portfolio
```

### 2. Fetch Stock Data

Use the `fetch_stock_data` function to retrieve historical stock data.

```python
# Fetch historical stock data for Apple
symbol = 'AAPL'  # Replace with your desired stock symbol
data = fetch_stock_data(symbol)

# Optionally preprocess data (e.g., fill missing values, normalize)
data = preprocess_data(data)  # Set normalize=True to apply normalization
```

### 3. Implement a Trading Strategy

Here's an example of implementing a **Moving Average Crossover** strategy:

```python
def moving_average_crossover(data, short_window, long_window):
    """
    Implements a simple moving average crossover strategy.

    Args:
        data: DataFrame containing stock data with 'Close' column.
        short_window: Window size for the short moving average.
        long_window: Window size for the long moving average.

    Returns:
        Pandas Series with trading signals (1.0 for buy, -1.0 for sell, 0.0 for hold).
    """
    short_ma = data['Close'].rolling(window=short_window).mean()
    long_ma = data['Close'].rolling(window=long_window).mean()

    signals = pd.Series(0.0, index=data.index)
    signals[short_ma > long_ma] = 1.0  # Buy signal
    signals[short_ma < long_ma] = -1.0  # Sell signal

    return signals

# Apply the strategy to generate trading signals
signals = moving_average_crossover(data, short_window=20, long_window=50)
```

### 4. Backtest the Strategy

To backtest the strategy, combine the trading signals with daily returns and apply risk management.

```python
# Calculate daily returns
daily_returns = data['Close'].pct_change()

# Create a DataFrame with returns and signals
results = pd.DataFrame({'Close': data['Close'], 'Returns': daily_returns, 'Signal': signals})

# Apply stop-loss (optional)
results = apply_stop_loss(results, stop_loss_pct=0.05)

# Calculate key performance metrics
sharpe_ratio = calculate_sharpe_ratio(results['Returns'])
max_drawdown = analyze_drawdown(results)  # Maximum drawdown in percentage
win_rate = analyze_win_rate(results)

# Output metrics
print("Sharpe Ratio:", sharpe_ratio)
print("Maximum Drawdown:", max_drawdown, "%")
print("Win Rate:", win_rate, "%")

# Visualize the backtest results
visualize_backtest_results(results)
```

### 5. Portfolio Optimization

If you have return data for multiple assets, use the following code to optimize portfolio weights for maximum Sharpe Ratio.

```python
# Example: Assuming you have return data for multiple assets
asset_returns = pd.DataFrame({
    'Asset1': [0.01, 0.02, -0.01, 0.005],  # Example returns
    'Asset2': [0.005, 0.015, 0.01, -0.02],
    # Add more assets here
})

# Optimize portfolio for maximum Sharpe Ratio
optimal_weights = optimize_portfolio(asset_returns)['max_sharpe']

# Output optimal portfolio weights
print("Optimal Portfolio Weights:", optimal_weights['weights'])
```

---

## Key Functions Overview

- **`fetch_stock_data(symbol)`**: Fetches historical stock data from Yahoo Finance.
- **`preprocess_data(data, normalize=False)`**: Preprocesses stock data (e.g., filling missing values and optional normalization).
- **`moving_average_crossover(data, short_window, long_window)`**: Implements a simple moving average crossover strategy.
- **`apply_stop_loss(results, stop_loss_pct)`**: Applies a stop-loss mechanism with a specified percentage threshold.
- **`calculate_sharpe_ratio(returns)`**: Computes the Sharpe Ratio based on strategy returns.
- **`analyze_drawdown(results)`**: Calculates maximum drawdown from backtest results.
- **`analyze_win_rate(results)`**: Computes the win rate of the strategy.
- **`visualize_backtest_results(results)`**: Plots the equity curve and cumulative returns of the backtest.
- **`optimize_portfolio(asset_returns)`**: Optimizes asset weights for a given portfolio using the Efficient Frontier and other criteria.

---

## Requirements

Make sure to install the required Python libraries:

```bash
pip install yfinance pandas numpy matplotlib scipy
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Explanation of Changes:
- **Clarified Functionality**: The `README.md` now clearly explains the project’s purpose, key features, and how to use the code.
- **Detailed Code Examples**: Added explanations and more consistent formatting for the examples.
- **Installation Instructions**: Provided the installation steps for dependencies.
- **Metrics and Optimization**: Expanded on the backtesting, performance metrics, and portfolio optimization functionality. 

