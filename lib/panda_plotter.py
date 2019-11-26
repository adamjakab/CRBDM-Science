import json
import os
import re

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from deepmerge import always_merger
from pandas.plotting import register_matplotlib_converters
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
                "top": 0.93,
                "bottom": 0.2,
                "left": 0.07,
                "right": 0.97,
                "hspace": 0.2,
                "wspace": 0.2,
                "default_style": "whitegrid",
                "palette_color": "baby shit green",
                "palette_length": 7,
                "line_width": 1,
                "line_style": "solid",
                "fill_alpha": 0.2,
                "title_font_size": 12,
                "axis_label_font_size": 10,
                "axis_value_font_size": 9,
                "x_axis_value_rotation": 0,
                "y_axis_value_rotation": 0,
                "label_pad": 10,
                "x_axis_value_format": "",
                "y_axis_value_format": "%.1f",
                "major_grid_alpha": 0.8,
                "minor_grid_alpha": 0.4,
                "major_tick_direction": "inout",
                "major_tick_length": 3,
                "major_tick_width": 1,
                "major_tick_pad": 5,
                "major_tick_color": "black",
                "minor_tick_direction": "inout",
                "minor_tick_length": 1,
                "minor_tick_width": 1,
                "minor_tick_pad": 1,
                "minor_tick_color": "gray",
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
        # print(pconf)

        # Styles and Colors
        pstyle = pconf["style"]
        # Use colors from : (from .colors import xkcd_rgb, crayons)
        palette_color = xkcd_rgb[pstyle["palette_color"]]
        palette = sns.dark_palette(palette_color, n_colors=pstyle["palette_length"])

        fig = plt.figure(num=None, figsize=(pstyle["width"], pstyle["height"]),
                         dpi=pstyle["dpi"], facecolor='w', edgecolor='k')

        # For now only single subplots are supported
        ax = fig.add_subplot(1, 1, 1)

        # Title
        ax.set_title(pconf["title"], fontsize=pstyle["title_font_size"], pad=pstyle["label_pad"])

        # Data for subplot
        subpconf = pconf["plots"][0]
        df = subpconf["data"]

        # X dimension
        x_column = subpconf["x_column"]
        x = df[x_column]

        # Y dimensions - allow for multiple columns passed as a list
        if isinstance(subpconf["y_column"], list):
            y_columns = subpconf["y_column"]
        else:
            y_columns = [subpconf["y_column"]]

        # Plot
        for i in range(0, len(y_columns)):
            y_column = y_columns[i]
            y = df[y_column]
            color = palette[i + 2]
            ax.plot(x, y, color=color, lw=pstyle["line_width"], linestyle=pstyle["line_style"])
            ax.fill_between(x, 0, y, alpha=pstyle["fill_alpha"], facecolor=color)

        # X ticks
        x_major_ticks_freq = subpconf["x_major_ticks_freq"]
        x_minor_ticks_freq = subpconf["x_minor_ticks_freq"]
        x_major_ticks = x[0::x_major_ticks_freq]
        x_minor_ticks = x[0::x_minor_ticks_freq]
        ax.set_xticks(x_major_ticks)
        ax.set_xticks(x_minor_ticks, minor=True)

        # X Label
        ax.set_xlabel(subpconf["x_label"], fontsize=pstyle["axis_label_font_size"], labelpad=pstyle["label_pad"])
        ax.tick_params(axis="x", labelrotation=pstyle["x_axis_value_rotation"],
                       labelsize=pstyle["axis_value_font_size"])

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

        # Y Label
        ax.set_ylabel(subpconf["y_label"], fontsize=pstyle["axis_label_font_size"], labelpad=pstyle["label_pad"])
        ax.tick_params(axis="y", labelrotation=pstyle["y_axis_value_rotation"],
                       labelsize=pstyle["axis_value_font_size"])

        # Grid & Ticks
        ax.grid(which='major', alpha=pstyle["major_grid_alpha"])
        ax.grid(which='minor', alpha=pstyle["minor_grid_alpha"])
        ax.tick_params(which='major', direction=pstyle["major_tick_direction"], length=pstyle["major_tick_length"],
                       width=pstyle["major_tick_width"], pad=pstyle["major_tick_pad"], color=pstyle["major_tick_color"])
        ax.tick_params(which='minor', direction=pstyle["minor_tick_direction"], length=pstyle["minor_tick_length"],
                       width=pstyle["minor_tick_width"], pad=pstyle["minor_tick_pad"], color=pstyle["minor_tick_color"])

        # Plot Spacing
        plt.subplots_adjust(top=pstyle["top"], bottom=pstyle["bottom"], left=pstyle["left"], right=pstyle["right"],
                            hspace=pstyle["hspace"], wspace=pstyle["wspace"])

        if pstyle["x_axis_value_format"] != "":
            ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(pstyle["x_axis_value_format"]))

        if pstyle["y_axis_value_format"] != "":
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(pstyle["y_axis_value_format"]))

        if save:
            self._save(pconf["title"])

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
