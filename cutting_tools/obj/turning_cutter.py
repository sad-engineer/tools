#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.tool import Tool
from cutting_tools.obj.sizes import PrismaticSizes
from cutting_tools.obj.blade_material import BladeMaterial
from cutting_tools.obj.angles import Angles
from cutting_tools.obj.checker_in_dict import CheckerInDictionary
from cutting_tools.obj.abstract_classes import Dictionarer


class TurningCutter(Tool, PrismaticSizes, BladeMaterial, Angles, CheckerInDictionary, Dictionarer):
    """ Управляет полями класса "Фреза"

    Parameters:
        radius_of_cutting_vertex : (float) : радиус режущей вершины.
        quantity : (int) : Количество одновременно работающих инструментов. По умолчанию: None.
        turret : (int, str) :  Наличие револьверной головки: 0-резец в резцедержателе, 1-резец в револьверной головке.
        load : (int, str) : Нагрузка на резец: 0-равномерная, 1-неравномерная, 2-неравномерная с большой неравномерностью.
        is_complex_profile : (bool) : Показатель наличия глубокого или сложного профиля. По умолчанию: None.

    Сostants:
        DEFAULT_SETTINGS : Настройки по умолчанию
    """
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS_FOR_CUTTING_TOOL['turning']
    TYPES_OF_TOOL_HOLDER: ClassVar[dict] = {"В резцедержателе": 0, "В револьверной головке": 1}
    TYPES_OF_LOADS: ClassVar[dict] = {"Равномерная": 0, "Неравномерная": 1,
                                      "Неравномерная с большой неравномерностью": 2}

    def __init__(self,
                 group: Union[str, int] = "Резец",
                 marking: str = str(DEFAULT_SETTINGS["marking"]),
                 standard: str = str(DEFAULT_SETTINGS["Стандарт"]),
                 length_mm: float = 100,
                 width_mm: float = 25,
                 height_mm: float = 25,
                 mat_of_cutting_part: Union[str, int] = str(DEFAULT_SETTINGS["mat_of_cutting_part"]),
                 main_angle_grad: float = 90,
                 front_angle_grad: float = 0,
                 inclination_of_main_blade_grad: float = 0,
                 radius_of_cutting_vertex: float = 1,
                 quantity: int = int(DEFAULT_SETTINGS["quantity"]),
                 turret: Union[str, int] = 0,
                 load: Union[str, int] = 0,
                 is_complex_profile: bool = False,
                 ):
        Tool.__init__(self, group, marking, standard)
        PrismaticSizes.__init__(self, length_mm, width_mm, height_mm)
        BladeMaterial.__init__(self, mat_of_cutting_part)
        Angles.__init__(self, main_angle_grad, front_angle_grad, inclination_of_main_blade_grad)

        self._radius_of_cutting_vertex = None
        self._quantity = None
        self._turret = None
        self._load = None
        self._is_complex_profile = None

        self.radius_of_cutting_vertex = radius_of_cutting_vertex
        self.quantity = quantity
        self.turret = turret
        self.load = load
        self.is_complex_profile = is_complex_profile

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

    @property
    def turret(self):
        return self._turret

    @turret.setter
    def turret(self, any_type):
        err_message = f'Неверное значение типа резцедержателя. Должно быть из: {self.TYPES_OF_TOOL_HOLDER}.\n ' \
                      f'Передано {any_type}.'
        any_type = self._check_in_dict(any_type, self.TYPES_OF_TOOL_HOLDER, err_message)
        self._turret = any_type if isinstance(any_type, (int, float)) else \
            self.TYPES_OF_TOOL_HOLDER[any_type]

    @property
    def load(self):
        return self._load

    @load.setter
    def load(self, any_type):
        err_message = f'Неверное значение типа нагрузки на резец. Должно быть из: {self.TYPES_OF_LOADS}.\n ' \
                      f'Передано {any_type}.'
        any_type = self._check_in_dict(any_type, self.TYPES_OF_LOADS, err_message)
        self._load = any_type if isinstance(any_type, (int, float)) else \
            self.TYPES_OF_LOADS[any_type]

    @property
    def is_complex_profile(self):
        return self._is_complex_profile

    @is_complex_profile.setter
    def is_complex_profile(self, any_value):
        if not isinstance(any_value, bool):
            raise InvalidValue('Передайте "True" если резец имеет глубокий и сложный профиль')
        self._is_complex_profile = any_value

    def _dict_parameters(self):
        tool_parameters = Tool._dict_parameters(self)
        size_parameters = PrismaticSizes._dict_parameters(self)
        blade_material_parameters = BladeMaterial._dict_parameters(self)
        angles_parameters = Angles._dict_parameters(self)
        parameters = {"radius_of_cutting_vertex": self._radius_of_cutting_vertex, "quantity": self._quantity,
                      "turret": self._turret, "load": self._load, "is_complex_profile": self._is_complex_profile}
        return tool_parameters | size_parameters | blade_material_parameters | angles_parameters | parameters


if __name__ == "__main__":
    cutter = TurningCutter()
    cutter.group = "Резец"
    # cutter.quantity = -1
    print(cutter.dict_parameters)
