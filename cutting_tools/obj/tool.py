#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional
from dataclasses import dataclass
from typing import ClassVar

from cutting_tools.obj.constants import GROUPS_TOOL, TYPES_STANDARD


@dataclass
class Tool:
    """ДатаКласс 'Инструмент'. Хранит состояние инструмента

    Parameters:
        group : (str, optional) : группа инструмента.
        marking : (str, optional) : обозначение инструмента.
        standard : (str, optional) : стандарт инструмента.
    """
    group: Optional[str] = "Инструмент"
    marking: Optional[str] = "0000-0000"
    standard: Optional[str] = "ГОСТ 5555-99"


    @property
    def name(self):
        return " ".join([self.group, self.marking, self.standard])
