import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = "application.log"

def setup_logger(name: str) -> logging.Logger:
    """Set up and return a configured logger instance."""
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = RotatingFileHandler(
            filename=os.path.join(LOG_DIR, LOG_FILE),
            maxBytes=1_000_000,  # 1MB
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger



# Testing
if __name__ == "__main__":
    log = setup_logger("TestLogger")
    log.debug("This is a DEBUG message.")
    log.info("This is an INFO message.")
    log.warning("This is a WARNING message.")
    log.error("This is an ERROR message.")
    log.critical("This is a CRITICAL message.")
