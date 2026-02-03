"""Order service for managing trade execution.

Provides high-level order creation interface that abstracts
away order type-specific logic.
"""

import logging
from .client import BinanceFuturesClient

logger = logging.getLogger("orders")


class OrderService:
    """Service for creating and managing futures orders.
    
    Acts as a facade over the Binance API client, providing
    a simplified interface for order placement.
    """
    
    def __init__(self, client: BinanceFuturesClient):
        """Initialize the OrderService with a Binance API client.
        
        Args:
            client (BinanceFuturesClient): Binance API client instance.
        """
        self.binance_client = client

    def create(self, order_arguments):
        """Create and submit an order based on provided arguments.
        
        Routes the order to the appropriate method (market or limit)
        based on the order type specified in the arguments.
        
        Args:
            order_arguments (argparse.Namespace): Order parameters including:
                - symbol: Trading pair (e.g., 'BTCUSDT')
                - side: 'BUY' or 'SELL'
                - type: 'MARKET' or 'LIMIT'
                - quantity: Order quantity
                - price: Limit price (for LIMIT orders only)
                
        Returns:
            dict: API response from the order submission.
            
        Raises:
            ValueError: If order type is not 'MARKET' or 'LIMIT'.
        """
        # Route market orders
        if order_arguments.type == "MARKET":
            return self.binance_client.place_market_order(
                order_arguments.symbol,
                order_arguments.side,
                order_arguments.quantity
            )

        # Route limit orders
        if order_arguments.type == "LIMIT":
            return self.binance_client.place_limit_order(
                order_arguments.symbol,
                order_arguments.side,
                order_arguments.quantity,
                order_arguments.price
            )

        # Handle unsupported order types
        raise ValueError(f"Unsupported order type: {order_arguments.type}")
