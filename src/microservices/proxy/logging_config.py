import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = os.getenv('LOG_DIR', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'proxy.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

os.makedirs(LOG_DIR, exist_ok=True)

# Формат логов
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Root logger
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
    ]
)
