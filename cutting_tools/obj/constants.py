#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Расположение БД
PATH_DB_FOR_TOOLS = f"{__file__}".replace("obj\\constants.py", "data\\cutting_tools.db")
# Настройки начальных данных
DEFAULT_SETTINGS_FOR_CUTTING_TOOL = {
    "milling":        {"marking": '2214-0507', "Стандарт": "ГОСТ 16223-81", "quantity": 1, "type_of_mat": 0,
                       "mat_of_cutting_part": "Р6М5"},
    "turning":        {"marking": '2100-0029', "Стандарт": "ГОСТ 18878-73", "quantity": 1, "type_of_mat": 0,
                       "mat_of_cutting_part": "Р6М5"},
    "planing":        {"marking": '2180-0803', "Стандарт": "ГОСТ 10046-72", "quantity": 1, "type_of_mat": 0,
                       "mat_of_cutting_part": "Р6М5"},
    "drilling":       {"marking": '2300-0041', "Стандарт": "ГОСТ 886-77", "quantity": 1, "type_of_mat": 0,
                       "mat_of_cutting_part": "Р6М5"},
    "countersinking": {"marking": '2320-2125', "Стандарт": "ГОСТ 21584-76", "quantity": 1, "type_of_mat": 0,
                       "mat_of_cutting_part": "Р6М5"},
    "deployment":     {"marking": '2364-0331', "Стандарт": "ГОСТ 883-80", "quantity": 1, "type_of_mat": 0,
                       "mat_of_cutting_part": "Р6М5"},
    "broaching":      {"pitch_of_teeth": 0.5,           # шаг зубьев
                       "angle_of_inclination": 0,       # угол наклона зубьев
                       "number_teeth_section": 5,       # количество зубьев в секции
                       "type_cutter": 0,                # тип протяжки (шлицевая, круглая и пр.)
                       "difference": 0.1,               # размерный перепад между соседними зубьями
                       "length_of_working_part": 1000,  # длина режущей части протяжки
                       },
        }
INDEXES_HARD_ALLOYS = {"Т5К12В": 0, "Т5К10": 1, "Т14К8": 2, "Т15К6":  3, "Т30К4": 4, "ВК3": 5, "ВК4": 6, "ВК6": 7,
                       "ВК8": 8}
INDEXES_HIGH_SPEED_STEELS = {"Р18": 9, "Р6М5": 10, "9ХС": 11, "ХГВ": 12, "У12А": 13}
# Словарь индексов материалов режущей части с доступом по наименованию
INDEXES_OF_MATERIALS_OF_CUTTING_PART = INDEXES_HARD_ALLOYS | INDEXES_HIGH_SPEED_STEELS
# Словарь наименований материалов режущей части с доступом по индексу
NAMES_OF_MATERIALS_OF_CUTTING_PART = {v: k for k, v in INDEXES_OF_MATERIALS_OF_CUTTING_PART.items()}
# NAMES_OF_MATERIALS_OF_CUTTING_PART = {0: "Т5К12В", 1: "Т5К10", 2: "Т14К8", 3: "Т15К6", 4: "Т30К4", 5: "ВК3", 6: "ВК4",
#                                       7: "ВК6", 8: "ВК8", 9: "Р18", 10: "Р6М5", 11: "9ХС", 12: "ХГВ", 13: "У12А"}

# Словарь наименований группы инструмента
GROUPS_TOOL = {"Инструмент": 0,
               "Резец": 1,
               "Фреза": 2,
               "Сверло": 3,
               "Зенкер": 4,
               "Развертка": 5,
               "Протяжка": 6,
               }
# Типы стандартов инструмента
TYPES_STANDARD = ["ГОСТ", "ОСТ", ]

# Типы фрез:
TYPES_OF_MILLING_CUTTER = {0: "Цилиндрическая/Червячная", 1: "Торцовая", 2: "Дисковая, обработка торца",
                           3: "Дисковая, обработка паза/Пазовая", 4: "Отрезная и прорезная",
                           5: "Концевая, обработка торца", 6: "Концевая, обработка паза", 7: "Угловая",
                           8: "Фасонная, с выпуклым профилем/Резьбовая", 9: "Фасонная, с вогнутым профилем",
                           10: "Шпоночная"}
# Типы режущей части фрезы:
TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER = {0: "Винтовые пластинки", 1: "Цельная", 2: "Коронка"}
# Типы частоты шага:
TYPES_OF_LARGE_TOOTH = {0: "Крупный шаг", 1: "Мелкий шаг"}
