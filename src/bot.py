import logging
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL
from datetime import datetime

class BinanceBotBase:
    def __init__(self, api_key, api_secret, testnet=True):
        """Initialize Binance Futures Testnet client & logging."""
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

        # Sync local time with Binance
        server_time = self.client.futures_time()
        local_time = int(datetime.now().timestamp() * 1000)
        self.client.timestamp_offset = server_time['serverTime'] - local_time

        # Logging setup
        logging.basicConfig(
            filename='bot.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def get_user_input(self, order_type_options):
        """Prompt user for basic order details and validate."""
        print(f"=== Binance Futures Trading Bot ===")
        
        order_type = input(f"Enter order type {order_type_options}: ").strip().lower()
        symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
        side = input("Enter side (buy/sell): ").strip().lower()
        quantity = input("Enter quantity: ").strip()

        # Validation
        if order_type not in [opt.lower() for opt in order_type_options]:
            logging.error(f"Invalid order type: {order_type}")
            print("Invalid order type.")
            return None

        if side not in ["buy", "sell"]:
            logging.error(f"Invalid side: {side}")
            print("Invalid side. Use 'buy' or 'sell'.")
            return None

        try:
            quantity = float(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            logging.error(f"Invalid quantity: {quantity}")
            print("Quantity must be a positive number.")
            return None

        if not self._validate_symbol(symbol):
            logging.error(f"Invalid symbol: {symbol}")
            print(f"Invalid symbol: {symbol}")
            return None

        return {
            "order_type": order_type,
            "symbol": symbol,
            "side": SIDE_BUY if side == "buy" else SIDE_SELL,
            "quantity": quantity
        }

    def _validate_symbol(self, symbol):
        """Check if symbol is valid in Futures exchange info."""
        try:
            exchange_info = self.client.futures_exchange_info()
            valid_symbols = [s['symbol'] for s in exchange_info['symbols']]
            return symbol in valid_symbols
        except Exception as e:
            logging.error(f"Error fetching exchange info: {e}")
            return False
