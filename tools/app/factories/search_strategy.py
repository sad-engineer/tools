#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.interfaces.search_strategy import ISearchStrategy
from tools.app.search_strategy import (
    SearchByIdStrategy, SearchByMarkingStrategy, SearchByGroupStrategy,
    SearchByStandardStrategy, SearchByMarkingAndGroupStrategy,
    SearchByGroupAndStandardStrategy, SearchAllStrategy
)
from tools.app.factories.base import BaseFactory


class SearchStrategyFactory(BaseFactory[ISearchStrategy]):
    """
    Фабрика для создания стратегий поиска.
    
    Создает и управляет экземплярами стратегий поиска.
    Поддерживает регистрацию новых стратегий.
    """

    def _register_defaults(self) -> None:
        """Регистрирует дефолтные стратегии поиска."""
        default_strategies = {
            'by_id': SearchByIdStrategy(),
            'by_marking': SearchByMarkingStrategy(),
            'by_group': SearchByGroupStrategy(),
            'by_standard': SearchByStandardStrategy(),
            'by_marking_and_group': SearchByMarkingAndGroupStrategy(),
            'by_group_and_standard': SearchByGroupAndStandardStrategy(),
            'all': SearchAllStrategy(),
        }
        
        for name, strategy in default_strategies.items():
            self.register(name, strategy)


# Создаем дефолтный экземпляр фабрики
default_strategy_factory = SearchStrategyFactory()
