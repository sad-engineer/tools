#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
from logger.obj.exceptions import InvalidValue


def get_name(params: dict):
    """ Определяет наименование инструмента в зависимости от ГОСТа

    :param params: словарь параметров инструмента.
    :param mat_of_cutting_part: материал режущей части.
    :return: Наименование инструмента по ГОСТу.
    """
    variants = {
        # Сверла
        'ГОСТ 886-77': name_tool_with_accuracy,
        'ГОСТ 2092-77': name_tool_with_accuracy,
        'ГОСТ 4010-77': name_tool_with_accuracy,
        'ГОСТ 8034-76': None,
        'ГОСТ 10902-77': name_tool_with_accuracy,
        'ГОСТ 10903-77': name_tool_with_accuracy,
        'ГОСТ 12121-77': name_tool_with_accuracy,
        'ГОСТ 12122-77': name_tool_with_accuracy,
        'ГОСТ 14952-75': None,
        'ГОСТ 17273-71': name_tool_with_material,
        'ГОСТ 17274-71': name_tool_with_material,  # TODO: Т в наименовании
        'ГОСТ 17275-71': name_tool_with_material,  # TODO: Т в наименовании
        'ГОСТ 17276-71': name_tool_with_material,  # TODO: Т в наименовании
        'ГОСТ 19543-74': None,
        'ГОСТ 19544-74': None,
        'ГОСТ 19545-74': None,
        'ГОСТ 19546-74': None,
        'ГОСТ 19547-74': None,
        'ГОСТ 20694-75': None,
        'ГОСТ 20695-75': None,
        'ГОСТ 20696-75': None,
        'ГОСТ 20697-75': None,
        'ГОСТ 22735-77': name_tool_with_accuracy,
        'ГОСТ 22736-77': name_tool_with_accuracy,
        'ГОСТ 28319-89': None,
        'ГОСТ 28320-89': None,
        # Зенкеры
        'ГОСТ 12489-71': name_tool_with_accuracy,
        'ГОСТ 21584-76': None,
        # Фрезы
        'ГОСТ 1336-77': name_tool_with_accuracy,
        'ГОСТ 3964-69': name_tool_with_accuracy,
        'ГОСТ 5348-69': name_tool_with_material,
        'ГОСТ 6396-78': name_tool_with_accuracy,
        'ГОСТ 6469-69': name_tool_with_material,
        'ГОСТ 6637-80': name_tool_with_accuracy_class_and_module,
        'ГОСТ 7063-72': None,
        'ГОСТ 8027-86': name_tool_with_accuracy_class,
        'ГОСТ 8543-71': name_tool_with_accuracy,
        'ГОСТ 9140-78': name_tool_with_accuracy,
        'ГОСТ 9304-69': None,
        'ГОСТ 9305-93': None,
        'ГОСТ 9324-80': name_tool_with_accuracy_class,
        'ГОСТ 9473-80': name_tool_with_material,
        'ГОСТ 10331-81': name_tool_with_accuracy_class,
        'ГОСТ 10673-75': None,
        'ГОСТ 13838-68': name_tool_with_number,
        'ГОСТ 15086-69': None,
        'ГОСТ 15127-83': name_tool_with_accuracy_class,
        'ГОСТ 16222-81': None,
        'ГОСТ 16223-81': None,
        'ГОСТ 16225-81': None,
        'ГОСТ 16226-81': None,
        'ГОСТ 16227-81': name_tool_with_accuracy,
        'ГОСТ 16228-81': None,
        'ГОСТ 16229-81': None,
        'ГОСТ 16230-81': None,
        'ГОСТ 16231-81': None,
        'ГОСТ 16463-80': name_tool_with_accuracy,
        'ГОСТ 18372-73': name_tool_with_material,
        'ГОСТ 17026-71': None,
        'ГОСТ 20533-75': None,
        'ГОСТ 20534-75': None,
        'ГОСТ 20535-75': None,
        'ГОСТ 20538-75': None,
        'ГОСТ 22088-76': None,
        'ГОСТ 23248-78': None,
        'ГОСТ 24359-80': None,
        'ГОСТ 24637-81': None,
        'ГОСТ 28527-90': name_tool_with_accuracy,
        'ГОСТ 28709-90': None,
        'ГОСТ 28719-90': None,
        'ГОСТ Р 50181-92': None,
        # Развертки
        'ГОСТ 7722-77': name_tool_with_accuracy,
        'ГОСТ 11179-71': None,
        'ГОСТ 11180-71': None,
        'ГОСТ 28321-89': None,
        'ГОСТ 883-80': name_tool_with_accuracy,
        # Резцы
        'ГОСТ 10046-72': None,
        'ГОСТ 18871-73': None,
        'ГОСТ 18878-73': name_tool_with_material,
        }
    if params['standard'] in variants:
        name_getter = variants[params['standard']]
        return name_getter(params) if not isinstance(name_getter, type(None)) else None
    raise InvalidValue(f"Необходимо добавить вариант определения наименования инструмента для инструмента "
                       f"{params['group']} {params['standard']}")


