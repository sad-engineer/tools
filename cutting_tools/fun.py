#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import sqlite3
import pandas as pd
from typing import Optional
from cutting_tools.obj.constants import PATH_DB_FOR_TOOLS as PATH_DB
from cutting_tools.obj.constants import MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.exceptions import InvalidValue


def get_name(params: dict, mat_of_cutting_part: str):
    """ Определяет наименование инструмента в зависимости от ГОСТа

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    variants = {
        # Сверла
        'ГОСТ 886-77': var_name_tool_2,
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
        # Зенкеры
        'ГОСТ 12489-71': var_name_tool_4,
        'ГОСТ 21584-76': var_name_tool_1,
        # Фрезы
        'ГОСТ 1336-77': var_name_tool_5,
        'ГОСТ 3964-69': var_name_tool_6,
        'ГОСТ 5348-69': var_name_tool_3,
        'ГОСТ 6396-78': var_name_tool_6,
        'ГОСТ 6469-69': var_name_tool_3,
        'ГОСТ 6637-80': var_name_tool_7,
        'ГОСТ 7063-72': var_name_tool_1,
        'ГОСТ 8027-86': var_name_tool_2,
        'ГОСТ 8543-71': var_name_tool_6,
        'ГОСТ 9140-78': var_name_tool_6,
        'ГОСТ 9304-69': var_name_tool_1,
        'ГОСТ 9305-93': var_name_tool_1,
        'ГОСТ 9324-80': var_name_tool_2,
        'ГОСТ 9473-80': var_name_tool_3,
        'ГОСТ 10331-81': var_name_tool_2,
        'ГОСТ 10673-75': var_name_tool_1,
        'ГОСТ 13838-68': var_name_tool_8,
        'ГОСТ 15086-69': var_name_tool_1,
        'ГОСТ 15127-83': var_name_tool_2,
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
        'ГОСТ 20534-75': var_name_tool_1,
        'ГОСТ 20535-75': var_name_tool_1,
        'ГОСТ 20538-75': var_name_tool_1,
        'ГОСТ 22088-76': var_name_tool_1,
        'ГОСТ 23248-78': var_name_tool_1,
        'ГОСТ 24359-80': var_name_tool_1,
        'ГОСТ 24637-81': var_name_tool_1,
        'ГОСТ 28527-90': var_name_tool_6,
        'ГОСТ 28709-90': var_name_tool_1,
        'ГОСТ 28719-90': var_name_tool_1,
        'ГОСТ Р 50181-92': var_name_tool_1,
        # Развертки
        'ГОСТ 7722-77': var_name_tool_2,
        'ГОСТ 11179-71': var_name_tool_1,
        'ГОСТ 11180-71': var_name_tool_1,
        'ГОСТ 28321-89': var_name_tool_2,
        'ГОСТ 883-80': var_name_tool_2,
        # Резцы
        'ГОСТ 10046-72': var_name_tool_1,
        'ГОСТ 18871-73': var_name_tool_1,
        'ГОСТ 18878-73': var_name_tool_3,
        }
    if params['Стандарт'] in variants:
        return variants[params['Стандарт']](params, mat_of_cutting_part)
    else:
        raise InvalidValue(f"Необходимо добавить вариант определения наименования инструмента для {params['Стандарт']}")


def var_name_tool_1(params: dict, mat_of_cutting_part: str) -> str:
    """ Наименование состоит из наименования, обозначения и стандарта.

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Стандарт"]])


def var_name_tool_2(params: dict, mat_of_cutting_part: str) -> str:
    """ Наименование состоит из наименования, обозначения, точности(опционально) и стандарта.

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    if "Точность" not in params:
        return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Стандарт"]])
    elif isinstance(params["Точность"], type(None)):
        return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Стандарт"]])
    elif params["Точность"] in ["B", "В", "A", "А"]:
        return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Стандарт"]])
    else:
        return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Точность"],
                         params["Стандарт"]])


def var_name_tool_3(params: dict, mat_of_cutting_part: str) -> str:
    """ Наименование состоит из наименования, обозначения, материала режущей части и стандарта.

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    # TODO: Соединить с БД
    if mat_of_cutting_part not in MATERIALS_OF_CUTTING_PART:
        raise InvalidValue(f"В качестве материала режущей части ({mat_of_cutting_part}) передан не верный параметр.")
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), mat_of_cutting_part,
                     params["Стандарт"]])


