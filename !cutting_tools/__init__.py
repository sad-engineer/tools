#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Константы пакета
from cutting_tools.obj.constants import DEFAULT_SETTINGS_FOR_TOOL
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
from cutting_tools.obj.constants import SAVED_FIELDS
# Методы пакета
# from !cutting_tools.fun import get_name
# Классы пакета
from cutting_tools.obj.milling_cutter import MillingCutter
from cutting_tools.obj.drilling_cutter import DrillingCutter
from cutting_tools.obj.countersinking_cutter import CountersinkingCutter
from cutting_tools.obj.deployment_cutter import DeploymentCutter
from cutting_tools.obj.turning_cutter import TurningCutter
from cutting_tools.obj.finder import Finder
from cutting_tools.obj.data_preparer import DataPreparer
from cutting_tools.obj.containers import Container



if __name__ == "__main__":
    import logger
    import os

    container = Container()
    container.init_resources()
    #
    # cutter = container.turning_cutter()
    # print(cutter)
    #
    # log = logger.Container.logger().log
    # terminal_printer = Container.standard_result_terminal_printer()
    # log(cutter, notifier=terminal_printer, message="""### Инструмент""")
    #
    # file_printer = logger.Container.standard_object_file_saver(decoding=DECODING, saved_fields=SAVED_FIELDS)
    # log(cutter, notifier=file_printer)
    #
    # creator = Container.creator_from_log_line()
    # print(creator._catalog.classes)
    #
    # with open(os.getcwd()+'\\logs\\log.txt', mode='r', encoding="utf8") as f:
    #     context = f.readlines()
    # for line in context:
    #     cutter = creator.create(log_line=line)
    #     print(cutter)
    #     print(cutter.name)

    finder = container.finder()
    for marking in ['2214-0507', '2100-0029',  '2300-0041',  '2320-2125',  '2364-0331',]:
        line = finder.find_by_marking(marking)
        # collumns = line.
        line = line.loc[0].to_dict()
        print(list(line.keys()))
        print(list(line.values()))

