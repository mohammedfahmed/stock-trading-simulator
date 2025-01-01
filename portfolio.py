import pandas as pd
import numpy as np

class Portfolio:
    def __init__(self, initial_balance=10000):
        """
        Initializes the Portfolio with an initial balance and no positions.
        
        Args:
            initial_balance (float): Initial capital for the portfolio.
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0  # 0 = no position, 1 = long position
        self.shares = 0  # Number of shares held

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
            max_shares = self.balance // price  # Maximum shares we can buy with available balance
            if max_shares > 0:
                self.shares = max_shares
                self.balance -= self.shares * price  # Deduct cost of shares from balance
                self.position = 1  # We are now in a long position
        elif signal == -1 and self.position == 1:  # Sell signal (exit long position)
            if self.shares > 0:
                self.balance += self.shares * price  # Add proceeds from selling shares
                self.shares = 0  # No more shares held
                self.position = 0  # We no longer have any position

        return {
            'balance': self.balance,
            'shares': self.shares,
            'position': self.position,
            'total_value': self.balance + (self.shares * price)  # Total value = cash + value of shares held
        }
