"""
Logger configuration for test execution
"""
import logging
import os
from datetime import datetime
from config.config import REPORTS_DIR


def setup_logger(name=__name__, log_file=None):
    """
    Setup logger with console and file handlers
    
    Args:
        name (str): Logger name
        log_file (str): Log file path
        
    Returns:
        Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler
    if log_file is None:
        log_file = os.path.join(REPORTS_DIR, f"test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Create default logger
logger = setup_logger(__name__)
