#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Константы пакета
# from tools_old.obj.constants import PATH_DB_FOR_TOOLS
from tools_old.obj.constants import (
    ACCURACY_CLASS_STANDARDS,
    ACCURACY_STANDARDS,
    DECODING,
    DEFAULT_SETTINGS_FOR_TOOL,
    GROUPS_TOOL,
    MATERIALS_OF_CUTTING_PART,
    SAVED_FIELDS,
    TOLERANCE_FIELDS,
    TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER,
    TYPES_OF_LARGE_TOOTH,
    TYPES_OF_LOADS,
    TYPES_OF_MILLING_CUTTER,
    TYPES_OF_TOOL_HOLDER,
    TYPES_STANDARD,
)

# Классы пакета
from tools_old.obj.containers import ToolContainer

# Методы пакета
from tools_old.scr.fun import get_name

MillingCutter = ToolContainer.milling_cutter
DrillingCutter = ToolContainer.drilling_cutter
CountersinkingCutter = ToolContainer.countersinking_cutter
DeploymentCutter = ToolContainer.deployment_cutter
TurningCutter = ToolContainer.turning_cutter
BroachingCutter = ToolContainer.broaching_cutter
ToolCreator = ToolContainer.creator
ToolLister = ToolContainer.lister
ToolFinder = ToolContainer.finder
from tools_old.obj.entities import CustomTool, Tool

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
#     from tools_old.obj.constants import PATH_DB_FOR_TOOLS
#     print(PATH_DB_FOR_TOOLS)
