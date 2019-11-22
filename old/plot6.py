#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#

import json
import os
from datetime import datetime

import pandas as pd

from lib.plot_base import PlotBase

__script_dir__ = os.path.dirname(os.path.realpath(__file__))
config_file = __script_dir__ + '/configuration.json'

# Load configuration file
with open(config_file) as config_file:
    config = json.load(config_file)

now = datetime.now()

plotconfig = {
    "number": 6,
    "kind": "line",
    "sql": 'SELECT DATE_FORMAT(MIN(ts), "%Y-%m-%d %H:00:00") AS TS, '
           'ROUND(COUNT(*) / COUNT(DISTINCT mqtt_batch)) AS CNT_PER_MIN, COUNT(DISTINCT mqtt_batch) AS BN, '
           'ROUND(SUM(IF(ssid = "5te", 1, 0)) / COUNT(DISTINCT mqtt_batch))       AS CNT_5TE, '
           'ROUND(SUM(IF(ssid = "eduroam", 1, 0)) / COUNT(DISTINCT mqtt_batch))   AS CNT_EDUROAM, '
           'ROUND(SUM(IF(ssid = "ITU++", 1, 0)) / COUNT(DISTINCT mqtt_batch))     AS CNT_ITU_PLUS, '
           'ROUND(SUM(IF(ssid = "ITU-guest", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS CNT_ITU_GUEST, '
           'ROUND(SUM(IF(ssid = "sensors", 1, 0)) / COUNT(DISTINCT mqtt_batch))   AS CNT_SENSORS '
           'FROM wifi_clients '
           'WHERE ts >= "2019-10-24 00:00:00" '
           'GROUP BY YEAR(ts), MONTH(ts), DAY(ts), HOUR(ts)',
    "x_column": "TS",
    "y_column": ["CNT_5TE", "CNT_ITU_GUEST", "CNT_SENSORS"],
    "index_column": "TS",
    "x_title": "T",
    "y_title": "Client Count",
    "plot_title": "Average Client Count Per Network SSID",
}

config["plot"] = plotconfig
pb = PlotBase(config)
pb.setup_dataframe()
df = pb.get_dataframe()

# print(df)
# print("-"*80)

newIndex = pd.date_range(start=df.TS.min(), end=df.TS.max(), freq="1H")
df['TS'] = pd.to_datetime(df['TS'])
df.set_index("TS", inplace=True, drop=True)
# print(df)
# print("-"*80)

df2 = df.reindex(newIndex, fill_value=0)
df2 = df2.fillna(0.0).rename_axis('TS').reset_index()

# print(df2)
# print("-"*80)

pb.set_dataframe(df2)
pb.plot()
pb.save()
pb.show()
