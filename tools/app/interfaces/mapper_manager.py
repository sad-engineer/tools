#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Protocol


class IMapperManager(Protocol):
    """Протокол для менеджера мапперов."""

    def map_tool_to_schema(self, tool: Any, schema: Any) -> bool:
        """
        Маппит инструмент в схему.
        
        Args:
            tool (Any): Инструмент из БД
            schema (Any): Схема для заполнения
            
        Returns:
            bool: True если маппинг выполнен успешно
        """
        ...

    def register_mapper(self, mapper: Any) -> None:
        """
        Регистрирует маппер.
        
        Args:
            mapper (Any): Маппер для регистрации
        """
        ...

    def unregister_mapper(self, mapper: Any) -> None:
        """
        Удаляет маппер.
        
        Args:
            mapper (Any): Маппер для удаления
        """
        ...

    def get_mapper_for_tool_type(self, tool_type: str) -> Any:
        """
        Получает маппер по типу инструмента.
        
        Args:
            tool_type (str): Тип инструмента
            
        Returns:
            Any: Маппер для данного типа или None
        """
        ... 