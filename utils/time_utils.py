from datetime import datetime, timedelta


def normalize_timestamp(ts: datetime, interval_sec: int) -> datetime:
    """Rounds down a datetime to the nearest interval boundary."""
    epoch = int(ts.timestamp())
    rounded = epoch - (epoch % interval_sec)
    return datetime.utcfromtimestamp(rounded)

def floor_timestamp_to_interval(ts: datetime, interval: int) -> datetime:
    """Round down timestamp to nearest interval (in seconds)."""
    return ts - timedelta(seconds=ts.timestamp() % interval)
