#!/usr/bin/env python
#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#


import json
import logging.config
import os
import sys
import pandas as pd

import pymysql.cursors
from pymysql import OperationalError

_config = None

__script_dir__ = os.path.dirname(os.path.realpath(__file__))
config_file = __script_dir__ + '/configuration.json'
log_config_file = __script_dir__ + '/logconfig.ini'


# Load configuration file
try:
    with open(config_file) as config_file:
        _config = json.load(config_file)
except Exception as e:
    print("The configuration file cannot be opened! Fatal error: {0}".format(e))
    sys.exit(201)

# Set up logging
if os.path.isfile(log_config_file) is False:
    print("Fatal error: The log configuration file does not exist: '{0}'".format(log_config_file))
    sys.exit(203)

logging.config.fileConfig(log_config_file)
logger = logging.getLogger(__name__)


def get_db_connection():
    conn_data = _config["db"]
    try:
        _connection = pymysql.connect(host=conn_data["host"],
                                      user=conn_data["username"],
                                      password=conn_data["password"],
                                      db=conn_data["database"],
                                      charset=conn_data["charset"],
                                      cursorclass=pymysql.cursors.DictCursor
                                      )
    except OperationalError as e:
        logger.error("MysqlDestination: Unable to connect to database. {0}".format(e))
        raise e

    return _connection


def get_panda_frame(sql, index_col=None):
    _conn = get_db_connection()
    f = pd.read_sql(sql, _conn, index_col=index_col)
    _conn.close()
    return f


print("Now you can use 'get_panda_frame(sql,index_col)' to get a panda frame.")

# pd.set_option('display.expand_frame_repr', False)


