from loguru import logger
from .interpreter import ParsedTrade
from .config import Config

class RiskManager:
    def __init__(self):
        self.current_daily_loss = 0.0
        # Connect to DB/Redis to persist daily metrics across restarts

    def check_trade(self, trade: ParsedTrade, calculated_size: float) -> bool:
        """
        Validate the trade against risk parameters before execution.
        Returns True if safe to execute, False to block.
        """
        if calculated_size <= 0:
            logger.warning("Trade size is zero or negative. Execution blocked.")
            return False

        if self.current_daily_loss >= Config.MAX_DAILY_LOSS:
            logger.error("Max daily loss limit reached. Trading halted.")
            return False

        # Additional checks can be implemented here (e.g., maximum margin per asset, 
        # avoiding illiquid prediction markets, etc.)
        
        return True
