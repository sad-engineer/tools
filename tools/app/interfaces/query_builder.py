#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, List, Union, Protocol

from sqlalchemy.sql.selectable import Select


class IQueryBuilder(Protocol):
    """
    Протокол для построителя запросов.
    
    Определяет интерфейс для построения и выполнения запросов к БД.
    Соответствует интерфейсу QueryBuilder.
    """

    def reset_builder(self) -> "IQueryBuilder":
        """
        Сброс всех фильтров и параметров запроса.
        
        Returns:
            IQueryBuilder: self для цепочки вызовов
        """
        ...

    def add_filter(self, filter_condition) -> "IQueryBuilder":
        """
        Добавляет фильтр к запросу.
        
        Args:
            filter_condition: Условие фильтрации (например, Tool.id == 1)
            
        Returns:
            IQueryBuilder: self для цепочки вызовов
        """
        ...

    def add_filters(self, filter_conditions: List) -> "IQueryBuilder":
        """
        Добавляет несколько фильтров к запросу.
        
        Args:
            filter_conditions (List): Список условий фильтрации
            
        Returns:
            IQueryBuilder: self для цепочки вызовов
        """
        ...

    def limit(self, limit: int) -> "IQueryBuilder":
        """
        Ограничение количества результатов.
        
        Args:
            limit (int): Максимальное количество результатов
            
        Returns:
            IQueryBuilder: self для цепочки вызовов
        """
        ...

    def offset(self, offset: int) -> "IQueryBuilder":
        """
        Смещение результатов.
        
        Args:
            offset (int): Количество пропускаемых записей
            
        Returns:
            IQueryBuilder: self для цепочки вызовов
        """
        ...

    def build(self) -> Select:
        """
        Построение запроса.
        
        Returns:
            Select: SQLAlchemy Select объект
        """
        ...

    def execute(self) -> List[Any]:
        """
        Выполнение запроса.
        
        Returns:
            List[Any]: Список инструментов
        """
        ...

    def count(self) -> int:
        """
        Подсчет количества записей.
        
        Returns:
            int: Количество записей
        """
        ...

    def first(self) -> Any:
        """
        Получение первой записи.
        
        Returns:
            Any: Первый инструмент или None
        """
        ...

    def update(self, update_data: Dict[str, Any]) -> int:
        """
        Обновление данных в БД.
        
        Args:
            update_data (Dict[str, Any]): Словарь с данными для обновления
            
        Returns:
            int: Количество обновленных записей
        """
        ...

    def delete(self) -> int:
        """
        Удаление записей из БД.
        
        Returns:
            int: Количество удаленных записей
        """
        ...

    def get_unique_values(self, column: str) -> List[Any]:
        """
        Получение уникальных значений колонки.
        
        Args:
            column (str): Название колонки
            
        Returns:
            List[Any]: Список уникальных значений
        """
        ...

    def debug_query(self) -> str:
        """
        Отладочный метод для вывода SQL запроса.
        
        Returns:
            str: SQL запрос в виде строки
        """
        ...
