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

sql = "SELECT * FROM "

df = cdl.get_dataframe(sql)
df = cdl.reindex_by_timestamp(df, "ts", "1H")

mask = (df['ts'] >= '2019-11-01 00:00:00') & (df['ts'] <= '2019-12-01 00:00:00')
mdf = df.loc[mask]


plotconfig = {
    "title": "Wifi Network Usage: 'eduroam' & 'ITU++'",
    "plots": [
        {
            "data": mdf,
            "title": "",
            "x_column": "ts",
            "y_column": ["CNT_ITU_PLUS", "CNT_EDUROAM"],
            "x_label": "Time",
            "y_label": "Number of connected devices",
            "x_major_ticks_freq": 24,
            "x_minor_ticks_freq": 6,
            "y_major_ticks_freq": 100,
            "y_minor_ticks_freq": 50,
        }
    ],
    "style": {
        "palette_color": "pink",
        "x_axis_value_rotation": 90,
        "y_axis_value_rotation": 90,
        "x_axis_value_format": "%m-%d",
        "y_axis_value_format": "",
    }
}
pp.plot(plotconfig)

