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
        group : (str) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str) : стандарт инструмента.
    """
    group: str = "Инструмент"
    marking: str = "0000-0000"
    standard: str = "ГОСТ 5555-99"


    @property
    def name(self):
        return " ".join([self.group, self.marking, self.standard])
