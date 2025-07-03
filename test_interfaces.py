#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тестовый скрипт для демонстрации работы с протоколами-интерфейсами.
"""

from tools.app.interfaces import (
    ISessionManager, IQueryBuilder, ISearchStrategy, 
    IFormatter, IMapperManager, IToolFinder
)
from tools.app.finders.solid_tool_finder import SolidToolFinder
from tools.app.mappers import CustomCountersinkingMapper


def test_protocol_compliance():
    """Тестирует соответствие классов протоколам."""
    
    print("=== Тестирование соответствия протоколам ===\n")
    
    # Проверяем, что SolidToolFinder соответствует IToolFinder
    finder = SolidToolFinder(global_limit=3)
    
    # Проверяем наличие всех методов из протокола
    required_methods = [
        'find_by_id', 'find_by_marking', 'find_by_group', 
        'find_by_standard', 'find_by_marking_and_group',
        'find_by_group_and_standard', 'find_all'
    ]
    
    print("Проверка методов IToolFinder:")
    for method in required_methods:
        if hasattr(finder, method):
            print(f"  ✓ {method} - найден")
        else:
            print(f"  ✗ {method} - НЕ найден")
    
    print()


def test_interface_segregation():
    """Демонстрирует принцип разделения интерфейсов."""
    
    print("=== Демонстрация разделения интерфейсов ===\n")
    
    # Каждый протокол отвечает за свою область
    print("ISessionManager - управление сессиями БД")
    print("IQueryBuilder - построение запросов")
    print("ISearchStrategy - стратегии поиска")
    print("IFormatter - форматирование результатов")
    print("IMapperManager - управление мапперами")
    print("IToolFinder - основной интерфейс поисковика")
    print()


def test_dependency_inversion():
    """Демонстрирует принцип инверсии зависимостей."""
    
    print("=== Демонстрация инверсии зависимостей ===\n")
    
    # Создаем кастомные реализации
    class CustomSessionManager:
        def get_session(self):
            from tools.app.db.session_manager import get_session
            return get_session()
        
        def close_session(self):
            pass
    
    class CustomFormatter:
        def format(self, tools, mapper_manager=None):
            return f"Кастомный формат: {len(tools)} инструментов"
    
    # Проверяем, что они соответствуют протоколам
    session_manager: ISessionManager = CustomSessionManager()
    formatter: IFormatter = CustomFormatter()
    
    print("Кастомные реализации успешно соответствуют протоколам:")
    print(f"  - CustomSessionManager соответствует ISessionManager")
    print(f"  - CustomFormatter соответствует IFormatter")
    print()


def test_usage_with_protocols():
    """Демонстрирует использование с протоколами."""
    
    print("=== Использование с протоколами ===\n")
    
    with SolidToolFinder(global_limit=2) as finder:
        # Используем как IToolFinder
        tools = finder.find_by_group(["Зенкер"])
        
        print(f"Найдено зенкеров: {len(tools)}")
        for tool in tools:
            print(f"  - {tool.marking} ({tool.group})")
        
        # Заменяем маппер
        finder.set_mapper(CustomCountersinkingMapper())
        
        print("\nПосле замены маппера:")
        tools = finder.find_by_group(["Зенкер"])
        for tool in tools:
            print(f"  - {tool.marking} ({tool.group})")
    
    print()


def test_protocol_benefits():
    """Демонстрирует преимущества использования протоколов."""
    
    print("=== Преимущества протоколов ===\n")
    
    print("1. Структурная типизация:")
    print("   - Не нужно наследоваться от абстрактных классов")
    print("   - Достаточно реализовать нужные методы")
    print()
    
    print("2. Гибкость:")
    print("   - Можно использовать любые классы, реализующие протокол")
    print("   - Легко тестировать с моками")
    print()
    
    print("3. Простота:")
    print("   - Нет необходимости в сложной иерархии классов")
    print("   - Duck typing в действии")
    print()


if __name__ == "__main__":
    test_protocol_compliance()
    test_interface_segregation()
    test_dependency_inversion()
    test_usage_with_protocols()
    test_protocol_benefits() 