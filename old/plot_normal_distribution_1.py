#!/usr/bin/env python
#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#

import json
import os
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from lib.plot_base import PlotBase

plotconfig = {
    "plot_title": "ADAM - Record count  (Full Period)",
    "kind": "line",
    "sql": 'SELECT v.ts AS TS, (v.mqtt_count * 5) AS calc_min_per_day '
           'FROM v__wcs__d__user__record_counts AS v '
           'WHERE v.user_name = \'YVpjMm4ySlpTMG9pVEhRUm1nYkVzUT09\';',
    "x_column": "",
    "y_column": "",
    "x_title": "",
    "y_title": "",
}

pb = PlotBase(plotconfig, cache_data=True)
pb.setup_dataframe(reindex=False)
df = pb.get_dataframe()

data = df["calc_min_per_day"]  # .values
print("data: {0}".format(data.values))


# Fit a normal distribution to the data:
mu, std = norm.fit(data)

print("Fit(mu): {0}".format(mu))
print("Fit(std): {0}".format(std))

# Plot the histogram.
plt.hist(data, bins=14, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)




plt.show()

