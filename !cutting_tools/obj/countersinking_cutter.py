#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from cutting_tools.obj.drilling_cutter import DrillingCutter


class CountersinkingCutter(DrillingCutter):
    CUTTER_NAME: ClassVar[str] = 'Зенкер'

    def __init__(self,
                 marking: str,
                 standard: str,
                 dia_mm: float,
                 length_mm: float,
                 mat_of_cutting_part: Union[str, int],
                 main_angle_grad: float,
                 front_angle_grad: float,
                 inclination_of_main_blade_grad: float,
                 num_of_cutting_blades: int,
                 radius_of_cutting_vertex: float,
                 quantity: int,
                 tolerance: Union[str, int, float],
                 ):

        DrillingCutter.__init__(self, marking, standard, dia_mm, length_mm, mat_of_cutting_part, main_angle_grad,
                                front_angle_grad, inclination_of_main_blade_grad, num_of_cutting_blades,
                                radius_of_cutting_vertex, quantity, tolerance)
        self.__doc__ = DrillingCutter.__doc__.replace("Сверло", "Зенкер")
        self.group = "Зенкер"
