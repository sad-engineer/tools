#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional, Union
from dataclasses import dataclass
from typing import ClassVar

from cutting_tools.obj.sizes import AxialSizes, PrismaticSizes
from cutting_tools.obj.standart_tool import StandartTool as Tool
from cutting_tools.obj.blade_material import BladeMaterial as Mat



@dataclass
class MillingCutter(Mat, AxialSizes, Tool):
    # def __init__(self, brand: Optional[str] = None):

    pass





if __name__ == "__main__":
    a = Tool()
    print(a)
    print(a.name)
    print(dir(a))

    a = AxialSizes()
    a.dia_mm = 50
    a.length_mm = 70
    print(a)
    print(a.volume)
    print(a.gabarit_str)

    a = PrismaticSizes()
    a.length_mm = 10
    a.width_mm = 20
    a.height_mm = 30
    print(a)
    print(a.volume)
    print(a.gabarit_str)

    a = BladeMaterial("Р18")
    print(a)
    print(a.HARD_ALLOYS)
    print(a.MATS_OF_CUTTING_PART)
    print(a.type_of_mat)

    a = MillingCutter('Фреза', '1111-2222', 'ГОСТ 6666-77', 25, 35, 'Р6М5')
    print(a)
    print(a.volume)
    print(a.gabarit_str)
    print(a.name)
    print(a.HARD_ALLOYS)
    print(a.MATS_OF_CUTTING_PART)
    print(a.type_of_mat)

