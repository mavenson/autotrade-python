# tests/test_message_parser.py

import pytest
from utils.message_parser import parse_trade_message

# Sample valid Coinbase trade message
valid_message = {
    "type": "match",
    "product_id": "BTC-USD",
    "price": "29600.23",
    "size": "0.0032",
    "time": "2023-10-01T12:00:00.000Z"
}

# Non-trade message
non_trade_message = {
    "type": "subscriptions"
}

# Malformed message (missing fields)
malformed_message = {
    "type": "match",
    "price": "29600.23"
}


def test_parse_valid_trade_message():
    parsed = parse_trade_message(valid_message)
    assert parsed is not None
    assert parsed["symbol"] == "BTC-USD"
    assert parsed["price"] == 29600.23
    assert parsed["volume"] == 0.0032
    assert parsed["timestamp"] == "2023-10-01T12:00:00.000Z"


def test_parse_non_trade_message():
    assert parse_trade_message(non_trade_message) is None


def test_parse_malformed_message():
    assert parse_trade_message(malformed_message) is None