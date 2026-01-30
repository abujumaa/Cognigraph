import logging
import sys
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "cognigraph"):
    logger = logging.getLogger(name)
    
    # prevent adding multiple handlers if setup is called multiple times
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.DEBUG) # Capture all, handlers will filter
    
    # Common Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 1. Console Handler (Stdout) - Info and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Ensure logs directory exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 2. File Handler (Info) - General application flow
    info_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"), maxBytes=10*1024*1024, backupCount=5
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    logger.addHandler(info_handler)

    # 3. File Handler (Error) - Critical issues
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, "error.log"), maxBytes=10*1024*1024, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # 4. File Handler (Debug) - Detailed execution trace
    debug_handler = RotatingFileHandler(
        os.path.join(log_dir, "debug.log"), maxBytes=10*1024*1024, backupCount=3
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    logger.addHandler(debug_handler)
    
    return logger

logger = setup_logger()
