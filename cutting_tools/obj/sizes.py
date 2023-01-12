#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional
from dataclasses import dataclass
from cutting_tools.obj.sizes_validator import SizesValidator


@dataclass
class AxialSizes(SizesValidator):
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
        return f"øDxL: ø{self.dia_mm}x{self.length_mm} мм"

    def update_dia(self, new_dia_mm: float):
        self.dia_mm = self.check_size(new_dia_mm)

    def update_length(self, new_length_mm: float):
        self.length_mm = self.check_size(new_length_mm)


@dataclass
class PrismaticSizes(SizesValidator):
    """ДатаКласс 'Призматические размеры'. Хранит состояние габаритных характеристик призматического предмета

    Parameters:
        length_mm : (float, optional) : длина инструмента.
        width_mm : (float, optional) : ширина  инструмента.
        height_mm : (float, optional) : высота инструмента.
    """
    length_mm: Optional[float] = 0
    width_mm: Optional[float] = 0
    height_mm: Optional[float] = 0

    @property
    def volume(self):
        return self.height_mm * self.width_mm * self.length_mm

    @property
    def gabarit_str(self):
        return f"LxBxH: ø{self.length_mm}x{self.width_mm}x{self.height_mm} мм"

    def update_length(self, new_length_mm: float):
        self.length_mm = self.check_size(new_length_mm)

    def update_width(self, new_width_mm: float):
        self.width_mm = self.check_size(new_width_mm)

    def update_height(self, new_height_mm: float):
        self.height_mm = self.check_size(new_height_mm)
#
#
# if __name__ == "__main__":
#     a = AxialSizes()
#     a.update_dia(50)
#     a.update_length(70)
#     print(a)
#     print(a.volume)
#     print(a.gabarit_str)
#
#     a = PrismaticSizes()
#     a.update_length(10)
#     a.update_width(20)
#     a.update_height(30)
#     print(a)
#     print(a.volume)
#     print(a.gabarit_str)
#     print(a._is_correct_size(50))
#     print(dir(a))
#
#     a = PrismaticSizes(20, "", 53)
#     print(a)
