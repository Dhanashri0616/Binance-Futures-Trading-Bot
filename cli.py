# ============================================
# Binance Futures Testnet Trading Bot
# Single File Complete Project
# ============================================

# Install:
# pip install python-binance python-dotenv requests

# ============================================
# IMPORTS
# ============================================

import os
import logging
import argparse

from dotenv import load_dotenv
from binance.client import Client

# ============================================
# LOAD ENV VARIABLES
# ============================================

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# ============================================
# LOGGING CONFIGURATION
# ============================================

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/trading.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()

# ============================================
# BINANCE CLIENT
# ============================================

client = Client(API_KEY, API_SECRET)

# Binance Futures Testnet URL
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

# ============================================
# VALIDATORS
# ============================================

def validate_side(side):

    side = side.upper()

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    return side


def validate_order_type(order_type):

    order_type = order_type.upper()

    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT")

    return order_type


def validate_quantity(quantity):

    quantity = float(quantity)

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    return quantity


def validate_price(price):

    if price is None:
        return None

    price = float(price)

    if price <= 0:
        raise ValueError("Price must be greater than 0")

    return price

# ============================================
# ORDER FUNCTIONS
# ============================================

def place_market_order(symbol, side, quantity):

    try:

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

        logger.info(f"MARKET ORDER RESPONSE: {order}")

        return order

    except Exception as e:

        logger.error(f"Market Order Error: {str(e)}")

        return {"error": str(e)}


def place_limit_order(symbol, side, quantity, price):

    try:

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )

        logger.info(f"LIMIT ORDER RESPONSE: {order}")

        return order

    except Exception as e:

        logger.error(f"Limit Order Error: {str(e)}")

        return {"error": str(e)}

# ============================================
# MAIN FUNCTION
# ============================================

def main():

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading Symbol"
    )

    parser.add_argument(
        "--side",
        required=True,
        help="BUY or SELL"
    )

    parser.add_argument(
        "--type",
        required=True,
        help="MARKET or LIMIT"
    )

    parser.add_argument(
        "--quantity",
        required=True,
        help="Order Quantity"
    )

    parser.add_argument(
        "--price",
        required=False,
        help="Price for LIMIT Order"
    )

    args = parser.parse_args()

    try:

        # ============================================
        # VALIDATE INPUTS
        # ============================================

        symbol = args.symbol.upper()

        side = validate_side(args.side)

        order_type = validate_order_type(args.type)

        quantity = validate_quantity(args.quantity)

        price = validate_price(args.price)

        # ============================================
        # PRINT ORDER REQUEST
        # ============================================

        print("\n========== ORDER REQUEST ==========")

        print(f"Symbol   : {symbol}")

        print(f"Side     : {side}")

        print(f"Type     : {order_type}")

        print(f"Quantity : {quantity}")

        if price:
            print(f"Price    : {price}")

        print("===================================\n")

        # ============================================
        # PLACE ORDER
        # ============================================

        if order_type == "MARKET":

            response = place_market_order(
                symbol,
                side,
                quantity
            )

        elif order_type == "LIMIT":

            if not price:
                raise ValueError(
                    "LIMIT order requires --price"
                )

            response = place_limit_order(
                symbol,
                side,
                quantity,
                price
            )

        # ============================================
        # PRINT RESPONSE
        # ============================================

        print("\n========== ORDER RESPONSE ==========")

        if "error" in response:

            print("Order Failed")

            print(response["error"])

        else:

            print(f"Order ID      : {response.get('orderId')}")

            print(f"Status        : {response.get('status')}")

            print(f"Executed Qty  : {response.get('executedQty')}")

            print(f"Avg Price     : {response.get('avgPrice')}")

            print("\nOrder Placed Successfully!")

    except Exception as e:

        logger.error(str(e))

        print(f"ERROR: {str(e)}")

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == "__main__":
    main()