# backtest/trade_meta.py

from dataclasses import dataclass

@dataclass
class TradeMeta:
    price: float
    timestamp: str
    trade_type: str = "taker"    # "maker" or "taker"
    exchange: str = "coinbase"   # Optional future use
