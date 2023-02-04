#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union, Optional

from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.tool import Tool
from cutting_tools.obj.sizes import AxialSizes
from cutting_tools.obj.blade_material import BladeMaterial
from cutting_tools.obj.angles import Angles
from cutting_tools.obj.tolerance import Tolerance
from cutting_tools.obj.interfaces import INumOfBlades
from cutting_tools.obj.interfaces import IRadius
from cutting_tools.obj.interfaces import IQuantity
from cutting_tools.obj.interfaces import IAccuracyClass
from cutting_tools.obj.interfaces import ITypeCutter
from cutting_tools.obj.interfaces import ITypeOfCuttingPart
from cutting_tools.obj.interfaces import ILargeTooth
from cutting_tools.obj.interfaces import ICutterNumber
from cutting_tools.obj.interfaces import IModule
from cutting_tools.fun import get_name


class MillingCutter(Tool, AxialSizes, BladeMaterial, Angles, Tolerance, ITypeCutter, ITypeOfCuttingPart, ILargeTooth,
                    INumOfBlades, IRadius, IQuantity, IAccuracyClass, ICutterNumber, IModule):
    """ Управляет полями класса "Фреза".

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
        type_cutter : (str, int, float in TYPES_OF_MILLING_CUTTER) : Тип инструмента:
        type_of_cutting_part : (str, int, float in TYPES_OF_CUTTING_PART) : тип режущей части.
        large_tooth : (str, int, float in TYPES_OF_LARGE_TOOTH) :  Крупный/мелкий зуб.
        num_of_cutting_blades : (int >= 0) : количество режущих граней.
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.
        quantity : (int >= 0) : количество одновременно работающих инструментов.
        accuracy_class : (str, int in ACCURACY_CLASS_STANDARDS) : класс точности инструмента.
        cutter_number : (Optional[str]) : номер фрезы ("1", "1 1/2", и т.д.).
        module : (Optional[float] >= 0) : модуль червячной фрезы.

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
        TYPES_OF_MILLING_CUTTER : Типы фрез.
        TYPES_OF_CUTTING_PART : Типы режущей части фрезы.
        TYPES_OF_LARGE_TOOTH : Типы частоты режущей части.
        ACCURACY_CLASS_STANDARDS : Классы точности инструмента.
        DEFAULT_SETTINGS : Настройки по умолчанию.
    """
    CUTTER_NAME: ClassVar[str] = 'Фреза'

    def __init__(self,
                 marking: str,
                 standard: str,
                 dia_mm: float,
                 length_mm: float,
                 mat_of_cutting_part: Union[str, int],

                 main_angle_grad: float,
                 front_angle_grad: float,
                 inclination_of_main_blade_grad: float,

                 tolerance: Union[str, int, float],
                 type_cutter: int,
                 type_of_cutting_part: Union[str, int, float],
                 num_of_cutting_blades: int,
                 radius_of_cutting_vertex: float,
                 large_tooth: float,
                 quantity: int,
                 accuracy_class: Optional[Union[str, int]],
                 number: Optional[str],
                 module: Optional[float],
                 ):
        Tool.__init__(self, self.CUTTER_NAME, marking, standard)
        AxialSizes.__init__(self, dia_mm, length_mm)
        BladeMaterial.__init__(self, mat_of_cutting_part)
        Angles.__init__(self, main_angle_grad, front_angle_grad, inclination_of_main_blade_grad)
        Tolerance.__init__(self, tolerance)
        ITypeCutter.__init__(self, type_cutter)
        ITypeOfCuttingPart.__init__(self, type_of_cutting_part)
        ILargeTooth.__init__(self, large_tooth)
        INumOfBlades.__init__(self, num_of_cutting_blades)
        IRadius.__init__(self, radius_of_cutting_vertex)
        IQuantity.__init__(self, quantity)
        IAccuracyClass.__init__(self, accuracy_class)
        ICutterNumber.__init__(self, number)
        IModule.__init__(self, module)

    @property
    def name(self):
        standard_name = " ".join([self._group, self._marking, self._standard])
        tool_parameters = {"group": self._group, "marking": self._marking, "standard": self._standard,
                           "mat_of_cutting_part": self._mat_of_cutting_part, "tolerance": self.tolerance,
                           "accuracy_class": self._accuracy_class}
        unique_name = get_name(tool_parameters)
        return unique_name if not isinstance(unique_name, type(None)) else standard_name

    def _parameters(self):
        tool_parameters = Tool._parameters(self)
        size_parameters = AxialSizes._parameters(self)
        blade_material_parameters = BladeMaterial._parameters(self)
        angles_parameters = Angles._parameters(self)
        tolerance_parameters = Tolerance._parameters(self)
        itypecutter = ITypeCutter._parameters(self)
        itypeofcuttingpart = ITypeOfCuttingPart._parameters(self)
        ilargetooth = ILargeTooth._parameters(self)
        inumofblades = INumOfBlades._parameters(self)
        iradius = IRadius._parameters(self)
        iquantity = IQuantity._parameters(self)
        inumber = ICutterNumber._parameters(self)
        imodule = IModule._parameters(self)
        return tool_parameters | size_parameters | blade_material_parameters | angles_parameters | \
               tolerance_parameters | itypecutter | itypeofcuttingpart | ilargetooth | inumofblades | iradius | \
               iquantity | inumber | imodule


if __name__ == "__main__":
    cutter = MillingCutter()
    cutter.group = "Фреза"
    # cutter.quantity = -1
    print(cutter.parameters)
    print(cutter.__class__.__name__)
