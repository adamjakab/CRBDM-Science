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
    "number": 7,
    "kind": "line",
    "sql": 'SELECT '
           'DATE_FORMAT(MIN(ts), "%Y-%m-%d %H:00:00") AS TS, '
           'ROUND(COUNT(*) / COUNT(DISTINCT mqtt_batch)) AS CNT_PER_MIN, '
           'COUNT(DISTINCT mqtt_batch) AS BN, '
           'ROUND(SUM(IF(user_profile = "Authenticated", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS UP_AUTH, '
           'ROUND(SUM(IF(user_profile = "Guest", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS UP_GUEST, '
           'ROUND(SUM(IF(user_profile = "Sensor", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS UP_SENSOR, '
           'ROUND(SUM(IF(user_profile = "default-profile", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS UP_DEFPROF, '
           'ROUND(SUM(IF(user_profile = "5te-1", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS UP_5TE_1, '
           'ROUND(SUM(IF(user_profile = "5te-3", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS UP_5TE_3, '
           'ROUND(SUM(IF(user_profile = "5te-5", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS UP_5TE_5, '
           'ROUND(SUM(IF(user_profile = "5te-7", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS UP_5TE_7 '
           'FROM wifi_clients '
           'WHERE ts >= "2019-10-18 00:00:00" '
           'GROUP BY YEAR(ts), MONTH(ts), DAY(ts), HOUR(ts)',
    "x_column": "TS",
    "y_column": ["UP_AUTH", "UP_GUEST", "UP_SENSOR", "UP_DEFPROF", "UP_5TE_1", "UP_5TE_3", "UP_5TE_5", "UP_5TE_7"],
    "index_column": "TS",
    "x_title": "T",
    "y_title": "Client Count",
    "plot_title": "Average Client Count Per User Profile",
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
