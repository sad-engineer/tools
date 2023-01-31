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

from cutting_tools.obj.interfaces import IRadius
from cutting_tools.obj.interfaces import IQuantity
from cutting_tools.obj.interfaces import ITurret
from cutting_tools.obj.interfaces import ILoad
from cutting_tools.obj.interfaces import IComplexProfile


class TurningCutter(Tool, PrismaticSizes, BladeMaterial, Angles, IRadius, IQuantity, ITurret, ILoad, IComplexProfile):
    """ Управляет полями класса "Фреза"

    Parameters:
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
        dict_parameters : (dict) : возвращает словарь параметров и свойств.

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
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS_FOR_CUTTING_TOOL['turning']

    def __init__(self,
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
        Tool.__init__(self, "Резец", marking, standard)
        PrismaticSizes.__init__(self, length_mm, width_mm, height_mm)
        BladeMaterial.__init__(self, mat_of_cutting_part)
        Angles.__init__(self, main_angle_grad, front_angle_grad, inclination_of_main_blade_grad)
        IRadius.__init__(self, radius_of_cutting_vertex)
        IQuantity.__init__(self, quantity)
        ITurret.__init__(self, turret)
        ILoad.__init__(self, load)
        IComplexProfile.__init__(self, is_complex_profile)

    def _dict_parameters(self):
        tool = Tool._dict_parameters(self)
        size = PrismaticSizes._dict_parameters(self)
        blade_material = BladeMaterial._dict_parameters(self)
        angles = Angles._dict_parameters(self)
        iradius = IRadius._dict_parameters(self)
        iquantity = IQuantity._dict_parameters(self)
        iturret = ITurret._dict_parameters(self)
        iload = ILoad._dict_parameters(self)
        icomplexprofile = IComplexProfile._dict_parameters(self)
        return tool | size | blade_material | angles | iradius | iquantity | iturret | iload | icomplexprofile


if __name__ == "__main__":
    cutter = TurningCutter()
    cutter.group = "Резец"
    # cutter.quantity = -1
    print(cutter.dict_parameters)
