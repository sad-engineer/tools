#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Константы пакета
from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_CUTTING_TOOL
from cutting_tools.obj.constants import MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import GROUPS_TOOL
from cutting_tools.obj.constants import TYPES_STANDARD
from cutting_tools.obj.constants import TYPES_OF_MILLING_CUTTER
from cutting_tools.obj.constants import TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER
from cutting_tools.obj.constants import TYPES_OF_LARGE_TOOTH
from cutting_tools.obj.constants import TYPES_OF_TOOL_HOLDER
from cutting_tools.obj.constants import TYPES_OF_LOADS
from cutting_tools.obj.constants import ACCURACY_STANDARDS
from cutting_tools.obj.constants import TOLERANCE_FIELDS
from cutting_tools.obj.constants import ACCURACY_CLASS_STANDARDS
from cutting_tools.obj.constants import DECODING
# Методы пакета
# from cutting_tools.fun import get_name
# Классы пакета
from cutting_tools.obj.milling_cutter import MillingCutter
from cutting_tools.obj.drilling_cutter import DrillingCutter
from cutting_tools.obj.countersinking_cutter import CountersinkingCutter
from cutting_tools.obj.deployment_cutter import DeploymentCutter
from cutting_tools.obj.turning_cutter import TurningCutter
from cutting_tools.obj.finder import Finder
from cutting_tools.obj.data_preparer import DataPreparer


if __name__ == "__main__":
    from logger import Logger
    from logger import StandardResultTerminalPrinter, StandardObjectTerminalPrinter
    from logger import StandardResultFilePrinter, StandardObjectFilePrinter

    variants = ["milling",
                "turning",
                "planing",
                "drilling",
                "countersinking",
                "deployment",
                # "broaching",
                ]
    cutter_clases = {"milling": MillingCutter,
                     "turning": TurningCutter,
                     "planing": TurningCutter,
                     "drilling": DrillingCutter,
                     "countersinking": CountersinkingCutter,
                     "deployment": DeploymentCutter,
                     }

    logger = Logger()
    # file_printer = StandardResultTerminalPrinter
    # file_printer = StandardObjectTerminalPrinter
    # file_printer = StandardResultFilePrinter
    file_printer = StandardObjectFilePrinter
    file_printer.DECODING = DECODING

    for variant in variants:
        marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL[variant]["marking"]
        raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
        raw_param = raw_table.loc[0].to_dict()
        kind_of_cut, param = DataPreparer(raw_param).get_params
        cutter_class = cutter_clases[variant]
        cutter = cutter_class(**param)
        logger.log(cutter, notifier=file_printer, message='### Параметры применяемого инструмента ###')

    # marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["drilling"]["marking"]
    # raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    # raw_param = raw_table.loc[0].to_dict()
    # param = DataPreparer(raw_param).get_params
    # cutter = DrillingCutter(**param)
    # Logger().log(cutter, notifier=file_printer, message='### Параметры применяемого инструмента ###')
    #
    # marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["countersinking"]["marking"]
    # raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    # raw_param = raw_table.loc[0].to_dict()
    # param = DataPreparer(raw_param).get_params
    # cutter = CountersinkingCutter(**param)
    # Logger().log(cutter, notifier=file_printer, message='### Параметры применяемого инструмента ###')
    #
    # marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["deployment"]["marking"]
    # raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    # raw_param = raw_table.loc[0].to_dict()
    # param = DataPreparer(raw_param).get_params
    # cutter = DeploymentCutter(**param)
    # Logger().log(cutter, notifier=file_printer, message='### Параметры применяемого инструмента ###')
    #
    # marking = DEFAULT_SETTINGS_FOR_CUTTING_TOOL["turning"]["marking"]
    # raw_table = Finder().find_by_marking(marking).dropna(how='any', axis=1)
    # raw_param = raw_table.loc[0].to_dict()
    # param = DataPreparer(raw_param).get_params
    # cutter = TurningCutter(**param)
    # Logger().log(cutter, notifier=file_printer, message='### Параметры применяемого инструмента ###')
