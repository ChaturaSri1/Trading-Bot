"""Validation utilities for order parameters.

Provides input validation to ensure orders have valid
and complete parameters before API submission.
"""


def validate_common(order_arguments):
    """Validate common order parameters.
    
    Checks that all required parameters are present and valid:
    - Side must be BUY or SELL
    - Quantity must be positive
    - Price is required for LIMIT orders
    
    Args:
        order_arguments (argparse.Namespace): Order parameters to validate.
        
    Raises:
        ValueError: If any validation check fails with a descriptive message.
    """
    # Validate order side
    if order_arguments.side not in ["BUY", "SELL"]:
        raise ValueError(
            f"Invalid order side '{order_arguments.side}'. Must be 'BUY' or 'SELL'"
        )

    # Validate order quantity is positive
    if order_arguments.quantity <= 0:
        raise ValueError(
            f"Invalid quantity {order_arguments.quantity}. Quantity must be greater than 0"
        )

    # Validate limit price is provided for limit orders
    if order_arguments.type == "LIMIT" and order_arguments.price is None:
        raise ValueError(
            "Price is required for LIMIT orders. Provide --price argument"
        )
