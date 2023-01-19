#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar

from cutting_tools.obj.abstract_classes import ToolValidator, ToolController
from cutting_tools.obj.data_classes import ToolData
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.checker_in_dict import CheckerInDictionary


class Tool(ToolData, ToolValidator, ToolController, CheckerInDictionary):
    """ Класс 'Инструмент' """
    @staticmethod
    def check_marking(marking):
        if isinstance(marking, str):
            return marking
        else:
            raise InvalidValue(f"Неверное задано обозначение инструмента: '{marking}'")

    def _is_correct_standard(self, any_standard):
        if isinstance(any_standard, str):
            for item in self.TYPES_STANDARD:
                if any_standard.find(item) != -1:
                    if any_standard.find("-") != -1:
                        return True
        return False

    def check_standard(self, standard):
        if self._is_correct_standard(standard):
            return standard
        else:
            raise InvalidValue(f"Неверное задан стандарт инструмента: '{standard}'")

    def update_group(self, new_group):
        if not isinstance(new_group, type(None)):
            self.group = self.check_index_in_dict(new_group, self.GROUPS_TOOL,
                                                  f"Неверное задана группа инструмента: '{new_group}'")

    def update_marking(self, new_marking):
        if not isinstance(new_marking, type(None)):
            self.marking = self.check_marking(new_marking)

    def update_standard(self, new_standard):
        if not isinstance(new_standard, type(None)):
            self.standard = self.check_standard(new_standard)



