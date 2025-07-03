#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.mappers.countersinking_mapper import CountersinkingMapper
from tools.app.models.tools import Tool
from tools.app.schemas.tool import BaseTool


class CustomCountersinkingMapper(CountersinkingMapper):
    """
    Кастомный маппер для зенкеров с дополнительной функциональностью.
    
    Расширяет базовый CountersinkingMapper дополнительными полями
    и кастомной логикой маппинга.
    """

    def map_to_schema(self, tool: Tool, schema: BaseTool) -> None:
        """
        Маппит геометрические данные зенкера из БД в схему с дополнительной логикой.
        
        Args:
            tool (Tool): Инструмент из БД с загруженными геометрическими данными
            schema (BaseTool): Схема зенкера для заполнения данными
        """
        # Сначала вызываем базовый маппинг
        super().map_to_schema(tool, schema)
        
        # Добавляем кастомную логику
        geometry_obj = self.get_geometry_object(tool)
        
        if not geometry_obj:
            return
        
        # Кастомные вычисления и маппинг
        self._map_custom_fields(geometry_obj, schema)
        self._apply_custom_business_logic(geometry_obj, schema)

    def _map_custom_fields(self, geometry_obj, schema: BaseTool) -> None:
        """
        Маппит дополнительные поля, специфичные для кастомного маппера.
        
        Args:
            geometry_obj: Объект геометрии из БД
            schema (BaseTool): Схема для заполнения
        """
        # Пример: маппинг исполнения в дополнительные поля
        if hasattr(geometry_obj, 'execution') and geometry_obj.execution:
            # Можно добавить логику для обработки исполнения
            pass
        
        # Пример: маппинг конуса Морзе
        if hasattr(geometry_obj, 'morse_taper') and geometry_obj.morse_taper:
            # Можно добавить логику для обработки конуса Морзе
            pass
        
        # Пример: маппинг типа отверстия
        if hasattr(geometry_obj, 'hole_type') and geometry_obj.hole_type:
            # Можно добавить логику для обработки типа отверстия
            pass

    def _apply_custom_business_logic(self, geometry_obj, schema: BaseTool) -> None:
        """
        Применяет кастомную бизнес-логику к данным.
        
        Args:
            geometry_obj: Объект геометрии из БД
            schema (BaseTool): Схема для заполнения
        """
        # Пример: валидация и коррекция данных
        if hasattr(schema, 'dia_mm') and schema.dia_mm:
            # Проверяем, что диаметр в допустимых пределах
            if schema.dia_mm < 1.0:
                print(f"Предупреждение: Диаметр зенкера {schema.marking} слишком мал: {schema.dia_mm} мм")
        
        # Пример: вычисление дополнительных параметров
        if hasattr(schema, 'dia_mm') and hasattr(schema, 'length_mm'):
            if schema.dia_mm and schema.length_mm:
                # Вычисляем соотношение длины к диаметру
                ratio = schema.length_mm / schema.dia_mm
                if ratio > 10:
                    print(f"Информация: Зенкер {schema.marking} имеет высокое соотношение L/D: {ratio:.2f}")

    def get_tool_type(self) -> str:
        """
        Возвращает тип инструмента, который обрабатывает этот маппер.
        
        Returns:
            str: Тип инструмента ("Зенкер")
        """
        return "Зенкер" 