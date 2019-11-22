#!/usr/bin/env python
#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#

import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from lib.plot_base import PlotBase

plotconfig = {
    "plot_title": "Daily permanence length PDF",
    "kind": "",
    "sql": 'SELECT v.user_name, (v.mqtt_count * 5) AS calc_min_per_day '
           'FROM v__wcs__d__user__record_counts AS v '
           # 'INNER JOIN students AS s ON s.user_name = v.user_name '
           # 'WHERE v.mqtt_count > 3 AND v.mqtt_count <= 144'
           ';',
    "x_column": "",
    "y_column": "",
    "x_title": "",
    "y_title": "",
}

pb = PlotBase(plotconfig, cache_data=True)
pb.setup_dataframe(reindex=False)
df = pb.get_dataframe()

bins = 96 * 3

data = df["calc_min_per_day"]
# print("data: {0}".format(data.values))

npa = np.array(data)
print("Length: {0}".format(len(npa)))
print("Mean: {0}".format(npa.mean()))
print("Std Dev: {0}".format(npa.std()))
print("Min: {0}".format(npa.min()))
print("Max: {0}".format(npa.max()))

print("Median: {0}".format(np.median(npa)))

for p in range(0, 101, 25):
    print("Percentile({0}): {1}".format(p, np.percentile(npa, p)))


# # Fit a normal distribution to the data:
loc, scale = stats.norm.fit(data)
#
# # Print Some stuff
# print("Desc(data): {0}".format(stats.describe(data)))
#
#
# # Plot the histogram.
plt.hist(data, bins=bins, alpha=0.6, color='g',  histtype='step')
#
# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, bins)
# print("x: {0}".format(x))
p = stats.norm.pdf(x, loc, scale)
plt.plot(x, p, 'k', linewidth=2)
title = plotconfig["plot_title"] + "(mean = %.2f,  std = %.2f)" % (loc, scale)
plt.title(title)

plt.show()


