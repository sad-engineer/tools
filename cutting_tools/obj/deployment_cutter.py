#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.drilling_cutter import DrillingCutter


class DeploymentCutter(DrillingCutter):
    """ Управляет полями класса "Развертка"

    Parameters:
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        dia_mm : (float >= 0) : диаметр инструмента.
        length_mm : (float >= 0) : длина инструмента.
        mat_of_cutting_part : (str, int in MATERIALS_OF_CUTTING_PART) : материал режущей пластины.
        main_angle_grad : (float >= 0) : главный угол в плане.
        front_angle_grad  : (float >= 0) : передний угол.
        inclination_of_main_blade_grad  : (float >= 0) : наклон передней грани.
        tolerance : (str, int содержит по одному из ACCURACY_STANDARDS, TOLERANCE_FIELDS) : допуск.
        num_of_cutting_blades : (int >= 0) : количество режущих граней.
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.
        quantity : (int >= 0) : количество одновременно работающих инструментов.

    Properties:
        name : (str) : возвращает название инструмента.
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.
        type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
        dict_parameters : (dict) : возвращает словарь параметров и свойств.

    Сostants:
        GROUPS_TOOL : Словарь наименований группы инструмента.
        TYPES_STANDARD : Типы стандартов инструмента.
        HARD_ALLOYS : перечень доступных твердосплавных материалов.
        HIGH_SPEED_STEELS : перечень доступных быстрорежущих материалов.
        MATS_OF_CUTTING_PART : перечень доступных материалов режущей части (общий).
        ACCURACY_STANDARDS : Квалитеты точности обработки.
        TOLERANCE_FIELDS : Поля допусков.
        DEFAULT_SETTINGS : Настройки по умолчанию.
    """
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["deployment"]

    def __init__(self,
                 marking: str = str(DEFAULT_SETTINGS["marking"]),
                 standard: str = str(DEFAULT_SETTINGS["Стандарт"]),
                 dia_mm: float = 2.4,
                 length_mm: float = 95,
                 mat_of_cutting_part: Union[str, int] = str(DEFAULT_SETTINGS["mat_of_cutting_part"]),
                 main_angle_grad: float = 90,
                 front_angle_grad: float = 0,
                 inclination_of_main_blade_grad: float = 0,
                 num_of_cutting_blades: int = 2,
                 radius_of_cutting_vertex: float = 1,
                 quantity: int = int(DEFAULT_SETTINGS["quantity"]),
                 accuracy: Union[str, int, float] = DEFAULT_SETTINGS["tolerance"],
                 ):
        DrillingCutter.__init__(self, marking, standard, dia_mm, length_mm, mat_of_cutting_part, main_angle_grad,
                                front_angle_grad, inclination_of_main_blade_grad, num_of_cutting_blades,
                                radius_of_cutting_vertex, quantity, accuracy)
        self.group = "Развертка"


if __name__ == "__main__":
    cutter = DeploymentCutter()
    print(cutter.dict_parameters)
    cutter.standard = "ГОСТ 883-80"
    print(cutter.name)
