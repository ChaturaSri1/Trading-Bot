"""Logging configuration for the trading bot.

Sets up both file and console logging to track bot activity,
errors, and API interactions.
"""

import logging
import sys
from pathlib import Path


def setup_logging():
    """Configure logging to output to both file and console.
    
    Creates a 'logs' directory and configures logging with:
    - INFO level logging
    - File output to 'logs/bot.log'
    - Console output to stdout
    - Timestamp, logger name, log level, and message in output format
    """
    # Create the logs directory if it doesn't exist
    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    # Configure logging with both file and console handlers
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            # Log to file for persistent record
            logging.FileHandler(log_directory / "bot.log"),
            # Log to console for real-time monitoring
            logging.StreamHandler(sys.stdout)
        ]
    )
