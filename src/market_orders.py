from bot import BinanceBotBase
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class MarketOrder(BinanceBotBase):
    logging.basicConfig(
        filename='bot.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    def place(self):
        user_input = self.get_user_input(["market"])
        if not user_input:
            return
        
        try:
            order = self.client.futures_create_order(
                symbol=user_input["symbol"],
                side=user_input["side"],
                type="MARKET",
                quantity=user_input["quantity"],
            )
            print("Market order placed:", order)
            logging.info(f"Market order placed: {order}")
            
        except Exception as e:
            logging.error(f"Error placing market order: {e}")
            print(f"Error placing market order: {e}")

if __name__ == "__main__":
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    print(f"API Key: {API_KEY}")
    print(f"API Secret: {API_SECRET}")
    logging.info(API_KEY )
    MarketOrder(API_KEY, API_SECRET, testnet=True).place()
