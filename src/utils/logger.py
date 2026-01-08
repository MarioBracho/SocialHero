"""
Logging systém pro aplikaci
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from .config import Config

def setup_logger(name: str, log_file: str = None, level: str = None) -> logging.Logger:
    """
    Vytvoří a nakonfiguruje logger

    Args:
        name: Jméno loggeru
        log_file: Cesta k log souboru (volitelné)
        level: Logging level (volitelné, default z Config)

    Returns:
        Nakonfigurovaný logger
    """
    logger = logging.getLogger(name)

    # Nastavení levelu
    log_level = level or Config.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper()))

    # Formát logů
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (pokud je specifikován)
    if log_file:
        log_path = Config.LOGS_DIR / log_file
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Vytvoření výchozích loggerů
main_logger = setup_logger('amity.main', 'main.log')
api_logger = setup_logger('amity.api', 'api.log')
monitor_logger = setup_logger('amity.monitor', 'monitor.log')
db_logger = setup_logger('amity.database', 'database.log')
notification_logger = setup_logger('amity.notifications', 'notifications.log')