def name_tool_with_accuracy(params: dict) -> str:
    """ Наименование состоит из наименования, обозначения, точности(опционально) и стандарта."""
    return " ".join([params["group"], params["marking"], params["tolerance"], params["standard"]])


def name_tool_with_accuracy_class(params: dict) -> str:
    """ Наименование состоит из наименования, обозначения, точности(опционально) и стандарта."""
    return " ".join([params["group"], params["marking"], params["accuracy_class"], params["standard"]])


def name_tool_with_material(params: dict,) -> str:
    """ Наименование состоит из наименования, обозначения, материала режущей части и стандарта. """
    return " ".join([params["group"], params["marking"], params["mat_of_cutting_part"], params["standard"]])


def name_tool_with_number(params: dict,) -> str:
    """ Наименование состоит из наименования, обозначения, материала режущей части и стандарта. """
    return " ".join([params["group"], params["marking"], params["cutter_number"], params["standard"]])


def name_tool_with_accuracy_class_and_module(params: dict) -> str:
    """ Наименование состоит из наименования, обозначения, точности(опционально) и стандарта."""
    return " ".join([params["group"], params["marking"], params["module"], params["accuracy_class"],
                     params["standard"]])



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


# def get_index_type_cutter(type_cutter: str = None, condition: str = None,) -> int:
#     """ Определяет индекс типа инструмента.
#
#     :param type_cutter: Текстовое описание типа инструмента по стандарту.
#     :param condition: Условие обработки (Например - 'Обработка торца').
#     :return: Индекс типа инструмента.
#     """
#     indexes_types_cutter = {'Концевая (для T-образных пазов)': 6,
#                             'Торцовая': 1,
#                             'Торцовая, Цилиндрическая': 1,
#                             'Угловая': 7,
#                             'Фасонная, с выпуклым профилем': 8,
#                             'Дисковая': 2,
#                             'Концевая': 5,
#                             'Резьбовая': 0,
#                             'Шпоночная': 10,
#                             'Концевая (для обработки Т-образного паза)': 6,
#                             'Пазовая': 6,
#                             'Червячная': 0,
#                             'Отрезная': 4,
#                             "Круглая": 0,
#                             "Квадратная": 1,
#                             "Многогранная": 2,
#                             "Одношпоночная": 3,
#                             "Многошпоночная": 4,
#                             "Шлицевая": 5,
#                             "Координатная": 6,
#                             "Прочие": 7}
#     index = indexes_types_cutter[type_cutter]
#     if not isinstance(condition, type(None)):
#         if type_cutter == 'Торцовая, Цилиндрическая':
#             if condition == 'Торцовая':
#                 index = 1
#             elif condition == 'Цилиндрическая':
#                 index = 0
#             else:
#                 raise InvalidValue("Схема обработки не определена!")
#         elif type_cutter == 'Дисковая':
#             if condition == 'Обработка торца':
#                 index = 2
#             elif condition == 'Обработка паза':
#                 index = 3
#             else:
#                 raise InvalidValue("Схема обработки не определена!")
#         elif type_cutter == 'Концевая':
#             if condition == 'Обработка торца':
#                 index = 5
#             elif condition == 'Обработка паза':
#                 index = 6
#             else:
#                 raise InvalidValue("Схема обработки не определена!")
#     return index
