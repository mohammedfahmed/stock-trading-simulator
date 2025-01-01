
import pandas as pd
import numpy as np

class Portfolio:
    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0
        self.shares = 0
        
    def execute_trade(self, price, signal):
        """Execute trade based on signal and available balance"""
        if signal == 1 and self.position <= 0:  # Buy signal
            max_shares = self.balance // price
            if max_shares > 0:
                self.shares = max_shares
                self.balance -= self.shares * price
                self.position = 1
        elif signal == -1 and self.position >= 0:  # Sell signal
            if self.shares > 0:
                self.balance += self.shares * price
                self.shares = 0
                self.position = -1
        
        return {
            'balance': self.balance,
            'shares': self.shares,
            'position': self.position,
            'total_value': self.balance + (self.shares * price)
        }
