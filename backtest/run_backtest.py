import asyncio
from core.db_api import fetch_all_trades  # Assumes you have this
from backtest.strategy import moving_average_crossover
from backtest.portfolio import BacktestPortfolio


async def main():
    trades = await fetch_all_trades("BTC-USD")  # Or whatever symbol
    print(f"Loaded {len(trades)} trades")

    signals = moving_average_crossover(trades)
    portfolio = BacktestPortfolio()

    for action, timestamp, price in signals:
        if action == "buy":
            portfolio.buy(price, timestamp)
        elif action == "sell":
            portfolio.sell(price, timestamp)

    final_value = portfolio.value(price)
    print(f"Final portfolio value: ${final_value:.2f}")
    for entry in portfolio.history:
        print(entry)


if __name__ == "__main__":
    asyncio.run(main())