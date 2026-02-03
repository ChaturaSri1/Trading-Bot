"""Binance Futures API client for placing orders on testnet.

This module provides low-level HTTP communication with the Binance Futures
API, including authentication, request signing, and error handling.
"""

import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode


class BinanceFuturesClient:
    """HTTP client for Binance Futures testnet API.
    
    Handles authentication, request signing, and API communication
    for placing and managing futures orders.
    """
    
    # Binance testnet endpoint for futures trading
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str, timeout: int = 10):
        """Initialize the Binance Futures client.
        
        Args:
            api_key (str): Binance API key for authentication.
            api_secret (str): Binance API secret for request signing.
            timeout (int): HTTP request timeout in seconds. Defaults to 10.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.request_timeout = timeout
        self.logger = logging.getLogger("client")

    # ========== Private Helper Methods ==========

    def _sign_request(self, params: dict) -> str:
        """Generate HMAC-SHA256 signature for API request authentication.
        
        Args:
            params (dict): Request parameters to be signed.
            
        Returns:
            str: Hexadecimal HMAC-SHA256 signature.
        """
        # Convert parameters dictionary to URL-encoded query string
        query_string = urlencode(params)
        
        # Sign the query string using HMAC-SHA256 with the API secret
        return hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()

    def _get_request_headers(self):
        """Build HTTP headers with API key authentication.
        
        Returns:
            dict: Headers dictionary containing the Binance API key.
        """
        return {"X-MBX-APIKEY": self.api_key}

    def _post_request(self, endpoint_path: str, request_params: dict):
        """Execute a signed POST request to the Binance API.
        
        Args:
            endpoint_path (str): API endpoint path (e.g., '/fapi/v1/order').
            request_params (dict): Query parameters to include in the request.
            
        Returns:
            dict: Parsed JSON response from the API.
            
        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        # Construct the full API URL
        full_url = f"{self.BASE_URL}{endpoint_path}"

        # Add current timestamp (required by Binance API)
        request_params["timestamp"] = int(time.time() * 1000)
        
        # Sign the request with API secret (required by Binance API)
        request_params["signature"] = self._sign_request(request_params)

        # Log the outgoing request
        self.logger.info(f"POST {endpoint_path} params={request_params}")

        try:
            # Execute the signed POST request
            response = requests.post(
                full_url,
                headers=self._get_request_headers(),
                params=request_params,
                timeout=self.request_timeout
            )

            # Log the response
            self.logger.info(f"RESPONSE {response.status_code} {response.text}")
            
            # Raise an exception for HTTP error status codes
            response.raise_for_status()

            # Return parsed JSON response
            return response.json()

        except Exception as api_error:
            # Log the error for debugging
            self.logger.error(f"API error: {api_error}")
            raise

    # ========== Account Management Methods ==========

    def set_leverage(self, symbol: str, leverage: int = 10):
        """Set the leverage multiplier for a trading pair.
        
        This is required on fresh testnet accounts to initialize trading
        permissions and avoid Binance error code -2019 (insufficient margin).
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
            leverage (int): Leverage multiplier (default: 10x).
            
        Returns:
            dict: API response containing updated leverage settings.
        """
        return self._post_request("/fapi/v1/leverage", {
            "symbol": symbol,
            "leverage": leverage
        })

    def ensure_symbol_ready(self, symbol: str):
        """Prepare a trading pair for order placement.
        
        Attempts to initialize the symbol by setting leverage. This is
        necessary on fresh testnet accounts before placing the first trade.
        Silently ignores errors as the symbol may already be initialized.
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
        """
        try:
            # Initialize leverage settings for the symbol
            self.set_leverage(symbol, 10)
        except Exception:
            # Initialization errors are not fatal (symbol may already be initialized)
            pass

    # ========== Order Placement Methods ==========

    def place_market_order(self, symbol: str, side: str, quantity: float):
        """Place a market order that executes immediately at current market price.
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
            side (str): Order direction - 'BUY' or 'SELL'.
            quantity (float): Order quantity in base asset.
            
        Returns:
            dict: API response containing order details and execution info.
        """
        # Initialize the trading pair if necessary
        self.ensure_symbol_ready(symbol)

        # Submit market order to API
        return self._post_request("/fapi/v1/order", {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity
        })

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        """Place a limit order at a specific price.
        
        Limit orders remain active until filled or manually cancelled.
        Uses GTC (Good Till Cancelled) time-in-force policy.
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
            side (str): Order direction - 'BUY' or 'SELL'.
            quantity (float): Order quantity in base asset.
            price (float): Limit price at which to place the order.
            
        Returns:
            dict: API response containing order details and status.
        """
        # Initialize the trading pair if necessary
        self.ensure_symbol_ready(symbol)

        # Submit limit order to API
        return self._post_request("/fapi/v1/order", {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",  # Good Till Cancelled
            "quantity": quantity,
            "price": price
        })
