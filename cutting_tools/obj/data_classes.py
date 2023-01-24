#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import Union, Optional, ClassVar

from cutting_tools.obj.constants import MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import HARD_ALLOYS, HIGH_SPEED_STEELS
from cutting_tools.obj.constants import GROUPS_TOOL, TYPES_STANDARD
from cutting_tools.obj.constants import TYPES_OF_MILLING_CUTTER, TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER, \
    TYPES_OF_LARGE_TOOTH


# @dataclass
# class AnglesData:
#     """ДатаКласс 'Углы режущего инструмента'. Хранит состояние инструмента
#
#     Parameters:
#         main_angle_grad : (float) : главный угол инструмента в плане .
#         front_angle_grad : (float) : передний угол в плане.
#         inclination_of_main_blade : (float) : угол наклона переднего лезвия.
#     """
#     main_angle_grad: float = 45
#     front_angle_grad: float = 45  # gamma передний угол в плане
#     inclination_of_main_blade_grad: float = 0  # lambda угол наклона переднего лезвия


# @dataclass
# class AxialSizesData:
#     """ДатаКласс 'Осевые размеры'. Хранит состояние габаритных характеристик осевого предмета
#
#     Parameters:
#         dia_mm : (float, optional) : диаметр инструмента.
#         length_mm : (float, optional) : длина инструмента.
#     """
#     dia_mm: float = 50
#     length_mm: float = 100
#
#
# @dataclass
# class BladeMaterialData:
#     """ДатаКласс 'Материал лезвия'.
#
#     Parameters:
#         mat_of_cutting_part : (str) : материал режущей пластины.
#         type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.
#
#     Сostants:
#         HARD_ALLOYS : перечень доступных твердосплавных материалов
#         HIGH_SPEED_STEELS : перечень доступных быстрорежущих материалов
#         MATS_OF_CUTTING_PART : перечень доступных материалов режущей части (общий)
#     """
#     mat_of_cutting_part: Union[str, int] = 'Т15К6'
#     MATS_OF_CUTTING_PART: ClassVar[dict] = MATERIALS_OF_CUTTING_PART
#     HARD_ALLOYS: ClassVar[dict] = HARD_ALLOYS
#     HIGH_SPEED_STEELS: ClassVar[dict] = HIGH_SPEED_STEELS
#     @property
#     def type_of_mat(self):
#         return 1 if self.mat_of_cutting_part in self.HARD_ALLOYS else 0
#
#
# @dataclass
# class PrismaticSizesData:
#     """ДатаКласс 'Призматические размеры'. Хранит состояние габаритных характеристик призматического предмета
#
#     Parameters:
#         length_mm : (float, optional) : длина инструмента.
#         width_mm : (float, optional) : ширина  инструмента.
#         height_mm : (float, optional) : высота инструмента.
#     """
#     length_mm: Optional[float] = 0
#     width_mm: Optional[float] = 0
#     height_mm: Optional[float] = 0
#
#
# @dataclass
# class ToolData:
#     """ДатаКласс 'Инструмент'. Хранит состояние инструмента
#
#     Parameters:
#         group : (str) : группа инструмента.
#         marking : (str) : обозначение инструмента.
#         standard : (str) : стандарт инструмента.
#
#     Сostants:
#         GROUPS_TOOL : Словарь наименований группы инструмента
#         TYPES_STANDARD : Типы стандартов инструмента
#     """
#     group: str = "Инструмент"
#     marking: str = "0000-0000"
#     standard: str = "ГОСТ 5555-99"
#
#     GROUPS_TOOL: ClassVar[dict] = GROUPS_TOOL
#     TYPES_STANDARD: ClassVar[dict] = TYPES_STANDARD
#
#     @property
#     def name(self):
#         return " ".join([self.group, self.marking, self.standard])


# @dataclass
# class MillingCutterData(AnglesData, AxialSizesData, BladeMaterialData, ToolData):
@dataclass
class MillingCutterData:
    """ Модель данных фрезы, содержит поля, специфичные для фрезы

     Parameters:
        type_cutter : (int) : Тип инструмента:
            0-Цилиндрическая,               4-Отрезная и прорезная,         8-Фасонная, с выпуклым профилем,
            1-Торцовая,                     5-Концевая, обработка торца,    9-Фасонная, с вогнутым профилем,
            2-Дисковая, обработка торца,    6-Концевая, обработка паза,     10-Шпоночная
            3-Дисковая, обработка паза,     7-Угловая,
            #TODO: определить типы:--Червячная, Пазовая, Резьбовая
        type_of_cutting_part : (int) : тип режущей части.
        num_of_cutting_blades : (int) : количество режущих граней фрезы.
        radius_of_cutting_vertex : (float) : радиус режущей вершины.
        large_tooth : (int) :  Крупный/мелкий зуб
        quantity : (int) : Количество одновременно работающих инструментов. По умолчанию: None.

    Сostants:
        TYPES_OF_MILLING_CUTTER : Типы фрез
        TYPES_OF_CUTTING_PART : Типы режущей части фрезы
    """
    type_cutter: int = 1
    type_of_cutting_part: int = 0
    num_of_cutting_blades: int = 2
    radius_of_cutting_vertex: float = 1  # r радиус режущей вершины
    large_tooth: float = 0  # Крупный/мелкий зуб
    quantity: int = 1

    TYPES_OF_MILLING_CUTTER: ClassVar[dict] = TYPES_OF_MILLING_CUTTER
    TYPES_OF_CUTTING_PART: ClassVar[dict] = TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER
    TYPES_OF_LARGE_TOOTH: ClassVar[dict] = TYPES_OF_LARGE_TOOTH


if __name__ == "__main__":
    cutter = MillingCutterData()
    print(cutter)
