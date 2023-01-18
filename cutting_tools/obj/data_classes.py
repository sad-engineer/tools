#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import Union, Optional, ClassVar

from cutting_tools.obj.constants import INDEXES_OF_MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import INDEXES_HARD_ALLOYS, INDEXES_HIGH_SPEED_STEELS


@dataclass
class AnglesData:
    """ДатаКласс 'Углы режущего инструмента'. Хранит состояние инструмента

    Parameters:
        main_angle_grad : (float) : главный угол инструмента в плане .
        front_angle_grad : (float) : передний угол в плане.
        inclination_of_main_blade : (float) : угол наклона переднего лезвия.
    """
    main_angle_grad: float = 45
    front_angle_grad: float = 45  # gamma передний угол в плане
    inclination_of_main_blade_grad: float = 0  # lambda угол наклона переднего лезвия


@dataclass
class AxialSizesData:
    """ДатаКласс 'Осевые размеры'. Хранит состояние габаритных характеристик осевого предмета

    Parameters:
        dia_mm : (float, optional) : диаметр инструмента.
        length_mm : (float, optional) : длина инструмента.
    """
    dia_mm: float = 50
    length_mm: float = 100


@dataclass
class BladeMaterialData:
    """ДатаКласс 'Материал лезвия'.

    Parameters:
        mat_of_cutting_part : (str) : материал режущей пластины.
        type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Сostants:
        HARD_ALLOYS : перечень доступных твердосплавных материалов
        HIGH_SPEED_STEELS : перечень доступных быстрорежущих материалов
        MATS_OF_CUTTING_PART : перечень доступных материалов режущей части (общий)
    """
    mat_of_cutting_part: Union[str, int] = 'Т15К6'
    HARD_ALLOYS: ClassVar[dict] = INDEXES_HARD_ALLOYS
    HIGH_SPEED_STEELS: ClassVar[dict] = INDEXES_HIGH_SPEED_STEELS
    MATS_OF_CUTTING_PART: ClassVar[dict] = INDEXES_OF_MATERIALS_OF_CUTTING_PART

    @property
    def type_of_mat(self):
        return 1 if self.mat_of_cutting_part in self.HARD_ALLOYS else 0


@dataclass
class PrismaticSizesData:
    """ДатаКласс 'Призматические размеры'. Хранит состояние габаритных характеристик призматического предмета

    Parameters:
        length_mm : (float, optional) : длина инструмента.
        width_mm : (float, optional) : ширина  инструмента.
        height_mm : (float, optional) : высота инструмента.
    """
    length_mm: Optional[float] = 0
    width_mm: Optional[float] = 0
    height_mm: Optional[float] = 0


@dataclass
class ToolData:
    """ДатаКласс 'Инструмент'. Хранит состояние инструмента

    Parameters:
        group : (str) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str) : стандарт инструмента.
    """
    group: str = "Инструмент"
    marking: str = "0000-0000"
    standard: str = "ГОСТ 5555-99"

    @property
    def name(self):
        return " ".join([self.group, self.marking, self.standard])





class MillingCutter(ToolData, AxialSizesData, BladeMaterialData, AnglesData):
    """ Модель данных фрезы

    Parameters:
        type_cutter : (int) : Тип инструмента:
            0-Цилиндрическая,               4-Отрезная и прорезная,         8-Фасонная, с выпуклым профилем,
            1-Торцовая,                     5-Концевая, обработка торца,    9-Фасонная, с вогнутым профилем,
            2-Дисковая, обработка торца,    6-Концевая, обработка паза,     10-Шпоночная
            3-Дисковая, обработка паза,     7-Угловая,
            #TODO: определить типы:--Червячная, Пазовая, Резьбовая
        marking : (str) : обозначение инструмента.
        standard : (str) : стандарт инструмента.
        dia_mm : (float) : диаметр инструмента.
        length_mm : (float) : длина инструмента.
        mat_of_cutting_part : (str) : материал режущей пластины.
        type_of_cutting_part : (str) : тип режущей части.
        main_angle_grad : (float) : главный угол инструмента в плане .
        front_angle_grad : (float) : передний угол в плане.
        inclination_of_main_blade : (float) : угол наклона переднего лезвия.
        radius_of_cutting_vertex : (float) : радиус режущей вершины.
        large_tooth : (int) :  Крупный/мелкий зуб
    """
    # TYPES_OF_MILLING_CUTTER: ClassVar[dict] = TYPES_OF_MILLING_CUTTER

    def __init__(self,
                 type_cutter: int = 1,
                 marking: str = "0000-0001",
                 standard: str = "ГОСТ 0001-22",
                 dia_mm: float = 40,
                 length_mm: float = 50,
                 mat_of_cutting_part: str = "Т15К6",
                 type_of_cutting_part: int = 0,
                 num_of_cutting_blades: int = 1,
                 main_angle: float = 45,
                 front_angle: float = 45,
                 inclination_of_main_blade: float = 0,
                 radius_of_cutting_vertex: float = 0,
                 large_tooth: float = 0,
                 ):
        Tool.__init__(self, "Фреза", marking, standard)
        AxialSizes.__init__(self, dia_mm, length_mm)
        Mat.__init__(self, mat_of_cutting_part)
        Angles.__init__(self, main_angle, front_angle, inclination_of_main_blade)

        self.type_cutter: int = type_cutter
        self.type_of_cutting_part: int = type_of_cutting_part
        self.num_of_cutting_blades: int = num_of_cutting_blades
        self.radius_of_cutting_vertex: float = radius_of_cutting_vertex  # r радиус режущей вершины
        self.large_tooth: float = large_tooth  # Крупный/мелкий зуб









