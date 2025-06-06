# backtest/strategy.py

from collections import deque
from typing import List, Dict, Tuple


def moving_average_crossover(trades: List[Dict], short_window: int = 5, long_window: int = 20):
    short_ma = deque(maxlen=short_window)
    long_ma = deque(maxlen=long_window)
    signals = []

    for trade in trades:
        price = float(trade['price'])
        short_ma.append(price)
        long_ma.append(price)

        if len(short_ma) == short_window and len(long_ma) == long_window:
            short_avg = sum(short_ma) / short_window
            long_avg = sum(long_ma) / long_window

            if short_avg > long_avg:
                signals.append(("buy", trade["timestamp"], price))
            elif short_avg < long_avg:
                signals.append(("sell", trade["timestamp"], price))

    return signals

def moving_average_crossover_candles(candles: List[Dict], short_window: int = 5, long_window: int = 20) -> List[Tuple[str, str, float]]:
    short_ma = deque(maxlen=short_window)
    long_ma = deque(maxlen=long_window)
    signals = []

    for candle in candles:
        close_price = float(candle["close"])
        timestamp = candle["timestamp"]

        short_ma.append(close_price)
        long_ma.append(close_price)

        if len(short_ma) == short_window and len(long_ma) == long_window:
            short_avg = sum(short_ma) / short_window
            long_avg = sum(long_ma) / long_window

            if short_avg > long_avg:
                signals.append(("buy", timestamp, close_price))
            elif short_avg < long_avg:
                signals.append(("sell", timestamp, close_price))

    return signals
