#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.tool import Tool
from cutting_tools.obj.sizes import AxialSizes
from cutting_tools.obj.blade_material import BladeMaterial
from cutting_tools.obj.angles import Angles
from cutting_tools.obj.checker_in_dict import CheckerInDictionary


class DrillingCutter(Tool, AxialSizes, BladeMaterial, Angles, CheckerInDictionary):
    """ Управляет полями класса "Сверло"

    Parameters:
        num_of_cutting_blades : (int) : количество режущих граней.
        radius_of_cutting_vertex : (float) : радиус режущей вершины.
        quantity : (int) : Количество одновременно работающих инструментов. По умолчанию: None.

    Сostants:
        DEFAULT_SETTINGS : Настройки по умолчанию
    """

    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS_FOR_CUTTING_TOOL['drilling']

    def __init__(self,
                 group: Union[str, int] = "Сверло",
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
                 quantity: int = int(DEFAULT_SETTINGS["quantity"])
                 ):
        Tool.__init__(self, group, marking, standard)
        AxialSizes.__init__(self, dia_mm, length_mm)
        BladeMaterial.__init__(self, mat_of_cutting_part)
        Angles.__init__(self, main_angle_grad, front_angle_grad, inclination_of_main_blade_grad)

        self._num_of_cutting_blades = None
        self._radius_of_cutting_vertex = None
        self._quantity = None

        self.num_of_cutting_blades = num_of_cutting_blades
        self.radius_of_cutting_vertex = radius_of_cutting_vertex
        self.quantity = quantity

    @property
    def num_of_cutting_blades(self):
        return self._num_of_cutting_blades

    @num_of_cutting_blades.setter
    def num_of_cutting_blades(self, any_num):
        if not isinstance(any_num, int) or any_num < 0:
            raise InvalidValue(f'Количество режущих граней должно быть целым положительным числом (передано {any_num})')
        self._num_of_cutting_blades = any_num

    @property
    def radius_of_cutting_vertex(self):
        return self._radius_of_cutting_vertex

    @radius_of_cutting_vertex.setter
    def radius_of_cutting_vertex(self, any_radius):
        if not isinstance(any_radius, (int, float)) or any_radius < 0:
            raise InvalidValue(f'Радиус вершины должен быть положительным числом (передано {any_radius})')
        self._radius_of_cutting_vertex = any_radius

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, any_quantity):
        if not isinstance(any_quantity, int) or any_quantity < 0:
            raise InvalidValue(f'Количество должно быть целым положительным числом (передано {any_quantity})')
        self._quantity = any_quantity

    def _dict_parameters(self):
        tool_parameters = Tool._dict_parameters(self)
        size_parameters = AxialSizes._dict_parameters(self)
        blade_material_parameters = BladeMaterial._dict_parameters(self)
        angles_parameters = Angles._dict_parameters(self)
        parameters = {"num_of_cutting_blades": self._num_of_cutting_blades,
                      "radius_of_cutting_vertex": self._radius_of_cutting_vertex, "quantity": self._quantity}
        return tool_parameters | size_parameters | blade_material_parameters | angles_parameters | parameters


if __name__ == "__main__":
    cutter = DrillingCutter()
    cutter.group = "Сверло"
    # cutter.quantity = -1
    print(cutter.dict_parameters)
