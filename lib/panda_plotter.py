import json
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from seaborn import xkcd_rgb, crayons
from pandas.plotting import register_matplotlib_converters


class PandaPlotter:
    __base_dir__ = None
    _config = None

    def __init__(self):
        self.__base_dir__ = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        # Load configuration file
        config_file = self.__base_dir__ + '/configuration.json'
        with open(config_file) as config_file:
            self._config = json.load(config_file)

        # Other
        register_matplotlib_converters()
        sns.set_style("whitegrid")


    def plot(self, plotconfig, df, show=True, save=False):
        fig = plt.figure(num=None, figsize=(8, 5), dpi=96, facecolor='w', edgecolor='k')
        ax = fig.add_subplot(1, 1, 1)

        # Colors (from .colors import xkcd_rgb, crayons)
        palette_color = xkcd_rgb["baby shit green"]
        if "palette_color" in plotconfig:
            palette_color = xkcd_rgb[plotconfig["palette_color"]]
        palette = sns.dark_palette(palette_color)

        # X
        x_column = plotconfig["x_column"]
        x = df[x_column]

        # Allow for multiple columns passed as a list
        if isinstance(plotconfig["y_column"], list):
            y_columns = plotconfig["y_column"]
        else:
            y_columns = [plotconfig["y_column"]]

        # Plot
        for y_column in y_columns:
            y = df[y_column]
            ax.plot(x, y, color=palette[3], lw=1, linestyle='solid')
            ax.fill_between(x, 0, y, alpha=.2, facecolor=palette[3])

        # X ticks
        x_major_ticks = x[0::24]
        x_minor_ticks = x[0::6]
        ax.set_xticks(x_major_ticks)
        ax.set_xticks(x_minor_ticks, minor=True)

        # Y ticks
        y_column = y_columns[0]
        y = df[y_column]
        y = np.array(range(min(y), max(y) + 1))

        y_major_ticks = y[0::2]
        y_minor_ticks = y[0::1]
        ax.set_yticks(y_major_ticks)
        ax.set_yticks(y_minor_ticks, minor=True)

        # And a corresponding grid
        ax.grid(which='both')

        # Or if you want different settings for the grids:
        ax.grid(which='minor', alpha=0.4)
        ax.grid(which='major', alpha=0.8)


        plt.subplots_adjust(bottom=0.3)
        ax.set_title(plotconfig["plot_title"], fontsize=12)
        ax.set_xlabel(plotconfig["x_label"], fontsize=9)
        ax.set_ylabel(plotconfig["y_label"], fontsize=9)
        ax.tick_params(axis="x", labelrotation=90, labelsize=7)
        ax.tick_params(axis="y", labelrotation=0, labelsize=7)

        # Need option for these
        # ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        # ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

        if save:
            self._save(plotconfig["plot_title"])

        if show:
            plt.show()

    def _save(self, plot_title):
        filename = self._get_plot_file_path(plot_title)
        plt.savefig(filename)

    def _get_plot_file_path(self, plot_title):
        name = str(plot_title).strip().lower().replace(' ', '_')
        clean_name = re.sub(r'(?u)[^-\w.]', '', name)
        extension = "png"
        plot_file_path = "{0}/images/{1}.{2}".format(self.__base_dir__, clean_name, extension)
        return plot_file_path

