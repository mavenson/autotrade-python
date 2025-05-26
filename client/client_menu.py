# client/client_menu.py

import asyncio
from client.services.queries import fetch_trade_counts, fetch_date_ranges, fetch_all_trades
from backtest.run_backtest import run_backtest

async def handle_backtest():
    trades = await fetch_all_trades("BTC-USD")
    run_backtest(trades)

def run_backtest_menu():
    asyncio.run(handle_backtest())

def check_data_coverage():
    rows = asyncio.run(fetch_date_ranges())
    print("\nData coverage per symbol:")
    for row in rows:
        print(f"  {row['symbol']}: {row['start_time']} → {row['end_time']}")

def trade_count_by_symbol():
    rows = asyncio.run(fetch_trade_counts())
    print("\nTrade count by symbol:")
    for row in rows:
        print(f"  {row['symbol']}: {row['trade_count']} trades")

def menu():
    while True:
        print("\n=== Autotrade Client Menu ===")
        print("1. Run backtest")
        print("2. Show trade count per symbol")
        print("3. Check available date range per symbol")
        print("4. Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            run_backtest_menu()
        elif choice == "2":
            trade_count_by_symbol()
        elif choice == "3":
            check_data_coverage()
        elif choice == "4":
            print("Exiting menu.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    menu()
