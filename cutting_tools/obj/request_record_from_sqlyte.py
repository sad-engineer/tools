#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import pandas as pd
import sqlite3

from cutting_tools.obj.abstract_classes import RecordRequester


class RequestRecordFromSQLyte(RecordRequester):
    """Класс запросов для работы с таблицами в базе данных."""

    def __init__(self, filename: str, tablename: str):
        """Инициализация объекта"""
        self.filename = filename
        self.tablename = tablename

    def get_records(self, values_dict: dict) -> pd.DataFrame:
        """
        Возвращает DataFrame с записями, которые соответствуют данным столбцам и значениям.

        Параметры
        ----------
        values_dict : dict
            Словарь с именами столбцов в качестве ключей и значениями в качестве значений.

        Возвращает
        -------
        DataFrame
            DataFrame с записями, соответствующими данным столбцам и значениям.
        """
        with sqlite3.connect(self.filename) as conn:
            query = f"SELECT * FROM {self.tablename} WHERE "
            for column, value in values_dict.items():
                query += f"{column} = '{value}' AND "
            query = query[:-4]
            df = pd.read_sql(query, conn)
        return df

    @property
    def get_all_records(self) -> pd.DataFrame:
        """ Возвращает DataFrame со всеми записями таблицы tablename."""
        with sqlite3.connect(self.filename) as conn:
            query = f"SELECT * FROM {self.tablename}"
            df = pd.read_sql(query, conn)
        return df
