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
    "number": 1,
    "kind": "bar",
    "sql": 'SELECT DISTINCT(os) AS OS, COUNT(*) AS CNT FROM wifi_clients GROUP BY os ORDER BY CNT DESC',
    "x_column": "OS",
    "y_column": "CNT",
    "x_title": "Client OS",
    "y_title": "Count",
    "plot_title": "Overall OS Distribution",
}

config["plot"] = plotconfig
pb = PlotBase(config)
pb.save()
# pb.show()

