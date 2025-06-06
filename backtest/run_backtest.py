# backtest/run_backtest.py

import asyncio
from backtest.strategy import (
    moving_average_crossover,
    moving_average_crossover_candles
)
from backtest.portfolio import BacktestPortfolio
from backtest.trade_meta import TradeMeta
from client.services.queries import fetch_all_trades
from client.services.candle_utils import get_candles


async def run_trade_ma_strategy(
    symbol: str,
    short_window: int = 5,
    long_window: int = 20,
    starting_cash: float = 1000.0,
    fee_rates: dict = None,
    exchange: str = "coinbase"
):
    print(f"\nRunning Trade-Based MA Strategy on {symbol}")
    trades = await fetch_all_trades(symbol)
    signals = moving_average_crossover(trades, short_window, long_window)
    portfolio = BacktestPortfolio(starting_cash, fee_rates=fee_rates)

    for action, timestamp, price in signals:
        trade = TradeMeta(price=float(price), timestamp=timestamp, trade_type="taker", exchange=exchange)
        if action == "buy":
            portfolio.buy(trade)
        elif action == "sell":
            portfolio.sell(trade)

    final_value = portfolio.value(float(trades[-1]["price"]))
    print_results(portfolio, final_value)


async def run_candle_ma_strategy(
    symbol: str,
    interval: str = "1m",
    short_window: int = 5,
    long_window: int = 20,
    starting_cash: float = 1000.0,
    fee_rates: dict = None,
    exchange: str = "coinbase",
    source: str = "generated"
):
    print(f"\nRunning Candle-Based MA Strategy on {symbol} ({interval} candles from {source})")
    try:
        candles = await get_candles(symbol, interval, source=source)
    except Exception as e:
        print(f"❌ Failed to fetch candles: {e}")
        return

    if not candles:
        print("⚠️ No candles returned. Try a different interval or data source.")
        return

    signals = moving_average_crossover_candles(candles, short_window, long_window)
    if not signals:
        print("⚠️ No signals generated. Try adjusting your MA windows.")
        return

    portfolio = BacktestPortfolio(starting_cash, fee_rates=fee_rates)

    for action, timestamp, price in signals:
        trade = TradeMeta(price=float(price), timestamp=timestamp, trade_type="taker", exchange=exchange)
        if action == "buy":
            portfolio.buy(trade)
        elif action == "sell":
            portfolio.sell(trade)

    final_value = portfolio.value(float(candles[-1]["close"]))
    print_results(portfolio, final_value)


def print_results(portfolio: BacktestPortfolio, final_value: float):
    print(f"\nFinal portfolio value: ${final_value:.2f}")
    print(f"Total trades executed: {len(portfolio.history)}")
    print(f"Total fees paid: ${portfolio.total_fees_paid:.2f}")
    print("\nTrade History:")
    for entry in portfolio.history:
        print(entry)
