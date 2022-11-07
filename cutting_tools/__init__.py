#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cutting_tools.find import by_dia_and_type
from cutting_tools.find import by_marking_and_stand
from cutting_tools.find import full_table
from cutting_tools.fun import get_name
from cutting_tools.insert import insert
from cutting_tools.obj.cutting_tool_class import CuttingTool

if __name__ == "__main__":
    table = full_table()
    print(table)

    params = by_marking_and_stand()
    print(params)

    params = by_dia_and_type(dia_out=200, type_tool="Фреза")
    print(params)

    cutting_tool = CuttingTool()
    cutting_tool.show
