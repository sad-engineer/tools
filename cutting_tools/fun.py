#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        fun
# Purpose:     Contains local functions for working with the database
#
# Author:      ANKorenuk
#
# Created:     28.10.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит локальные функции работы с БД
# -------------------------------------------------------------------------------
import sqlite3
import pandas as pd
from cutting_tools.obj.constants import PATH_DB_FOR_TOOLS as PATH_DB
from cutting_tools.obj.exceptions import InvalidValue


def connect(filename):
    """
    Создает и подключает базу данных если ее нет. Если БД есть - подключает ее

    Parameters
    ----------
    filename : str
        Имя файла БД.

    Returns
    -------
    db : TYPE
        Указатель на подключенную БД
    cursor : TYPE
        Указатель на курсор БД
    """
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    db.commit()
    return db, cursor


def save_table(name: str = "",
               table=None,
               path_bd: str = PATH_DB):
    """ Сохраняет таблицу DataFrame в БД. Если таблица существует - заменяет ее

    Parameters
    ----------
    name : str, optional 
        Имя таблицы в БД
    table : DataFrame, optional 
        DataFrame для сохранения в БД.
    path_bd : str, optional 
        Путь к базе данных по материалам

    Returns
    -------
        True - если данные были записаны/перезаписаны
        InvalidValue - если на вход дали некорректное имя таблицы или таблицу, 
            тип которой отличается от pd.DataFrame
    """
    is_correct_name = isinstance(name, str) and name not in ["", " ", "  "]
    is_correct_table = isinstance(table, pd.DataFrame)
    if is_correct_name and is_correct_table:
        db, cursor = connect(path_bd)
        cursor.execute(f"DROP TABLE IF EXISTS {name}")
        table.to_sql(name=f'{name}', con=db)
        db.commit()
        db.close()
        return True
    else:
        if not is_correct_name:
            raise InvalidValue(f"Переменная 'name' должна содержать название таблицы. Вы передали: {name}.")
        elif not is_correct_table:
            raise InvalidValue("Переменная 'table' должна содержать таблицу типа pd.DataFrame. Проверьте входные "
                               "данные.")
        return False


