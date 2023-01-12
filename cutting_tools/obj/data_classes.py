#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional, Union
from dataclasses import dataclass
from typing import ClassVar

from cutting_tools.obj.constants import INDEXES_OF_MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import INDEXES_HARD_ALLOYS, INDEXES_HIGH_SPEED_STEELS
from cutting_tools.obj.sizes import AxialSizes, PrismaticSizes


@dataclass
class Tool:
    """ДатаКласс 'Инструмент'. Хранит состояние инструмента

    Parameters:
        group : (str, optional) : группа инструмента.
        marking : (str, optional) : обозначение инструмента.
        standard : (str, optional) : стандарт инструмента.
    """
    type_of_tool: Optional[str] = "Инструмент"
    marking: Optional[str] = "0000-0000"
    standard: Optional[str] = "ГОСТ 5555-99"

    @property
    def name(self):
        return " ".join([self.type_of_tool, self.marking, self.standard])


@dataclass
class BladeMaterial:
    """ДатаКласс 'Материал лезвия'.
    """
    mat_of_cutting_part: Optional[Union[str, int]] = 'Т15К6'
    HARD_ALLOYS: ClassVar[dict] = INDEXES_HARD_ALLOYS
    HIGH_SPEED_STEELS: ClassVar[dict] = INDEXES_HIGH_SPEED_STEELS
    MATS_OF_CUTTING_PART: ClassVar[dict] = INDEXES_OF_MATERIALS_OF_CUTTING_PART

    def __post_init__(self):
        if not self._is_correct_mat_of_cutting_part:
            self.mat_of_cutting_part = list(self.MATS_OF_CUTTING_PART.keys())[3]

    @property
    def type_of_mat(self):
        return 1 if self.mat_of_cutting_part in self.HARD_ALLOYS else 0

    @property
    def _is_correct_mat_of_cutting_part(self):
        return self.mat_of_cutting_part in self.MATS_OF_CUTTING_PART


@dataclass
class MillingCutter(BladeMaterial, AxialSizes, Tool):
    # def __init__(self, brand: Optional[str] = None):

    pass





if __name__ == "__main__":
    a = Tool()
    print(a)
    print(a.name)
    print(dir(a))

    a = AxialSize()
    a.dia_mm = 50
    a.length_mm = 70
    print(a)
    print(a.volume)
    print(a.gabarit_str)

    a = PrismaticSize()
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

