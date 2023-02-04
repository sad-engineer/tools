#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from cutting_tools.obj.tool import Tool
from cutting_tools.obj.sizes import PrismaticSizes
from cutting_tools.obj.blade_material import BladeMaterial
from cutting_tools.obj.angles import Angles

from cutting_tools.obj.interfaces import IRadius
from cutting_tools.obj.interfaces import IQuantity
from cutting_tools.obj.interfaces import ITurret
from cutting_tools.obj.interfaces import ILoad
from cutting_tools.obj.interfaces import IComplexProfile


class TurningCutter(Tool, PrismaticSizes, BladeMaterial, Angles, IRadius, IQuantity, ITurret, ILoad, IComplexProfile):
    """ Управляет полями класса "Фреза"

    parameters:
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        length_mm : (float >= 0) : длина инструмента.
        width_mm : (float >= 0) : ширина инструмента.
        height_mm : (float >= 0) : высота инструмента.
        mat_of_cutting_part : (str, int is MATERIALS_OF_CUTTING_PART) : материал режущей пластины.
        main_angle_grad : (float >= 0) : главный угол в плане.
        front_angle_grad  : (float >= 0) : передний угол.
        inclination_of_main_blade_grad  : (float >= 0) : наклон передней грани
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.
        quantity : (int >= 0) : количество одновременно работающих инструментов.
        turret : (int, str in TYPES_OF_TOOL_HOLDER) :  Наличие револьверной головки.
        load : (int, str in TYPES_OF_TOOL_HOLDER) : Нагрузка на резец.
        is_complex_profile : (Optional[bool]) : Показатель наличия глубокого или сложного профиля. По умолчанию: None.

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
        TYPES_OF_TOOL_HOLDER : Типы установки резца.
        TYPES_OF_LOADS : Типы нагрузок на резец.
        DEFAULT_SETTINGS : Настройки по умолчанию
    """
    CUTTER_NAME: ClassVar[str] = 'Резец'

    def __init__(self,
                 marking: str,
                 standard: str,
                 length_mm: float,
                 width_mm: float,
                 height_mm: float,
                 mat_of_cutting_part: Union[str, int],
                 main_angle_grad: float,
                 front_angle_grad: float,
                 inclination_of_main_blade_grad: float,
                 radius_of_cutting_vertex: float,
                 quantity: int,
                 turret: Union[str, int],
                 load: Union[str, int],
                 is_complex_profile: bool,
                 ):
        Tool.__init__(self, self.CUTTER_NAME, marking, standard)
        PrismaticSizes.__init__(self, length_mm, width_mm, height_mm)
        BladeMaterial.__init__(self, mat_of_cutting_part)
        Angles.__init__(self, main_angle_grad, front_angle_grad, inclination_of_main_blade_grad)
        IRadius.__init__(self, radius_of_cutting_vertex)
        IQuantity.__init__(self, quantity)
        ITurret.__init__(self, turret)
        ILoad.__init__(self, load)
        IComplexProfile.__init__(self, is_complex_profile)

    def _parameters(self):
        tool = Tool._parameters(self)
        size = PrismaticSizes._parameters(self)
        blade_material = BladeMaterial._parameters(self)
        angles = Angles._parameters(self)
        iradius = IRadius._parameters(self)
        iquantity = IQuantity._parameters(self)
        iturret = ITurret._parameters(self)
        iload = ILoad._parameters(self)
        icomplexprofile = IComplexProfile._parameters(self)
        return tool | size | blade_material | angles | iradius | iquantity | iturret | iload | icomplexprofile


if __name__ == "__main__":
    cutter = TurningCutter()
    cutter.group = "Резец"
    # cutter.quantity = -1
    print(cutter.parameters)
