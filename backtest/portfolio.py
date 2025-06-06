# backtest/portfolio.py

from backtest.trade_meta import TradeMeta

class BacktestPortfolio:
    def __init__(self, starting_cash=1000.0, fee_rates=None):
        self.cash = starting_cash
        self.position = 0
        self.history = []
        self.total_fees_paid = 0.0
        self.fee_rates = fee_rates or {"taker": 0.001}

    def get_fee_rate(self, trade_type: str) -> float:
        return self.fee_rates.get(trade_type, 0.001)

    def buy(self, trade: TradeMeta):
        if self.cash > 0:
            rate = self.get_fee_rate(trade.trade_type)
            fee = self.cash * rate
            investable = self.cash - fee
            self.position = investable / trade.price
            self.cash = 0
            self.total_fees_paid += fee
            self.history.append((trade.timestamp, "BUY", trade.price, fee))

    def sell(self, trade: TradeMeta):
        if self.position > 0:
            gross = self.position * trade.price
            rate = self.get_fee_rate(trade.trade_type)
            fee = gross * rate
            self.cash = gross - fee
            self.position = 0
            self.total_fees_paid += fee
            self.history.append((trade.timestamp, "SELL", trade.price, fee))

    def value(self, price: float) -> float:
        return self.cash + self.position * price
