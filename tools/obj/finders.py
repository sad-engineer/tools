#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from typing import Optional, Any

from service import RecordRequester, logged

from tools.obj.decorator import output_debug_message_for_init_method as debug_for_init


def output_debug_message_with_kwargs_and_length(message: str):
    """ Выводит в лог сообщение message"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.debug(message) if message.find("{") == -1 else self.debug(
                message.format('; '.join([f'{k}= {v}' for k, v in kwargs.items()]), len(result)))
            return result
        return wrapper
    return decorator


def output_debug_message_with_with_length(message: str):
    """ Выводит в лог сообщение message"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.debug(message) if message.find("{") == -1 else self.debug(
                message.format(len(result)))
            return result
        return wrapper
    return decorator


@logged
class Finder:
    """ Содержит список методов поиска в БД, обязательных для поиска при любом типе БД """
    @debug_for_init()
    def __init__(self, record_requester: RecordRequester) -> None:
        self._requester = record_requester

    @output_debug_message_with_kwargs_and_length("По ключам {0}  найдено записей: {1}")
    def by_dia(self, dia: float, dia_out: float = None) -> pd.DataFrame:
        """ Возвращает найденные записи по значению диаметра в виде таблицы pd.DataFrame.

        Parameters:
            dia: str : Значение диаметра инструмента
            dia_out: str : Значение диаметра инструмента (указывается для насадных инструментов)
        """
        if not isinstance(dia_out, type(None)):
            df = self._requester.get_records({"D": dia_out})
        else:
            df = self._requester.get_records({"d_": dia})
        records = df.dropna(how='any', axis=1)
        return records if not records.empty else None

    @output_debug_message_with_kwargs_and_length("По ключу {0} найдено записей: {1}")
    def by_type(self, type_tool: str) -> pd.DataFrame:
        """ Возвращает найденные записи по указанному обозначению в виде таблицы pd.DataFrame.

        Parameters:
            type_tool: str : Тип инструмента (Сверло, резец, и т.д.) для поиска в БД
        """
        df = self._requester.get_records({"Тип_инструмента": type_tool})
        records = df.dropna(how='any', axis=1)
        return records if not records.empty else None

    @output_debug_message_with_kwargs_and_length("По ключу {0} найдено записей: {1}")
    def by_marking(self, marking: str) -> pd.DataFrame:
        """ Возвращает найденные записи по указанному обозначению в виде таблицы pd.DataFrame.

        Parameters:
            marking: str : Обозначение для поиска в БД
        """
        df = self._requester.get_records({"Обозначение": marking})
        records = df.dropna(how='any', axis=1)
        return records if not records.empty else None

    @output_debug_message_with_kwargs_and_length("По ключу {0} найдено записей: {1}")
    def by_stand(self, standard: str) -> pd.DataFrame:
        """ Возвращает найденные записи по указанному стандарту в виде таблицы pd.DataFrame.

        Parameters:
            standard: str : Обозначение стандарта для поиска в БД
        """
        df = self._requester.get_records({"Стандарт": standard})
        records = df.dropna(how='any', axis=1)
        return records if not records.empty else None

    # @output_debug_message_with_kwargs_and_length("По ключу {0} найдено записей: {1}")
    def by_dia_and_type(self, dia: Optional[float], dia_out: Optional[float], type_tool: str) -> pd.DataFrame:
        """ Возвращает найденные записи по значению диаметра в виде таблицы pd.DataFrame.

        Parameters:
            dia: str : Значение диаметра инструмента
            dia_out: str : Значение диаметра инструмента (указывается для насадных инструментов)
            type_tool: str : Тип инструмента (Сверло, резец, и т.д.) для поиска в БД
        """
        df = self.by_dia(dia, dia_out)
        if not isinstance(df, type(None)):
            records = df[df["Тип_инструмента"] == type_tool].dropna(how='any', axis=1)
            self.debug(f"""По ключу {type_tool=} отфильтровано записей: {len(records)}""")
            return records if not records.empty else None

    @output_debug_message_with_kwargs_and_length("По ключам {0} найдено записей: {1}")
    def by_marking_and_stand(self, marking: str, standard: str) -> pd.DataFrame:
        """ Возвращает найденные записи по указанному стандарту в виде таблицы pd.DataFrame.

        Parameters:
            marking: str : Обозначение для поиска в БД
            standard: str : Обозначение стандарта для поиска в БД
        """
        df = self._requester.get_records({"Обозначение": marking, "Стандарт": standard})
        records = df.dropna(how='any', axis=1)
        return records if not records.empty else None

    @property
    @output_debug_message_with_with_length("Инициирован поиск всех записей таблицы. Найдено записей: {}")
    def all(self) -> pd.DataFrame:
        """ Возвращает все записи в виде таблицы pd.DataFrame """
        df = self._requester.get_all_records
        return df if not df.empty else None

    @property
    def available_values(self) -> Any:
        """ Возвращает наборы доступных в таблице БД значений по категориям."""
        return self._requester.available_values


# if __name__ == '__main__':
#     from tools.obj.constants import PATH_DB_FOR_TOOLS as DB_PATH
#     from tools.obj.constants import REQUESTER_TYPE as DB_type
#
#     from tools.logger_settings import config
#     import logging.config
#
#     logging.config.dictConfig(config)
#
#     container = Requester()
#     container.config.from_dict({
#         'path': DB_PATH,
#         'requester_type': DB_type,
#         'reader_type': 'pandas_table',
#         'tablename': "tools"
#     })
#     requester = container.requester()
#     finder = Finder(record_requester = requester)
#     print(finder)
