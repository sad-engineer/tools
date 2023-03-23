#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Константы пакета
# from tools.obj.constants import PATH_DB_FOR_TOOLS
from tools.obj.constants import DEFAULT_SETTINGS_FOR_TOOL
from tools.obj.constants import MATERIALS_OF_CUTTING_PART
from tools.obj.constants import GROUPS_TOOL
from tools.obj.constants import TYPES_STANDARD
from tools.obj.constants import TYPES_OF_MILLING_CUTTER
from tools.obj.constants import TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER
from tools.obj.constants import TYPES_OF_LARGE_TOOTH
from tools.obj.constants import TYPES_OF_TOOL_HOLDER
from tools.obj.constants import TYPES_OF_LOADS
from tools.obj.constants import ACCURACY_STANDARDS
from tools.obj.constants import TOLERANCE_FIELDS
from tools.obj.constants import ACCURACY_CLASS_STANDARDS
from tools.obj.constants import DECODING
from tools.obj.constants import SAVED_FIELDS
# Методы пакета
from tools.scr.fun import get_name
# Классы пакета
from tools.obj.containers import ToolContainer
MillingCutter = ToolContainer.milling_cutter
DrillingCutter = ToolContainer.drilling_cutter
CountersinkingCutter = ToolContainer.countersinking_cutter
DeploymentCutter = ToolContainer.deployment_cutter
TurningCutter = ToolContainer.turning_cutter
BroachingCutter = ToolContainer.broaching_cutter
ToolCreator = ToolContainer.creator
ToolLister = ToolContainer.lister
ToolFinder = ToolContainer.finder
from tools.obj.entities import Tool, CustomTool


__all__ = [
    # Константы пакета
    # "PATH_DB_FOR_TOOLS",
    "DEFAULT_SETTINGS_FOR_TOOL",
    "MATERIALS_OF_CUTTING_PART",
    "GROUPS_TOOL",
    "TYPES_STANDARD",
    "TYPES_OF_MILLING_CUTTER",
    "TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER",
    "TYPES_OF_LARGE_TOOTH",
    "TYPES_OF_TOOL_HOLDER",
    "TYPES_OF_LOADS",
    "ACCURACY_STANDARDS",
    "TOLERANCE_FIELDS",
    "ACCURACY_CLASS_STANDARDS",
    "DECODING",
    "SAVED_FIELDS",
    # Методы пакета
    "get_name",
    # Классы пакета
    "ToolContainer",
    "MillingCutter",
    "DrillingCutter",
    "CountersinkingCutter",
    "DeploymentCutter",
    "TurningCutter",
    "BroachingCutter",
    "ToolCreator",
    "ToolLister",
    "ToolFinder",
    "Tool",
    "CustomTool",
    ]

# if __name__ == "__main__":
#
#     cutter = MillingCutter()
#     print(cutter.name)
#
#     from tools.obj.constants import PATH_DB_FOR_TOOLS
#     print(PATH_DB_FOR_TOOLS)

