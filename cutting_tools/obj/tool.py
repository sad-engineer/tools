#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar

from cutting_tools.obj.abstract_classes import ToolValidator, ToolController
from cutting_tools.obj.data_classes import ToolData
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.constants import GROUPS_TOOL, TYPES_STANDARD


class ToolInterface(ToolData, ToolValidator, ToolController):
    """ Класс 'Инструмент'

    Сostants:
        GROUPS_TOOL : Словарь наименований группы инструмента
        TYPES_STANDARD : Типы стандартов инструмента
    """
    GROUPS_TOOL: ClassVar[dict] = GROUPS_TOOL
    TYPES_STANDARD: ClassVar[dict] = TYPES_STANDARD

    def check_group(self, group):
        if self._is_correct_group(group):
            return group
        else:
            raise InvalidValue(f"Неверное задана группа инструмента: '{group}'")

    def check_standard(self, standard):
        if self._is_correct_standard(standard):
            return standard
        else:
            raise InvalidValue(f"Неверное задан стандарт инструмента: '{standard}'")

    @staticmethod
    def check_marking(marking):
        if isinstance(marking, str):
            return marking
        else:
            raise InvalidValue(f"Неверное задано обозначение инструмента: '{marking}'")

    def _is_correct_group(self, any_group):
        if isinstance(any_group, str):
            return any_group in self.GROUPS_TOOL
        return False

    def _is_correct_standard(self, any_standard):
        if isinstance(any_standard, str):
            for item in self.TYPES_STANDARD:
                if any_standard.find(item) != -1:
                    if any_standard.find("-") != -1:
                        return True
        return False

    def update_group(self, new_group):
        if not isinstance(new_group, type(None)):
            self.group = self.check_group(new_group)

    def update_marking(self, new_marking):
        if not isinstance(new_marking, type(None)):
            self.marking = self.check_marking(new_marking)

    def update_standard(self, new_standard):
        if not isinstance(new_standard, type(None)):
            self.standard = self.check_standard(new_standard)


if __name__ == "__main__":
    tool = ToolInterface(group="Инструмент", marking="0000-0000", standard="ГОСТ 5555-99")
    print(tool)
    tool.update_group("Резец")
    print(tool)
    print(tool._is_correct_group("Резец"))


