"""Command-line interface for the Binance Futures trading bot.

This module handles parsing command-line arguments and orchestrating
order submission through the OrderService.
"""

import argparse
import json
import os
from bot.client import BinanceFuturesClient
from bot.orders import OrderService
from bot.validators import validate_common
from bot.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger("cli")

def parse_command_line_arguments():
    """Parse and return command-line arguments for order placement.
    
    Returns:
        argparse.Namespace: Parsed arguments containing symbol, side, type, quantity, and optional price.
    """
    argument_parser = argparse.ArgumentParser(
        description="Place a futures order on Binance testnet"
    )

    argument_parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT)"
    )
    argument_parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL"
    )
    argument_parser.add_argument(
        "--type",
        required=True,
        choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT"
    )
    argument_parser.add_argument(
        "--quantity",
        type=float,
        required=True,
        help="Order quantity in base asset"
    )
    argument_parser.add_argument(
        "--price",
        type=float,
        help="Limit price (required for LIMIT orders)"
    )

    return argument_parser.parse_args()

def main():
    """Main entry point for the trading bot CLI application.
    
    Orchestrates the process of:
    1. Parsing command-line arguments
    2. Validating input parameters
    3. Initializing the Binance client
    4. Creating and executing the order
    5. Displaying results
    """
    # Parse command-line arguments from user input
    parsed_arguments = parse_command_line_arguments()
    
    # Validate the parsed arguments before making API calls
    validate_common(parsed_arguments)

    # Retrieve API credentials from environment variables
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    # Ensure both API credentials are available
    if not api_key or not api_secret:
        raise SystemExit(
            "ERROR: Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables"
        )

    # Initialize Binance Futures client with API credentials
    binance_client = BinanceFuturesClient(api_key, api_secret)
    order_service = OrderService(binance_client)

    # Display the order request details
    print("\n---- Order Request ----")
    print(json.dumps(vars(parsed_arguments), indent=2))

    try:
        # Attempt to create and submit the order
        api_response = order_service.create(parsed_arguments)

        # Display the API response
        print("\n---- API Response ----")
        print(json.dumps(api_response, indent=2))

        print("\n✓ SUCCESS: Order placed successfully")

    except Exception as error:
        logger.exception("Order placement failed")
        print(f"\n✗ FAILED: {error}")

if __name__ == "__main__":
    """Execute the CLI application when run directly."""
    main()
