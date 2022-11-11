#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        cutting_tool
# Purpose:     Contains the functions of working with the database for the tool
#
# Author:      ANKorenuk
#
# Created:     28.10.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит функции работы с базой данных по инструменту
# -------------------------------------------------------------------------------
import pandas as pd
from cutting_tools.fun import connect
from cutting_tools.obj.exceptions import ReceivedEmptyDataFrame
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.constants import PATH_DB_FOR_TOOLS as PATH_DB


def by_dia_and_type(dia: float = None,
                    dia_out: float = None,
                    type_tool: str = None,
                    path_bd: str = PATH_DB) -> pd.DataFrame:
    """Открывает базу данных по инструментам (по пути 'path_bd'), запрашивает
    список всех доступных инструментов по критериям отбора (dia, stand,
    type_tool и т.д.).

    Parameters
    ----------
    dia : float, optional
        Диаметр инструмента.
        По умолчанию : None
    dia_out : float, optional
        Диаметр инструмента. (Для насадных инструментов)
        По умолчанию : None
    type_tool : str, optional
        Тип инструмента (Сверло, резец, и т.д.).
        По умолчанию : None
    path_bd : str, optional
        Путь к базе данных по материалам

    Returns
    -------
    table : DataFrame
        Сортированную таблицу инструментов из БД.
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
    ct.dropna(how='all', axis=1, inplace=True)
    return ct


def by_marking(marking: str = "2300-0041",
               path_bd: str = PATH_DB) -> pd.DataFrame:
    """Открывает базу данных по инструментам (по пути 'path_bd'), запрашивает
    параметры инструмента по наименованию.

    Parameters
    ----------
    marking : str, optional
        Наименование инструмента.
        По умолчанию : "2300-0041"
    path_bd : str, optional
        Путь к базе данных по материалам

    Returns
    -------
    ct : pd.DataFrame
        Таблица найденного инструмента по обозначению.
        Внимание! Таблица может содержать более одной строки.
    """
    db, cursor = connect(path_bd)
    ct = pd.read_sql(f"SELECT * FROM cutting_tools WHERE Обозначение = '{marking}' ", db)
    if len(ct) == 0:
        message = f"Инструмента с обозначением {marking} найдено не было."
        raise ReceivedEmptyDataFrame(message)
    return ct


def by_marking_and_stand(marking: str = "2300-0041",
                         standart: str = "ГОСТ 886-77",
                         path_bd: str = PATH_DB) -> dict:
    """Формирует словарь параметров инструмента. Поиск происходит по обозначению и стандарту в базе данных
    по пути 'path_bd'.

    Parameters
    ----------
    marking : str, optional
        Наименование инструмента.
        По умолчанию : "2300-0041"
    standart : str, optional
        Стандарт инструмента.
        По умолчанию : "ГОСТ 886-77"
    path_bd : str, optional
        Путь к базе данных по материалам

    Returns
    -------
    params : dict
        Словарь параметров инструмента.
    """
    params = {}
    ct = by_marking(marking, path_bd)
    if len(ct) > 1:
        ct = ct[ct["Стандарт"] == standart]
    for k, v in ct.to_dict().items():
        params[k] = v[0]
    return params


def full_table(table_name: str = "cutting_tools",
               path_bd: str = PATH_DB) -> pd.DataFrame:
    """ Получает всю таблицу инструментов

    Parameters
    ----------
    table_name : str
        Имя таблицы в БД
    path_bd : str, optional
        Путь к БД

    Returns
    -------
        table_ct - Таблица DataFrame(), содержащая весь имеющийся инструмент.
    """
    is_correct_name = isinstance(table_name, str) and table_name not in ["", " ", "  "]
    if is_correct_name:
        db, cursor = connect(path_bd)
        table_ct = pd.read_sql(f"SELECT * FROM {table_name}", db)
        db.close()
    else:
        if not is_correct_name:
            raise InvalidValue(f"Переменная 'name' должна содержать название таблицы. Вы передали: {table_name}.")
        table_ct = pd.DataFrame()
    return table_ct
