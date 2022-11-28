#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cutting_tools.find import by_dia_and_type
from cutting_tools.find import by_marking_and_stand
from cutting_tools.find import full_table
from cutting_tools.fun import get_name
from cutting_tools.insert import insert
from cutting_tools.obj.cutting_tool_class import CuttingTool
from cutting_tools.obj.constants import INDEXES_OF_MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import NAMES_OF_MATERIALS_OF_CUTTING_PART

if __name__ == "__main__":
    # table = full_table()
    # print(table[table["fi_"].str.contains("°")])

    # params = by_marking_and_stand()
    # print(params)
    #
    # params = by_dia_and_type(dia_out=200, type_tool="Фреза")
    # print(params)
    #
    cutting_tool = CuttingTool('turning')
    cutting_tool.show()

    print(INDEXES_OF_MATERIALS_OF_CUTTING_PART)
    print(NAMES_OF_MATERIALS_OF_CUTTING_PART)
