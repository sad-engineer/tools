#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable

from service import logged

from tools.obj.creators import ToolCreator
from tools.obj.decorator import debugging_message_for_init_method as debug_for_init


@logged
class ToolLister:
    @debug_for_init()
    def __init__(self, tool_creator: Callable[..., ToolCreator]):
        self._tool_creator = tool_creator

        self.debug(f"""Создан {self.__class__.__name__} со следующими зависимостями: {tool_creator=} """)

    def by_marking_and_stand(self, marking: str, standard: str) -> list:
        self.debug(f"Создаем список инструментов по ключам: {marking=}, {standard=}.")
        return [tool for tool in self._tool_creator().by_marking_and_stand(marking=marking, standard=standard)]

    def by_marking(self, marking: str) -> list:
        self.debug(f"Создаем список инструментов по ключу: {marking=}.")
        return [tool for tool in self._tool_creator().by_marking(marking=marking)]

    def by_stand(self, standard: str) -> list:
        self.debug(f"Создаем список инструментов по ключу: {standard=}.")
        return [tool for tool in self._tool_creator().by_stand(standard=standard)]

    @property
    def all(self) -> list:
        self.debug(f"Получен запрос на создание всех материалов БД")
        return [tool for tool in self._tool_creator().all]
