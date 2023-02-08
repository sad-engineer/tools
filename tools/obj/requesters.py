#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import pandas as pd
import sqlite3
from abc import ABC, abstractmethod


class RecordRequester(ABC):
    """ Абстрактный класс, реализующий работу с какой-либо БД"""
    @abstractmethod
    def get_records(self, values_dict: dict):
        # """ Реализация метода должна обеспечивать получение записей по словарю столбцов:значений, передаваемых в
        # values_dict """
        pass

    @property
    @abstractmethod
    def get_all_records(self):
        # """ Возвращает DataFrame со всеми записями таблицы tablename."""
        pass


class RequestRecordFromSQLyte(RecordRequester):
    """Класс запросов для работы с таблицами в базе данных SQLyte."""

    def __init__(self, tablename: str, database_client: sqlite3.Connection):
        """Инициализация объекта"""
        self.database_client = database_client
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
        with self.database_client as conn:
            query = f"SELECT * FROM {self.tablename} WHERE "
            for column, value in values_dict.items():
                query += f"{column} = '{value}' AND "
            query = query[:-4]
            df = pd.read_sql(query, conn)
        return df

    @property
    def get_all_records(self) -> pd.DataFrame:
        """ Возвращает DataFrame со всеми записями таблицы tablename."""
        with self.database_client as conn:
            query = f"SELECT * FROM {self.tablename}"
            df = pd.read_sql(query, conn)
        return df
