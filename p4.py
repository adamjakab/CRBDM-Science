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

# Init the main tools
cdl = CachedDataLoader()
pp = PandaPlotter()

sql = 'SELECT v.ts AS TS, v.per_minute_count AS CNT_PER_MIN FROM v__wcb__h__record_counts AS v'
df = cdl.get_dataframe(sql, reindex=True)
print(df.describe())

# Filter a time period by mask
# mask = (df['TS'] >= '2019-10-21 00:00:00') & (df['TS'] < '2019-10-26 00:00:00')
# mdf = df.loc[mask]
# print(mdf)

plotconfig = {
    "plot_title": "Client Count Per Minute (Full Period)",
    "kind": "line",
    "x_column": "TS",
    "y_column": "CNT_PER_MIN",
    "x_label": "Timestamp",
    "y_label": "Client count per minute",
    "x_major_ticks_freq": 168,
    "x_minor_ticks_freq": 24,
    "y_major_ticks_freq": 250,
    "y_minor_ticks_freq": 50,
    "palette_color": "light teal"
}
pp.plot(plotconfig, df, save=True)

