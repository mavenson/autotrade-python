# backtest/run_backtest.py

from backtest.strategy import moving_average_crossover
from backtest.portfolio import BacktestPortfolio


def run_backtest(trades):
    print("Running backtest...")
    signals = moving_average_crossover(trades)
    portfolio = BacktestPortfolio()

    for action, timestamp, price in signals:
        if action == "buy":
            portfolio.buy(price, timestamp)
        elif action == "sell":
            portfolio.sell(price, timestamp)

    final_value = portfolio.value(float(trades[-1]["price"]))
    print(f"Final portfolio value: ${final_value:.2f}")
    print(f"\nExecuted {len(portfolio.history)} trades:")
    print(f"Final portfolio value: ${final_value:.2f}")
