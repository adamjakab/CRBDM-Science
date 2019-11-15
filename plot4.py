#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#

from lib.plot_base import PlotBase

plotconfig = {
    "plot_title": "Hourly Average Client Count (Full Period)",
    "kind": "line",
    "sql": 'SELECT '
           'v.ts AS TS, '
           'v.per_minute_count AS CNT_PER_MIN '
           'FROM v__wcb__h__record_counts AS v '
           # 'WHERE ts >= \'2019-10-22 00:00:00\' AND ts < \'2019-10-26 00:00:00\' '
           '',
    "x_column": "TS",
    "y_column": "CNT_PER_MIN",
    "index_column": "TS",
    "x_title": "T",
    "y_title": "Client Count"
}

pb = PlotBase(plotconfig, cache_data=True)
pb.setup_dataframe(reindex=True)
pb.plot()
pb.save()
pb.show()
