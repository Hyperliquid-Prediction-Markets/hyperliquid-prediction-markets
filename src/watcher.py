from typing import Callable, List
from loguru import logger
from .hl_l1_api import HyperliquidAPI

class WalletWatcher:
    def __init__(self, api: HyperliquidAPI, addresses: List[str]):
        self.api = api
        self.addresses = addresses

    async def start_watching(self, on_message_callback: Callable):
        """
        Initiate the asynchronous WebSocket stream to monitor target addresses.
        Passes incoming messages to the orchestrator callback.
        """
        valid_addresses = [addr for addr in self.addresses if addr.strip()]
        
        if not valid_addresses:
            logger.error("No valid target addresses configured to watch.")
            return

        logger.info(f"Starting real-time wallet monitor for: {valid_addresses}")
        
        # Delegate WS connection to the API module, passing the callback
        await self.api.connect_ws(valid_addresses, on_message_callback)