def var_name_tool_4(params: dict, mat_of_cutting_part: str) -> str:
    """ Наименование состоит из наименования, обозначения, допуска инструмента и стандарта.

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    # TODO: Удалить заглушку
    if "d_доп._" not in params:
        params["d_доп._"] = "h14"
    elif isinstance(params["d_доп._"], type(None)):
        params["d_доп._"] = "h14"
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["d_доп._"],
                     params["Стандарт"]])


def var_name_tool_5(params: dict, mat_of_cutting_part: str) -> str:
    """ Наименование состоит из наименования, обозначения, точности резьбы и стандарта.

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    # TODO: Удалить заглушку
    if "Точность_резьбы" not in params:
        params["Точность_резьбы"] = "6g"
    elif isinstance(params["Точность_резьбы"], type(None)):
        params["Точность_резьбы"] = "6g"
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Точность_резьбы"],
                     params["Стандарт"]])


def var_name_tool_6(params: dict, mat_of_cutting_part: str) -> str:
    """ Наименование состоит из наименования, обозначения, точности паза и стандарта.

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    # TODO: Удалить заглушку
    if "Точность_паза" not in params:
        return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Стандарт"]])
    elif params["Точность_паза"] == "Фреза общего назначения" or isinstance(params["Точность_паза"], type(None)):
        return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Стандарт"]])
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Точность_паза"],
                     params["Стандарт"]])


def var_name_tool_7(params: dict, mat_of_cutting_part: str) -> str:
    """ Наименование состоит из наименования, обозначения, модуля (фрезы) и стандарта.

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    return " ".join([params["Тип_инструмента"], params["Обозначение"].replace("*", ""), str(params["m_n0_"]),
                     params["Точность"], params["Стандарт"]])


def var_name_tool_8(params: dict, mat_of_cutting_part: str) -> str:
    """ Наименование состоит из наименования, обозначения, номера и стандарта.

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    # TODO: Добавить выбор номера фрезы и выбор количества зубьев
    if "Номер" not in params:
        params["Номер"] = 'N1'
    elif isinstance(params["Номер"], type(None)):
        params["Номер"] = "N1"
    return " ".join(
        [params["Тип_инструмента"], params["Обозначение"].replace("*", ""), params["Номер"], params["Стандарт"]])


def get_index_type_cutter(type_cutter: str = None, condition: str = None,) -> int:
    """ Определяет индекс типа инструмента.

    :param type_cutter: Текстовое описание типа инструмента по стандарту.
    :param condition: Условие обработки (Например - 'Обработка торца').
    :return: Индекс типа инструмента.
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
                raise InvalidValue("Схема обработки не определена!")
        elif type_cutter == 'Дисковая':
            if condition == 'Обработка торца':
                index = 2
            elif condition == 'Обработка паза':
                index = 3
            else:
                raise InvalidValue("Схема обработки не определена!")
        elif type_cutter == 'Концевая':
            if condition == 'Обработка торца':
                index = 5
            elif condition == 'Обработка паза':
                index = 6
            else:
                raise InvalidValue("Схема обработки не определена!")
    return index





