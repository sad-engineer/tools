#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable
import pandas as pd
from pydantic import ValidationError

from service import Cataloger
from service import logged

from tools.obj.finders import Finder
from tools.obj.data_preparers import DataPreparer
from tools.obj.entities import ErrorWithData
from tools.obj.decorator import debugging_message_for_init_method as debug_for_init


def debug_message_when_creating_instance_of_class():
    """Логирует создание объекта (экземпляра модели данных). При ошибке создания - логирует ошибку."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            object = func(self, *args, **kwargs)
            if not isinstance(object, ErrorWithData):
                if self._verbose == True:
                    self.debug(f"Создан экземпляр класса {object.__class__.__name__}: {object.name}.")
                return object
            else:
                if isinstance(object.err, ValueError):
                    self.error(f"Переданные данные не соответствуют ожидаемой схеме модели {object.name}."
                               f"Данные, полученные из БД: {object.raw_data}."
                               f"Данные, загружаемые в модель: {object.params}.")
                elif isinstance(object.err, TypeError):
                    self.error(f"Данные, загружаемые в модель должны быть словарем. "
                               f"Полученный тип данных: {type(object.params)}.")
                elif isinstance(object.err, ValidationError):
                    self.error(f"Входные данные содержат неверные значения для полей модели {object.name}."
                               f"Данные, полученные из БД: {object.raw_data}."
                               f"Данные, загружаемые в модель: {object.params}.")
                elif isinstance(object.err, AttributeError):
                    self.error(f"Входные данные содержат неверные значения для полей модели {object.name}."
                               f"Данные, полученные из БД: {object.raw_data}."
                               f"Данные, загружаемые в модель: {object.params}.")
                else:
                    self.error(f"Ошибка создания экземпляра класса {object.name} с параметрами {object.params}."
                               f"Данные, полученные из БД: {object.raw_data}.")
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

    @debug_message_when_creating_instance_of_class()
    def create_tool(self, records: pd.Series):
        """ Создает инструмент по переданной записи pd.Series. В случае неудачи, сохранит в ErrorWithData ожибку,
        класс инструмента, данные из БД и обработанные данные."""
        raw_data = records.dropna().to_dict()
        preparer = self._preparer_factory(raw_data)
        params = preparer.to_generate
        cutter_class = self._catalog.by_type(type_tool=raw_data["Тип_инструмента"])
        try:
            return cutter_class.parse_obj(params)
        except Exception as error:
            return ErrorWithData(err=error, name=cutter_class.__name__, params=params, raw_data=raw_data)

