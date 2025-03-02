import logging
from config import LOG_FORMAT, LOG_LEVEL

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up and returns a logger instance with the specified configuration
    
    Args:
        name: Name of the logger

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set logging level
    logger.setLevel(LOG_LEVEL)
    
    # Create console handler and set level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    return logger
