#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import pandas as pd
from cutting_tools.fun import connect
from cutting_tools.obj.exceptions import ReceivedEmptyDataFrame
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.constants import PATH_DB_FOR_TOOLS as PATH_DB


def by_dia_and_type(dia: float = None, dia_out: float = None, type_tool: str = None, path_bd: str = PATH_DB)\
        -> pd.DataFrame:
    """ Открывает базу данных по инструментам (по пути 'path_bd'), запрашивает список всех доступных инструментов по
    критериям отбора (dia, stand, type_tool и т.д.)

    :param dia: Диаметр инструмента.
    :param dia_out: Диаметр инструмента. (Для насадных инструментов).
    :param type_tool: Тип инструмента (Сверло, резец, и т.д.).
    :param path_bd: Путь к базе данных по инструментам.
    :return: pd.DataFrame, содержащий данные по запрошенному инструменту
    """
    db, cursor = connect(path_bd)
    if not isinstance(dia, type(None)) and not isinstance(type_tool, type(None)):
        ct = pd.read_sql(f"SELECT * FROM cutting_tools WHERE d_ = '{dia}' AND Тип_инструмента = '{type_tool}'  ", db)
    elif not isinstance(dia_out, type(None)) and not isinstance(type_tool, type(None)):
        ct = pd.read_sql(f"SELECT * FROM cutting_tools WHERE D = '{dia_out}' AND Тип_инструмента = '{type_tool}'  ", db)
    elif not isinstance(dia, type(None)):
        ct = pd.read_sql(f"SELECT * FROM cutting_tools WHERE d_ = '{dia}' ", db)
    elif not isinstance(dia_out, type(None)):
        ct = pd.read_sql(f"SELECT * FROM cutting_tools WHERE D = '{dia_out}' ", db)
    elif not isinstance(type_tool, type(None)):
        ct = pd.read_sql(f"SELECT * FROM cutting_tools WHERE Тип_инструмента = '{type_tool}'  ", db)
    else:
        message = "Нужно задать диаметр и/или тип инструмента."
        raise InvalidValue(message)
    ct = ct.set_index('Обозначение')
    ct.drop(['index', ], axis=1, inplace=True)  # Удаляем столбец с индексом
    return ct


def by_marking(marking: str = "2300-0041", path_bd: str = PATH_DB) -> pd.DataFrame:
    """ Открывает базу данных по инструментам (по пути 'path_bd'), запрашивает параметры инструмента по наименованию.

    :param marking: Наименование инструмента.
    :param path_bd: Путь к базе данных по инструментам.
    :return: pd.DataFrame, содержащий данные найденного инструмента по обозначению.
        Внимание! Таблица может содержать более одной строки.
    """
    db, cursor = connect(path_bd)
    ct = pd.read_sql(f"SELECT * FROM cutting_tools WHERE Обозначение = '{marking}' ", db)
    if len(ct) == 0:
        raise ReceivedEmptyDataFrame(f"Инструмента с обозначением {marking} найдено не было.")
    ct.drop(['index', ], axis=1, inplace=True)  # Удаляем столбец с индексом
    return ct


def by_marking_and_stand(marking: str = "2300-0041", standard: str = "ГОСТ 886-77", path_bd: str = PATH_DB) -> dict:
    """ Формирует словарь параметров инструмента. Поиск происходит по обозначению и стандарту в базе данных
    по пути 'path_bd'.

    :param marking: Наименование инструмента.
    :param standard: Стандарт инструмента.
    :param path_bd: Путь к базе данных по инструментам.
    :return: Словарь параметров инструмента.
    """
    params = {}
    ct = by_marking(marking, path_bd)
    if len(ct) > 1:
        ct = ct[ct["Стандарт"] == standard]
        ct.reset_index(inplace=True)
    for k, v in ct.to_dict().items():
        params[k] = v[0]
    return params


def full_table(path_bd: str = PATH_DB) -> pd.DataFrame:
    """ Получает всю таблицу инструментов.

    :param path_bd: Путь к базе данных по инструментам.
    :return: Таблицу DataFrame(), содержащую весь имеющийся инструмент.
    """
    db, cursor = connect(path_bd)
    table_ct = pd.read_sql(f"SELECT * FROM cutting_tools", db)
    table_ct.drop(['index', ], axis=1, inplace=True)            # Удаляем столбец с индексом
    db.close()
    return table_ct
