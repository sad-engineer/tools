#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Константы пакета
from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.constants import HARD_ALLOYS
from cutting_tools.obj.constants import HIGH_SPEED_STEELS
from cutting_tools.obj.constants import MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import GROUPS_TOOL
from cutting_tools.obj.constants import TYPES_STANDARD
from cutting_tools.obj.constants import TYPES_OF_MILLING_CUTTER
from cutting_tools.obj.constants import TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER
from cutting_tools.obj.constants import TYPES_OF_LARGE_TOOTH
from cutting_tools.obj.constants import TYPES_OF_TOOL_HOLDER
from cutting_tools.obj.constants import TYPES_OF_LOADS

# Методы пакета
from cutting_tools.fun import get_name


# Классы пакета
from cutting_tools.obj.milling_cutter import MillingCutter
from cutting_tools.obj.drilling_cutter import DrillingCutter
from cutting_tools.obj.countersinking_cutter import CountersinkingCutter
from cutting_tools.obj.deployment_cutter import DeploymentCutter
from cutting_tools.obj.turning_cutter import TurningCutter
from cutting_tools.obj.finder import Finder
from cutting_tools.obj.data_preparer import DataPreparer
from cutting_tools.obj.logger import Logger
from cutting_tools.obj.file_printer import FilePrinter


if __name__ == "__main__":
    marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["milling"]["marking"]
    raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    raw_param = raw_table.loc[0].to_dict()
    param = DataPreparer(raw_param).get_params
    cutter = MillingCutter(**param)
    Logger().log(cutter, message='### Параметры применяемого инструмента ###')
    Logger().log(cutter, notifier=FilePrinter, message='### Параметры применяемого инструмента ###')

    marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["drilling"]["marking"]
    raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    raw_param = raw_table.loc[0].to_dict()
    param = DataPreparer(raw_param).get_params
    cutter = DrillingCutter(**param)
    Logger().log(cutter, message='### Параметры применяемого инструмента ###')
    Logger().log(cutter, notifier=FilePrinter, message='### Параметры применяемого инструмента ###')

    marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["countersinking"]["marking"]
    raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    raw_param = raw_table.loc[0].to_dict()
    param = DataPreparer(raw_param).get_params
    cutter = CountersinkingCutter(**param)
    Logger().log(cutter, message='### Параметры применяемого инструмента ###')
    Logger().log(cutter, notifier=FilePrinter, message='### Параметры применяемого инструмента ###')

    marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["deployment"]["marking"]
    raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    raw_param = raw_table.loc[0].to_dict()
    param = DataPreparer(raw_param).get_params
    cutter = DeploymentCutter(**param)
    Logger().log(cutter, message='### Параметры применяемого инструмента ###')
    Logger().log(cutter, notifier=FilePrinter, message='### Параметры применяемого инструмента ###')

    marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["turning"]["marking"]
    raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    raw_param = raw_table.loc[0].to_dict()
    param = DataPreparer(raw_param).get_params
    cutter = TurningCutter(**param)
    Logger().log(cutter, message='### Параметры применяемого инструмента ###')
    Logger().log(cutter, notifier=FilePrinter, message='### Параметры применяемого инструмента ###')
