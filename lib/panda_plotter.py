import json
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from deepmerge import conservative_merger, always_merger
from pandas.plotting import register_matplotlib_converters
import pandas as pd
from seaborn import xkcd_rgb


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

    @staticmethod
    def _get_default_plot_config():
        cfg = {
            "title": "Untitled Plot",
            "plots": [],
            "style": {
                "width": 10,
                "height": 5,
                "dpi": 96,
                "default_style": "whitegrid",
                "palette_color": "baby shit green",
                "line_width": 1,
                "line_style": "solid",
                "fill_alpha": 0.2
            }
        }
        return cfg

    @staticmethod
    def _get_default_subplot_config():
        cfg = {
            "data": pd.DataFrame([]),
            "title": "Untitled Plot",
            "kind": "line",
            "x_column": "x",
            "y_column": "y",
            "x_label": "X",
            "y_label": "Y",
            "x_major_ticks_freq": 10,
            "x_minor_ticks_freq": 1,
            "y_major_ticks_freq": 10,
            "y_minor_ticks_freq": 1,
        }
        return cfg

    def plot(self, cfg, show=True, save=False):
        # Merge the default configuration with the selected configuration section
        pconf = always_merger.merge(self._get_default_plot_config(), cfg)
        for i in range(0, len(pconf["plots"])):
            pconf["plots"][i] = always_merger.merge(self._get_default_subplot_config(), pconf["plots"][i])
        print(pconf)

        # Styles and Colors
        # Use colors from : (from .colors import xkcd_rgb, crayons)
        # sns.set_style(pconf["style"]["default_style"])
        palette_color = xkcd_rgb[pconf["style"]["palette_color"]]
        palette = sns.dark_palette(palette_color, n_colors=7)

        fig = plt.figure(num=None, figsize=(pconf["style"]["width"], pconf["style"]["height"]),
                         dpi=pconf["style"]["dpi"], facecolor='w', edgecolor='k')

        # For now only single subplots are supported
        ax = fig.add_subplot(1, 1, 1)

        # Data for subplot
        subpconf = pconf["plots"][0]
        df = subpconf["data"]

        # X
        x_column = subpconf["x_column"]
        x = df[x_column]

        # Y (Allow for multiple columns passed as a list)
        if isinstance(subpconf["y_column"], list):
            y_columns = subpconf["y_column"]
        else:
            y_columns = [subpconf["y_column"]]

        # Plot
        for i in range(0, len(y_columns)):
            y_column = y_columns[i]
            y = df[y_column]
            color = palette[i+2]
            ax.plot(x, y, color=color, lw=pconf["style"]["line_width"], linestyle=pconf["style"]["line_style"])
            ax.fill_between(x, 0, y, alpha=pconf["style"]["fill_alpha"], facecolor=color)

        # X ticks
        x_major_ticks_freq = subpconf["x_major_ticks_freq"]
        x_minor_ticks_freq = subpconf["x_minor_ticks_freq"]
        x_major_ticks = x[0::x_major_ticks_freq]
        x_minor_ticks = x[0::x_minor_ticks_freq]
        ax.set_xticks(x_major_ticks)
        ax.set_xticks(x_minor_ticks, minor=True)

        # Y ticks
        y_major_ticks_freq = subpconf["y_major_ticks_freq"]
        y_minor_ticks_freq = subpconf["y_minor_ticks_freq"]

        y_column = y_columns[0]
        y = df[y_column]
        y = np.array(range(0, int(max(y)) + 1))

        y_major_ticks = y[0::y_major_ticks_freq]
        y_minor_ticks = y[0::y_minor_ticks_freq]
        ax.set_yticks(y_major_ticks)
        ax.set_yticks(y_minor_ticks, minor=True)

        # Grid & Ticks
        ax.grid(which='major', alpha=0.8)
        ax.grid(which='minor', alpha=0.4)
        ax.tick_params(which='major', direction='inout', pad=5, length=3, width=1, color="k")
        ax.tick_params(which='minor', length=0, width=0)

        # Plot Spacing
        plt.subplots_adjust(top=0.93, bottom=0.2, left=0.07, right=0.97, hspace=0.2, wspace=0.2)



        if show:
            plt.show()

    def plot_(self, cfg, df, show=True, save=False):






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
