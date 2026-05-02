import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Hyperliquid L1 Wallet Credentials
    HL_WALLET_ADDRESS = os.getenv("HL_WALLET_ADDRESS", "")
    HL_PRIVATE_KEY = os.getenv("HL_PRIVATE_KEY", "")

    # Copy Trading Targets (Comma-separated addresses)
    TARGET_ADDRESSES = os.getenv("TARGET_ADDRESSES", "").split(",")

    # Sizing Configuration: "FIXED" or "PROPORTIONAL"
    SIZING_MODE = os.getenv("SIZING_MODE", "FIXED")
    FIXED_TRADE_AMOUNT_USDC = float(os.getenv("FIXED_TRADE_AMOUNT_USDC", 50.0))

    # Risk Controls
    MAX_SLIPPAGE_PCT = float(os.getenv("MAX_SLIPPAGE_PCT", 0.05))
    MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", 200.0))
