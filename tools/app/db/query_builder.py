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

    def filter_by_id(self, tool_id: Union[int, List[int]]) -> "QueryBuilder":
        """Фильтр по ID инструмента

        Args:
            tool_id (Union[int, List[int]]): Одно значение ID или список значений ID
        """
        if isinstance(tool_id, list):
            self._filters.append(Tool.id.in_(tool_id))
        else:
            self._filters.append(Tool.id == tool_id)
        return self

    def filter_by_marking(
        self, marking: str, case_sensitive: bool = False, exact_match: bool = False
    ) -> "QueryBuilder":
        """Фильтр по обозначению инструмента

        Args:
            marking (str): Обозначение инструмента для поиска
            case_sensitive (bool, optional): Учитывать регистр. По умолчанию False
            exact_match (bool, optional): Точное совпадение. По умолчанию False
        """
        if exact_match:
            if case_sensitive:
                self._filters.append(Tool.marking == marking)
            else:
                self._filters.append(Tool.marking.ilike(marking))
        else:
            if case_sensitive:
                self._filters.append(Tool.marking.contains(marking))
            else:
                self._filters.append(Tool.marking.ilike(f"%{marking}%"))
        return self

    def filter_by_group(self, group: Union[str, List[str]], case_sensitive: bool = False) -> "QueryBuilder":
        """Фильтр по группе инструмента

        Args:
            group (Union[str, List[str]]): Одно значение группы или список значений групп
            case_sensitive (bool, optional): Учитывать регистр. По умолчанию False
        """
        if isinstance(group, list):
            if case_sensitive:
                self._filters.append(Tool.group.in_(group))
            else:
                # Для регистронезависимого поиска в списке
                group_filters = [Tool.group.ilike(g) for g in group]
                self._filters.append(or_(*group_filters))
        else:
            if case_sensitive:
                self._filters.append(Tool.group == group)
            else:
                self._filters.append(Tool.group.ilike(group))
        return self

    def filter_by_standard(self, standard: Union[str, List[str]], case_sensitive: bool = False) -> "QueryBuilder":
        """Фильтр по стандарту

        Args:
            standard (Union[str, List[str]]): Одно значение стандарта или список значений стандартов
            case_sensitive (bool, optional): Учитывать регистр. По умолчанию False
        """
        if isinstance(standard, list):
            if case_sensitive:
                self._filters.append(Tool.standard.in_(standard))
            else:
                # Для регистронезависимого поиска в списке
                standard_filters = [Tool.standard.ilike(s) for s in standard]
                self._filters.append(or_(*standard_filters))
        else:
            if case_sensitive:
                self._filters.append(Tool.standard == standard)
            else:
                self._filters.append(Tool.standard.ilike(standard))
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


# Пример использования:
if __name__ == "__main__":
    from tools.app.db.session_manager import get_session

    with get_session() as session:
        try:
            # Создаем построитель запросов
            builder = QueryBuilder(session)

            # Сначала найдем инструмент с обозначением "2100-0001" без фильтра по группе
            print("=== Поиск инструмента с обозначением '2100-0001' ===")
            tools_by_marking = builder.reset_builder().filter_by_marking("2100-0001", exact_match=True).execute()
            print(f"Найдено инструментов по обозначению: {len(tools_by_marking)}")
            for tool in tools_by_marking:
                print(f"ID: {tool.id}, Обозначение: {tool.marking}, Группа: {tool.group}")

            # Теперь проверим комбинированный запрос
            print("\n=== Комбинированный запрос ===")
            tools = (
                builder.reset_builder()
                .filter_by_group(["Резец", "Сверло"])
                .filter_by_marking("2100", exact_match=False)
                .limit(10)
                .execute()
            )
            print(f"Найдено инструментов в комбинированном запросе: {len(tools)}")

            # Выведем SQL запрос для отладки
            print(f"\nSQL запрос:")
            print(
                builder.reset_builder()
                .filter_by_group(["Фреза", "Сверло"])
                .filter_by_marking("2100-0001", exact_match=True)
                .debug_query()
            )

            # Получение уникальных значений
            unique_groups = builder.reset_builder().get_unique_values("group")
            print("\nУникальные группы:", unique_groups)

        except Exception as e:
            print(f"Ошибка: {e}")
            session.rollback()
