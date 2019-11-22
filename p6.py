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

sql = 'SELECT DATE_FORMAT(MIN(ts), "%Y-%m-%d %H:00:00") AS TS, ' \
      'ROUND(COUNT(*) / COUNT(DISTINCT mqtt_batch)) AS CNT_PER_MIN, ' \
      'COUNT(DISTINCT mqtt_batch) AS BN, ' \
      'ROUND(SUM(IF(ssid = "5te", 1, 0)) / COUNT(DISTINCT mqtt_batch))       AS CNT_5TE, ' \
      'ROUND(SUM(IF(ssid = "eduroam", 1, 0)) / COUNT(DISTINCT mqtt_batch))   AS CNT_EDUROAM, ' \
      'ROUND(SUM(IF(ssid = "ITU++", 1, 0)) / COUNT(DISTINCT mqtt_batch))     AS CNT_ITU_PLUS, ' \
      'ROUND(SUM(IF(ssid = "ITU-guest", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS CNT_ITU_GUEST, ' \
      'ROUND(SUM(IF(ssid = "sensors", 1, 0)) / COUNT(DISTINCT mqtt_batch))   AS CNT_SENSORS ' \
      'FROM wifi_clients ' \
      'WHERE ts >= "2019-10-24 00:00:00" ' \
      'GROUP BY YEAR(ts), MONTH(ts), DAY(ts), HOUR(ts)'
df = cdl.get_dataframe(sql, reindex=True)
# print(df.describe())

# Filter a time period by mask
mask = (df['TS'] >= '2019-11-01 00:00:00') & (df['TS'] < '2019-11-23 00:00:00')
mdf = df.loc[mask]
print(mdf.describe())

# ["CNT_5TE", "CNT_ITU_GUEST", "CNT_SENSORS"]
plotconfig = {
    "plot_title": "Client Count On Sensors Network (SSID=sensors)",
    "kind": "line",
    "x_column": "TS",
    "y_column": ["CNT_SENSORS"],
    "x_label": "Timestamp",
    "y_label": "Client count per minute",
    "x_major_ticks_freq": 24,
    "x_minor_ticks_freq": 6,
    "y_major_ticks_freq": 5,
    "y_minor_ticks_freq": 1,
    "palette_color": "purple"
}
pp.plot(plotconfig, mdf, save=True)

