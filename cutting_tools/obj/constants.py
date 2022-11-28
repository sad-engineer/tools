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
    "broaching":      {"pitch_of_teeth": 0.5,      # шаг зубьев
                       "angle_of_inclination": 0,  # угол наклона зубьев
                       "number_teeth_section": 5,  # количество зубьев в секции
                       "type_cutter": 0,           # тип протяжки (шлицевая, круглая и пр.)
                       "difference": 0.1,          # размерный перепад между соседними зубьями
                       },
        }
# Словарь индексов материалов режущей части с доступом по наименованию
INDEXES_OF_MATERIALS_OF_CUTTING_PART = {"T5K12V": 0, "T5K10": 1, "T14K8": 2, "T15K6":  3, "T30K4": 4, "BK3": 5,
                                        "BK4": 6, "BK6": 7, "BK8": 8, "P18": 9, "P6M5": 10, "9XC": 11, "ХГВ": 12,
                                        "У12А": 13}
# Словарь наименований материалов режущей части с доступом по индексу
NAMES_OF_MATERIALS_OF_CUTTING_PART = {0: "T5K12V", 1: "T5K10", 2: "T14K8", 3: "T15K6", 4: "T30K4", 5: "BK3", 6: "BK4",
                                      7: "BK6", 8: "BK8", 9: "P18", 10: "P6M5", 11: "9XC", 12: "ХГВ", 13: "У12А"}
