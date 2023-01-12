#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional, Union
from dataclasses import dataclass, field
from typing import Dict
from typing import ClassVar

from cutting_tools.obj.constants import INDEXES_OF_MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import INDEXES_HARD_ALLOYS, INDEXES_HIGH_SPEED_STEELS

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
class AxialSize:
    """ДатаКласс 'Осевые размеры'. Хранит состояние габаритных характеристик осевого предмета

    Parameters:
        dia_mm : (float, optional) : диаметр инструмента.
        length_mm : (float, optional) : длина инструмента.
    """
    dia_mm: Optional[float] = None
    length_mm: Optional[float] = None

    @property
    def volume(self):
        return self.dia_mm ** 2 * self.length_mm

    @property
    def gabarit_str(self):
        return f"DxL: ø{self.dia_mm}x{self.length_mm} мм"




@dataclass
class PrismaticSize:
    """ДатаКласс 'Призматические размеры'. Хранит состояние габаритных характеристик призматического предмета

    Parameters:
        length_mm : (float, optional) : длина инструмента.
        width_mm : (float, optional) : ширина  инструмента.
        height_mm : (float, optional) : высота инструмента.
    """
    length_mm: Optional[float] = None
    width_mm: Optional[float] = None
    height_mm: Optional[float] = None

    @property
    def volume(self):
        return self.height_mm * self.width_mm * self.length_mm

    @property
    def gabarit_str(self):
        return f"LxBxH: ø{self.length_mm}x{self.width_mm}x{self.height_mm} мм"


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
class MillingCutter(BladeMaterial, AxialSize, Tool):
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

