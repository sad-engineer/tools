#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, List, Protocol

from tools.app.factories import ToolSchemaFactory
from tools.app.models.tools import Tool
from tools.app.schemas.tool import BaseTool


class ToolFormatter(Protocol):
    """Протокол для форматтеров инструментов"""

    def format(self, tools: List[Tool]) -> Any:
        """Форматирует список инструментов"""
        ...


class ListFormatter(ToolFormatter):
    """Форматтер, возвращающий список схем инструментов"""

    def format(self, tools: List[Tool]) -> List[BaseTool]:
        result = []
        for tool in tools:
            try:
                schema = ToolSchemaFactory.create_schema(tool)
                result.append(schema)
            except ValueError as e:
                # Если схема не поддерживается, создаем базовую схему
                from tools.app.schemas.tool import Tool as BaseToolSchema

                schema = BaseToolSchema(marking=tool.marking, standard=tool.standard)
                result.append(schema)
        return result


class DictFormatter(ToolFormatter):
    """Форматтер, возвращающий словарь {marking: схема}"""

    def format(self, tools: List[Tool]) -> Dict[str, BaseTool]:
        result = {}
        for tool in tools:
            try:
                schema = ToolSchemaFactory.create_schema(tool)
                result[tool.marking] = schema
            except ValueError as e:
                # Если схема не поддерживается, создаем базовую схему
                from tools.app.schemas.tool import Tool as BaseToolSchema

                schema = BaseToolSchema(marking=tool.marking, standard=tool.standard)
                result[tool.marking] = schema
        return result


class IndexedNameFormatter(ToolFormatter):
    """Форматтер, возвращающий словарь {номер: схема}"""

    def format(self, tools: List[Tool]) -> Dict[int, BaseTool]:
        result = {}
        for i, tool in enumerate(tools):
            try:
                schema = ToolSchemaFactory.create_schema(tool)
                result[i + 1] = schema
            except ValueError as e:
                # Если схема не поддерживается, создаем базовую схему
                from tools.app.schemas.tool import Tool as BaseToolSchema

                schema = BaseToolSchema(marking=tool.marking, standard=tool.standard)
                result[i + 1] = schema
        return result
