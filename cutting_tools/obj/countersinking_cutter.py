#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.drilling_cutter import DrillingCutter


class CountersinkingCutter(DrillingCutter):
    """ Управляет полями класса "Зенкер"

    Parameters:
        num_of_cutting_blades : (int) : количество режущих граней.
        radius_of_cutting_vertex : (float) : радиус режущей вершины.
        quantity : (int) : Количество одновременно работающих инструментов. По умолчанию: None.

    Сostants:
        DEFAULT_SETTINGS : Настройки по умолчанию
    """
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["countersinking"]

    def __init__(self,
                 group: Union[str, int] = "Зенкер",
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
                 quantity: int = int(DEFAULT_SETTINGS["quantity"])
                 ):
        DrillingCutter.__init__(self, group, marking, standard, dia_mm, length_mm, mat_of_cutting_part, main_angle_grad,
                                front_angle_grad, inclination_of_main_blade_grad, num_of_cutting_blades,
                                radius_of_cutting_vertex, quantity)


if __name__ == "__main__":
    cutter = CountersinkingCutter()
    cutter.group = "Зенкер"
    # cutter.quantity = -1
    print(cutter.dict_parameters)
