import unittest
from datetime import datetime, timezone
from client.services.candle_utils import build_candles

class TestBuildCandles(unittest.TestCase):
    def test_build_candles_single_bucket(self):
        trades = [
            {"timestamp": "2025-06-06T12:00:05Z", "price": "100.0", "volume": "0.5"},
            {"timestamp": "2025-06-06T12:00:15Z", "price": "101.0", "volume": "0.3"},
            {"timestamp": "2025-06-06T12:00:50Z", "price": "99.0", "volume": "0.2"},
        ]
        interval = 60  # 1-minute candles
        candles = build_candles(trades, interval)

        self.assertEqual(len(candles), 1)
        c = candles[0]
        self.assertEqual(c["timestamp"], datetime(2025, 6, 6, 12, 0, tzinfo=timezone.utc))
        self.assertEqual(c["open"], 100.0)
        self.assertEqual(c["high"], 101.0)
        self.assertEqual(c["low"], 99.0)
        self.assertEqual(c["close"], 99.0)
        self.assertAlmostEqual(c["volume"], 1.0, places=8)

    def test_build_candles_multiple_buckets(self):
        trades = [
            {"timestamp": "2025-06-06T12:00:05Z", "price": "100.0", "volume": "1"},
            {"timestamp": "2025-06-06T12:01:10Z", "price": "102.0", "volume": "1"},
        ]
        candles = build_candles(trades, 60)
        self.assertEqual(len(candles), 2)
        self.assertEqual(candles[0]["timestamp"], datetime(2025, 6, 6, 12, 0, tzinfo=timezone.utc))
        self.assertEqual(candles[1]["timestamp"], datetime(2025, 6, 6, 12, 1, tzinfo=timezone.utc))

if __name__ == "__main__":
    unittest.main()
