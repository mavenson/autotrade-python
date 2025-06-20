# tests/test_rest_candles.py

import pytest
from aioresponses import aioresponses
from datetime import datetime, timedelta
import re

from client.services.rest_candles import fetch_rest_candles


url_pattern = re.compile(r"https://api\.exchange\.coinbase\.com/products/BTC-USD/candles.*")
interval = "1m"
symbol = "BTC-USD"


@pytest.mark.asyncio
async def test_fetch_rest_candles_success():
    now = datetime.utcnow()

    mock_response = [
        [int((now - timedelta(seconds=60)).timestamp()), 30000, 30500, 29900, 30400, 12.5],
        [int(now.timestamp()), 30400, 31000, 30300, 30800, 15.0]
    ]


    with aioresponses() as m:
        m.get(url_pattern, payload=mock_response)
        candles = await fetch_rest_candles(symbol, interval)

    assert len(candles) == 2
    assert candles[0]["open"] == 29900
    assert candles[1]["close"] == 30800

@pytest.mark.asyncio
async def test_fetch_rest_candles_bad_status():
    symbol = "BTC-USD"
    interval = "1m"

    url_pattern = re.compile(r"https://api\.exchange\.coinbase\.com/products/BTC-USD/candles.*")

    with aioresponses() as m:
        m.get(url_pattern, status=400)

        with pytest.raises(Exception) as exc_info:
            await fetch_rest_candles(symbol, interval)

        assert "REST candle request failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_fetch_rest_candles_empty_response():
    with aioresponses() as m:
        m.get(url_pattern, payload=[])
        candles = await fetch_rest_candles(symbol, interval)

    assert candles == []


@pytest.mark.asyncio
async def test_fetch_rest_candles_malformed_rows():
    now = datetime.utcnow()
    # One valid row, two malformed (wrong length and wrong type)
    mock_response = [
        [int(now.timestamp()), 30400, 31000, 30300, 30800, 15.0],
        [int(now.timestamp()), 30400, 31000, 30300],  # Too short
        "not-a-row"  # Not a list
    ]

    with aioresponses() as m:
        m.get(url_pattern, payload=mock_response)
        candles = await fetch_rest_candles(symbol, interval)

    assert len(candles) == 1
    assert candles[0]["close"] == 30800