def show_cutting_tool(cutting_tool) -> None:
    """ Выводит параметры класса "Режущий инструмент" в консоль.

    :param cutting_tool: класс "Режущий инструмент".
    """
    if cutting_tool.kind_of_cut == "broaching":
        print(f"""### Параметры применяемого режущего инструмента (протяжки) ###""")
        if not isinstance(cutting_tool.type_cutter, type(None)):
            print(f"""Тип инструмента: {cutting_tool.type_cutter}.""")
        if not isinstance(cutting_tool.angle_of_inclination, type(None)):
            print(f"""Угол наклона зубьев протяжки: {cutting_tool.angle_of_inclination}.""")
        if not isinstance(cutting_tool.pitch_of_teeth, type(None)):
            print(f"""Шаг зубьев протяжки: {cutting_tool.pitch_of_teeth}.""")
        if not isinstance(cutting_tool.number_teeth_section, type(None)):
            print(f"""Число зубьев секции протяжки: {cutting_tool.number_teeth_section}.""")
        if not isinstance(cutting_tool.difference, type(None)):
            print(f"""Подача на зуб протяжки: {cutting_tool.difference}.""")
        if not isinstance(cutting_tool.length_of_working_part, type(None)):
            print(f"""Длина режущей части протяжки: {cutting_tool.length_of_working_part}.""")
    else:
        print(f"""### Параметры применяемого режущего инструмента ###""")
        if not isinstance(cutting_tool.name, type(None)):
            print(f"""Обозначение инструмента: {cutting_tool.name}.""")
        if not isinstance(cutting_tool.type_cutter, type(None)):
            print(f"""Тип инструмента: {cutting_tool.type_cutter}.""")
        if not isinstance(cutting_tool.dia_mm, type(None)):
            print(f"""Диаметр инструмента = {cutting_tool.dia_mm} мм.""")
        if not isinstance(cutting_tool.height_mm, type(None)):
            print(f"""Высота инструмента = {cutting_tool.height_mm} мм.""")
        if not isinstance(cutting_tool.width_mm, type(None)):
            print(f"""Ширина инструмента = {cutting_tool.width_mm} мм.""")
        if not isinstance(cutting_tool.num_of_cutting_blades, type(None)):
            print(f"""Количество режущих лезвий инструмента = {cutting_tool.num_of_cutting_blades} шт.""")
        if not isinstance(cutting_tool.type_of_mat, type(None)):
            print(f"""Тип материала инструмента: {cutting_tool.type_of_mat}.""")
        if not isinstance(cutting_tool.mat_of_cutting_part, type(None)):
            print(f"""Материал инструмента: {cutting_tool.mat_of_cutting_part}.""")
        if not isinstance(cutting_tool.type_of_cutting_part, type(None)):
            print(f"""Вид режущей части инструмента: {cutting_tool.type_of_cutting_part}.""")
        if not isinstance(cutting_tool.additional_blade, type(None)):
            print(f"""Наличие дополнительного лезвия: {cutting_tool.additional_blade}.""")
        if not isinstance(cutting_tool.large_tooth, type(None)):
            print(f"""Крупный/мелкий зуб: {cutting_tool.large_tooth}.""")
        if not isinstance(cutting_tool.deep_or_complex_profile, type(None)):
            print(f"""Показатель наличия глубокого или сложного профиля: {cutting_tool.deep_or_complex_profile}.""")
        if not isinstance(cutting_tool.quantity, type(None)):
            print(f"""Количество одновременно работающих инструментов: {cutting_tool.quantity}.""")
        if not isinstance(cutting_tool.turret, type(None)):
            print(f"""Инструмент установлен на револьверную головку: {cutting_tool.turret}.""")
        if not isinstance(cutting_tool.load, type(None)):
            print(f"""Нагрузка на инструмент: {cutting_tool.load}.""")
        if not isinstance(cutting_tool.main_angle_grad, type(None)):
            print(f"""Главный угол в плане: {cutting_tool.main_angle_grad}.""")
        if not isinstance(cutting_tool.front_angle_grad, type(None)):
            print(f"""Передний угол в плане: {cutting_tool.front_angle_grad}.""")
        if not isinstance(cutting_tool.inclination_of_main_blade, type(None)):
            print(f"""Угол наклона переднего лезвия: {cutting_tool.inclination_of_main_blade}.""")
        if not isinstance(cutting_tool.radius_of_cutting_vertex, type(None)):
            print(f"""Радиус режущей вершины инструмента: {cutting_tool.radius_of_cutting_vertex}.""")
        if not isinstance(cutting_tool.blade_length, type(None)):
            print(f"""Длина лезвия инструмента: {cutting_tool.blade_length}. """)

