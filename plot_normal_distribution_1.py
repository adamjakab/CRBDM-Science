#!/usr/bin/env python
#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#

import json
import logging.config
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
from numpy.random import randn
from lib.plot_base import PlotBase
from scipy.stats import norm
import numpy as np

__script_dir__ = os.path.dirname(os.path.realpath(__file__))
config_file = __script_dir__ + '/configuration.json'

# Load configuration file
with open(config_file) as config_file:
    config = json.load(config_file)


plotconfig = {
    "number": 1,
    "kind": "",
    "sql": 'SELECT v.ts, (v.mqtt_count * 5) AS calc_min_per_day '
           'FROM v__wcs__d__user__record_counts AS v '
           'WHERE v.user_name = \'YVpjMm4ySlpTMG9pVEhRUm1nYkVzUT09\';',
    "x_column": "",
    "y_column": "",
    "x_title": "",
    "y_title": "",
    "plot_title": "",
}
config["plot"] = plotconfig
cachename = __script_dir__ + "/cache/nd_{0}".format(config["plot"]["number"])


df = None
try:
    df = pd.read_pickle(cachename)
except Exception as e:
    print(e)
    pass
if df is None:
    pb = PlotBase(config)
    pb.setup_dataframe()
    df = pb.get_dataframe()
    df.to_pickle(cachename)

data = df["calc_min_per_day"]  # .values
print("data: {0}".format(data.values))


# Fit a normal distribution to the data:
mu, std = norm.fit(data)

print("Fit(mu): {0}".format(mu))
print("Fit(std): {0}".format(std))

# Plot the histogram.
plt.hist(data, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)


plt.show()

