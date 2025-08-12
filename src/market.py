from bot import BasicBot
from binance.enums import *
from datetime import datetime

# Replace with your Testnet API keys
API_KEY = "7831bfd34acc879805eabe4615d565d42ea4fd00c8e7e9048db95751c3c33571"
API_SECRET = "730f1154a4717158fe5fa84c17839db5359ee2dd84a09bc73edc41f80666b2e5"

bot = BasicBot(API_KEY, API_SECRET, testnet=True)

# Sync local time with Binance server
server_time = bot.client.futures_time()
local_time = int(datetime.now().timestamp() * 1000)
bot.client.timestamp_offset = server_time['serverTime'] - local_time

def main():
    print("=== Binance Futures Testnet Trading Bot ===")

    # Get user inputs
    order_type = input("Enter order type (market/limit): ").strip().lower()
    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
    side = input("Enter side (buy/sell): ").strip().lower()
    quantity = float(input("Enter quantity: "))

    if order_type == "market":
        result = bot.place_market_order(symbol, SIDE_BUY if side == "buy" else SIDE_SELL, quantity)
    elif order_type == "limit":
        price = float(input("Enter limit price: "))
        result = bot.place_limit_order(symbol, SIDE_BUY if side == "buy" else SIDE_SELL, quantity, price)
    elif order_type == '3':
        stop_price = float(input("Enter stop price: "))
        limit_price = float(input("Enter limit price: "))
        result = bot.place_stop_limit_order(symbol, SIDE_BUY if side == "buy" else SIDE_SELL, quantity, stop_price, limit_price)
    else:
        print("Invalid order type.")
        return

    # Output order details
    if result:
        print("Order placed successfully!")
        print(result)
    else:
        print("Order placement failed. Check logs for details.")

if __name__ == "__main__":
    main()
