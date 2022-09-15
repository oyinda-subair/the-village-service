import logging.config
from .settings import ROOT, Settings
from os.path import join
from pythonjsonlogger import jsonlogger

logging_ini_path = join(ROOT, 'logging.ini')

logging.config.fileConfig(logging_ini_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
