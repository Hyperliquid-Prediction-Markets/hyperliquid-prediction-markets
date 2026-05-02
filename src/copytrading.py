from loguru import logger
from .watcher import WalletWatcher
from .interpreter import TradeInterpreter
from .sizing import SizingEngine
from .risk import RiskManager
from .executor import TradeExecutor

class CopyBotLogic:
    def __init__(self, watcher: WalletWatcher, executor: TradeExecutor):
        self.watcher = watcher
        self.executor = executor
        
        # Initialize pure logic modules
        self.interpreter = TradeInterpreter()
        self.sizing = SizingEngine()
        self.risk = RiskManager()

    async def process_ws_message(self, raw_message: dict):
        """
        Main pipeline: Listen -> Interpret -> Size -> Risk Check -> Execute
        """
        # 1. Parse raw L1 data
        trade = self.interpreter.parse_ws_message(raw_message)
        if not trade:
            return # Not a trade event, ignore

        logger.info(f"⚡ Detected trade from {trade.source_address}: {trade.asset} @ {trade.price}")

        # 2. Calculate dynamic or fixed size
        calculated_size = self.sizing.calculate_size(trade)

        # 3. Pass through risk firewall
        if not self.risk.check_trade(trade, calculated_size):
            logger.warning("Trade rejected by Risk Engine. Skipping.")
            return

        # 4. Fire transaction
        await self.executor.execute(trade, calculated_size)

    async def run(self):
        """
        Boot up the copy trading engine.
        """
        logger.info("Initializing Copy Trading Pipeline...")
        # Bind the processing pipeline to the watcher stream
        await self.watcher.start_watching(self.process_ws_message)
