# Stock Portfolio Analysis and Optimization

This project provides a set of Python tools for analyzing and optimizing stock portfolios. It leverages historical stock data from Yahoo Finance and performs various risk and performance analyses, including calculating key financial ratios and portfolio optimizations.

## Features

- **Fetch Historical Stock Data**: Fetches stock data from Yahoo Finance for a given symbol and time period.
- **Portfolio Performance Metrics**: Includes metrics like Sharpe Ratio, Sortino Ratio, Max Drawdown, and Calmar Ratio.
- **Portfolio Optimization**: Optimizes portfolio weights using the Efficient Frontier, maximizing the Sharpe ratio, minimizing variance, and targeting a specific return.
- **Backtest Visualization**: Visualizes backtesting results, including cumulative returns and equity curves.
- **Risk Management**: Includes stop-loss functionality for backtesting portfolio strategies.

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/stock-portfolio-analysis.git
    cd stock-portfolio-analysis
    ```

2. **Install Dependencies:**
    You can install the required Python libraries using `pip` or `conda`:
    
    Using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

    Or using `conda`:
    ```bash
    conda install --file requirements.txt
    ```

   Dependencies include:
   - `yfinance`: For fetching stock data from Yahoo Finance.
   - `pandas`: For data manipulation.
   - `numpy`: For numerical operations.
   - `matplotlib`: For visualizations.
   - `scipy`: For optimization functions.
   - `seaborn`: For enhanced data visualizations.

3. **Create a Virtual Environment (Optional but recommended):**

    If you want to set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Usage

### Fetching Stock Data

You can fetch historical stock data for a given symbol and period using the `fetch_stock_data` function:

```python
import yfinance as yf
from your_module import fetch_stock_data

symbol = 'AAPL'
data = fetch_stock_data(symbol, period='1y')
print(data.head())
```

### Calculating Portfolio Metrics

You can calculate various portfolio metrics like the **Sharpe Ratio**, **Sortino Ratio**, and **Max Drawdown**:

```python
import pandas as pd
from your_module import calculate_sharpe_ratio, calculate_max_drawdown, calculate_sortino_ratio

# Assuming `returns` is a pandas Series of daily returns
returns = pd.Series([0.01, -0.02, 0.03, 0.04, -0.01])

sharpe = calculate_sharpe_ratio(returns)
max_drawdown = calculate_max_drawdown(returns)
sortino = calculate_sortino_ratio(returns)

print(f"Sharpe Ratio: {sharpe}")
print(f"Max Drawdown: {max_drawdown}%")
print(f"Sortino Ratio: {sortino}")
```

### Optimizing Portfolio Weights

Optimize portfolio weights based on historical returns:

```python
from your_module import optimize_portfolio
import pandas as pd

# Assuming `returns_df` is a DataFrame of asset returns
returns_df = pd.DataFrame({
    'Asset1': [0.01, -0.02, 0.03, 0.01],
    'Asset2': [0.03, 0.01, -0.02, 0.04],
    'Asset3': [-0.01, 0.02, 0.01, 0.03]
})

optimized = optimize_portfolio(returns_df)

print(f"Min Variance Portfolio: {optimized['min_variance']}")
print(f"Max Sharpe Portfolio: {optimized['max_sharpe']}")
```

### Visualizing Backtest Results

To visualize backtest results, use the `visualize_backtest_results` function:

```python
from your_module import visualize_backtest_results
import pandas as pd

# Assuming `backtest_results` is a DataFrame containing backtest results
backtest_results = pd.DataFrame({
    'Cumulative_Returns': [0.01, 0.03, 0.05, 0.08],
    'Strategy_Cumulative_Returns': [0.02, 0.04, 0.06, 0.10],
    'Portfolio_Value': [10000, 10200, 10500, 10800]
})

visualize_backtest_results(backtest_results)
```

### Applying Stop-Loss to Backtesting

You can apply a stop-loss strategy to your backtesting results:

```python
from your_module import apply_stop_loss
import pandas as pd

# Assuming `backtest_results` contains the necessary columns ('Close', 'Position', etc.)
backtest_results = pd.DataFrame({
    'Close': [150, 145, 160, 155],
    'Position': [1, 1, 0, 1],
    'Strategy_Returns': [0.01, -0.02, 0.03, -0.01]
})

modified_results = apply_stop_loss(backtest_results, stop_loss_pct=0.05)
print(modified_results)
```

## Additional Notes

- **Data Frequency**: The data is daily by default. Ensure your portfolio return calculations take this into account when modifying functions.
- **Risk-free Rate**: The default risk-free rate is set at 1% annual. Adjust this as needed for your analysis.
- **Backtesting**: The backtesting results assume you have a strategy that generates buy/sell signals. Modify the code to suit your strategy.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
