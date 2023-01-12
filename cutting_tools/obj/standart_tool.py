#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.tool import Tool
from cutting_tools.obj.standart_tool_validator import StandartToolValidator as Validator


class StandartTool(Tool, Validator):
    """ Класс "Стандартный инструмент", наследует: Tool, StandartToolValidator

    Parameters:
        group : (str, optional) : группа инструмента.
        marking : (str, optional) : обозначение инструмента.
        standard : (str, optional) : стандарт инструмента.
    """
    def __init__(self, group=None, marking=None, standard=None):
        Tool.__init__(self)
        Validator.__init__(self)
        self.update_group(group)
        self.update_marking(marking)
        self.update_standard(standard)

    def update_group(self, new_group):
        if not isinstance(new_group, type(None)):
            self.group = self.check_group(new_group)

    def update_marking(self, new_marking):
        if not isinstance(new_marking, type(None)):
            self.marking = self.check_marking(new_marking)

    def update_standard(self, new_standard):
        if not isinstance(new_standard, type(None)):
            self.standard = self.check_standard(new_standard)

# if __name__ == "__main__":
#     a = StandartTool("Резец", "0100-0200", "ГОСТ 6666-99")
#     print(a.name)

