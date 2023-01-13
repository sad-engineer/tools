#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from abc import ABC, abstractmethod

from cutting_tools.obj.sizes_validator import SizesValidator
from cutting_tools.obj.sizes import AxialSizes, PrismaticSizes
from cutting_tools.obj.standart_tool import StandartTool as Tool
from cutting_tools.obj.blade_material import BladeMaterial as Mat
from cutting_tools.obj.cutting_tool_angles import CuttingToolAngles as Angles


class MillingCutter(Tool, AxialSizes, Mat, Angles):
    def __init__(self,
                 marking: str = "0000-0001",
                 standard: str = "ГОСТ 0001-22",
                 dia_mm: float = 40,
                 length_mm: float = 50,
                 mat_of_cutting_part: str = "Т15К6",
                 main_angle: float = 45,
                 front_angle: float = 45,
                 inclination_of_main_blade: float = 0,
                 ):
        Tool.__init__(self, "Фреза", marking, standard)
        AxialSizes.__init__(self, dia_mm, length_mm)
        Mat.__init__(self, mat_of_cutting_part)
        Angles.__init__(self, main_angle, front_angle, inclination_of_main_blade)

        # self.type_cutter: Optional[int] = None
        # self.num_of_cutting_blades: Optional[float] = None
        #
        # self.type_of_cutting_part: Optional[int] = None
        #
        # self.radius_of_cutting_vertex: Optional[float] = None  # r радиус режущей вершины
        # self.large_tooth: Optional[float] = None  # Крупный/мелкий зуб
        # self.blade_length: Optional[float] = None  # длина лезвия резца



if __name__ == "__main__":
    cutter = MillingCutter()
    # Tool
    print(cutter.group)
    print(cutter.marking)
    print(cutter.standard)
    print(cutter.name)
    # AxialSizes
    print(cutter.dia_mm)
    print(cutter.length_mm)
    print(cutter.gabarit_volume)
    print(cutter.gabarit_str)
    # Mat
    print(cutter.mat_of_cutting_part)
    print(cutter.type_of_mat)
    # Angles
    print(cutter.main_angle_grad)
    print(cutter.front_angle_grad)
    print(cutter.inclination_of_main_blade_grad)


