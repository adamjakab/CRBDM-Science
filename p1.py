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

sql = 'SELECT * FROM v__wcb__h__record_counts'
df = cdl.get_dataframe(sql)
df = cdl.reindex_by_timestamp(df, "ts", "1H")

# Filter a time period by mask
mask = (df['ts'] >= '2019-10-21 00:00:00') & (df['ts'] <= '2019-10-26 00:00:00')
mdf_1 = df.loc[mask]
# print(mdf_1)


plotconfig = {
    "title": "Major Downtime 23-24 October",
    "plots": [
        {
            "data": mdf_1,
            "title": "Major Downtime 23-24 October",
            "x_column": "ts",
            "y_column": ["mqtt_count"],
            "x_label": "Time (granularity 1H)",
            "y_label": "Number of MQTT batches per hour",
            "x_major_ticks_freq": 24,
            "x_minor_ticks_freq": 6,
            "y_major_ticks_freq": 2,
            "y_minor_ticks_freq": 1,
        }
    ],
    "style": {
        "palette_color": "purple",
        "x_axis_value_rotation": 45,
        "y_axis_value_format": "",
    }
}
pp.plot(plotconfig, save=True)
