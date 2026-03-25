import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Configure a standardized logger for the application.
    Ensures that logs are properly formatted and emitted to stdout.
    """
    logger = logging.getLogger(name)
    
    # Only configure if no handlers are present to avoid duplicate logs
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
    return logger
