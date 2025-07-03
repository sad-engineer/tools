#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тестовый скрипт для проверки маппинга геометрических данных из БД в схемы
"""

from tools.app.finders.finder import ToolFinder
from tools.app.formatters import ListFormatter
from tools.app.factories.tool_schema import ToolSchemaFactory


def test_geometry_mapping():
    """Тестирует маппинг геометрических данных из БД в схемы"""
    
    print("=== Тестирование маппинга геометрических данных ===\n")
    
    with ToolFinder(limit=5) as finder:
        finder.set_formatter(ListFormatter())
        
        # Поиск всех инструментов
        tools = finder.find_all()
        print(f"Найдено инструментов: {len(tools)}")
        
        for i, tool_schema in enumerate(tools, 1):
            print(f"\n{i}. Инструмент: {tool_schema.marking}")
            print(f"   Тип схемы: {type(tool_schema).__name__}")
            print(f"   Группа: {tool_schema.group}")
            print(f"   Стандарт: {tool_schema.standard}")
            
            # Показываем геометрические параметры
            if hasattr(tool_schema, 'dia_mm') and tool_schema.dia_mm is not None:
                print(f"   Диаметр: {tool_schema.dia_mm} мм")
            if hasattr(tool_schema, 'length_mm') and tool_schema.length_mm is not None:
                print(f"   Длина: {tool_schema.length_mm} мм")
            if hasattr(tool_schema, 'num_of_cutting_blades') and tool_schema.num_of_cutting_blades is not None:
                print(f"   Количество режущих граней: {tool_schema.num_of_cutting_blades}")
            if hasattr(tool_schema, 'main_angle_grad') and tool_schema.main_angle_grad is not None:
                print(f"   Главный угол: {tool_schema.main_angle_grad}°")
            
            # Специфичные параметры для разных типов инструментов
            if hasattr(tool_schema, 'type_cutter') and tool_schema.type_cutter is not None:
                print(f"   Тип фрезы: {tool_schema.type_cutter}")
            if hasattr(tool_schema, 'type_of_cutting_part') and tool_schema.type_of_cutting_part is not None:
                print(f"   Тип режущей части: {tool_schema.type_of_cutting_part}")
            if hasattr(tool_schema, 'large_tooth') and tool_schema.large_tooth is not None:
                print(f"   Крупность зуба: {tool_schema.large_tooth}")
            if hasattr(tool_schema, 'accuracy_class') and tool_schema.accuracy_class is not None:
                print(f"   Класс точности: {tool_schema.accuracy_class}")


def test_specific_groups():
    """Тестирует поиск по конкретным группам инструментов"""
    
    print("\n=== Тестирование поиска по группам ===\n")
    
    with ToolFinder(limit=3) as finder:
        finder.set_formatter(ListFormatter())
        
        # Тестируем зенкеры
        print("Зенкеры:")
        countersinks = finder.find_by_group("Зенкер")
        for tool in countersinks:
            print(f"  - {tool.marking}: D={tool.dia_mm}мм, L={tool.length_mm}мм, z={tool.num_of_cutting_blades}")
        
        # Тестируем фрезы
        print("\nФрезы:")
        cutters = finder.find_by_group("Фреза")
        for tool in cutters:
            print(f"  - {tool.marking}: D={tool.dia_mm}мм, L={tool.length_mm}мм, z={tool.num_of_cutting_blades}")
        
        # Тестируем сверла
        print("\nСверла:")
        drills = finder.find_by_group("Сверло")
        for tool in drills:
            print(f"  - {tool.marking}: D={tool.dia_mm}мм, L={tool.length_mm}мм, z={tool.num_of_cutting_blades}")
        
        # Тестируем резцы
        print("\nРезцы:")
        turning_tools = finder.find_by_group("Резец")
        for tool in turning_tools:
            print(f"  - {tool.marking}: D={tool.dia_mm}мм, L={tool.length_mm}мм")


def test_factory_directly():
    """Тестирует фабрику схем напрямую"""
    
    print("\n=== Тестирование фабрики схем ===\n")
    
    from tools.app.db.session_manager import get_session
    from tools.app.models.tools import Tool
    
    with get_session() as session:
        # Получаем несколько инструментов разных типов
        tools = session.query(Tool).limit(3).all()
        
        for tool in tools:
            print(f"Инструмент из БД: {tool.marking} ({tool.group})")
            
            try:
                # Создаем схему через фабрику
                schema = ToolSchemaFactory.create_schema(tool)
                print(f"  Создана схема: {type(schema).__name__}")
                print(f"  Обозначение: {schema.marking}")
                print(f"  Группа: {schema.group}")
                
                # Показываем геометрические параметры
                if hasattr(schema, 'dia_mm') and schema.dia_mm is not None:
                    print(f"  Диаметр: {schema.dia_mm} мм")
                if hasattr(schema, 'length_mm') and schema.length_mm is not None:
                    print(f"  Длина: {schema.length_mm} мм")
                if hasattr(schema, 'num_of_cutting_blades') and schema.num_of_cutting_blades is not None:
                    print(f"  Количество режущих граней: {schema.num_of_cutting_blades}")
                
            except ValueError as e:
                print(f"  Ошибка создания схемы: {e}")
            
            print()


if __name__ == "__main__":
    test_geometry_mapping()
    test_specific_groups()
    test_factory_directly() 