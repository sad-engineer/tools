#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        constants
# Purpose:     Contains local constants
#
# Author:      ANKorenuk
#
# Created:     2.06.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит локальные переменные
# -------------------------------------------------------------------------------
# Расположение БД
PATH_DB_FOR_TOOLS = f"{__file__}".replace("obj\\constants.py", "data\\cutting_tools.db")
# Настройки начальных данных
DEFAULT_SETTINGS_FOR_CUTTING_TOOL = {
    "milling":        {"marking": '2214-0507', "Стандарт": "ГОСТ 16223-81", "quantity": 1, "type_of_mat": 0, },
    "turning":        {"marking": '2100-0029', "Стандарт": "ГОСТ 18878-73", "quantity": 1, "type_of_mat": 0, },
    "planing":        {"marking": '2180-0803', "Стандарт": "ГОСТ 10046-72", "quantity": 1, "type_of_mat": 0, },
    "drilling":       {"marking": '2300-0041', "Стандарт": "ГОСТ 886-77", "quantity": 1, "type_of_mat": 0, },
    "countersinking": {"marking": '2320-2125', "Стандарт": "ГОСТ 21584-76", "quantity": 1, "type_of_mat": 0, },
    "deployment":     {"marking": '2364-0331', "Стандарт": "ГОСТ 883-80", "quantity": 1, "type_of_mat": 0, },
    "broaching":      {"pitch_of_teeth": 0.5,      #шаг зубьев
                       "angle_of_inclination": 0,  #угол наклона зубьев
                       "number_teeth_section": 5,  #количество зубьев в секции
                       "type_cutter": 0,           #тип протяжки (шлицевая, круглая и пр.)
                       "difference": 0.1,          #размерный перепад между соседними зубьями
                      },
    }
