#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import Any, List, Union

from sqlalchemy import or_

from tools.app.interfaces.query_builder import IQueryBuilder
from tools.app.models.tools import Tool
from tools.app.enumerations import ToolGroups


class SearchStrategy(ABC):
    """Абстрактная стратегия поиска инструментов."""

    @abstractmethod
    def execute(self, builder: IQueryBuilder, **kwargs) -> List[Any]:
        """
        Выполняет поиск с использованием переданного builder.
        
        Args:
            builder (IQueryBuilder): Построитель запросов
            **kwargs: Дополнительные параметры поиска
            
        Returns:
            List[Any]: Результаты поиска
        """
        pass


class SearchByIdStrategy(SearchStrategy):
    """Стратегия поиска по ID."""

    def execute(self, builder: IQueryBuilder, tool_id: Union[int, List[int]], **kwargs) -> List[Any]:
        """
        Выполняет поиск по ID инструмента.
        
        Args:
            builder (IQueryBuilder): Построитель запросов
            tool_id (Union[int, List[int]]): Одно значение ID или список значений ID
            **kwargs: Дополнительные параметры поиска
        """
        if isinstance(tool_id, list):
            builder.add_filter(Tool.id.in_(tool_id))
        else:
            builder.add_filter(Tool.id == tool_id)
        return builder.execute()


class SearchByMarkingStrategy(SearchStrategy):
    """Стратегия поиска по обозначению."""

    def execute(self, builder: IQueryBuilder, marking: str, case_sensitive: bool = False, 
                exact_match: bool = True, **kwargs) -> List[Any]:
        """
        Выполняет поиск по обозначению инструмента.
        
        Args:
            builder (IQueryBuilder): Построитель запросов
            marking (str): Обозначение инструмента для поиска
            case_sensitive (bool, optional): Учитывать регистр. По умолчанию False  
            exact_match (bool, optional): Точное совпадение. По умолчанию True
            **kwargs: Дополнительные параметры поиска
        """
        if exact_match:
            if case_sensitive:
                builder.add_filter(Tool.marking == marking)
            else:
                builder.add_filter(Tool.marking.ilike(marking))
        else:
            if case_sensitive:
                builder.add_filter(Tool.marking.contains(marking))
            else:
                builder.add_filter(Tool.marking.ilike(f"%{marking}%"))
        return builder.execute()


class SearchByGroupStrategy(SearchStrategy):
    """Стратегия поиска по группе."""

    def execute(self, builder: IQueryBuilder, group: Union[ToolGroups, List[ToolGroups]], **kwargs) -> List[Any]:
        """
        Выполняет поиск по группе инструмента.
        
        Args:
            builder (IQueryBuilder): Построитель запросов
            group (Union[ToolGroups, List[ToolGroups]]): Группа инструмента из перечисления ToolGroups
            **kwargs: Дополнительные параметры поиска
        """
        if isinstance(group, list):
            # Для регистронезависимого поиска в списке
            group_filters = [Tool.group.ilike(g) for g in group]
            builder.add_filter(or_(*group_filters))
        else:
            builder.add_filter(Tool.group.ilike(group))
        return builder.execute()


class SearchByStandardStrategy(SearchStrategy):
    """Стратегия поиска по стандарту."""

    def execute(self, builder: IQueryBuilder, standard: Union[str, List[str]], **kwargs) -> List[Any]:
        """
        Выполняет поиск по стандарту инструмента.
        
        Args:
            builder (IQueryBuilder): Построитель запросов
            standard (Union[str, List[str]]): Одно значение стандарта или список значений стандартов
            **kwargs: Дополнительные параметры поиска
        """
        if isinstance(standard, list):
            # Для регистронезависимого поиска в списке
            standard_filters = [Tool.standard.ilike(s) for s in standard]
            builder.add_filter(or_(*standard_filters))
        else:
            builder.add_filter(Tool.standard.ilike(standard))
        return builder.execute()


class SearchByMarkingAndGroupStrategy(SearchStrategy):
    """Стратегия поиска по обозначению и группе."""

    def execute(self, builder: IQueryBuilder, marking: Union[str, List[str]], exact_match: bool = True, **kwargs) -> List[Any]:
        """
        Выполняет поиск по обозначению и группе инструмента.
        
        Args:
            builder (IQueryBuilder): Построитель запросов
            marking (Union[str, List[str]]): Обозначение инструмента для поиска
            exact_match (bool, optional): Точное совпадение. По умолчанию True
            **kwargs: Дополнительные параметры поиска
        """
        # Фильтр по обозначению
        if exact_match:
            if isinstance(marking, list):
                marking_filters = [Tool.marking.ilike(m) for m in marking]
                builder.add_filter(or_(*marking_filters))
            else:
                builder.add_filter(Tool.marking == marking)
        else:
            if isinstance(marking, list):
                marking_filters = [Tool.marking.ilike(m) for m in marking]
                builder.add_filter(or_(*marking_filters))
        return builder.execute()


class SearchByGroupAndStandardStrategy(SearchStrategy):
    """Стратегия поиска по группе и стандарту."""

    def execute(self, builder: IQueryBuilder, group: Union[ToolGroups, List[ToolGroups]], 
                standard: Union[str, List[str]], **kwargs) -> List[Any]:
        """
        Выполняет поиск по группе и стандарту инструмента.
        
        Args:
            builder (IQueryBuilder): Построитель запросов
            group (Union[ToolGroups, List[ToolGroups]]): Группа инструмента из перечисления ToolGroups
            standard (Union[str, List[str]]): Одно значение стандарта или список значений стандартов
            **kwargs: Дополнительные параметры поиска
        """
        # Фильтр по группе
        if isinstance(group, list):
            group_filters = [Tool.group.ilike(g) for g in group]
            builder.add_filter(or_(*group_filters))
        else:
            builder.add_filter(Tool.group.ilike(group))
        
        # Фильтр по стандарту
        if isinstance(standard, list):
            standard_filters = [Tool.standard.ilike(s) for s in standard]
            builder.add_filter(or_(*standard_filters))
        else:
            builder.add_filter(Tool.standard.ilike(standard))
        
        return builder.execute()


class SearchAllStrategy(SearchStrategy):
    """Стратегия поиска всех инструментов."""

    def execute(self, builder: IQueryBuilder, **kwargs) -> List[Any]:
        return builder.execute() 