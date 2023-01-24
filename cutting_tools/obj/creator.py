#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from cutting_tools.obj.milling_cutter import MillingCutter
from cutting_tools.obj.exceptions import InvalidValue


class Creator:
    TOOL_CLASSES: ClassVar[dict] = {"Резец": None, "Фреза": MillingCutter, "Сверло": None, "Зенкер": None,
                                    "Развертка": None, "Протяжка": None, }

    def get_slass_tool(self, type_tool):
        return self.TOOL_CLASSES[type_tool]

    def get_tool(self, dict_par):
        type_tool = dict_par["Тип_инструмента"]
        class_tool = self.TOOL_CLASSES[type_tool]
        if class_tool:
            return class_tool(dict_par)
        else:
            raise InvalidValue(f"Класс для инструмента '{dict_par['Тип_инструмента']}' не определен.")




