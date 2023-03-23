#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from service import logged
from service import output_debug_message_for_init_method as debug_for_init

from tools.obj.creators import ToolCreator
from tools.obj.finders import ToolFinder
from tools.obj.fields_types import InGroupsTool
from tools.obj.constants import DEFAULT_SETTINGS_FOR_TOOL as DEFAULT_TOOL


def output_debug_message(message: str):
    """ Выводит в лог сообщение message"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            self.debug(message) if message.find("{") == -1 else self.debug(
                message.format('; '.join([f'{k}= {v}' for k, v in kwargs.items()])))
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


@logged
class ToolLister:
    @debug_for_init()
    def __init__(self, tool_creator: ToolCreator, finder: ToolFinder):
        self._tool_creator = tool_creator
        self._finder = finder

    @output_debug_message("Создаем список инструментов по ключам: {}.")
    def by_marking_and_stand(self, marking: str, standard: str) -> list:
        table_records = self._finder.by_marking_and_stand(marking=marking, standard=standard)
        self._tool_creator._verbose = True
        return [self._tool_creator.create_tool(row) for index, row in table_records.iterrows()]

    @output_debug_message("Создаем список инструментов по ключу: {}.")
    def by_marking(self, marking: str) -> list:
        table_records = self._finder.by_marking(marking=marking)
        self._tool_creator._verbose = True
        return [self._tool_creator.create_tool(row) for index, row in table_records.iterrows()]

    @output_debug_message("Создаем список инструментов по ключу: {}.")
    def by_stand(self, standard: str) -> list:
        table_records = self._finder.by_stand(standard=standard)
        self._tool_creator._verbose = True
        return [self._tool_creator.create_tool(row) for index, row in table_records.iterrows()]

    @property
    @output_debug_message("Создаем список всех инструментов БД.")
    def all(self) -> list:
        table_records = self._finder.all
        self._tool_creator._verbose = False
        return [self._tool_creator.create_tool(row) for index, row in table_records.iterrows()]

    @output_debug_message("Создаем список инструментов по ключу: {}.")
    def by_group(self, group: InGroupsTool = "Фреза") -> list:
        table_records = self._finder.by_group(group=group)
        return [self._tool_creator.create_tool(row) for index, row in table_records.iterrows()]

    @output_debug_message("Создаем инструмент с настройками по умолчанию: {}.")
    def default(self, group: InGroupsTool = "Фреза") -> list:
        deftool = DEFAULT_TOOL[group]
        return self.by_marking_and_stand(marking=deftool["marking"], standard=deftool["Стандарт"])
