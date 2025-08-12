from src.bot import BinanceBotBase

class StopLimitOrder(BinanceBotBase):
    def place(self):
        # Get validated base inputs
        user_input = self.get_user_input(["stop-limit"])
        if not user_input:
            return
        
        try:
            # Fetch filters for validation
            info = self.client.futures_exchange_info()
            symbol_filters = None
            for s in info['symbols']:
                if s['symbol'] == user_input["symbol"]:
                    symbol_filters = s['filters']
                    break

            if not symbol_filters:
                print("Symbol not found in exchange info.")
                return

            # Show filters (optional for debugging)
            print("Symbol filters:", symbol_filters)

            # Get stop and limit price from user
            stop_price = float(input("Enter stop price: "))
            limit_price = float(input("Enter limit price: "))

            # Validation against PRICE_FILTER
            price_filter = next(f for f in symbol_filters if f['filterType'] == 'PRICE_FILTER')
            min_price = float(price_filter['minPrice'])
            tick_size = float(price_filter['tickSize'])

            for price_val, label in [(stop_price, "Stop Price"), (limit_price, "Limit Price")]:
                if price_val < min_price:
                    print(f"{label} must be >= {min_price}")
                    return
                if round((price_val - min_price) % tick_size, 10) != 0:
                    print(f"{label} must be in increments of {tick_size}")
                    return

            # Validation against LOT_SIZE and MIN_NOTIONAL
            lot_filter = next(f for f in symbol_filters if f['filterType'] == 'LOT_SIZE')
            min_qty = float(lot_filter['minQty'])
            step_size = float(lot_filter['stepSize'])

            min_notional_filter = next(f for f in symbol_filters if f['filterType'] == 'MIN_NOTIONAL')
            min_notional = float(min_notional_filter['notional'])
            if user_input['quantity'] < min_qty:
                print(f"Quantity must be >= {min_qty}")
                return
            if round(user_input['quantity'] % step_size, 10) != 0:
                print(f"Quantity must be in increments of {step_size}")
                return
            if limit_price * user_input['quantity'] < min_notional:
                print(f"Order notional must be >= {min_notional}")
                return

            # Place STOP (stop-limit) order
            order = self.client.futures_create_order(
                symbol=user_input["symbol"],
                side=user_input["side"],
                type="STOP",  # Correct type for stop-limit
                quantity=user_input["quantity"],
                price=limit_price,
                stopPrice=stop_price,
                timeInForce="GTC"
            )

            print("Stop-limit order placed:", order)

        except Exception as e:
            print(f"Error placing stop-limit order: {e}")

if __name__ == "__main__":
    API_KEY = "7831bfd34acc879805eabe4615d565d42ea4fd00c8e7e9048db95751c3c33571"
    API_SECRET = "730f1154a4717158fe5fa84c17839db5359ee2dd84a09bc73edc41f80666b2e5"
    StopLimitOrder(API_KEY, API_SECRET, testnet=True).place()
