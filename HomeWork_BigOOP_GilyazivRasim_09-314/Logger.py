import logging
import os
from logging.handlers import RotatingFileHandler

log_folder = "logs"
log_file = "system.log"
log_path = os.path.join(log_folder, log_file)

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

def setup_logger(log_path):
    logger = logging.getLogger("equipment_system")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger

logger = setup_logger(log_path)