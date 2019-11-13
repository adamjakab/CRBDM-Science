import base64
import hashlib
import json
# import logging.config
import os
import re
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import pymysql.cursors
from pymysql import OperationalError


class PlotBase:
    __base_dir__ = None
    _config = None
    _plot_config = None
    _dataframe = None
    _subplots = []
    _cache_data = False
    _max_cache_file_age = 1 * 24 * 60 * 60

    def __init__(self, plot_config, cache_data=False):
        self._plot_config = plot_config
        self._cache_data = cache_data

        # Load configuration file
        self.__base_dir__ = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        config_file = self.__base_dir__ + '/configuration.json'
        with open(config_file) as config_file:
            self._config = json.load(config_file)

        # Other Options
        pd.set_option('display.max_rows', None)

    def plot(self):
        fig = plt.figure()
        self._subplots.append(fig.add_subplot(1, 1, 1))

        # Allow for multiple columns passed as a list
        if isinstance(self._plot_config["y_column"], list):
            y_columns = self._plot_config["y_column"]
        else:
            y_columns = [self._plot_config["y_column"]]
        for y_column in y_columns:
            self._dataframe.plot(kind=self._plot_config["kind"],
                                 x=self._plot_config["x_column"],
                                 y=y_column,
                                 ax=self._subplots[0])

        plt.subplots_adjust(bottom=0.3)
        self._subplots[0].set_title(self._plot_config["plot_title"], fontsize=12)
        self._subplots[0].set_xlabel(self._plot_config["x_title"], fontsize=9)
        self._subplots[0].set_ylabel(self._plot_config["y_title"], fontsize=9)
        self._subplots[0].tick_params(axis="x", labelrotation=45, labelsize=7)
        self._subplots[0].tick_params(axis="y", labelrotation=0, labelsize=7)

        # Need option for these
        # self._subplots[0].xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        # self._subplots[0].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    def setup_dataframe(self, reindex=False):
        index_column = None
        # if "index_column" in self._plot_config:
        #     index_column = self._plot_config["index_column"]

        df = self._get_panda_frame(self._plot_config["sql"], index_col=index_column)

        # Reindex for missing data
        if reindex:
            new_index = pd.date_range(start=df.TS.min(), end=df.TS.max(), freq="1H")
            df['TS'] = pd.to_datetime(df['TS'])
            df.set_index("TS", inplace=True, drop=True)
            #
            df2 = df.reindex(new_index, fill_value=0)
            df2 = df2.fillna(0.0).rename_axis('TS').reset_index()
            df = df2

        self._dataframe = df

    def get_dataframe(self):
        return self._dataframe

    def set_dataframe(self, df):
        self._dataframe = df

    @staticmethod
    def show():
        plt.show()

    def save(self):
        filename = self._get_plot_file_path()
        # if os.path.isfile(filename):
        #     os.remove(filename)
        plt.savefig(filename)

    def get_db_connection(self):
        conn_data = self._config["db"]
        try:
            _connection = pymysql.connect(host=conn_data["host"],
                                          user=conn_data["username"],
                                          password=conn_data["password"],
                                          db=conn_data["database"],
                                          charset=conn_data["charset"],
                                          cursorclass=pymysql.cursors.DictCursor
                                          )
            return _connection

        except OperationalError as e:
            print("Mysql error: {0}".format(e))
            raise e

    def get_config(self):
        return self._config

    def _get_panda_frame(self, sql, index_col=None):
        f = self._get_cached_panda_frame()

        if f is None:
            conn = self.get_db_connection()
            f = pd.read_sql(sql, conn, index_col=index_col)

            self._set_cached_panda_frame(f)
            conn.close()

        return f

    def _set_cached_panda_frame(self, f):
        cache_file_path = self._get_cache_file_path()
        f.to_pickle(cache_file_path)

    def _get_cached_panda_frame(self):
        answer = None

        if self._cache_data:
            cache_file_path = self._get_cache_file_path()
            # print("Cache file path: {0}".format(cache_file_path))
            if os.path.isfile(cache_file_path):
                now = datetime.now()
                creation_time = datetime.fromtimestamp(os.path.getmtime(cache_file_path))
                delta = now - creation_time
                if delta.total_seconds() > self._max_cache_file_age:
                    os.remove(cache_file_path)
                    print("Old cache file deleted.")
                else:
                    answer = pd.read_pickle(cache_file_path)
                    print("Reusing cache data")

        return answer

    def _get_plot_file_path(self):
        clean_name = self._get_clean_file_name_from_title()
        plot_extension = "png"
        plot_file_name = "{0}.{1}".format(clean_name, plot_extension)
        plot_file_path = "{0}/Plots/{1}".format(self.__base_dir__, plot_file_name)
        return plot_file_path

    def _get_clean_file_name_from_title(self):
        s = str(self._plot_config["plot_title"]).strip().lower().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', s)

    def _get_cache_file_path(self):
        s = str(self._plot_config["sql"]).strip().lower().replace(' ', '_')
        m = hashlib.md5()
        m.update(s.encode('UTF-8'))
        cache_name_base = m.hexdigest()
        cache_extension = "cache"
        cache_file_name = "{0}.{1}".format(cache_name_base, cache_extension)
        cache_file_path = "{0}/cache/{1}".format(self.__base_dir__, cache_file_name)
        return cache_file_path



