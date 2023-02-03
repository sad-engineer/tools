#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.drilling_cutter import DrillingCutter


class CountersinkingCutter(DrillingCutter):
    CUTTER_NAME: ClassVar[str] = 'Зенкер'
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS_FOR_CUTTING_TOOL[CUTTER_NAME]

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
        self.__doc__ = DrillingCutter.__doc__.replace("Сверло", "Зенкер")
        self.group = "Зенкер"


if __name__ == "__main__":
    cutter = CountersinkingCutter()
    print(cutter.parameters)
    cutter.standard = 'ГОСТ 12489-71'
    print(cutter.parameters)
