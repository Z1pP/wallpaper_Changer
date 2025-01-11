import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """Настройка логгера"""
    logger = logging.getLogger(name or __name__)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Форматирование
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Вывод в консоль
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Вывод в файл
        log_file = Path("anime_parser.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
