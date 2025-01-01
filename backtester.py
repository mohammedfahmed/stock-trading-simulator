import pandas as pd
import numpy as np

class Backtester:
    """
    Backtester class for performing backtesting on trading strategies.
    """
    def __init__(self, initial_balance=10000, transaction_cost=10):
        """
        Initializes the Backtester with initial balance and optional transaction cost.

        Args:
            initial_balance (float): Initial capital for backtesting.
            transaction_cost (float): Transaction cost per trade (fixed amount).
        """
        self.initial_balance = initial_balance
        self.transaction_cost = transaction_cost


    def backtest(self, df, signals):
        """
        Performs backtesting on the strategy using portfolio simulation (vectorized).

        Args:
            df (pandas.DataFrame): DataFrame containing stock data.
            signals (pandas.Series): Series containing trading signals 
                                    (1.0: Buy, -1.0: Sell, 0.0: Hold).

        Returns:
            pandas.DataFrame: DataFrame containing backtesting results 
                                (balance, shares, portfolio value, returns, etc.).
        """
        # Initialize results DataFrame
        results = signals.to_frame(name='Signal').copy()
        results['Close'] = df['Close']
        results['Position'] = 0  # Start with no position
        results['Shares'] = 0.0
        results['Balance'] = self.initial_balance
        results['Transaction_Cost'] = 0.0
        results['Portfolio_Value'] = self.initial_balance

        # Identify buy and sell signals
        buy_signals = results['Signal'] == 1
        sell_signals = results['Signal'] == -1

        # Calculate shares bought and sold
        results.loc[buy_signals, 'Shares'] = (results['Balance'] - self.transaction_cost) / results['Close']
        results.loc[sell_signals, 'Shares'] = 0

        # Update balance for buy and sell trades
        results.loc[buy_signals, 'Transaction_Cost'] = self.transaction_cost
        results.loc[buy_signals, 'Balance'] -= results['Shares'] * results['Close'] + self.transaction_cost
        results.loc[sell_signals, 'Balance'] += results.shift(1)['Shares'] * results['Close'] - self.transaction_cost

        # Update positions based on signals
        results['Position'] = buy_signals.astype(int) - sell_signals.astype(int)

        # Forward-fill position and balance to track holding periods
        results['Position'] = results['Position'].replace(0, np.nan).ffill().fillna(0).astype(int)
        results['Balance'] = results['Balance'].fillna(method='ffill')

        # Calculate portfolio value
        results['Portfolio_Value'] = results['Balance'] + (results['Shares'] * results['Close'])

        # Calculate returns
        results['Returns'] = results['Close'].pct_change().fillna(0)
        results['Strategy_Returns'] = results['Portfolio_Value'].pct_change().fillna(0)

        # Calculate cumulative returns
        results['Cumulative_Returns'] = (1 + results['Returns']).cumprod()
        results['Strategy_Cumulative_Returns'] = results['Portfolio_Value'] / self.initial_balance

        return results

    def calculate_metrics(self, results):
        """
        Calculates performance metrics.

        Args:
            results (pandas.DataFrame): DataFrame containing backtesting results.

        Returns:
            dict: Dictionary containing performance metrics 
                    (total_return, sharpe_ratio, max_drawdown, win_rate).
        """
        if 'Strategy_Returns' not in results.columns:
            return {
                'total_return': 0,
                'sharpe_ratio': 0,
                'max_drawdown': 0,
                'win_rate': 0
            }

        # Total Return
        metrics = {'total_return': (results['Strategy_Cumulative_Returns'].iloc[-1] - 1) * 100}

        # Sharpe Ratio (assuming risk-free rate of 0.01)
        risk_free_rate = 0.01
        excess_returns = results['Strategy_Returns'] - risk_free_rate / 252
        metrics['sharpe_ratio'] = (np.sqrt(252) * excess_returns.mean() / excess_returns.std()) if excess_returns.std() > 0 else 0

        # Maximum Drawdown
        cum_returns = results['Strategy_Cumulative_Returns']
        rolling_max = cum_returns.expanding().max()
        drawdowns = (cum_returns - rolling_max) / rolling_max
        metrics['max_drawdown'] = drawdowns.min() * 100

        # Win Rate
        winning_trades = (results['Strategy_Returns'] > 0).sum()
        total_trades = (results['Signal'].isin([1, -1])).sum()
        metrics['win_rate'] = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

        return metrics






    # def backtest(self, df, signals):
    #     """
    #     Performs backtesting on the strategy using portfolio simulation.

    #     Args:
    #         df (pandas.DataFrame): DataFrame containing stock data.
    #         signals (pandas.Series): Series containing trading signals 
    #                                   (1.0: Buy, -1.0: Sell, 0.0: Hold).

    #     Returns:
    #         pandas.DataFrame: DataFrame containing backtesting results 
    #                             (balance, shares, portfolio value, returns, etc.).
    #     """
    #     results = signals.to_frame(name='Signal').copy()
    #     results['Close'] = df['Close']
    #     results['Position'] = 0  # Position: 0 = no position, 1 = holding shares
    #     results['Balance'] = self.initial_balance
    #     results['Shares'] = 0
    #     results['Portfolio_Value'] = self.initial_balance
    #     results['Transaction_Cost'] = 0

    #     for i in range(1, len(results)):
    #         prev_pos = results.iloc[i - 1]['Position']
    #         curr_signal = results.iloc[i]['Signal']

    #         if prev_pos == 0 and curr_signal == 1:  # Buy
    #             transaction_cost = self.transaction_cost
    #             shares_to_buy = (results.iloc[i]['Balance'] - transaction_cost) / results.iloc[i]['Close']
    #             if shares_to_buy > 0:
    #                 results.at[results.index[i], 'Shares'] = shares_to_buy
    #                 results.at[results.index[i], 'Balance'] -= (shares_to_buy * results.iloc[i]['Close'] + transaction_cost)
    #                 results.at[results.index[i], 'Position'] = 1

    #         elif prev_pos == 1 and curr_signal == -1:  # Sell
    #             transaction_cost = self.transaction_cost
    #             results.at[results.index[i], 'Balance'] += (results.iloc[i - 1]['Shares'] * results.iloc[i]['Close'] - transaction_cost)
    #             results.at[results.index[i], 'Shares'] = 0
    #             results.at[results.index[i], 'Position'] = 0

    #         # Update Portfolio Value
    #         results.at[results.index[i], 'Portfolio_Value'] = results.iloc[i]['Balance'] + (results.iloc[i]['Shares'] * results.iloc[i]['Close'])

    #     # Post-loop calculations
    #     results['Returns'] = results['Close'].pct_change().fillna(0)
    #     results['Strategy_Returns'] = results['Portfolio_Value'].pct_change().fillna(0)
    #     results['Cumulative_Returns'] = (1 + results['Returns']).cumprod()
    #     results['Strategy_Cumulative_Returns'] = results['Portfolio_Value'] / self.initial_balance

    #     return results