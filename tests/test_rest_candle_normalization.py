import unittest
from datetime import datetime
from utils.time_utils import normalize_timestamp

class TestRestCandleNormalization(unittest.TestCase):

    def test_timestamp_rounding_1m(self):
        ts = datetime(2025, 6, 6, 12, 3, 29)  # 12:03:29
        rounded = normalize_timestamp(ts, 60)
        self.assertEqual(rounded, datetime(2025, 6, 6, 12, 3, 0))

    def test_timestamp_rounding_5m(self):
        ts = datetime(2025, 6, 6, 12, 7, 45)  # 12:07:45
        rounded = normalize_timestamp(ts, 300)  # 5 minutes
        self.assertEqual(rounded, datetime(2025, 6, 6, 12, 5, 0))

    def test_timestamp_rounding_1h(self):
        ts = datetime(2025, 6, 6, 12, 47, 30)
        rounded = normalize_timestamp(ts, 3600)
        self.assertEqual(rounded, datetime(2025, 6, 6, 12, 0, 0))

if __name__ == "__main__":
    unittest.main()