def get_name(params: dict, mat_of_cutting_part: str = None) -> str:
    """ Определяет наименование инструмента в зависимости от ГОСТа:
    params - словарь параметров инструмента;
    mat_of_cutting_part - материал режущей части.
    """
    variants = {'ГОСТ 886-77': var_name_tool_2,
                'ГОСТ 2092-77': var_name_tool_2,
                'ГОСТ 4010-77': var_name_tool_2,
                'ГОСТ 8034-76': var_name_tool_1,
                'ГОСТ 10902-77': var_name_tool_2,
                'ГОСТ 10903-77': var_name_tool_2,
                'ГОСТ 12121-77': var_name_tool_2,
                'ГОСТ 12122-77': var_name_tool_2,
                'ГОСТ 14952-75': var_name_tool_1,
                'ГОСТ 17273-71': var_name_tool_3,
                'ГОСТ 17274-71': var_name_tool_3,  # Т в наименовании
                'ГОСТ 17275-71': var_name_tool_3,  # Т в наименовании
                'ГОСТ 17276-71': var_name_tool_3,  # Т в наименовании
                'ГОСТ 19543-74': var_name_tool_1,
                'ГОСТ 19544-74': var_name_tool_1,
                'ГОСТ 19545-74': var_name_tool_1,
                'ГОСТ 19546-74': var_name_tool_1,
                'ГОСТ 19547-74': var_name_tool_1,
                'ГОСТ 20694-75': var_name_tool_1,
                'ГОСТ 20695-75': var_name_tool_1,
                'ГОСТ 20696-75': var_name_tool_1,
                'ГОСТ 20697-75': var_name_tool_1,
                'ГОСТ 22735-77': var_name_tool_2,
                'ГОСТ 22736-77': var_name_tool_2,
                'ГОСТ 28319-89': var_name_tool_1,
                'ГОСТ 28320-89': var_name_tool_1,

                'ГОСТ 12489-71': var_name_tool_4,
                'ГОСТ 21584-76': var_name_tool_1,

                'ГОСТ 1336-77': var_name_tool_5,
                'ГОСТ 3964-69': var_name_tool_6,
                'ГОСТ 5348-69': var_name_tool_3,
                'ГОСТ 6396-78': var_name_tool_6,
                'ГОСТ 6469-69': var_name_tool_3,
                'ГОСТ 6637-80': var_name_tool_7,
                'ГОСТ 7063-72': var_name_tool_1,
                'ГОСТ 8027-86': var_name_tool_8,
                'ГОСТ 8543-71': var_name_tool_6,
                'ГОСТ 9140-78': var_name_tool_6,
                'ГОСТ 9304-69': var_name_tool_1,
                'ГОСТ 9305-93': var_name_tool_1,
                'ГОСТ 9324-80': var_name_tool_8,
                'ГОСТ 9473-80': var_name_tool_3,
                'ГОСТ 10331-81': var_name_tool_8,
                'ГОСТ 10673-75': var_name_tool_1,
                'ГОСТ 13838-68': var_name_tool_9,
                'ГОСТ 15086-69': var_name_tool_1,
                'ГОСТ 15127-83': var_name_tool_8,
                'ГОСТ 16222-81': var_name_tool_1,
                'ГОСТ 16223-81': var_name_tool_1,
                'ГОСТ 16225-81': var_name_tool_1,
                'ГОСТ 16226-81': var_name_tool_1,
                'ГОСТ 16227-81': var_name_tool_6,
                'ГОСТ 16228-81': var_name_tool_1,
                'ГОСТ 16229-81': var_name_tool_1,
                'ГОСТ 16230-81': var_name_tool_1,
                'ГОСТ 16231-81': var_name_tool_1,
                'ГОСТ 16463-80': var_name_tool_6,
                'ГОСТ 18372-73': var_name_tool_3,
                'ГОСТ 17026-71': var_name_tool_1,
                'ГОСТ 20533-75': var_name_tool_1,
                'ГОСТ 23248-78': var_name_tool_1,
                'ГОСТ 24359-80': var_name_tool_1,
                'ГОСТ 24637-81': var_name_tool_1,
                'ГОСТ 28527-90': var_name_tool_6,
                'ГОСТ 28709-90': var_name_tool_1,
                'ГОСТ 28719-90': var_name_tool_1,
                'ГОСТ Р 50181-92': var_name_tool_1,

                'ГОСТ 7722-77': var_name_tool_8,
                'ГОСТ 11179-71': var_name_tool_1,
                'ГОСТ 11180-71': var_name_tool_1,
                'ГОСТ 28321-89': var_name_tool_8,
                'ГОСТ 883-80': var_name_tool_8,

                'ГОСТ 10046-72': var_name_tool_1,
                'ГОСТ 18871-73': var_name_tool_1,
                'ГОСТ 18878-73': var_name_tool_3,
                }
    if params['Стандарт'] in variants:
        get_name = variants[params['Стандарт']]
        return get_name(params, mat_of_cutting_part)
    else:
        raise InvalidValue(
            f"Необходимо добавить вариант определения наименования инструмента для {params['Стандарт']}")


def var_name_tool_1(params: dict, mat_of_cutting_part: str) -> str:
    """ Определяет наименование инструмента в зависимости от типа инструмента,
    обозначения и ГОСТа
    """
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Стандарт"]])


def var_name_tool_2(params: dict, mat_of_cutting_part: str) -> str:
    """ Определяет наименование инструмента в зависимости от типа инструмента,
    обозначения, точности и ГОСТа
    """
    if params["Точность"] in ["B", "В", "A", "А"]:
        return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Стандарт"]])
    else:
        return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Точность"],
                         params["Стандарт"]])


def var_name_tool_3(params: dict, mat_of_cutting_part: str) -> str:
    """ Определяет наименование инструмента в зависимости от типа инструмента,
    обозначения и ГОСТа:
    params - словарь параметров инструмента;
    mat_of_cutting_part - материал режущей части.
    """
    # TODO: Соединить с БД
    mat = {0: "T5K12V", 1: "T5K10", 2: "T14K8", 3: "T15K6", 4: "T30K4",
           5: "BK3", 6: "BK4", 7: "BK6", 8: "BK8", 9: "P18", 10: "P6M5",
           11: "9XC", 12: "ХГВ", 13: "У12А"}
    mat = mat[mat_of_cutting_part] if not isinstance(mat_of_cutting_part, type(None)) else ""
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), mat,
                     params["Стандарт"]])


def var_name_tool_4(params: dict, mat_of_cutting_part: str) -> str:
    """ Определяет наименование инструмента в зависимости от типа инструмента,
    обозначения, допуска на инструмент и ГОСТа;
    params - словарь параметров инструмента.
    """
    return " ".join(
        [params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["d_доп._"], params["Стандарт"]])


