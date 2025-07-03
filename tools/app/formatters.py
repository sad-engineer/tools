#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, List, Protocol

from tools.app.factories import default_tool_schema_factory
from tools.app.models.tools import Tool
from tools.app.schemas.tool import BaseTool


class ToolFormatter(Protocol):
    """Протокол для форматтеров инструментов"""

    def format(self, tools: List[Tool], mapper_factory=None) -> Any:
        """Форматирует список инструментов"""
        ...


class ListFormatter(ToolFormatter):
    """Форматтер, возвращающий список схем инструментов"""

    def format(self, tools: List[Tool], mapper_factory=None) -> List[BaseTool]:
        result = []
        for tool in tools:
            try:
                schema = default_tool_schema_factory.create_schema(tool)
                # Если передан кастомный маппер, используем его
                if mapper_factory:
                    mapper_factory.map_tool_to_schema(tool, schema)
                result.append(schema)
            except ValueError as e:
                # Если схема не поддерживается, создаем базовую схему
                from tools.app.schemas.tool import Tool as BaseToolSchema

                print(f"Предупреждение: Группа '{tool.group}' не поддерживается для инструмента {tool.marking}. "
                      f"Используется базовая схема. Ошибка: {e}")
                schema = BaseToolSchema(marking=tool.marking, standard=tool.standard)
                result.append(schema)
        return result


class DictFormatter(ToolFormatter):
    """Форматтер, возвращающий словарь {marking: схема}"""

    def format(self, tools: List[Tool], mapper_factory=None) -> Dict[str, BaseTool]:
        result = {}
        for tool in tools:
            try:
                schema = default_tool_schema_factory.create_schema(tool)
                # Если передан кастомный маппер, используем его
                if mapper_factory:
                    mapper_factory.map_tool_to_schema(tool, schema)
                result[tool.marking] = schema
            except ValueError as e:
                # Если схема не поддерживается, создаем базовую схему
                from tools.app.schemas.tool import Tool as BaseToolSchema

                print(f"Предупреждение: Группа '{tool.group}' не поддерживается для инструмента {tool.marking}. "
                      f"Используется базовая схема. Ошибка: {e}")
                schema = BaseToolSchema(marking=tool.marking, standard=tool.standard)
                result[tool.marking] = schema
        return result


class IndexedNameFormatter(ToolFormatter):
    """Форматтер, возвращающий словарь {номер: схема}"""

    def format(self, tools: List[Tool], mapper_factory=None) -> Dict[int, BaseTool]:
        result = {}
        for i, tool in enumerate(tools):
            try:
                schema = default_tool_schema_factory.create_schema(tool)
                # Если передан кастомный маппер, используем его
                if mapper_factory:
                    mapper_factory.map_tool_to_schema(tool, schema)
                result[i + 1] = schema
            except ValueError as e:
                # Если схема не поддерживается, создаем базовую схему
                from tools.app.schemas.tool import Tool as BaseToolSchema

                print(f"Предупреждение: Группа '{tool.group}' не поддерживается для инструмента {tool.marking}. "
                      f"Используется базовая схема. Ошибка: {e}")
                schema = BaseToolSchema(marking=tool.marking, standard=tool.standard)
                result[i + 1] = schema
        return result
