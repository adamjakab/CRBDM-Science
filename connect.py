import logging.config

import pymysql.cursors
from pymysql import OperationalError
from pymysql import Error as PyMysqlError
import json
import os
import sys

__script_dir__ = os.path.dirname(os.path.realpath(__file__))
config_file = __script_dir__ + '/config.json'
log_configuration_file = __script_dir__ + '/logconfig.ini'


logging.config.fileConfig(log_configuration_file)
logger = logging.getLogger(__name__)




def _connect_do_database(cfg):
    # Connect to the database - https://pypi.org/project/PyMySQL/
    try:
        _connection = pymysql.connect(host=cfg["host"],
                                      user=cfg["user_name"],
                                      password=cfg["password"],
                                      db=cfg["database"],
                                      charset=cfg["charset"])
    except OperationalError as e:
        logger.error("Connection error: {0}".format(e))
        raise e

    logger.info("Connected(var: _conn).")
    return _connection


# Load configuration file
try:
    with open(config_file) as config_file:
        full_configuration = json.load(config_file)
except Exception as e:
    print("The configuration file cannot be opened! Fatal error: {0}".format(e))
    sys.exit(201)

# Default configuration
cfg = full_configuration["default"]

#logger.info(cfg)

_conn = _connect_do_database(cfg["connection"])



