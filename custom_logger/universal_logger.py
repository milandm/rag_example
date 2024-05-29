import logging
from logging.handlers import RotatingFileHandler
from custom_logger.logger_interface import LoggerInterface
class UniversalLogger(LoggerInterface):
    def __init__(self, log_file: str, max_bytes: int = 1048576, backup_count: int = 3):
        self.logger = logging.getLogger('universal_logger')
        self.logger.setLevel(logging.DEBUG)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Rotating File Handler
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)


    def log(self, message: str) -> None:
        self.logger.log(message)


    def error(self, message: str) -> None:
        self.logger.error(message)


    def warning(self, message: str) -> None:
        self.logger.warning(message)


    def info(self, message: str) -> None:
        self.logger.info(message)
