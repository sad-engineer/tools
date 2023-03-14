#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable
import pandas as pd
from pydantic import ValidationError

from service import Cataloger
from service import logged
from service import output_debug_message_for_init_method as debug_for_init

from tools.obj.data_preparers import DataPreparer
from tools.obj.entities import ErrorWithData


def output_debug_message():
    """Логирует создание объекта (экземпляра модели данных). При ошибке создания - логирует ошибку."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not isinstance(result, (ErrorWithData, type(None))) and self._verbose:
                self.debug(f"Создан экземпляр класса {result.__class__.__name__}: {result.name}.")
            return result
        return wrapper
    return decorator


def output_error_message():
    """Логирует ошибку создания объекта (экземпляра модели данных)."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not isinstance(result, ErrorWithData):
                return result
            if isinstance(result.err, ValueError):
                self.error(f"Переданные данные не соответствуют ожидаемой схеме модели {result.name}."
                           f"Данные, полученные из БД: {result.raw_data}."
                           f"Данные, загружаемые в модель: {result.params}.")
            elif isinstance(result.err, TypeError):
                self.error(f"Данные, загружаемые в модель должны быть словарем. "
                           f"Полученный тип данных: {type(result.params)}.")
            elif isinstance(result.err, ValidationError):
                self.error(f"Входные данные содержат неверные значения для полей модели {result.name}."
                           f"Данные, полученные из БД: {result.raw_data}."
                           f"Данные, загружаемые в модель: {result.params}.")
            elif isinstance(result.err, AttributeError):
                self.error(f"Входные данные содержат неверные значения для полей модели {result.name}."
                           f"Данные, полученные из БД: {result.raw_data}."
                           f"Данные, загружаемые в модель: {result.params}.")
            else:
                self.error(f"Ошибка создания экземпляра класса {result.name} с параметрами {result.params}."
                           f"Данные, полученные из БД: {result.raw_data}.")
        return wrapper
    return decorator


@logged
class ToolCreator:
    """ Создает инструмент с соответствующими параметрами в соответствующем классе """
    @debug_for_init()
    def __init__(self,
                 catalog: Cataloger,
                 preparer_factory: Callable[..., DataPreparer]) -> None:
        self._catalog = catalog
        self._preparer_factory = preparer_factory

        self._verbose = True

    @output_debug_message()
    @output_error_message()
    def create_tool(self, records: pd.Series):
        """ Создает инструмент по переданной записи pd.Series. В случае неудачи, сохранит в ErrorWithData ошибку,
        класс инструмента, данные из БД и обработанные данные."""
        raw_data = records.dropna().to_dict()
        preparer = self._preparer_factory(raw_data)
        params = preparer.to_generate
        cutter_class = self._catalog.by_type(type_tool=raw_data["Тип_инструмента"])
        try:
            return cutter_class.parse_obj(params)
        except Exception as error:
            return ErrorWithData(err=error, name=cutter_class.__name__, params=params, raw_data=raw_data)
