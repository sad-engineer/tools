#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
from typing import Optional
from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL as DEFAULT_SETTINGS
from cutting_tools.find import by_marking_and_stand
from cutting_tools.fun import get_name
from cutting_tools.fun import get_index_type_cutter as index_tc


class CuttingTool:
    """ Параметры применяемого режущего инструмента

    Parameters:
    -----
    kind_of_cut (str, optional) :
        Тип расчета.
        По умолчанию: "milling"
    name : str, optional
        Наименование инструмента
        По умолчанию: None
    standard : str, optional
        Наименование стандарта инструмента.
        По умолчанию: None.
    type_cutter : int, optional
        Тип инструмента:
            Фрезерование:
                0-Цилиндрическая
                1-Торцовая
                2-Дисковая, обработка торца
                3-Дисковая, обработка паза
                4-Отрезная и прорезная
                5-Концевая, обработка торца
                6-Концевая, обработка паза
                7-Угловая
                8-Фасонная, с выпуклым профилем
                9-Фасонная, с вогнутым профилем
                10-Шпоночная
                #TODO: определить типы:--Червячная, Пазовая, Резьбовая
            Протяжки
                0-Круглая
                1-Квадратная
                2-Многогранная
                3-Одношпоночная
                4-Многошпоночная
                5-Шлицевая
                6-Координатная
                7-Прочие
        По умолчанию: None.
    type_of_mat: int, optional
        Тип материала инструмента:
            0-Быстрорез
            1-Твердый сплав
        По умолчанию: None.
    quantity: int, optional
        Количество одновременно работающих инструментов
        По умолчанию: None.
    turret: int, optional
        Наличие револьверной головки: 
            0-резец в резцедержателе,
            1- резец в револьверной головке
        По умолчанию: None.
    load: int, optional
        Нагрузка на резец: 
            0-равномерная, 
            1-неравномерная, 
            2-неравномерная с большой неравномерностью  
        По умолчанию: None.
    deep_or_complex_profile:bool, optional
        Показатель наличия глубокого или сложного профиля
        По умолчанию: None.
        
    angle_of_inclination:float, optional
        Угол наклона зубьев протяжки
        По умолчанию: None.
    pitch_of_teeth:bool, optional
        Шаг зубьев протяжки
        По умолчанию: None.
    number_teeth_section:bool, optional
        Число зубьев секции протяжки 
        По умолчанию: None.
    difference:bool, optional
        Подача на зуб протяжки (размерный перепад между соседними зубьями)
        По умолчанию: None.
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
                 ):
        self.kind_of_cut = kind_of_cut
        self.name = name  # Наименование инструмента
        self.standard = standard  # Стандарт инструмента
        self.type_of_mat = type_of_mat  # mat_R Тип материала инструмента, 0-P6M5, 1-T15K6
        self.mat_of_cutting_part = mat_of_cutting_part  # материал режущей пластины
        self.quantity = quantity  # Количество одновременно работающих инструментов:
        self.turret = turret  # наличие револьверной головки:
        self.load = load  # нагрузка на резец:

        self.deep_or_complex_profile = deep_or_complex_profile  # 0 - нет, 1 - да. Показатель наличия глубокого или сложного профиля

        self.angle_of_inclination = angle_of_inclination
        self.pitch_of_teeth = pitch_of_teeth
        self.number_teeth_section = number_teeth_section
        self.difference = difference

        self.get_default_settings()

    def show(self):
        if self.kind_of_cut == "broaching":
            report = f"""
        ### Параметры применяемого режущего инструмента (протяжки) ###
            Тип инструмента: {self.type_cutter}.
            Угол наклона зубьев протяжки: {self.angle_of_inclination} град.
            Шаг зубьев протяжки: {self.pitch_of_teeth} мм.
            Число зубьев секции протяжки: {self.number_teeth_section} мм.
            Подача на зуб протяжки: {self.difference} мм. """
        else:
            report = f"""
        ### Параметры применяемого режущего инструмента ###"""
            if not isinstance(self.name, type(None)):
                report += f"""
            Обозначение инструмента: {self.name}."""
            if not isinstance(self.type_cutter, type(None)):
                report += f"""
            Тип инструмента: {self.type_cutter}."""
            if not isinstance(self.dia_mm, type(None)):
                report += f"""
            Диаметр инструмента = {self.dia_mm} мм."""
            if not isinstance(self.height_mm, type(None)):
                report += f"""
            Высота инструмента = {self.height_mm} мм."""
            if not isinstance(self.width_mm, type(None)):
                report += f"""
            Ширина инструмента = {self.width_mm} мм."""
            if not isinstance(self.num_of_cutting_blades, type(None)):
                report += f"""
            Количество режущих лезвий инструмента = {self.num_of_cutting_blades} шт."""
            if not isinstance(self.type_of_mat, type(None)):
                report += f"""
            Тип материала инструмента: {self.type_of_mat}."""
            if not isinstance(self.mat_of_cutting_part, type(None)):
                report += f"""
            Материал инструмента: {self.mat_of_cutting_part}."""
            if not isinstance(self.type_of_cutting_part, type(None)):
                report += f"""
            Вид режущей части инструмента: {self.type_of_cutting_part}."""
            # if not isinstance(self.additional_blade, type(None)):
            #     report += f"""
            # Наличие дополнительного лезвия: {self.additional_blade}."""
            # if not isinstance(self.large_tooth, type(None)):
            #     report += f"""
            # Крупный/мелкий зуб: {self.large_tooth}."""
            if not isinstance(self.deep_or_complex_profile, type(None)):
                report += f"""
            Показатель наличия глубокого или сложного профиля: {self.deep_or_complex_profile}."""
            if not isinstance(self.quantity, type(None)):
                report += f"""
            Количество одновременно работающих инструментов: {self.quantity}."""
            if not isinstance(self.turret, type(None)):
                report += f"""
            Инструмент установлен на револьверную головку: {self.turret}."""
            if not isinstance(self.load, type(None)):
                report += f"""
            Нагрузка на инструмент: {self.load}."""
            if not isinstance(self.main_angle_grad, type(None)):
                report += f"""
            Главный угол в плане: {self.main_angle_grad}."""
            if not isinstance(self.front_angle_grad, type(None)):
                report += f"""
            Передний угол в плане: {self.front_angle_grad}."""
            if not isinstance(self.inclination_of_main_blade, type(None)):
                report += f"""
            Угол наклона переднего лезвия: {self.inclination_of_main_blade}."""
            if not isinstance(self.radius_of_cutting_vertex, type(None)):
                report += f"""
            Радиус режущей вершины инструмента: {self.radius_of_cutting_vertex}."""
            if not isinstance(self.blade_length, type(None)):
                report += f"""
            Длина лезвия инструмента: {self.blade_length}. """
        print(report)

    def get_default_settings(self) -> None:
        """ Настраивает атрибуты класса в соответствии с 
        глобальными дефолтными настройками """
        def_sets = DEFAULT_SETTINGS[self.kind_of_cut]
        for setting_name, setting_val in def_sets.items():
            if setting_name == "marking":
                self.get_settings(def_sets["marking"], def_sets["Стандарт"])
            else:
                setattr(self, setting_name, setting_val)

    def get_settings(self, marking, standard, mat_of_cutting_part=None, accuracy=None) -> None:
        """ Задает свойства инструмента по его обозначению (marking) """
        if isinstance(mat_of_cutting_part, type(None)):
            mat_of_cutting_part = self.mat_of_cutting_part
        params = by_marking_and_stand(marking, standard)
        if not isinstance(accuracy, type(None)):
            params["Точность"] = accuracy
        self.name = get_name(params, mat_of_cutting_part)
        self.type_cutter = index_tc(params['type_cutter_']) if not isinstance(params['type_cutter_'],
                                                                              type(None)) else None
        if not isinstance(params['D'], type(None)):
            self.dia_mm = float(params['D'])
        elif not isinstance(params['d_'], type(None)):
            self.dia_mm = float(params['d_'])
        else:
            self.dia_mm = None
        self.height_mm = float(params['H']) if not isinstance(params['H'], type(None)) else None
        self.width_mm = float(params['B']) if not isinstance(params['B'], type(None)) else None
        self.length_mm = float(params['L']) if not isinstance(params['L'], type(None)) else None
        self.num_of_cutting_blades = float(params['z']) if not isinstance(params['z'], type(None)) else None
        self.type_of_cutting_part = int(params['type_of_cutting_part_']) if not isinstance(
            params['type_of_cutting_part_'], type(None)) else None
        self.main_angle_grad = float(params['fi_']) if not isinstance(params['fi_'], type(None)) else None
        self.front_angle_grad = float(params['gamma_']) if not isinstance(params['gamma_'], type(
            None)) else None  # gamma передний угол в плане
        self.inclination_of_main_blade = float(params['lambda_']) if not isinstance(params['lambda_'], type(
            None)) else None  # lambda угол наклона переднего лезвия
        self.radius_of_cutting_vertex = float(params['r_']) if not isinstance(params['r_'], type(
            None)) else None  # r радиус режущей вершины
        # TODO: Организовать выбор из таблицы:
        # self.large_tooth = large_tooth  # Крупный/мелкий зуб
        # self.additional_blade = additional_blade  # наличие дополнительного лезвия
        self.large_tooth = 0
        self.additional_blade = 0
        self.blade_length: Optional[float] = 5  # длина лезвия резца


# mat_of_cutting_part  
#     0 -T5K12V
#     1 -T5K10
#     2 -T14K8
#     3 -T15K6
#     4 -T30K4
#     5 -BK3
#     6 -BK4
#     7 -BK6
#     8 -BK8
#     9 -P18
#     10-P6M5
#     11-9XC
#     12-ХГВ
#     13-У12А
#     Другие мартериалы приписывать к существующим индексам

"""
Список задач в данном модуле программе:
    сделать БД по инструменту
    переменные для БД записывать данными из БД

"""
