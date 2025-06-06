# client/client_menu.py


import asyncio
from client.services.queries import (
    fetch_all_trades,
    fetch_trade_counts,
    fetch_date_ranges
)
from client.services.fee_config import load_exchange_fees
from backtest.run_backtest import (
    run_trade_ma_strategy,
    run_candle_ma_strategy
)

def display_menu():
    print("\n📊 Autotrade Client Menu")
    print("1. Run backtest")
    print("2. Show trade counts")
    print("3. Check data coverage")
    print("4. Exit")

def check_trade_counts():
    rows = asyncio.run(fetch_trade_counts())
    print("\nTrade counts by symbol:")
    for row in rows:
        print(f"  {row['symbol']}: {row['count']} trades")

def check_data_coverage():
    rows = asyncio.run(fetch_date_ranges())
    print("\nData coverage per symbol:")
    for row in rows:
        print(f"  {row['symbol']}: {row['start_time']} → {row['end_time']}")

async def handle_backtest():
    # Strategy choice
    print("\nSelect strategy:")
    print("1. Moving Average (Trades)")
    print("2. Moving Average (Candles)")
    strategy_choice = input("Choice (1 or 2): ").strip()

    # Exchange and fees
    exchange = input("Exchange (default: coinbase): ").strip().lower() or "coinbase"
    fee_rates = load_exchange_fees(exchange)
    if not fee_rates:
        print(f"Unknown exchange '{exchange}', using default fee rates.")
        fee_rates = {"maker": 0.0040, "taker": 0.0060}

    # Symbol and strategy parameters
    symbol = input("Symbol (e.g., BTC-USD): ").strip().upper() or "BTC-USD"
    try:
        short_window = int(input("Short MA window (default 5): ") or 5)
        long_window = int(input("Long MA window (default 20): ") or 20)
        starting_cash = float(input("Starting cash (default 1000): ") or 1000.0)
    except ValueError:
        print("Invalid input. Using defaults.")
        short_window, long_window = 5, 20
        starting_cash = 1000.0

    if strategy_choice == "1":
        await run_trade_ma_strategy(
            symbol=symbol,
            short_window=short_window,
            long_window=long_window,
            starting_cash=starting_cash,
            fee_rates=fee_rates,
            exchange=exchange
        )
    elif strategy_choice == "2":
        interval = input("Candle interval (1m, 5m, 15m, etc. default: 1m): ").strip() or "1m"
        source = input("Candle source - 'generated' or 'rest' (default: generated): ").strip().lower() or "generated"
        await run_candle_ma_strategy(
            symbol=symbol,
            interval=interval,
            short_window=short_window,
            long_window=long_window,
            starting_cash=starting_cash,
            fee_rates=fee_rates,
            exchange=exchange,
            source=source
        )
    else:
        print("Invalid strategy choice.")

def main():
    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            asyncio.run(handle_backtest())
        elif choice == "2":
            check_trade_counts()
        elif choice == "3":
            check_data_coverage()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
