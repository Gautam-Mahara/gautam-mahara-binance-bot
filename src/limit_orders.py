from bot import BinanceBotBase
import logging
from dotenv import load_dotenv
import os

load_dotenv()



class LimitOrder(BinanceBotBase):
    logging.basicConfig(
        filename='bot.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    def place(self):
        user_input = self.get_user_input(["limit"])
        if not user_input:
            return
        
        try:
            order = self.client.futures_create_order(
                symbol=user_input["symbol"],
                side=user_input["side"],
                type="LIMIT",
                quantity=user_input["quantity"],
                price=input("Enter limit price: "),
                timeInForce="GTC"
            )
            print("Limit order placed:", order)
        except Exception as e:
            print(f"Error placing limit order: {e}")
            
if __name__ == "__main__":
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    LimitOrder(API_KEY, API_SECRET, testnet=True).place()