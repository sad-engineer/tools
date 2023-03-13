#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable
import pandas as pd

from service import Cataloger
from service import InvalidValue
from service import logged

from tools.obj.finders import Finder
from tools.obj.data_preparers import DataPreparer


@logged
class ToolCreator:
    """ Создает объект из лога """
    def __init__(self,
                 finder: Finder,
                 catalog: Cataloger,
                 preparer_factory: Callable[..., DataPreparer]) -> None:
        self._finder = finder
        self._catalog = catalog
        self._preparer_factory = preparer_factory

        self.debug(f"""Создан {self.__class__.__name__} со следующими зависимостями:
            {finder=},
            {catalog=},
            {preparer_factory=} """)

    def _all_from_table(self, table: pd.DataFrame):
        """ Вернет список инструментов по данным из таблицы table"""
        tools = []
        for index, row in table.iterrows():
            raw_data = row.dropna().to_dict()
            preparer = self._preparer_factory(raw_data)
            params = preparer.to_generate
            cutter_class = self._catalog.by_type(type_tool=raw_data["Тип_инструмента"])
            # tools.append(cutter_class(**params))
            try:
                tools.append(cutter_class.parse_obj(params))
            except InvalidValue:
                self.error(f"Ошибка создания инструмента {cutter_class.__name__} ({cutter_class().group}). "
                           f"Данные получены из БД: {raw_data}."
                           f"Параметры инструмента: {params}.")
        return tools

    def by_marking_and_stand(self, marking: str, standard: str):
        self.debug(f"Создаем список инструментов по ключам: {marking=}, {standard=}.")
        df = self._finder.by_marking_and_stand(marking, standard)
        return self._all_from_table(df)

    def by_marking(self, marking: str):
        self.debug(f"Создаем список инструментов по ключу: {marking=}.")
        df = self._finder.by_marking(marking)
        return self._all_from_table(df)

    def by_stand(self, standard: str):
        self.debug(f"Создаем список инструментов по ключу: {standard=}.")
        df = self._finder.by_stand(standard)
        return self._all_from_table(df)

    @property
    def all(self):
        self.debug(f"Получен запрос на создание всех материалов БД")
        return self._all_from_table(self._finder.all)
