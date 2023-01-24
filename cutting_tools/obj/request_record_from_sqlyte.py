#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import pandas as pd
import sqlite3
from typing import ClassVar

from cutting_tools.obj.constants import PATH_DB_FOR_TOOLS
from cutting_tools.obj.abstract_classes import RecordRequester


class RequestRecordFromSQLyte(RecordRequester):
    """Класс запросов для работы с таблицами в базе данных."""
    FILENAME: ClassVar[dict] = PATH_DB_FOR_TOOLS

    def __init__(self, filename=FILENAME, tablename="cutting_tools"):
        """Инициализация объекта"""
        self.conn = sqlite3.connect(filename)
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
        query = f"SELECT * FROM {self.tablename} WHERE "
        for column, value in values_dict.items():
            query += f"{column} = '{value}' AND "
        query = query[:-4]
        df = pd.read_sql(query, self.conn)
        # self.conn.commit()
        self.conn.close()
        return df

    @property
    def get_all_records(self) -> pd.DataFrame:
        """ Возвращает DataFrame со всеми записями таблицы tablename."""
        query = f"SELECT * FROM {self.tablename}"
        df = pd.read_sql(query, self.conn)
        # self.conn.commit()
        self.conn.close()
        return df


if __name__ == '__main__':
    rrq = RequestRecordFromSQLyte()
    result = rrq.get_records({"Обозначение": "2100-0001"})
    print(result)
