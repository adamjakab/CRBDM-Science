#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#
from lib.cached_data_loader import CachedDataLoader
from lib.panda_plotter import PandaPlotter

# Init the main tools
cdl = CachedDataLoader()
pp = PandaPlotter()

sql = 'SELECT * FROM v__wcb__d__record_counts'
df = cdl.get_dataframe(sql)
df = cdl.reindex_by_timestamp(df, "ts", "1D")
# mask = (df['ts'] >= '2019-10-26 00:00:00') & (df['ts'] <= '2019-10-28 00:00:00')
# mdf = df.loc[mask]


plotconfig = {
    "title": "Overview #2",
    "plots": [
        {
            "data": df,
            "title": "",
            "x_column": "ts",
            "y_column": ["per_minute_count"],
            "x_label": "Time",
            "y_label": "Average daily connections",
            "x_major_ticks_freq": 1,
            "x_minor_ticks_freq": 1,
            "y_major_ticks_freq": 100,
            "y_minor_ticks_freq": 25,
        }
    ],
    "style": {
        "palette_color": "blue",
        "x_axis_value_rotation": 90,
        "y_axis_value_rotation": 0,
        "x_axis_value_format": "%m-%d",
        "y_axis_value_format": "",
    }
}
pp.plot(plotconfig, save=True)

