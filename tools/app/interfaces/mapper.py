#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Protocol, TYPE_CHECKING

from tools.app.models.tools import Tool

if TYPE_CHECKING:
    from tools.app.schemas.tool import BaseTool


class IMapper(Protocol):
    """
    Интерфейс для мапперов.
    
    Определяет базовый контракт для преобразования данных из БД в схемы инструментов.
    """

    def can_map(self, tool: Tool) -> bool:
        """
        Проверяет, может ли этот маппер обработать данный инструмент.
        
        Args:
            tool (Tool): Инструмент из БД
            
        Returns:
            bool: True если маппер может обработать этот инструмент
        """
        ...

    def map_to_schema(self, tool: Tool, schema: 'BaseTool') -> None:
        """
        Маппит геометрические данные из БД в схему инструмента.
        
        Args:
            tool (Tool): Инструмент из БД с загруженными геометрическими данными
            schema (BaseTool): Схема инструмента для заполнения данными
        """
        ...

    def get_geometry_object(self, tool: Tool) -> Any:
        """
        Получает объект геометрии из связанной таблицы.
        
        Args:
            tool (Tool): Инструмент из БД
            
        Returns:
            Any: Объект геометрии или None если не найден
        """
        ...

    def get_tool_type(self) -> str:
        """
        Возвращает тип инструмента, который обрабатывает этот маппер.
        
        Returns:
            str: Тип инструмента (например, "Зенкер", "Фреза", etc.)
        """
        ... 