# from dataclasses import dataclass
# from abc import ABC, abstractmethod
# from typing import Union, Optional
# from typing import ClassVar
#
# from cutting_tools.obj.sizes import AxialSizes, PrismaticSizes
# from cutting_tools.obj.tool_controller import Tool
# from cutting_tools.obj.blade_material import BladeMaterial as Mat
# from cutting_tools.obj.angles import CuttingToolAngles as Angles
# from cutting_tools.obj.constants import TYPES_OF_MILLING_CUTTER
#
#
# class MillingCutter(Tool, AxialSizes, Mat, Angles):
#     """ Параметры применяемого режущего инструмента
#
#     Parameters:
#         group : (str, optional) : группа инструмента.
#         marking : (str, optional) : обозначение инструмента.
#         standard : (str, optional) : стандарт инструмента.
#
#         type_cutter : (int) : Тип инструмента:
#             0-Цилиндрическая,               4-Отрезная и прорезная,         8-Фасонная, с выпуклым профилем,
#             1-Торцовая,                     5-Концевая, обработка торца,    9-Фасонная, с вогнутым профилем,
#             2-Дисковая, обработка торца,    6-Концевая, обработка паза,     10-Шпоночная
#             3-Дисковая, обработка паза,     7-Угловая,
#             #TODO: определить типы:--Червячная, Пазовая, Резьбовая
#     -----
#     name : Наименование инструмента.
#
#
#     quantity: int, optional
#         Количество одновременно работающих инструментов. По умолчанию: None.
#     turret: int, optional
#         Наличие револьверной головки: 0-резец в резцедержателе, 1-резец в револьверной головке. По умолчанию: None.
#     load: int, optional
#         Нагрузка на резец: 0-равномерная, 1-неравномерная, 2-неравномерная с большой неравномерностью.
#         По умолчанию: None.
#     deep_or_complex_profile:bool, optional
#         Показатель наличия глубокого или сложного профиля. По умолчанию: None.
#
#     angle_of_inclination: float, optional
#         Угол наклона зубьев протяжки. По умолчанию: None.
#     pitch_of_teeth: float, optional
#         Шаг зубьев протяжки. По умолчанию: None.
#     number_teeth_section:float, optional
#         Число зубьев секции протяжки. По умолчанию: None.
#     difference:float, optional
#         Подача на зуб протяжки (размерный перепад между соседними зубьями). По умолчанию: None.
#     length_of_working_part:float, optional
#         Длина режущей части протяжки. По умолчанию: None.
#     """
#
#     TYPES_OF_MILLING_CUTTER: ClassVar[dict] = TYPES_OF_MILLING_CUTTER
#
#     def __init__(self,
#                  type_cutter: int = 1,
#                  marking: str = "0000-0001",
#                  standard: str = "ГОСТ 0001-22",
#                  dia_mm: float = 40,
#                  length_mm: float = 50,
#                  mat_of_cutting_part: str = "Т15К6",
#                  type_of_cutting_part: int = 0,
#                  num_of_cutting_blades: int = 1,
#                  main_angle: float = 45,
#                  front_angle: float = 45,
#                  inclination_of_main_blade: float = 0,
#                  radius_of_cutting_vertex: float = 0,
#                  large_tooth: float = 0,
#
#                  ):
#         Tool.__init__(self, "Фреза", marking, standard)
#         AxialSizes.__init__(self, dia_mm, length_mm)
#         Mat.__init__(self, mat_of_cutting_part)
#         Angles.__init__(self, main_angle, front_angle, inclination_of_main_blade)
#
#         self.type_cutter: int = type_cutter
#         self.type_of_cutting_part: int = type_of_cutting_part
#         self.num_of_cutting_blades: int = num_of_cutting_blades
#         self.radius_of_cutting_vertex: float = radius_of_cutting_vertex  # r радиус режущей вершины
#         self.large_tooth: float = large_tooth  # Крупный/мелкий зуб






# if __name__ == "__main__":
#     cutter = MillingCutter()
#     # Tool
#     print(cutter.group)
#     print(cutter.marking)
#     print(cutter.standard)
#     print(cutter.name)
#     # AxialSizes
#     print(cutter.dia_mm)
#     print(cutter.length_mm)
#     print(cutter.gabarit_volume)
#     print(cutter.gabarit_str)
#     # Mat
#     print(cutter.mat_of_cutting_part)
#     print(cutter.type_of_mat)
#     # Angles
#     print(cutter.main_angle_grad)
#     print(cutter.front_angle_grad)
#     print(cutter.inclination_of_main_blade_grad)
#     # Self
#     print(cutter.TYPES_OF_MILLING_CUTTER)
#     print(cutter.type_cutter)
#     print(cutter.type_of_cutting_part)
#     print(cutter.num_of_cutting_blades)
#     print(cutter.radius_of_cutting_vertex)
#     print(cutter.large_tooth)



