import json
import logging.config
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
from numpy.random import randn

import pymysql.cursors
from pymysql import OperationalError



class PlotBase:
    _config = None
    _dataframe = None
    _subplots = []

    def __init__(self, config):
        self._config = config
        pd.set_option('display.max_rows', None)

    def plot(self):
        plotconfig = self._config["plot"]

        fig = plt.figure()
        self._subplots.append(fig.add_subplot(1, 1, 1))

        self._dataframe.plot(kind=plotconfig["kind"], x=plotconfig["x_column"], y=plotconfig["y_column"], ax=self._subplots[0])

        plt.subplots_adjust(bottom=0.3)
        self._subplots[0].set_title(plotconfig["plot_title"], fontsize=12)
        self._subplots[0].set_xlabel(plotconfig["x_title"], fontsize=9)
        self._subplots[0].set_ylabel(plotconfig["y_title"], fontsize=9)
        self._subplots[0].tick_params(axis="x", labelrotation=45, labelsize=7)
        self._subplots[0].tick_params(axis="y", labelrotation=0, labelsize=7)

        # Need option for these
        # self._subplots[0].xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        # self._subplots[0].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))



    def setup_dataframe(self):
        plotconfig = self._config["plot"]
        index_column = None
        # if "index_column" in plotconfig:
        #     index_column = plotconfig["index_column"]
        self._dataframe = self._get_panda_frame(plotconfig["sql"], index_col=index_column)

    def get_dataframe(self):
        return self._dataframe

    def set_dataframe(self, df):
        self._dataframe = df

    @staticmethod
    def show():
        plt.show()

    def save(self):
        plotconfig = self._config["plot"]
        filename = 'Plots/plot_{0}.png'.format(plotconfig["number"])
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


    def _get_panda_frame(self, sql, index_col=None):
        conn = self.get_db_connection()
        f = pd.read_sql(sql, conn, index_col=index_col)
        conn.close()
        return f

