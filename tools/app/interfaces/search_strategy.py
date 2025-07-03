#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List, Protocol

from tools.app.interfaces.query_builder import IQueryBuilder


class ISearchStrategy(Protocol):
    """Протокол для стратегии поиска инструментов."""

    def execute(self, builder: IQueryBuilder, **kwargs) -> List[Any]:
        """
        Выполняет поиск с использованием переданного builder.
        
        Args:
            builder (IQueryBuilder): Построитель запросов
            **kwargs: Дополнительные параметры поиска
            
        Returns:
            List[Any]: Результаты поиска
        """
        ...
