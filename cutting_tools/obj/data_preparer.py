#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cutting_tools.obj.finder import Finder
from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL, GROUPS_TOOL
from typing import ClassVar


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

    # TODO: Переделать выбор типа фрезы для вариантов 'Торцовая, Цилиндрическая', 'Концевая (для T-образных пазов)', 'Концевая (для обработки Т-образного паза)'
    type_cutter = raw_data.get('type_cutter_')
    type_cutter = type_cutter.split(", ")[0]
    type_cutter = type_cutter.split(" (")[0]
    param["type_cutter"] = type_cutter

    param["type_of_cutting_part"] = int(raw_data.get('type_of_cutting_part_', 1))
    param["num_of_cutting_blades"] = int(raw_data.get('z', 2))
    param["radius_of_cutting_vertex"] = float(raw_data.get('r_', 1.0))
    param["large_tooth"] = raw_data.get('large_tooth', 0)
    param["quantity"] = int(default_settings["quantity"])
    return param


def select_data_for_drilling(raw_data: dict, DEFAULT_SETTINGS: dict) -> dict:
    """ Из словаря данных, полученных из БД (сырых), выбирает данные для класса 'Сверло'. """
    param = dict()
    # param["group"] = raw_data.get('Тип_инструмента')
    param["marking"] = raw_data.get('Обозначение')
    param["standard"] = raw_data.get('Стандарт')
    param["mat_of_cutting_part"] = DEFAULT_SETTINGS["mat_of_cutting_part"]
    param["dia_mm"] = float(raw_data.get('D', 10))
    param["length_mm"] = float(raw_data.get('L', 95))
    param["main_angle_grad"] = float(raw_data.get('fi_', 60))
    param["front_angle_grad"] = float(raw_data.get('gamma_', 0))
    param["inclination_of_main_blade_grad"] = float(raw_data.get('lambda_', 0))
    param["num_of_cutting_blades"] = int(raw_data.get('z', 2))
    param["radius_of_cutting_vertex"] = float(raw_data.get('r_', 0.2))
    param["quantity"] = int(DEFAULT_SETTINGS["quantity"])
    return param


def select_data_for_turning(raw_data: dict, DEFAULT_SETTINGS: dict) -> dict:
    """ Из словаря данных, полученных из БД (сырых), выбирает данные для класса 'Резец'. """
    param = dict()
    # param["group"] = raw_data.get('Тип_инструмента')
    param["marking"] = raw_data.get('Обозначение')
    param["standard"] = raw_data.get('Стандарт')
    param["mat_of_cutting_part"] = DEFAULT_SETTINGS["mat_of_cutting_part"]
    param["length_mm"] = float(raw_data.get('L', 120))
    param["width_mm"] = float(raw_data.get('B', 16))
    param["height_mm"] = float(raw_data.get('H', 20))
    param["main_angle_grad"] = float(raw_data.get('fi_', 45))
    param["front_angle_grad"] = float(raw_data.get('gamma_', 10))
    param["inclination_of_main_blade_grad"] = float(raw_data.get('lambda_', 0))
    param["radius_of_cutting_vertex"] = float(raw_data.get('r_', 0.2))
    param["quantity"] = int(DEFAULT_SETTINGS["quantity"])
    return param


class DataPreparer:
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS_FOR_CUTTING_TOOL
    GROUPS_TOOL: ClassVar[dict] = GROUPS_TOOL
    SCRIPTS: ClassVar[dict] = {'milling': select_data_for_milling,
                               'drilling': select_data_for_drilling,
                               'countersinking': select_data_for_drilling,
                               'deployment': select_data_for_drilling,
                               'turning': select_data_for_turning,
                                }

    def __init__(self, raw_data: dict):
        self._raw_data = raw_data

    @property
    def get_params(self):
        kind_of_cut = self.GROUPS_TOOL[self._raw_data['Тип_инструмента']]
        script = self.SCRIPTS[kind_of_cut]
        param = script(self._raw_data, self.DEFAULT_SETTINGS[kind_of_cut])
        return kind_of_cut, param


if __name__ == "__main__":
    marking = "2300-0007"
    raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    raw_param = raw_table.loc[0].to_dict()
    print(raw_param)

    param = DataPreparer(raw_param).get_params
    print(param)
