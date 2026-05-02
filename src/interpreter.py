from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ParsedTrade:
    """Standardized representation of an intercepted trade."""
    source_address: str
    asset: str
    is_buy: bool
    price: float
    size: float

class TradeInterpreter:
    @staticmethod
    def parse_ws_message(msg: Dict[str, Any]) -> ParsedTrade | None:
        """
        Parse raw WebSocket JSON payload into a structured ParsedTrade object.
        Returns None if the message is not an actionable trade.
        """
        if msg.get("type") != "orderFill":
            return None # Ignore heartbeat or unrelated WS messages

        try:
            return ParsedTrade(
                source_address=msg["address"],
                asset=msg["coin"],
                is_buy=(msg["dir"] in ["Long", "Buy"]),
                price=float(msg["price"]),
                size=float(msg["sz"])
            )
        except KeyError as e:
            # Handle missing fields silently or log them
            return None
