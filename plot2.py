#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#

import json
import os

from lib.plot_base import PlotBase

__script_dir__ = os.path.dirname(os.path.realpath(__file__))
config_file = __script_dir__ + '/configuration.json'

# Load configuration file
with open(config_file) as config_file:
    config = json.load(config_file)


plotconfig = {
    "number": 2,
    "kind": "line",
    "sql": 'SELECT mqtt_batch, MIN(ts) AS TS, COUNT(*) AS CNT FROM wifi_clients '
           'WHERE ts >= DATE_SUB(NOW(),INTERVAL 1 HOUR) GROUP BY mqtt_batch ORDER BY mqtt_batch',
    "x_column": "mqtt_batch",
    "y_column": "CNT",
    "x_title": "Batch Number",
    "y_title": "Count",
    "plot_title": "Connections in the last hour",
}

config["plot"] = plotconfig
pb = PlotBase(config)
pb.save()
pb.show()

