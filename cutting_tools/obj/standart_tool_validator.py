#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.constants import GROUPS_TOOL, TYPES_STANDARD
from typing import ClassVar


class StandartToolValidator(ABC):
    """ Абстрактный класс, реализует проверки полей стандартного инструмента

    Сostants:
        GROUPS_TOOL : Словарь наименований группы инструмента
        TYPES_STANDARD : Типы стандартов инструмента

    Methods:
        check_group(group) : Проверяет на соответствие группы инструмента (группа инструмента должна быть строкой и из
            списка наименований групп инструмента)
        check_standard(standard) : Проверяет на соответствие стандарта инструмента (стандарт инструмента должен быть
            строкой и содержать одно из слов списка типов стандарта(ГОСТ, ОСТ))
        check_marking(marking) : Проверяет на соответствие обозначения инструмента (обозначение инструмента должно быть
            строкой)

        _is_correct_group(any_group) : Бросит True если any_group в словаре наименований групп инструмента
        _is_correct_standard(any_standard) : Бросит True если any_standard содержит одно из слов списка типов стандарта
            (ГОСТ, ОСТ))
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
