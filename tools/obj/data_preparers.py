#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import ClassVar, Optional
from tools.obj.constants import DEFAULT_SETTINGS_FOR_TOOL


def select_data_for_milling(raw_data: dict, default_settings: dict) -> dict:
    param = dict()
    # param["group"] = raw_data.get('Тип_инструмента')
    param["marking"] = raw_data.get('Обозначение')
    param["standard"] = raw_data.get('Стандарт')
    param["mat_of_cutting_part"] = default_settings["mat_of_cutting_part"]
    param["dia_mm"] = float(raw_data.get('D', 25))
    param["length_mm"] = float(raw_data.get('L', 25))
    param["main_angle_grad"] = float(raw_data.get('fi_', 45))
    param["front_angle_grad"] = float(raw_data.get('gamma_', 0))
    param["inclination_of_main_blade_grad"] = float(raw_data.get('lambda_', 0))
    param["tolerance"] = default_settings["tolerance"]

    # TODO: Переделать выбор типа фрезы для вариантов 'Торцовая, Цилиндрическая', 
    #  'Концевая (для T-образных пазов)', 'Концевая (для обработки Т-образного паза)'
    param["type_cutter"] = raw_data.get('type_cutter_')

    param["type_of_cutting_part"] = int(raw_data.get('type_of_cutting_part_', 1))
    param["num_of_cutting_blades"] = int(raw_data.get('z', 2))
    param["radius_of_cutting_vertex"] = float(raw_data.get('r_', 1.0))
    param["large_tooth"] = raw_data.get('large_tooth', 0)
    param["quantity"] = int(default_settings["quantity"])
    param["accuracy_class"] = None
    param["number"] = None
    param["module"] = None
    return param


def select_data_for_drilling(raw_data: dict, default_settings: dict) -> dict:
    """ Из словаря данных, полученных из БД (сырых), выбирает данные для класса 'Сверло'. """
    param = dict()
    # param["group"] = raw_data.get('Тип_инструмента')
    param["marking"] = raw_data.get('Обозначение')
    param["standard"] = raw_data.get('Стандарт')
    param["mat_of_cutting_part"] = default_settings["mat_of_cutting_part"]
    param["dia_mm"] = float(raw_data.get('D', 10))
    param["length_mm"] = float(raw_data.get('L', 95))
    param["main_angle_grad"] = float(raw_data.get('fi_', 60))
    param["front_angle_grad"] = float(raw_data.get('gamma_', 0))
    param["inclination_of_main_blade_grad"] = float(raw_data.get('lambda_', 0))
    param["num_of_cutting_blades"] = int(raw_data.get('z', 2))
    param["radius_of_cutting_vertex"] = float(raw_data.get('r_', 0.2))
    param["quantity"] = int(default_settings["quantity"])
    param["tolerance"] = str(default_settings["tolerance"])
    return param


def select_data_for_turning(raw_data: dict, default_settings: dict) -> dict:
    """ Из словаря данных, полученных из БД (сырых), выбирает данные для класса 'Резец'. """
    param = dict()
    # param["group"] = raw_data.get('Тип_инструмента')
    param["marking"] = raw_data.get('Обозначение')
    param["standard"] = raw_data.get('Стандарт')
    param["mat_of_cutting_part"] = default_settings["mat_of_cutting_part"]
    param["length_mm"] = float(raw_data.get('L', 120))
    param["width_mm"] = float(raw_data.get('B', 16))
    param["height_mm"] = float(raw_data.get('H', 20))
    param["main_angle_grad"] = float(raw_data.get('fi_', 45))
    param["front_angle_grad"] = float(raw_data.get('gamma_', 10))
    param["inclination_of_main_blade_grad"] = float(raw_data.get('lambda_', 0))
    param["radius_of_cutting_vertex"] = float(raw_data.get('r_', 0.2))
    param["quantity"] = int(default_settings["quantity"])
    param["turret"] = int(default_settings["turret"])
    param["load"] = int(default_settings["load"])
    param["is_complex_profile"] = True if default_settings["is_complex_profile"] == "True" else False
    return param


class ToolDataPreparer:
    SCRIPTS: ClassVar[dict] = {'Фреза': select_data_for_milling,
                               'Сверло': select_data_for_drilling,
                               'Зенкер': select_data_for_drilling,
                               'Развертка': select_data_for_drilling,
                               'Резец': select_data_for_turning, 
                               }
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS_FOR_TOOL

    def __init__(self, raw_data: Optional[dict]):
        self._raw_data = raw_data

    @property
    def to_generate(self):
        assert self._raw_data['Тип_инструмента'] in self.SCRIPTS
        script = self.SCRIPTS[self._raw_data['Тип_инструмента']]
        assert self._raw_data['Тип_инструмента'] in self.DEFAULT_SETTINGS
        param = script(self._raw_data, self.DEFAULT_SETTINGS[self._raw_data['Тип_инструмента']])
        return param
