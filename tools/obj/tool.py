#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union, ClassVar
from tools.obj.constants import GROUPS_TOOL, TYPES_STANDARD
from logger.obj.exceptions import InvalidValue
from logger import Dictionarer


class Tool(Dictionarer):
    """Управляет полями класса 'Инструмент'.

    Parameters:
        group : (str is GROUPS_TOOL) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.

    Properties:
        name : (str) : возвращает название инструмента.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.

    Сostants:
        GROUPS_TOOL : Словарь наименований группы инструмента.
        TYPES_STANDARD : Типы стандартов инструмента.
    """
    GROUPS_TOOL: ClassVar[dict] = GROUPS_TOOL
    TYPES_STANDARD: ClassVar[dict] = TYPES_STANDARD

    def __init__(self, group: Union[str, int] = "Инструмент", marking: str = "0000-0000", standard: str = "ГОСТ 5555-99"):
        self._name: str = None
        self._group: str = None
        self._marking: str = None
        self._standard: str = None

        self.group = group
        self.marking = marking
        self.standard = standard

    @property
    def group(self) -> str:
        return self._group

    @group.setter
    def group(self, group) -> None:
        if isinstance(group, (int, float)) and group not in self.GROUPS_TOOL.values():
            raise InvalidValue(f'Неверное значение индекса группы инструмента. Значение должно быть из '
                             f'{self.GROUPS_TOOL}.')
        if isinstance(group, str) and group not in self.GROUPS_TOOL:
            raise InvalidValue(f'Неверное значение группы инструмента. Значение должно быть из {self.GROUPS_TOOL}.')
        if not isinstance(group, (int, float, str)):
            raise InvalidValue(f'Неверное значение группы инструмента. Значение должно быть из {self.GROUPS_TOOL}.')
        self._group = group if isinstance(group, str) else [k for k, v in self.GROUPS_TOOL.items() if v == group][0]

    @property
    def marking(self) -> str:
        return self._marking

    @marking.setter
    def marking(self, any_marking) -> None:
        if not isinstance(any_marking, str):
            raise InvalidValue(f'Неверное обозначение инструмента.')
        self._marking = any_marking

    @property
    def standard(self) -> str:
        return self._standard

    @standard.setter
    def standard(self, any_standard) -> None:
        if not isinstance(any_standard, str):
            raise InvalidValue(f'Неверное значение стандарта инструмента.')
        if any_standard.split(" ")[0] not in self.TYPES_STANDARD:
            raise InvalidValue(f'Неверное значение стандарта инструмента.')
        if not any_standard.find("-") != -1:
            raise InvalidValue(f'Неверное значение стандарта инструмента (возможно не указан год).')
        self._standard = any_standard

    @property
    def name(self) -> str:
        self._name = " ".join([self.group, self.marking, self.standard])
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value

    def _parameters(self) -> dict:
        return {"group": self._group, "marking": self._marking, "standard": self._standard, "name": self.name}


if __name__ == "__main__":
    obj = Tool()

    obj.group = "Резец"
    print(obj.group)
    print(obj.GROUPS_TOOL)
    # obj.group = "Плашка"
    # print(obj.group)
    print(obj.name)

    obj = Tool(group=0)
    print(obj.group)
    print(obj.name)

    obj = Tool(group="Фреза")
    print(obj.group)
    print(obj.parameters)




