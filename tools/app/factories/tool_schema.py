#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Dict, Type

from tools.app.models.tools import Tool
from tools.app.schemas import (
    BroachingCutter,
    CountersinkingCutter,
    DeploymentCutter,
    DrillingCutter,
    MillingCutter,
    TurningCutter,
)
from tools.app.schemas.tool import BaseTool
from tools.app.factories.base import BaseFactory


class ToolSchemaFactory(BaseFactory[Type[BaseTool]]):
    """
    Фабрика для создания схем инструментов на основе группы инструмента.

    Сопоставляет группы инструментов с соответствующими схемами данных.
    """

    def _register_defaults(self) -> None:
        """Регистрирует дефолтные схемы инструментов."""
        default_schemas = {
            "Фреза": MillingCutter,
            "Сверло": DrillingCutter,
            "Резец": TurningCutter,
            "Развертка": DeploymentCutter,
            "Зенкер": CountersinkingCutter,
            "Протяжка": BroachingCutter,
        }
        
        for group, schema_class in default_schemas.items():
            self.register(group, schema_class)

    def create_schema(self, tool: Tool) -> BaseTool:
        """
        Создает схему инструмента на основе группы инструмента.
        
        Args:
            tool (Tool): Инструмент из БД
            
        Returns:
            BaseTool: Схема инструмента
            
        Raises:
            ValueError: Если группа инструмента не поддерживается
        """
        schema_class = self.create(tool.group)
        if not schema_class:
            raise ValueError(f"Группа '{tool.group}' не поддерживается")
        
        return schema_class(marking=tool.marking, standard=tool.standard)

# Создаем дефолтный экземпляр фабрики
default_tool_schema_factory = ToolSchemaFactory()
