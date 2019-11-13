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
    "number": 3,
    "kind": "line",
    "sql": 'SELECT '
           'v.ts AS TS, '
           'v.mqtt_count AS BATCH_COUNT '
           'FROM v__wcb__h__record_counts AS v '
           'WHERE ts >= "2019-10-10 00:00:00" '
           '',
    "x_column": "TS",
    "y_column": "BATCH_COUNT",
    "index_column": "TS",
    "x_title": "T",
    "y_title": "Batch Count",
    "plot_title": "Hourly MQTT Payload Statistics",
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
