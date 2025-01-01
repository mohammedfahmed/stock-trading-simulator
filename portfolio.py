import pandas as pd
import numpy as np

class Portfolio:
    def __init__(self, initial_balance=10000, transaction_cost=10):
        """
        Initializes the Portfolio with an initial balance and no positions.
        
        Args:
            initial_balance (float): Initial capital for the portfolio.
            transaction_cost (float): Transaction cost per trade (fixed amount).
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0  # 0 = no position, 1 = long position
        self.shares = 0  # Number of shares held
        self.transaction_cost = transaction_cost

    def execute_trade(self, price, signal):
        """
        Executes a trade based on the signal and available balance.
        
        Args:
            price (float): The price of the asset.
            signal (int): The trading signal. 1 = Buy, -1 = Sell, 0 = Hold.
        
        Returns:
            dict: Updated portfolio information including balance, shares, and total value.
        """
        if signal == 1 and self.position == 0:  # Buy signal (enter long position)
            max_shares = (self.balance - self.transaction_cost) // price  # Maximum shares we can buy with available balance
            if max_shares > 0:
                self.shares = max_shares
                self.balance -= (self.shares * price + self.transaction_cost)  # Deduct cost of shares and transaction cost from balance
                self.position = 1  # We are now in a long position
        elif signal == -1 and self.position == 1:  # Sell signal (exit long position)
            if self.shares > 0:
                self.balance += (self.shares * price - self.transaction_cost)  # Add proceeds from selling shares minus transaction cost
                self.shares = 0  # No more shares held
                self.position = 0  # We no longer have any position

        return {
            'balance': self.balance,
            'shares': self.shares,
            'position': self.position,
            'total_value': self.balance + (self.shares * price)  # Total value = cash + value of shares held
        }

    def backtest(self, df, signals):
        """
        Performs backtesting on the strategy using portfolio simulation (vectorized).

        Args:
            df (pandas.DataFrame): DataFrame containing stock data.
            signals (pandas.Series): Series containing trading signals 
                                      (1.0: Buy, -1.0: Sell, 0.0: Hold).

        Returns:
            pandas.DataFrame: DataFrame containing backtesting results 
                                (balance, shares, portfolio value, etc.).
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

        return results
