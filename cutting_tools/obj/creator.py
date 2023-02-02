#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from cutting_tools.obj.milling_cutter import MillingCutter
from cutting_tools.obj.exceptions import InvalidValue
import re
from ast import literal_eval
from cutting_tools.obj.finder import Finder
from cutting_tools.obj.data_preparer import DataPreparer
from cutting_tools.obj.cataloger import Cataloger


# class Creator:
#
#     TOOL_CLASSES: ClassVar[dict] = {"Резец": None, "Фреза": MillingCutter, "Сверло": None, "Зенкер": None,
#                                     "Развертка": None, "Протяжка": None, }
#
#     def get_slass_tool(self, type_tool):
#         return self.TOOL_CLASSES[type_tool]
#
#     def get_tool(self, dict_par):
#         type_tool = dict_par["Тип_инструмента"]
#         class_tool = self.TOOL_CLASSES[type_tool]
#         if class_tool:
#             return class_tool(dict_par)
#         else:
#             raise InvalidValue(f"Класс для инструмента '{dict_par['Тип_инструмента']}' не определен.")



class CreatorFromLogLine:
    """ Создает объект из лога """
    def create(self, text_line: str):
        objects = re.split("[\(\)]", text_line)
        class_name = objects[0]
        dict_params = literal_eval(objects[1])
        del dict_params['name']

        return class_name, dict_params


if __name__ == "__main__":
    text = "MillingCutter({'name': 'Фреза 2214-0507 ГОСТ 28719-90', 'standard': 'ГОСТ 28719-90', 'marking': '2214-0507', 'mat_of_cutting_part': 'Р6М5', 'tolerance': 'h14', 'quantity': 1, 'type_cutter': 1})"

    create = CreatorFromLogLine().str
    class_name, dict_params = create(text)
    print(class_name, dict_params)

    del dict_params['name']
    print(class_name, dict_params)

    raw_table = Finder().find_by_marking_and_stand(dict_params["marking"], dict_params["standard"]).dropna(how='any', axis=1)
    print(raw_table)

    raw_param = raw_table.loc[0].to_dict()
    kind_of_cut, param = DataPreparer(raw_param).get_params
    print(class_name, param)

    cataloger = Cataloger()
    class_ = cataloger.get_class(class_name)

    cutter = class_(**param)
    print(cutter)
    print(cutter.__doc__)
    print(cutter.parameters)
