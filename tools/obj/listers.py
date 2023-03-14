#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable

from service import logged

from tools.obj.creators import ToolCreator
from tools.obj.finders import Finder
from tools.obj.decorator import debugging_message_for_init_method as output_debug_message_for_init


def output_debug_message(message: str):
    """ Выводит в лог сообщение message"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.debug(message) if message.find("{") == -1 else self.debug(
                message.format('; '.join([f'{k}= {v}' for k, v in kwargs.items()])))
            return result
        return wrapper
    return decorator


@logged
class ToolLister:
    @output_debug_message_for_init()
    def __init__(self, tool_creator: ToolCreator, finder: Finder):
        self._tool_creator = tool_creator
        self._finder = finder

    @output_debug_message("Создаем список инструментов по ключам: {}.")
    def by_marking_and_stand(self, marking: str, standart: str) -> list:
        table_records = self._finder.by_marking_and_stand(marking=marking, standart=standart)
        self._tool_creator._verbose = True
        return [self._tool_creator.create_tool(row) for index, row in table_records.iterrows()]

    @output_debug_message("Создаем список инструментов по ключу: {}.")
    def by_marking(self, marking: str) -> list:
        table_records = self._finder.by_marking(marking=marking)
        self._tool_creator._verbose = True
        return [self._tool_creator.create_tool(row) for index, row in table_records.iterrows()]

    @output_debug_message("Создаем список инструментов по ключу: {}.")
    def by_stand(self, standart: str) -> list:
        table_records = self._finder.by_stand(standart=standart)
        self._tool_creator._verbose = True
        return [self._tool_creator.create_tool(row) for index, row in table_records.iterrows()]

    @property
    @output_debug_message("Создаем список всех инструментов БД.")
    def all(self) -> list:
        table_records = self._finder.all
        self._tool_creator._verbose = False
        return [self._tool_creator.create_tool(row) for index, row in table_records.iterrows()]
