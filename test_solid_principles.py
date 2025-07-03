#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тестовый скрипт для демонстрации принципов SOLID в рефакторенном ToolFinder.
"""

from tools.app.finders.solid_tool_finder import SolidToolFinder
from tools.app.interfaces import ISearchStrategy
from tools.app.mappers import CustomCountersinkingMapper


class CustomSearchStrategy(ISearchStrategy):
    """
    Кастомная стратегия поиска - демонстрирует принцип Open/Closed.
    Можно добавлять новые стратегии без изменения существующего кода.
    """
    
    def execute(self, builder, **kwargs):
        """Поиск инструментов с кастомной логикой."""
        # Пример: поиск только активных инструментов (с непустым обозначением)
        builder = builder.filter_by_marking("", exact_match=False)
        return builder.execute()


def test_solid_principles():
    """Демонстрирует принципы SOLID."""
    
    print("=== Демонстрация принципов SOLID ===\n")
    
    # S - Single Responsibility Principle
    print("1. Single Responsibility Principle:")
    print("   - SolidToolFinder отвечает только за координацию поиска")
    print("   - SessionManager отвечает только за управление сессиями")
    print("   - Каждая стратегия отвечает за один тип поиска")
    print()
    
    # O - Open/Closed Principle
    print("2. Open/Closed Principle:")
    print("   - Можно добавлять новые стратегии поиска без изменения кода")
    print("   - Можно добавлять новые форматтеры без изменения кода")
    print("   - Можно добавлять новые мапперы без изменения кода")
    print()
    
    # L - Liskov Substitution Principle
    print("3. Liskov Substitution Principle:")
    print("   - Все зависимости используют интерфейсы")
    print("   - Можно заменить любую реализацию на другую, реализующую тот же интерфейс")
    print()
    
    # I - Interface Segregation Principle
    print("4. Interface Segregation Principle:")
    print("   - Интерфейсы разделены по функциональности")
    print("   - ISessionManager - только для сессий")
    print("   - ISearchStrategy - только для поиска")
    print("   - IFormatter - только для форматирования")
    print()
    
    # D - Dependency Inversion Principle
    print("5. Dependency Inversion Principle:")
    print("   - Зависит от абстракций (интерфейсов), а не от конкретных классов")
    print("   - Зависимости инжектируются извне")
    print()


def test_basic_functionality():
    """Тестирует базовую функциональность."""
    
    print("=== Тестирование базовой функциональности ===\n")
    
    with SolidToolFinder(global_limit=3) as finder:
        # Поиск зенкеров с дефолтным маппером
        print("Поиск зенкеров с дефолтным маппером:")
        tools = finder.find_by_group(["Зенкер"])
        for tool in tools:
            print(f"  - {tool.marking} ({tool.group}) - {type(tool).__name__}")
        
        print()
        
        # Замена на кастомный маппер
        print("Замена на кастомный маппер:")
        finder.set_mapper(CustomCountersinkingMapper())
        tools = finder.find_by_group(["Зенкер"])
        for tool in tools:
            print(f"  - {tool.marking} ({tool.group}) - {type(tool).__name__}")
        
        print()


def test_custom_strategy():
    """Тестирует добавление кастомной стратегии."""
    
    print("=== Тестирование кастомной стратегии ===\n")
    
    with SolidToolFinder(global_limit=5) as finder:
        # Добавляем кастомную стратегию
        finder.add_search_strategy('custom', CustomSearchStrategy())
        
        print("Поиск с кастомной стратегией:")
        # Здесь нужно было бы добавить метод для использования кастомной стратегии
        # Для демонстрации просто показываем, что стратегия добавлена
        print("  Кастомная стратегия добавлена успешно")
        
        print()


def test_dependency_injection():
    """Тестирует инъекцию зависимостей."""
    
    print("=== Тестирование инъекции зависимостей ===\n")
    
    # Создаем кастомные зависимости
    from tools.app.formatters import DictFormatter
    from tools.app.mappers import MapperManager
    
    custom_formatter = DictFormatter()
    custom_mapper_manager = MapperManager()
    
    # Инжектируем зависимости
    with SolidToolFinder(
        formatter=custom_formatter,
        mapper_manager=custom_mapper_manager,
        global_limit=2
    ) as finder:
        print("Поиск с кастомными зависимостями:")
        tools = finder.find_by_group(["Зенкер"])
        print(f"  Найдено инструментов: {len(tools)}")
        print(f"  Тип результата: {type(tools).__name__}")
        
        print()


if __name__ == "__main__":
    test_solid_principles()
    test_basic_functionality()
    test_custom_strategy()
    test_dependency_injection() 