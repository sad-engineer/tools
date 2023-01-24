#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cutting_tools.find import by_dia_and_type
from cutting_tools.find import by_marking_and_stand
from cutting_tools.find import full_table
from cutting_tools.fun import get_name
from cutting_tools.obj.cutting_tool_class import CuttingTool
from cutting_tools.obj.constants import MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import MATERIALS_OF_CUTTING_PART



# from cutting_tools.fun import get_tool
from cutting_tools.obj.finder import Finder
from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.milling_cutter import MillingCutter
from typing import ClassVar


class DataPreparer:
    DEFAULT_SETTINGS_FOR_CUTTING_TOOL: ClassVar[dict] = DEFAULT_SETTINGS_FOR_CUTTING_TOOL

    def __init__(self, raw_data: dict):
        self.raw_data = raw_data

    def get_params(self, cutter_tool_cls):
        param = dict()
        param["group"] = self.raw_data.get('Тип_инструмента')
        param["marking"] = self.raw_data.get('Обозначение')
        param["standard"] = self.raw_data.get('Стандарт')
        param["mat_of_cutting_part"] = self.DEFAULT_SETTINGS_FOR_CUTTING_TOOL['milling']["mat_of_cutting_part"]
        param["dia_mm"] = float(self.raw_data.get('D', 25))
        param["length_mm"] = float(self.raw_data.get('L', 25))
        param["main_angle_grad"] = float(self.raw_data.get('fi_', 45))
        param["front_angle_grad"] = float(self.raw_data.get('gamma_', 0))
        param["inclination_of_main_blade_grad"] = float(self.raw_data.get('lambda_', 0))
        param["type_cutter"] = self.raw_data.get('type_cutter_')
        param["type_of_cutting_part"] = int(self.raw_data.get('type_of_cutting_part_', 1))
        param["num_of_cutting_blades"] = int(self.raw_data.get('z', 2))
        param["radius_of_cutting_vertex"] = float(self.raw_data.get('r_', 1.0))
        param["large_tooth"] = self.raw_data.get('large_tooth', 0)
        param["quantity"] = int(self.DEFAULT_SETTINGS_FOR_CUTTING_TOOL['milling']["quantity"])
        return cutter_tool_cls(**param)


if __name__ == "__main__":
    marking = "2210-0061"
    raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    raw_dict = raw_table.loc[0].to_dict()
    print(raw_dict)

    preparer = DataPreparer(raw_dict)
    print(preparer.DEFAULT_SETTINGS_FOR_CUTTING_TOOL['milling'])
    cutter = preparer.get_params(MillingCutter)

    print(cutter)


    # print(DEFAULT_SETTINGS_FOR_CUTTING_TOOL)
    # dict_param = {
    #     "group": raw_dict['Тип_инструмента'],
    #     "marking": raw_dict['Обозначение'],
    #     "standard": raw_dict['Стандарт'],
    #
    #     "mat_of_cutting_part": DEFAULT_SETTINGS_FOR_CUTTING_TOOL['milling']["mat_of_cutting_part"],
    #
    #     "dia_mm": raw_dict['D'],
    #     "length_mm": raw_dict['L'],
    #
    #     "main_angle_grad": lambda x: raw_dict['fi_'] if 'fi_' in raw_dict else 1.0,
    #     "front_angle_grad": lambda x: raw_dict['gamma_'] if 'gamma_' in raw_dict else 1.0,
    #     "inclination_of_main_blade_grad": lambda x: raw_dict['lambda_'] if 'lambda_' in raw_dict else 1.0,
    #
    #     "type_cutter": raw_dict['type_cutter_'],
    #     "type_of_cutting_part": raw_dict['type_of_cutting_part_'],
    #     "num_of_cutting_blades": raw_dict['z'],
    #     "radius_of_cutting_vertex": lambda x: raw_dict['r_'] if 'r_' in raw_dict else 1.0,
    #     "large_tooth": lambda x: raw_dict['large_tooth'] if 'large_tooth' in raw_dict else 0,
    #     "quantity": DEFAULT_SETTINGS_FOR_CUTTING_TOOL['milling']["quantity"],
    # }
    # print(dict_param)
    # a = MillingCutter(dict_param)
    # print(a)
    #
    # checker = RawDataChecker()
    # a = checker.check_and_create_params()

    # print(result[0].to_dict())
    # table = full_table()
    # print(table[table["fi_"].str.contains("°")])
    # params = by_marking_and_stand()
    # print(params)
    #
    # params = by_dia_and_type(dia_out=200, type_tool="Фреза")
    # print(params)
    #
    # cutting_tool = CuttingTool('broaching')
    # cutting_tool.get_default_settings()
    # cutting_tool.show()
    #
    # print(INDEXES_OF_MATERIALS_OF_CUTTING_PART)
    # print(NAMES_OF_MATERIALS_OF_CUTTING_PART)
