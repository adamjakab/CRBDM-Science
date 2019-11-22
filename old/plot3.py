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


plotconfig = {
    "number": 3,
    "kind": "line",
    "sql": 'SELECT '
           'v.ts AS TS, '
           'v.mqtt_count AS BATCH_COUNT '
           'FROM v__wcb__h__record_counts AS v '
           '',
    "x_column": "TS",
    "y_column": "BATCH_COUNT",
    "index_column": "TS",
    "x_title": "Timestamp",
    "y_title": "Mqtt Count per hour",
    "plot_title": "Major Downtime 23-24 October",
}

pb = PlotBase(plotconfig, cache_data=True)
pb.setup_dataframe(reindex=True)
df = pb.get_dataframe()

# Filter by index
# df = df.set_index(['TS'])
# print(df.loc['2019-10-22':'2019-10-23'])

# Filter by mask
mask = (df['TS'] >= '2019-10-22 00:00:00') & (df['TS'] < '2019-10-24 16:00:00')
mdf = df.loc[mask]
print(mdf)

#
# df['date'] = pd.date_range('2000-1-1', periods=200, freq='D')
# df = df.set_index(['date'])
# print(df.loc['2000-6-1':'2000-6-10'])
#
#
# print(fdf)


# pb.plot()
# pb.save()
# pb.show()


#
# now = datetime.now()
# pb = PlotBase(config)
# pb.setup_dataframe()
# df = pb.get_dataframe()
#
# # print(df)
# # print("-"*80)
#
# newIndex = pd.date_range(start=df.TS.min(), end=df.TS.max(), freq="1H")
# df['TS'] = pd.to_datetime(df['TS'])
# df.set_index("TS", inplace=True, drop=True)
# # print(df)
# # print("-"*80)
#
# df2 = df.reindex(newIndex, fill_value=0)
# df2 = df2.fillna(0.0).rename_axis('TS').reset_index()
#
# # print(df2)
# # print("-"*80)
#
# pb.set_dataframe(df2)
# pb.plot()
# pb.save()
# pb.show()
