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

sql = 'SELECT v.ts AS TS, ' \
      'v.mqtt_count AS BATCH_COUNT, ' \
      'v.per_minute_count AS PER_MINUTE_COUNT ' \
      'FROM v__wcb__h__record_counts AS v'
df = cdl.get_dataframe(sql, reindex=True)

# Filter a time period by mask
mask = (df['TS'] >= '2019-10-21 00:00:00') & (df['TS'] < '2019-10-26 00:00:00')
mdf_1 = df.loc[mask]
# print(mdf_1)


plotconfig = {
    "title": "Jack-1",
    "plots": [
        {
            "data": mdf_1,
            "title": "Major Downtime 23-24 October",
            "x_column": "TS",
            "y_column": ["BATCH_COUNT"],
            "x_label": "Timestamp",
            "y_label": "Mqtt batch count per hour",
            "x_major_ticks_freq": 24,
            "x_minor_ticks_freq": 6,
            "y_major_ticks_freq": 2,
            "y_minor_ticks_freq": 1,
        }
    ],
    "style": {
        "palette_color": "purple"
    }
}
pp.plot(plotconfig, save=True)
