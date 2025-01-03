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

    def simulate_trading(self, df, signals, take_profit=0.05, stop_loss=0.02):
        """
        Simulates backtesting by buying based on signals and selling only on take-profit or stop-loss.

        Args:
            df (pandas.DataFrame): DataFrame containing stock data with 'Close' prices.
            signals (pandas.Series): Series containing buy signals (1.0: Buy, 0.0: Hold).
            take_profit (float): Take-profit percentage (e.g., 0.05 for 5% profit).
            stop_loss (float): Stop-loss percentage (e.g., 0.02 for 2% loss).

        Returns:
            pandas.DataFrame: DataFrame containing backtesting results.
        """
        results = signals.to_frame(name='Signal').copy()
        results['Close'] = df['Close']
        results['Shares'] = 0.0
        results['Balance'] = self.initial_balance
        results['Transaction_Cost'] = 0.0
        results['Portfolio_Value'] = self.initial_balance
        results['Position'] = 0
        results['Buy_Price'] = np.nan

        # Initialize state variables
        position_open = False
        buy_price = 0.0

        st.dataframe(results)

        for i in range(len(results)):
            if results.index[i] not in results.index:
                # Skip invalid indices
                continue
                
            if results['Signal'].iloc[i] == 1 and not position_open:
                # Execute buy action
                shares = (results['Balance'].iloc[i] - self.transaction_cost) / results['Close'].iloc[i]
                results.at[i, 'Shares'] = shares
                results.at[i, 'Transaction_Cost'] = self.transaction_cost
                results.at[i, 'Balance'] -= shares * results['Close'].iloc[i] + self.transaction_cost
                results.at[i, 'Position'] = 1
                results.at[i, 'Buy_Price'] = results['Close'].iloc[i]
                buy_price = results['Close'].iloc[i]
                position_open = True

            elif position_open:
                # Evaluate exit conditions
                current_price = results['Close'].iloc[i]
                price_change = (current_price - buy_price) / buy_price

                if price_change >= take_profit or price_change <= -stop_loss:
                    # Execute sell action
                    shares = results['Shares'].iloc[i - 1]
                    results.at[i, 'Balance'] += shares * current_price - self.transaction_cost
                    results.at[i, 'Transaction_Cost'] = self.transaction_cost
                    results.at[i, 'Shares'] = 0
                    results.at[i, 'Position'] = 0
                    position_open = False

            # Carry forward values for non-trading days
            if i > 0:
                results.at[i, 'Shares'] = results['Shares'].iloc[i - 1] if results['Shares'].iloc[i] == 0 else results['Shares'].iloc[i]
                results.at[i, 'Balance'] = results['Balance'].iloc[i] if results['Balance'].iloc[i] > 0 else results['Balance'].iloc[i - 1]
                results.at[i, 'Position'] = results['Position'].iloc[i - 1]

        # Calculate portfolio value
        results['Portfolio_Value'] = results['Balance'] + (results['Shares'] * results['Close'])
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
        if 'Portfolio_Value' not in results.columns:
            return {
                'total_return': 0,
                'sharpe_ratio': 0,
                'max_drawdown': 0,
                'win_rate': 0
            }

        # Total Return
        metrics = {'total_return': (results['Portfolio_Value'].iloc[-1] - self.initial_balance) / self.initial_balance * 100}

        # Sharpe Ratio (assuming risk-free rate of 0.01)
        risk_free_rate = 0.01
        daily_returns = results['Portfolio_Value'].pct_change().fillna(0)
        excess_returns = daily_returns - risk_free_rate / 252
        metrics['sharpe_ratio'] = (np.sqrt(252) * excess_returns.mean() / excess_returns.std()) if excess_returns.std() > 0 else 0

        # Maximum Drawdown
        rolling_max = results['Portfolio_Value'].expanding().max()
        drawdowns = (results['Portfolio_Value'] - rolling_max) / rolling_max
        metrics['max_drawdown'] = drawdowns.min() * 100

        # Win Rate
        winning_trades = (daily_returns > 0).sum()
        total_trades = len(daily_returns[daily_returns != 0])
        metrics['win_rate'] = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

        return metrics
