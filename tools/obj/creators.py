#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable
import pandas as pd

from service import Cataloger
from service import logged

from tools.obj.finders import Finder
from tools.obj.data_preparers import DataPreparer
from tools.obj.entities import ErrorWithData
from tools.obj.decorator import debug_message_when_creating_instance_of_class
from tools.obj.decorator import debugging_message_for_init_method as debug_for_init
from tools.obj.decorator import output_debug_message_for_function_with_parameters


@logged
class ToolCreator:
    """ Создает инструмент с соответствующими параметрами в соответствующем классе """
    @debug_for_init()
    def __init__(self,
                 finder: Finder,
                 catalog: Cataloger,
                 preparer_factory: Callable[..., DataPreparer]) -> None:
        self._finder = finder
        self._catalog = catalog
        self._preparer_factory = preparer_factory
        self._verbose = True

    @debug_message_when_creating_instance_of_class()
    def _all_from_table(self, table_records: pd.DataFrame):
        """ Вернет список инструментов по данным из таблицы table"""
        for index, row in table_records.iterrows():
            raw_data = row.dropna().to_dict()
            preparer = self._preparer_factory(raw_data)
            params = preparer.to_generate
            cutter_class = self._catalog.by_type(type_tool=raw_data["Тип_инструмента"])
            try:
                yield cutter_class.parse_obj(params)
            except Exception as error:
                return ErrorWithData(err=error, name=cutter_class.__name__, params=params, raw_data=raw_data)

    @output_debug_message_for_function_with_parameters("Создаем список инструментов по ключам: {}.")
    def by_marking_and_stand(self, marking: str, standard: str):
        self._verbose = True
        df = self._finder.by_marking_and_stand(marking, standard)
        return self._all_from_table(df)

    @output_debug_message_for_function_with_parameters("Создаем список инструментов по ключу: {}.")
    def by_marking(self, marking: str):
        self._verbose = True
        df = self._finder.by_marking(marking)
        return self._all_from_table(table_records=df)

    @output_debug_message_for_function_with_parameters("Создаем список инструментов по ключу: {}.")
    def by_stand(self, standard: str):
        self._verbose = True
        df = self._finder.by_stand(standard)
        return self._all_from_table(table_records=df)

    @property
    @output_debug_message_for_function_with_parameters("Получен запрос на создание всех материалов БД")
    def all(self):
        self._verbose = False
        return self._all_from_table(table_records=self._finder.all)
