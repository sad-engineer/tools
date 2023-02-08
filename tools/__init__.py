#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Константы пакета
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
# from tools.fun import get_name
# Классы пакета
from tools.obj.containers import ToolContainer
MillingCutter = ToolContainer.milling_cutter
DrillingCutter = ToolContainer.drilling_cutter
CountersinkingCutter = ToolContainer.countersinking_cutter
DeploymentCutter = ToolContainer.deployment_cutter
TurningCutter = ToolContainer.turning_cutter
BroachingCutter = ToolContainer.broaching_cutter
Lister = ToolContainer.lister
Finder = ToolContainer.finder


if __name__ == "__main__":
    cutter = MillingCutter()
    print(cutter.name)


