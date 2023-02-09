#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from logger.obj.abstract_classes import RecordRequester
import pandas as pd

class Finder:
    """ Содержит список методов поиска в БД, обязательных для поиска при любом типе БД """
    def __init__(self, record_requester: RecordRequester):
        self._requester = record_requester

    def find_by_dia(self, dia: float, dia_out: float=None) -> pd.DataFrame:
        """ Возвращает найденные записи по значению диаметра в виде таблицы pd.DataFrame.

        Аргументы
        ---------
        dia: str
            Значение диаметра инструмента
        dia_out: str
            Значение диаметра инструмента (указывается для насадных инструментов)
        """
        if not isinstance(dia_out, type(None)):
            df = self._requester.get_records({"D": dia_out})
        else:
            df = self._requester.get_records({"d_": dia})
        return df.dropna(how='any', axis=1) if not df.empty else None

    def find_by_type(self, type_tool: str) -> pd.DataFrame:
        """ Возвращает найденные записи по указанному обозначению в виде таблицы pd.DataFrame.

        Аргументы
        ---------
        type_tool: str
            Тип инструмента (Сверло, резец, и т.д.) для поиска в БД
        """
        df = self._requester.get_records({"Тип_инструмента": type_tool})
        return df.dropna(how='any', axis=1) if not df.empty else None

    def find_by_marking(self, marking: str) -> pd.DataFrame:
        """ Возвращает найденные записи по указанному обозначению в виде таблицы pd.DataFrame.

        Аргументы
        ---------
        marking: str
            Обозначение для поиска в БД
        """
        dict = {"Обозначение": marking}
        df = self._requester.get_records(values_dict=dict)
        return df.dropna(how='any', axis=1) if not df.empty else None

    def find_by_stand(self, standart: str) -> pd.DataFrame:
        """ Возвращает найденные записи по указанному стандарту в виде таблицы pd.DataFrame.

        Аргументы
        ---------
        standart: str
            Обозначение стандарта для поиска в БД
        """
        df = self._requester.get_records({"Стандарт": standart})
        return df.dropna(how='any', axis=1) if not df.empty else None

    def find_by_dia_and_type(self, dia: float, dia_out: float, type_tool: str) -> pd.DataFrame:
        """ Возвращает найденные записи по значению диаметра в виде таблицы pd.DataFrame.

        Аргументы
        ---------
        dia: str
            Значение диаметра инструмента
        dia_out: str
            Значение диаметра инструмента (указывается для насадных инструментов)
        type_tool: str
            Тип инструмента (Сверло, резец, и т.д.) для поиска в БД
        """
        df = self.find_by_dia(dia, dia_out)
        if not isinstance(df, type(None)):
            return df[df["Тип_инструмента"] == type_tool].dropna(how='any', axis=1) if not df.empty else None

    def find_by_marking_and_stand(self, marking: str, standart: str) -> pd.DataFrame:
        """ Возвращает найденные записи по указанному стандарту в виде таблицы pd.DataFrame.

        Аргументы
        ---------
        marking: str
            Обозначение для поиска в БД
        standart: str
            Обозначение стандарта для поиска в БД
        """
        df = self._requester.get_records({"Обозначение": marking, "Стандарт": standart})
        return df.dropna(how='any', axis=1) if not df.empty else None

    @property
    def find_all(self) -> pd.DataFrame:
        """ Возвращает все записи в виде таблицы pd.DataFrame """
        df = self._requester.get_all_records
        return df.dropna(how='any', axis=1) if not df.empty else None
