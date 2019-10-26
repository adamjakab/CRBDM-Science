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

    def __init__(self, config):
        self._config = config
        self.configure()

    def configure(self):
        plotconfig = self._config["plot"]

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)

        df = self.get_panda_frame(plotconfig["sql"])
        df.plot(kind=plotconfig["kind"], x=plotconfig["x_column"], y=plotconfig["y_column"], ax=ax1)

        plt.subplots_adjust(bottom=0.3)
        ax1.set_title(plotconfig["plot_title"], fontsize=12)
        ax1.set_xlabel(plotconfig["x_title"], fontsize=9)
        ax1.set_ylabel(plotconfig["y_title"], fontsize=9)
        ax1.tick_params(axis="x", labelrotation=45, labelsize=7)
        ax1.tick_params(axis="y", labelrotation=0, labelsize=7)

        ax1.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

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


    def get_panda_frame(self, sql, index_col=None):
        conn = self.get_db_connection()
        f = pd.read_sql(sql, conn, index_col=index_col)
        conn.close()
        return f

