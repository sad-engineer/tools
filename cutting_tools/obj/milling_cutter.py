#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from cutting_tools.obj.constants import TYPES_OF_MILLING_CUTTER
from cutting_tools.obj.constants import TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER
from cutting_tools.obj.constants import TYPES_OF_LARGE_TOOTH
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.tool import Tool
from cutting_tools.obj.sizes import AxialSizes
from cutting_tools.obj.blade_material import BladeMaterial
from cutting_tools.obj.angles import Angles
from cutting_tools.obj.checker_in_dict import CheckerInDictionary


class MillingCutter(Tool, AxialSizes, BladeMaterial, Angles, CheckerInDictionary):
    """ Управляет полями класса "MillingCutter"

    Parameters:
        type_cutter : (int) : Тип инструмента:
            0-Цилиндрическая,               4-Отрезная и прорезная,         8-Фасонная, с выпуклым профилем,
            1-Торцовая,                     5-Концевая, обработка торца,    9-Фасонная, с вогнутым профилем,
            2-Дисковая, обработка торца,    6-Концевая, обработка паза,     10-Шпоночная
            3-Дисковая, обработка паза,     7-Угловая,
            #TODO: определить типы:--Червячная, Пазовая, Резьбовая
        type_of_cutting_part : (int) : тип режущей части.
        num_of_cutting_blades : (int) : количество режущих граней фрезы.
        radius_of_cutting_vertex : (float) : радиус режущей вершины.
        large_tooth : (int) :  Крупный/мелкий зуб
        quantity : (int) : Количество одновременно работающих инструментов. По умолчанию: None.

    Сostants:
        TYPES_OF_MILLING_CUTTER : Типы фрез
        TYPES_OF_CUTTING_PART : Типы режущей части фрезы
    """

    TYPES_OF_MILLING_CUTTER: ClassVar[dict] = TYPES_OF_MILLING_CUTTER
    TYPES_OF_CUTTING_PART: ClassVar[dict] = TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER
    TYPES_OF_LARGE_TOOTH: ClassVar[dict] = TYPES_OF_LARGE_TOOTH

    def __init__(self, group: Union[str, int] = "Инструмент", marking: str = "0000-0000",
                 standard: str = "ГОСТ 5555-99", dia_mm: float = 50, length_mm: float = 100,
                 mat_of_cutting_part: Union[str, int] = 'Т15К6', main_angle_grad: float = 45,
                 front_angle_grad: float = 45, inclination_of_main_blade_grad: float = 0,

                 type_cutter: int = 1, type_of_cutting_part: int = 0, num_of_cutting_blades: int = 2,
                 radius_of_cutting_vertex: float = 1, large_tooth: float = 0, quantity: int = 1
                 ):
        Tool.__init__(self, group, marking, standard)
        AxialSizes.__init__(self, dia_mm, length_mm)
        BladeMaterial.__init__(self, mat_of_cutting_part)
        Angles.__init__(self, main_angle_grad, front_angle_grad, inclination_of_main_blade_grad)

        self._type_cutter = None
        self._type_of_cutting_part = None
        self._num_of_cutting_blades = None
        self._radius_of_cutting_vertex = None
        self._large_tooth = None
        self._quantity = None

        self.type_cutter = type_cutter
        self.type_of_cutting_part = type_of_cutting_part
        self.num_of_cutting_blades = num_of_cutting_blades
        self.radius_of_cutting_vertex = radius_of_cutting_vertex
        self.large_tooth = large_tooth
        self.quantity = quantity

    @property
    def type_cutter(self):
        return self._type_cutter

    @type_cutter.setter
    def type_cutter(self, any_type):
        err_message = f'Неверное значение типа фрезы.' \
                      f' Значение должно быть из {self.TYPES_OF_MILLING_CUTTER}.\n Передано {any_type}.'
        any_type = self._check_in_dict(any_type, self.TYPES_OF_MILLING_CUTTER, err_message)
        self._type_cutter = any_type if isinstance(any_type, (int, float)) else self.TYPES_OF_MILLING_CUTTER[any_type]

    @property
    def type_of_cutting_part(self):
        return self._type_of_cutting_part

    @type_of_cutting_part.setter
    def type_of_cutting_part(self, any_type):
        err_message = f'Неверное значение типа режущей части фрезы. ' \
                      f'Значение должно быть из {self.TYPES_OF_CUTTING_PART}.\n Передано {any_type}.'
        any_type = self._check_in_dict(any_type, self.TYPES_OF_CUTTING_PART, err_message)
        self._type_of_cutting_part = any_type if isinstance(any_type, (int, float)) else \
            self.TYPES_OF_CUTTING_PART[any_type]

    @property
    def num_of_cutting_blades(self):
        return self._num_of_cutting_blades

    @num_of_cutting_blades.setter
    def num_of_cutting_blades(self, any_num):
        if not isinstance(any_num, int) or any_num < 0:
            raise InvalidValue(f'Количество режущих граней должно быть целым положительным числом. (передано {any_num})')
        self._num_of_cutting_blades = any_num

    @property
    def radius_of_cutting_vertex(self):
        return self._radius_of_cutting_vertex

    @radius_of_cutting_vertex.setter
    def radius_of_cutting_vertex(self, any_radius):
        if not isinstance(any_radius, (int, float)) or any_radius < 0:
            raise InvalidValue(f'Радиус вершины должен быть положительным числом. (передано {any_radius})')
        self._radius_of_cutting_vertex = any_radius

    @property
    def large_tooth(self):
        return self._large_tooth

    @large_tooth.setter
    def large_tooth(self, any_large_tooth):
        err_message = f'Неверное значение типа режущей части фрезы. ' \
                      f'Значение должно быть из {self.TYPES_OF_LARGE_TOOTH}.\n Передано {any_large_tooth}.'
        any_type = self._check_in_dict(any_large_tooth, self.TYPES_OF_LARGE_TOOTH, err_message)
        self._large_tooth = any_type if isinstance(any_type, (int, float)) else self.TYPES_OF_LARGE_TOOTH[any_type]

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, any_quantity):
        if not isinstance(any_quantity, int) or any_quantity < 0:
            raise InvalidValue(f'Количество должно быть целым положительным числом. (передано {any_quantity})')
        self._quantity = any_quantity


if __name__ == "__main__":

    cutter = MillingCutter()
    # print(dir(cutter))
    # print(cutter.__doc__)
    # print(cutter.GROUPS_TOOL)
    # print(cutter.HARD_ALLOYS)
    # print(cutter.HIGH_SPEED_STEELS)
    # print(cutter.MATS_OF_CUTTING_PART)
    # print(cutter.TYPES_STANDARD)
    # print(cutter.TYPES_OF_MILLING_CUTTER)

    cutter.group = "Резец"
    cutter.quantity = -1
    print(cutter.quantity)
