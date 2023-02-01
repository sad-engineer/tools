#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.tool import Tool
from cutting_tools.obj.sizes import AxialSizes
from cutting_tools.obj.blade_material import BladeMaterial
from cutting_tools.obj.angles import Angles
from cutting_tools.obj.tolerance import Tolerance
from cutting_tools.obj.interfaces import INumOfBlades, IRadius, IQuantity
from cutting_tools.fun import get_name


class DrillingCutter(Tool, AxialSizes, BladeMaterial, Angles, Tolerance, INumOfBlades, IRadius, IQuantity):
    """ Управляет полями класса "Сверло"

    Parameters:
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        dia_mm : (float >= 0) : диаметр инструмента.
        length_mm : (float >= 0) : длина инструмента.
        mat_of_cutting_part : (str, int is MATERIALS_OF_CUTTING_PART) : материал режущей пластины.
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
        parameters : (dict) : возвращает словарь параметров и свойств.

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
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS_FOR_CUTTING_TOOL['drilling']

    def __init__(self,
                 marking: str = str(DEFAULT_SETTINGS["marking"]),
                 standard: str = str(DEFAULT_SETTINGS["Стандарт"]),
                 dia_mm: float = 2.4,
                 length_mm: float = 95,
                 mat_of_cutting_part: Union[str, int] = str(DEFAULT_SETTINGS["mat_of_cutting_part"]),
                 main_angle_grad: float = 59,
                 front_angle_grad: float = 0,
                 inclination_of_main_blade_grad: float = 0,
                 num_of_cutting_blades: int = 2,
                 radius_of_cutting_vertex: float = 1,
                 quantity: int = int(DEFAULT_SETTINGS["quantity"]),
                 tolerance: Union[str, int, float] = DEFAULT_SETTINGS["tolerance"],
                 ):
        Tool.__init__(self, "Сверло", marking, standard)
        AxialSizes.__init__(self, dia_mm, length_mm)
        BladeMaterial.__init__(self, mat_of_cutting_part)
        Angles.__init__(self, main_angle_grad, front_angle_grad, inclination_of_main_blade_grad)
        Tolerance.__init__(self, tolerance)
        INumOfBlades.__init__(self, num_of_cutting_blades)
        IRadius.__init__(self, radius_of_cutting_vertex)
        IQuantity.__init__(self, quantity)

    @property
    def name(self):
        standard_name = " ".join([self._group, self._marking, self._standard])
        tool_parameters = {"group": self._group, "marking": self._marking, "standard": self._standard,
                           "mat_of_cutting_part": self._mat_of_cutting_part, "tolerance": self.tolerance}
        unique_name = get_name(tool_parameters)
        return unique_name if not isinstance(unique_name, type(None)) else standard_name

    def _parameters(self):
        tool_parameters = Tool._parameters(self)
        size_parameters = AxialSizes._parameters(self)
        blade_material_parameters = BladeMaterial._parameters(self)
        angles_parameters = Angles._parameters(self)
        tolerance_parameters = Tolerance._parameters(self)
        inumofblades = INumOfBlades._parameters(self)
        iradius = IRadius._parameters(self)
        iquantity = IQuantity._parameters(self)
        return tool_parameters | size_parameters | blade_material_parameters | angles_parameters | \
               tolerance_parameters | inumofblades | iradius | iquantity


if __name__ == "__main__":
    cutter = DrillingCutter()
    cutter.standard = 'ГОСТ 10903-77'
    print(cutter.parameters)
    cutter.tolerance = 'H8'
    print(cutter.parameters)

    cutter.tolerance = 'H12'
    print(cutter.parameters)
