#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from abc import ABC

from cutting_tools.obj.tool import Tool
from cutting_tools.obj.sizes import AxialSizes
from cutting_tools.obj.blade_material import BladeMaterial
from cutting_tools.obj.angles import Angles
from cutting_tools.obj.data_classes import MillingCutterData
from cutting_tools.obj.abstract_classes import MillingCutterController
from cutting_tools.obj.checker_in_dict import CheckerInDictionary


class MillingCutter(Tool, AxialSizes, BladeMaterial, Angles, MillingCutterData, MillingCutterController,
                    CheckerInDictionary):
    """ Управляет полями класса "MillingCutter"    """
    def update_type_cutter(self, new_type):
        self.type_cutter = self.check_index_in_dict(new_type, self.TYPES_OF_MILLING_CUTTER,
                                                    f"Неверное значение типа фрезы: {new_type}")

    def update_type_of_cutting_part(self, new_type):
        self.type_of_cutting_part = self.check_index_in_dict(new_type, self.TYPES_OF_CUTTING_PART,
                                                             f"Неверное значение типа режущей части фрезы: {new_type}")

    def update_num_of_cutting_blades(self, new_num_of_cutting_blades):
        self.num_of_cutting_blades = self.check_size(new_num_of_cutting_blades)

    def update_radius_of_cutting_vertex(self, new_radius):
        self.radius_of_cutting_vertex = self.check_size(new_radius)

    def update_large_tooth(self, new_large_tooth):
        self.large_tooth = self.check_index_in_dict(new_large_tooth, self.TYPES_OF_LARGE_TOOTH,
                                                    f"Неверное значение частоты зуба фрезы: {new_large_tooth}")

    def __repr__(self):
        return MillingCutterData.__repr__(self)


if __name__ == "__main__":

    cutter = MillingCutter()
    print(dir(cutter))
    print(cutter.__doc__)
    print(cutter.GROUPS_TOOL)
    print(cutter.HARD_ALLOYS)
    print(cutter.HIGH_SPEED_STEELS)
    print(cutter.MATS_OF_CUTTING_PART)
    print(cutter.TYPES_STANDARD)
    print(cutter.TYPES_OF_MILLING_CUTTER)
    print(repr(cutter))

