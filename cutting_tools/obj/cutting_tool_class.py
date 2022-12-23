#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
from typing import Optional
from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL as DEFAULT_SETTINGS
from cutting_tools.find import by_marking_and_stand
from cutting_tools.fun import get_name
from cutting_tools.fun import get_index_type_cutter as index_tc
from cutting_tools.fun import get_float_value, get_int_value, get_diameter
from cutting_tools.fun import show_cutting_tool


class CuttingTool:
    """ Параметры применяемого режущего инструмента

    Parameters:
    -----
    kind_of_cut: str, optional
        Тип расчета. По умолчанию: "milling"
    name : str, optional
        Наименование инструмента. По умолчанию: None
    standard : str, optional
        Наименование стандарта инструмента. По умолчанию: None.
    type_cutter : int, optional
        Тип инструмента:
            Фрезерование:
                0-Цилиндрическая,               4-Отрезная и прорезная,         8-Фасонная, с выпуклым профилем,
                1-Торцовая,                     5-Концевая, обработка торца,    9-Фасонная, с вогнутым профилем,
                2-Дисковая, обработка торца,    6-Концевая, обработка паза,     10-Шпоночная
                3-Дисковая, обработка паза,     7-Угловая,
                #TODO: определить типы:--Червячная, Пазовая, Резьбовая
            Протяжки
                0-Круглая       3-Одношпоночная     6-Координатная
                1-Квадратная    4-Многошпоночная    7-Прочие
                2-Многогранная  5-Шлицевая
        По умолчанию: None.
    type_of_mat: int, optional
        Тип материала инструмента: 0-быстрорез; 1-твердый сплав. По умолчанию: None.
    quantity: int, optional
        Количество одновременно работающих инструментов. По умолчанию: None.
    turret: int, optional
        Наличие револьверной головки: 0-резец в резцедержателе, 1-резец в револьверной головке. По умолчанию: None.
    load: int, optional
        Нагрузка на резец: 0-равномерная, 1-неравномерная, 2-неравномерная с большой неравномерностью.
        По умолчанию: None.
    deep_or_complex_profile:bool, optional
        Показатель наличия глубокого или сложного профиля. По умолчанию: None.
        
    angle_of_inclination: float, optional
        Угол наклона зубьев протяжки. По умолчанию: None.
    pitch_of_teeth: float, optional
        Шаг зубьев протяжки. По умолчанию: None.
    number_teeth_section:float, optional
        Число зубьев секции протяжки. По умолчанию: None.
    difference:float, optional
        Подача на зуб протяжки (размерный перепад между соседними зубьями). По умолчанию: None.
    length_of_working_part:float, optional
        Длина режущей части протяжки. По умолчанию: None.
    """
    def __init__(self,
                 kind_of_cut: str = 'milling',
                 name: Optional[str] = None,
                 standard: Optional[str] = None,
                 type_of_mat: Optional[int] = None,
                 mat_of_cutting_part: Optional[int] = None,
                 quantity: Optional[int] = None,
                 turret: Optional[int] = None,
                 load: Optional[int] = None,
                 deep_or_complex_profile: Optional[bool] = False,

                 angle_of_inclination: Optional[float] = None,
                 pitch_of_teeth: Optional[float] = None,
                 number_teeth_section: Optional[float] = None,
                 difference: Optional[float] = None,
                 length_of_working_part: Optional[float] = None,
                 ):
        self.kind_of_cut = kind_of_cut
        self.name = name                                        # Наименование инструмента
        self.standard = standard                                # Стандарт инструмента
        self.type_of_mat = type_of_mat                          # mat_R Тип материала инструмента, 0-P6M5, 1-T15K6
        self.mat_of_cutting_part = mat_of_cutting_part          # материал режущей пластины
        self.quantity = quantity                                # Количество одновременно работающих инструментов:
        self.turret = turret                                    # наличие револьверной головки:
        self.load = load                                        # нагрузка на резец:
        self.deep_or_complex_profile = deep_or_complex_profile  # Показатель наличия глубокого или сложного профиля

        self.type_cutter: Optional[int] = None
        self.dia_mm: Optional[float] = None
        self.height_mm: Optional[float] = None
        self.width_mm: Optional[float] = None
        self.length_mm: Optional[float] = None
        self.num_of_cutting_blades: Optional[float] = None
        self.type_of_cutting_part: Optional[int] = None
        self.main_angle_grad: Optional[float] = None
        self.front_angle_grad: Optional[float] = None  # gamma передний угол в плане
        self.inclination_of_main_blade: Optional[float] = None  # lambda угол наклона переднего лезвия
        self.radius_of_cutting_vertex: Optional[float] = None  # r радиус режущей вершины
        self.large_tooth: Optional[float] = None  # Крупный/мелкий зуб
        self.additional_blade: Optional[float] = None  # наличие дополнительного лезвия
        self.blade_length: Optional[float] = None  # длина лезвия резца

        self.angle_of_inclination = angle_of_inclination
        self.pitch_of_teeth = pitch_of_teeth
        self.number_teeth_section = number_teeth_section
        self.difference = difference
        self.length_of_working_part = length_of_working_part

        self.get_default_settings()

    def get_default_settings(self) -> None:
        """ Настраивает атрибуты класса в соответствии с глобальными дефолтными настройками """
        def_sets = DEFAULT_SETTINGS[self.kind_of_cut]
        for setting_name, setting_val in def_sets.items():
            if setting_name != "marking":
                setattr(self, setting_name, setting_val)
        if "marking" in def_sets:
            self.get_settings(def_sets["marking"], def_sets["Стандарт"])

    def get_settings(self, marking, standard, mat_of_cutting_part=None, accuracy=None) -> None:
        """ Задает свойства инструмента по его обозначению (marking) """
        if isinstance(mat_of_cutting_part, type(None)):
            mat_of_cutting_part = self.mat_of_cutting_part
        params = by_marking_and_stand(marking, standard)
        if not isinstance(accuracy, type(None)):
            params["Точность"] = accuracy
        self.name = get_name(params, mat_of_cutting_part)
        self.type_cutter = index_tc(params['type_cutter_']) if not isinstance(
            params['type_cutter_'], type(None)) else None
        self.dia_mm = get_diameter(params)
        self.height_mm = get_float_value(params['H'])
        self.width_mm = get_float_value(params['B'])
        self.length_mm = get_float_value(params['L'])
        self.num_of_cutting_blades = get_int_value(params['z'])
        self.type_of_cutting_part = get_int_value(params['type_of_cutting_part_'])
        self.main_angle_grad = get_float_value(params['fi_'])
        self.front_angle_grad = get_float_value(params['gamma_'])               # gamma передний угол в плане
        self.inclination_of_main_blade = get_float_value(params['lambda_'])     # lambda угол наклона переднего лезвия
        self.radius_of_cutting_vertex = get_float_value(params['r_'])           # r радиус режущей вершины
        # TODO: Организовать выбор из таблицы:
        # self.large_tooth = large_tooth  # Крупный/мелкий зуб
        # self.additional_blade = additional_blade  # наличие дополнительного лезвия
        self.large_tooth = 0
        self.additional_blade = 0
        self.blade_length: Optional[float] = 5  # длина лезвия резца

    def show(self):
        show_cutting_tool(self)

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        """ Создает словарь всех параметров класса 'Режущий инструмент'."""
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        """ Загружает все параметры класса из словаря"""
        for key, val in state.items():
            setattr(self, key, val)
