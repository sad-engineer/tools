#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List, Protocol


class IFormatter(Protocol):
    """Протокол для форматтера результатов."""

    def format(self, tools: List[Any], mapper_manager=None) -> Any:
        """
        Форматирует результаты поиска.
        
        Args:
            tools (List[Any]): Список инструментов из БД
            mapper_manager: Менеджер мапперов для преобразования данных
            
        Returns:
            Any: Отформатированные результаты
        """
        ...