def var_name_tool_5(params: dict, mat_of_cutting_part: str) -> str:
    """ Определяет наименование инструмента в зависимости от типа инструмента,
    обозначения, точности обрабатываемой резьбы и ГОСТа;
    params - словарь параметров инструмента.
    """
    if "Точность_резьбы" not in params:
        params["Точность_резьбы"] = "6g"  # TODO: Удалить заглушку
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Точность_резьбы"],
                     params["Стандарт"]])


def var_name_tool_6(params: dict, mat_of_cutting_part: str) -> str:
    """ Определяет наименование инструмента в зависимости от типа инструмента,
    обозначения, точности обрабатываемого паза и ГОСТа;
    params - словарь параметров инструмента.
    """
    # TODO: Удалить заглушку
    if "Точность_паза" not in params:
        params["Точность_паза"] = ""
    elif params["Точность_паза"] == "Фреза общего назначения":
        params["Точность_паза"] = ""
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Точность_паза"],
                     params["Стандарт"]])


def var_name_tool_7(params: dict, mat_of_cutting_part: str) -> str:
    """ Определяет наименование инструмента в зависимости от типа инструмента,
    обозначения, модуля, точности и ГОСТа;
    params - словарь параметров инструмента.
    """
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), str(params["m_n0_"]),
                     params["Точность"], params["Стандарт"]])


def var_name_tool_8(params: dict, mat_of_cutting_part: str) -> str:
    """ Определяет наименование инструмента в зависимости от типа инструмента,
    обозначения, точности и ГОСТа;
    params - словарь параметров инструмента.
    """
    if "Точность" not in params or isinstance(params["Точность"], type(None)):
        params["Точность"] = "H7"  # TODO: Удалить заглушку
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Точность"],
                     params["Стандарт"]])


def var_name_tool_9(params: dict, mat_of_cutting_part: str) -> str:
    """ Определяет наименование инструмента в зависимости от типа инструмента,
    обозначения, номера фрезы и ГОСТа;
    params - словарь параметров инструмента.
    """
    # TODO: Добавить выбор номера фрезы и выбор количества зубьев
    if "Номер" not in params:
        params["Номер"] = 'N1'
    return " ".join(
        [params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Номер"], params["Стандарт"]])


def get_index_type_cutter(type_cutter: str = None, condition: str = None,) -> int:
    """ Определяет индекс типа инструмента

    Parameters
    ----------
    type_cutter : str, optional
        Текстовое описание типа инструмента по стандарту
    condition : str, optional
        Условие обработки (Например - 'Обработка торца').

    Returns
    -------
        index : int
            Индекс типа инструмента.
    """
    indexes_types_cutter = {'Концевая (для T-образных пазов)': 6,
                            'Торцовая': 1,
                            'Торцовая, Цилиндрическая': 1,
                            'Угловая': 7,
                            'Фасонная, с выпуклым профилем': 8,
                            'Дисковая': 2,
                            'Концевая': 5,
                            'Резьбовая': 0,
                            'Шпоночная': 10,
                            'Концевая (для обработки Т-образного паза)': 6,
                            'Пазовая': 6,
                            'Червячная': 0,
                            'Отрезная': 4,
                            "Круглая": 0,
                            "Квадратная": 1,
                            "Многогранная": 2,
                            "Одношпоночная": 3,
                            "Многошпоночная": 4,
                            "Шлицевая": 5,
                            "Координатная": 6,
                            "Прочие": 7}
    index = indexes_types_cutter[type_cutter]
    if not isinstance(condition, type(None)):
        if type_cutter == 'Торцовая, Цилиндрическая':
            if condition == 'Торцовая':
                index = 1
            elif condition == 'Цилиндрическая':
                index = 0
            else:
                message = "Схема обработки не определена!"
                raise InvalidValue(message)
        elif type_cutter == 'Дисковая':
            if condition == 'Обработка торца':
                index = 2
            elif condition == 'Обработка паза':
                index = 3
            else:
                message = "Схема обработки не определена!"
                raise InvalidValue(message)
        elif type_cutter == 'Концевая':
            if condition == 'Обработка торца':
                index = 5
            elif condition == 'Обработка паза':
                index = 6
            else:
                message = "Схема обработки не определена!"
                raise InvalidValue(message)
    return index
