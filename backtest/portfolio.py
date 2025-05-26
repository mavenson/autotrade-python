# backtest/portfolio.py

class BacktestPortfolio:
    def __init__(self, starting_cash=1000.0):
        self.cash = starting_cash
        self.position = 0
        self.history = []

    def buy(self, price, timestamp):
        if self.cash > 0:
            self.position = self.cash / price
            self.cash = 0
            self.history.append((timestamp, "BUY", price))

    def sell(self, price, timestamp):
        if self.position > 0:
            self.cash = self.position * price
            self.position = 0
            self.history.append((timestamp, "SELL", price))

    def value(self, price):
        return self.cash + self.position * price
