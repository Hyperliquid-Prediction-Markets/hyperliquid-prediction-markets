from loguru import logger
from .hl_l1_api import HyperliquidAPI
from .interpreter import ParsedTrade
from .config import Config

class TradeExecutor:
    def __init__(self, api: HyperliquidAPI):
        self.api = api

    async def execute(self, trade: ParsedTrade, size: float):
        """
        Prepare and send the transaction payload to the blockchain.
        """
        logger.debug(f"Preparing execution payload for {trade.asset}...")
        
        try:
            # Calculate slippage tolerance based on config
            slippage_multiplier = 1 + Config.MAX_SLIPPAGE_PCT if trade.is_buy else 1 - Config.MAX_SLIPPAGE_PCT
            adjusted_price = trade.price * slippage_multiplier
            
            # Send to Hyperliquid API
            response = await self.api.place_order(
                coin=trade.asset,
                is_buy=trade.is_buy,
                price=adjusted_price,
                size=size
            )
            
            logger.success(f"Copied trade successfully | Hash: {response.get('tx_hash')}")
            
        except Exception as e:
            logger.error(f"Execution failed due to L1 API error: {e}")
