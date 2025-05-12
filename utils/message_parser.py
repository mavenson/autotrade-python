# utils/message_parser.py

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def parse_trade_message(message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Parses a Coinbase trade message and extracts relevant fields.

    Parameters:
        message (dict): Raw message from Coinbase WebSocket.

    Returns:
        dict or None: Parsed trade info or None if message is not a trade.
    """
    if message.get("type") != "match":
        return None

    try:
        return {
            "symbol": message["product_id"],                      # e.g., 'BTC-USD'
            "price": float(message["price"]),
            "volume": float(message["size"]),
            "timestamp": message["time"]                          # ISO 8601 format
        }
    except (KeyError, ValueError, TypeError) as e:
        logger.warning(f"Failed to parse message: {e}, raw: {message}")
        return None