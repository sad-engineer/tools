#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable
import pandas as pd

from tools.obj.finders import Finder
from tools.obj.data_preparers import DataPreparer
from service import Cataloger
from service import InvalidValue


class ToolCreator:
    """ Создает объект из лога """
    def __init__(self,
                 finder: Finder,
                 catalog: Cataloger,
                 preparer_factory: Callable[..., DataPreparer]):
        self._finder = finder
        self._catalog = catalog
        self._preparer_factory = preparer_factory

    def _all_from_table(self, table: pd.DataFrame):
        """ Вернет список инструментов по данным из таблицы"""
        tools = []
        for index, row in table.iterrows():
            raw_data = row.dropna().to_dict()
            preparer = self._preparer_factory(raw_data)
            params = preparer.to_generate
            cutter_class = self._catalog.by_type(type_tool=raw_data["Тип_инструмента"])
            # tools.append(cutter_class(**params))
            try:
                tools.append(cutter_class(**params))
            except InvalidValue:
                print(raw_data)
                print(params)
        return tools

    def by_marking_and_stand(self, marking: str, standard: str):
        df = self._finder.by_marking_and_stand(marking, standard)
        return self._all_from_table(df)

    def by_marking(self, marking: str):
        df = self._finder.by_marking(marking)
        return self._all_from_table(df)

    def by_stand(self, standard: str):
        df = self._finder.by_stand(standard)
        return self._all_from_table(df)

    @property
    def all(self):
        return self._all_from_table(self._finder.all)
