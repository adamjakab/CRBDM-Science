#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#
import pandas as pd
from lib.cached_data_loader import CachedDataLoader
from lib.panda_plotter import PandaPlotter

# Other Options
# pd.set_option('display.max_rows', None)

# Init the main tools
cdl = CachedDataLoader()
pp = PandaPlotter()

sql = 'SELECT v.ts AS TS, v.mqtt_count AS BATCH_COUNT FROM v__wcb__h__record_counts AS v'
df = cdl.get_dataframe(sql, reindex=True)

# Filter a time period by mask
mask = (df['TS'] >= '2019-10-21 00:00:00') & (df['TS'] < '2019-10-26 00:00:00')
mdf = df.loc[mask]
# print(mdf)

plotconfig = {
    "plot_title": "Major Downtime 23-24 October",
    "kind": "line",
    "x_column": "TS",
    "y_column": "BATCH_COUNT",
    "x_label": "Timestamp",
    "y_label": "Mqtt batch count per hour",
    "palette_color": "purple"
}
pp.plot(plotconfig, mdf, save=True)

