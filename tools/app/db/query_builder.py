#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, List, Union

from sqlalchemy import and_, or_, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

from tools.app.models.tools import Tool


class QueryBuilder:
    """
    Класс для построения и управления запросами к таблице tools.
    """

    def __init__(self, session: Session):
        self.session = session
        self._query = select(Tool)
        self._filters = []
        self._order_by = []
        self._limit = None
        self._offset = None

    def reset_builder(self) -> "QueryBuilder":
        """Сброс всех фильтров и параметров запроса"""
        self._query = select(Tool)
        self._filters = []
        self._order_by = []
        self._limit = None
        self._offset = None
        return self

    def add_filter(self, filter_condition) -> "QueryBuilder":
        """Добавляет фильтр к запросу

        Args:
            filter_condition: Условие фильтрации (например, Tool.id == 1)

        Returns:
            QueryBuilder: self для цепочки вызовов
        """
        self._filters.append(filter_condition)
        return self

    def add_filters(self, filter_conditions: List) -> "QueryBuilder":
        """Добавляет несколько фильтров к запросу

        Args:
            filter_conditions (List): Список условий фильтрации

        Returns:
            QueryBuilder: self для цепочки вызовов
        """
        self._filters.extend(filter_conditions)
        return self

    def limit(self, limit: int) -> "QueryBuilder":
        """Ограничение количества результатов

        Args:
            limit (int): Максимальное количество результатов
        """
        self._limit = limit
        return self

    def offset(self, offset: int) -> "QueryBuilder":
        """Смещение результатов

        Args:
            offset (int): Количество пропускаемых записей
        """
        self._offset = offset
        return self

    def build(self) -> Select:
        """Построение запроса"""
        # Применяем фильтры
        if self._filters:
            self._query = self._query.where(and_(*self._filters))

        # Применяем сортировку
        if self._order_by:
            self._query = self._query.order_by(*self._order_by)

        # Применяем лимит и смещение
        if self._limit is not None:
            self._query = self._query.limit(self._limit)
        if self._offset is not None:
            self._query = self._query.offset(self._offset)

        return self._query

    def execute(self) -> List[Tool]:
        """Выполнение запроса

        Returns:
            List[Tool]: Список инструментов
        """
        query = self.build()

        # Если нет явной сортировки, сортируем по id
        if not self._order_by:
            query = query.order_by(Tool.id)

        return self.session.execute(query).scalars().all()

    def count(self) -> int:
        """Подсчет количества записей

        Returns:
            int: Количество записей
        """
        query = self.build()
        return self.session.execute(query).scalars().count()

    def first(self) -> Tool:
        """Получение первой записи

        Returns:
            Tool: Первый инструмент или None
        """
        query = self.build()
        return self.session.execute(query).scalars().first()

    def update(self, update_data: Dict[str, Any]) -> int:
        """
        Обновление данных в БД.

        Args:
            update_data (Dict[str, Any]): Словарь с данными для обновления

        Returns:
            int: Количество обновленных записей
        """
        # Создаем запрос на обновление
        stmt = update(Tool)

        # Применяем фильтры
        if self._filters:
            stmt = stmt.where(and_(*self._filters))

        # Применяем данные для обновления
        stmt = stmt.values(**update_data)

        # Выполняем обновление
        result = self.session.execute(stmt)
        self.session.commit()

        return result.rowcount

    def delete(self) -> int:
        """
        Удаление записей из БД.

        Returns:
            int: Количество удаленных записей
        """
        # Получаем записи для удаления
        tools_to_delete = self.execute()
        count = len(tools_to_delete)

        # Удаляем записи
        for tool in tools_to_delete:
            self.session.delete(tool)

        self.session.commit()
        return count

    def get_unique_values(self, column: str) -> List[Any]:
        """Получение уникальных значений колонки

        Args:
            column (str): Название колонки

        Returns:
            List[Any]: Список уникальных значений
        """
        column_obj = getattr(Tool, column, None)
        if column_obj is None:
            return []

        query = select(column_obj).distinct()
        if self._filters:
            query = query.where(and_(*self._filters))

        return self.session.execute(query).scalars().all()

    def debug_query(self) -> str:
        """Отладочный метод для вывода SQL запроса

        Returns:
            str: SQL запрос в виде строки
        """
        query = self.build()
        return str(query.compile(compile_kwargs={"literal_binds": True}))
