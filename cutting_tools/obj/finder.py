#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.abstract_classes import RecordRequester
from cutting_tools.obj.request_record_from_sqlyte import RequestRecordFromSQLyte


class Finder:
    """ Содержит список методов поиска в БД, обязательных для поиска при любом типе БД """
    def __init__(self, record_requester: RecordRequester = RequestRecordFromSQLyte):
        self._requester = record_requester

    def find_by_dia(self, dia): pass
        # self._requester.get_records()

    def find_by_type(self, type_tool):
        """ Возвращает найденные записи по указанному обозначению.

        Аргументы
        ---------
        marking: str
            Обозначение для поиска в БД
        """
        df = self._requester.get_records({"Тип_инструмента": type_tool})
        return df if not df.empty else None

    def find_by_marking(self, marking):
        """ Возвращает найденные записи по указанному обозначению.

        Аргументы
        ---------
        marking: str
            Обозначение для поиска в БД
        """
        df = self._requester.get_records({"Обозначение": marking})
        return df if not df.empty else None

    def find_by_stand(self, standart):
        """ Возвращает найденные записи по указанному стандарту.

        Аргументы
        ---------
        standart: str
            Обозначение стандарта для поиска в БД
        """
        df = self._requester.get_records({"Стандарт": standart})
        return df if not df.empty else None

    def find_by_dia_and_type(self): pass

    def find_by_marking_and_stand(self, marking, standart):
        """ Возвращает найденные записи по указанному стандарту.

        Аргументы
        ---------
        marking: str
            Обозначение для поиска в БД
        standart: str
            Обозначение стандарта для поиска в БД
        """
        df = self._requester.get_records({"Обозначение": marking, "Стандарт": standart})
        return df if not df.empty else None

    def find_all(self):
        df = self._requester.get_all_records
        return df if not df.empty else None

