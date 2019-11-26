#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#  Description: Caching database

import hashlib
import json
import os
from datetime import datetime
import pandas as pd
import pymysql.cursors
from pymysql import OperationalError


class CachedDataLoader:
    __base_dir__ = None
    _config = None
    _cache_data = False
    _max_cache_file_age = 3 * 24 * 60 * 60

    def __init__(self, cache_data=True):
        self._cache_data = cache_data

        self.__base_dir__ = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        # Load configuration file
        config_file = self.__base_dir__ + '/configuration.json'
        with open(config_file) as config_file:
            self._config = json.load(config_file)

        # Do some maintenance
        self._clear_cache()

    def get_dataframe(self, sql):
        index_column = None
        # if "index_column" in self._plot_config:
        #     index_column = self._plot_config["index_column"]

        df = self._get_panda_frame(sql, index_col=index_column)
        return df

    def reindex_by_timestamp(self, df, ts_col_name, freq):
        new_index = pd.date_range(start=df[ts_col_name].min(), end=df[ts_col_name].max(), freq=freq)
        df[ts_col_name] = pd.to_datetime(df[ts_col_name])
        df.set_index(ts_col_name, inplace=True, drop=True)
        #
        df2 = df.reindex(new_index, fill_value=0)
        df2 = df2.fillna(0.0).rename_axis(ts_col_name).reset_index()
        return df2

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
        df = self._get_cached_panda_frame(sql)

        if df is None:
            conn = self.get_db_connection()
            df = pd.read_sql(sql, conn, index_col=index_col)
            self._set_cached_panda_frame(df, sql)
            conn.close()

        return df

    def _set_cached_panda_frame(self, df, sql):
        df.to_pickle(self._get_cache_file_path(sql))

    def _get_cached_panda_frame(self, sql):
        df = None
        if self._cache_data:
            cache_file_path = self._get_cache_file_path(sql)
            if os.path.isfile(cache_file_path):
                df = pd.read_pickle(cache_file_path)

        return df

    def _get_cache_file_path(self, sql):
        s = str(sql).strip().lower().replace(' ', '_')
        m = hashlib.md5()
        m.update(s.encode('UTF-8'))
        cache_name_base = m.hexdigest()
        cache_extension = "cache"
        cache_file_name = "{0}.{1}".format(cache_name_base, cache_extension)
        cache_file_path = "{0}/cache/{1}".format(self.__base_dir__, cache_file_name)
        return cache_file_path

    def _clear_cache(self):
        now = datetime.now()
        cache_path = "{0}/cache/".format(self.__base_dir__)
        files = os.listdir(cache_path)
        for file in files:
            cache_file_path = "{0}/{1}".format(cache_path, file)
            creation_time = datetime.fromtimestamp(os.path.getmtime(cache_file_path))
            delta = now - creation_time
            if delta.total_seconds() > self._max_cache_file_age:
                os.remove(cache_file_path)
                #print("Old cache file({0}) deleted.".format(file))
