from .interpreter import ParsedTrade
from .config import Config

class SizingEngine:
    @staticmethod
    def calculate_size(target_trade: ParsedTrade) -> float:
        """
        Calculate how many contracts/tokens to buy based on the configured strategy.
        """
        if Config.SIZING_MODE == "FIXED":
            # If we want to bet exactly $50 USDC, divide by current asset price
            return Config.FIXED_TRADE_AMOUNT_USDC / target_trade.price
            
        elif Config.SIZING_MODE == "PROPORTIONAL":
            # Placeholder for proportional sizing logic
            # Requires querying both wallets' total equity via API
            balance_ratio = 0.5  # E.g., our bank is half the size of the target's
            return target_trade.size * balance_ratio
            
        else:
            return 0.0
