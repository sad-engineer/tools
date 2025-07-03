#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тестовый скрипт для проверки работы ToolFinder с различными форматтерами и схемами
"""

from tools.app.finders.finder import ToolFinder
from tools.app.formatters import ListFormatter, DictFormatter, IndexedNameFormatter


def test_finder_with_different_formatters():
    """Тестирует ToolFinder с различными форматтерами"""
    
    print("=== Тестирование ToolFinder с различными форматтерами ===\n")
    
    # Тест 1: ListFormatter
    print("1. Тест с ListFormatter:")
    with ToolFinder(limit=3) as finder:
        finder.set_formatter(ListFormatter())
        
        # Поиск всех инструментов
        tools = finder.find_all()
        print(f"Найдено инструментов: {len(tools)}")
        
        for i, tool_schema in enumerate(tools, 1):
            print(f"  {i}. Тип схемы: {type(tool_schema).__name__}")
            print(f"     Обозначение: {tool_schema.marking}")
            print(f"     Группа: {tool_schema.group}")
            print(f"     Стандарт: {tool_schema.standard}")
            
            # Показываем специфичные свойства для разных типов инструментов
            if hasattr(tool_schema, 'type_cutter'):
                print(f"     Тип фрезы: {tool_schema.type_cutter}")
            if hasattr(tool_schema, 'type_of_cutting_part'):
                print(f"     Тип режущей части: {tool_schema.type_of_cutting_part}")
            print()
    
    # Тест 2: DictFormatter
    print("2. Тест с DictFormatter:")
    with ToolFinder(limit=3) as finder:
        finder.set_formatter(DictFormatter())
        
        # Поиск всех инструментов
        tools_dict = finder.find_all()
        print(f"Найдено инструментов: {len(tools_dict)}")
        
        for marking, tool_schema in tools_dict.items():
            print(f"  Обозначение '{marking}':")
            print(f"    Тип схемы: {type(tool_schema).__name__}")
            print(f"    Группа: {tool_schema.group}")
            print(f"    Стандарт: {tool_schema.standard}")
            print()
    
    # Тест 3: IndexedNameFormatter
    print("3. Тест с IndexedNameFormatter:")
    with ToolFinder(limit=3) as finder:
        finder.set_formatter(IndexedNameFormatter())
        
        # Поиск всех инструментов
        indexed_tools = finder.find_all()
        print(f"Найдено инструментов: {len(indexed_tools)}")
        
        for index, tool_schema in indexed_tools.items():
            print(f"  {index}. Тип схемы: {type(tool_schema).__name__}")
            print(f"     Обозначение: {tool_schema.marking}")
            print(f"     Группа: {tool_schema.group}")
            print(f"     Стандарт: {tool_schema.standard}")
            print()
    
    # Тест 4: Поиск по группам
    print("4. Тест поиска по группам:")
    with ToolFinder(limit=2) as finder:
        finder.set_formatter(ListFormatter())
        
        # Поиск фрез
        milling_cutters = finder.find_by_group("Фреза")
        print(f"Найдено фрез: {len(milling_cutters)}")
        for cutter in milling_cutters:
            print(f"  - {cutter.marking} ({type(cutter).__name__})")
        
        # Поиск сверл
        drills = finder.find_by_group("Сверло")
        print(f"Найдено сверл: {len(drills)}")
        for drill in drills:
            print(f"  - {drill.marking} ({type(drill).__name__})")
        
        # Поиск резцов
        cutters = finder.find_by_group("Резец")
        print(f"Найдено резцов: {len(cutters)}")
        for cutter in cutters:
            print(f"  - {cutter.marking} ({type(cutter).__name__})")
    
    # Тест 5: Поиск по обозначению
    print("\n5. Тест поиска по обозначению:")
    with ToolFinder() as finder:
        finder.set_formatter(ListFormatter())
        
        # Поиск по частичному совпадению
        tools = finder.find_by_marking("2100", exact_match=False, limit=3)
        print(f"Найдено инструментов с '2100' в обозначении: {len(tools)}")
        for tool in tools:
            print(f"  - {tool.marking} ({tool.group}) - {type(tool).__name__}")


if __name__ == "__main__":
    test_finder_with_different_formatters() 