import logging
import sys
from datetime import datetime

class Logger:
    COLORS = {
        'DEBUG': '\033[96m',  # Cyan
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m'   # Red
    }

    RESET_COLOR = '\033[0m'

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    def _get_colored_message(self, level, message, exc_info=None):
        color = self.COLORS.get(level, '')
        log_message = f"{color}[{level}]{self.RESET_COLOR} - {message}"
        if exc_info:
            log_message += f"\n{exc_info}"
        return log_message

    def log(self, level, message, exc_info=None):
        log_message = self._get_colored_message(level, message, exc_info)
        self.logger.log(logging._nameToLevel[level], log_message, exc_info=exc_info)

    def debug(self, message, exc_info):
        self.log('DEBUG', message, exc_info)

    def info(self, message):
        self.log('INFO', message)

    def warning(self, message, exc_info=None):
        self.log('WARNING', message, exc_info)

    def error(self, message, exc_info):
        self.log('ERROR', message, exc_info)
