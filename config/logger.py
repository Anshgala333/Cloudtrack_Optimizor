import logging
import os
from datetime import datetime

def create_logger():
    # Get today's date folder
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join("log", today)
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("CloudTrackLogger")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # Avoid duplicate logs

    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s")

    # Helper to attach file handlers
    def add_file_handler(name, level):
        filepath = os.path.join(log_dir, name)
        handler = logging.FileHandler(filepath)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        

    # Add file handlers
    add_file_handler("combined.log", logging.DEBUG)
    add_file_handler("info.log", logging.INFO)
    add_file_handler("error.log", logging.ERROR)
    
    logger.info("System initialized")
    logger.debug("Debugging details")
    logger.warning("Heads up!")
    logger.error("Major failure occurred")


    return logger

logger = create_logger()
