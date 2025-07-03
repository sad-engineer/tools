#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, TYPE_CHECKING

from tools.app.interfaces.mapper import IMapper
from tools.app.models.tools import Tool

if TYPE_CHECKING:
    from tools.app.schemas.tool import BaseTool


class BaseMapper(IMapper):
    """
    Универсальный базовый класс для мапперов.
    
    Предоставляет общую реализацию для преобразования данных из БД в схемы инструментов.
    Наследники должны только указать группу инструмента и маппинг полей.
    """

    def __init__(self, tool_group: str, field_mapping: Dict[str, str], geometry_attr: str = None):
        """
        Инициализация маппера.
        
        Args:
            tool_group (str): Группа инструмента, которую обрабатывает этот маппер
            field_mapping (Dict[str, str]): Маппинг полей БД -> поля схемы
            geometry_attr (str, optional): Имя атрибута для получения объекта геометрии
        """
        self.tool_group = tool_group
        self.field_mapping = field_mapping
        self.geometry_attr = geometry_attr

    def can_map(self, tool: Tool) -> bool:
        """
        Проверяет, может ли этот маппер обработать данный инструмент.
        
        Args:
            tool (Tool): Инструмент из БД
            
        Returns:
            bool: True если маппер может обработать этот инструмент
        """
        return tool.group == self.tool_group

    def map_to_schema(self, tool: Tool, schema: 'BaseTool') -> None:
        """
        Маппит геометрические данные из БД в схему инструмента.
        
        Args:
            tool (Tool): Инструмент из БД с загруженными геометрическими данными
            schema (BaseTool): Схема инструмента для заполнения данными
        """
        geometry_obj = self.get_geometry_object(tool)
        if not geometry_obj:
            return

        # Маппим поля из объекта геометрии в схему
        for db_field, schema_field in self.field_mapping.items():
            if hasattr(geometry_obj, db_field) and hasattr(schema, schema_field):
                value = getattr(geometry_obj, db_field)
                if value is not None:
                    setattr(schema, schema_field, value)

    def get_geometry_object(self, tool: Tool) -> Any:
        """
        Получает объект геометрии из связанной таблицы.
        
        Args:
            tool (Tool): Инструмент из БД
            
        Returns:
            Any: Объект геометрии или None если не найден
        """
        if self.geometry_attr and hasattr(tool, self.geometry_attr):
            return getattr(tool, self.geometry_attr)
        return None

    def get_tool_type(self) -> str:
        """
        Возвращает тип инструмента, который обрабатывает этот маппер.
        
        Returns:
            str: Тип инструмента
        """
        return self.tool_group
