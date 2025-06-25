#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List, Optional, Union

from sqlalchemy.orm import Session

from tools.app.db.query_builder import QueryBuilder
from tools.app.db.session_manager import get_session
from tools.app.formatters import (
    DictFormatter,
    IndexedNameFormatter,
    ListFormatter,
    ToolFormatter,
)


class ToolFinder:
    """
    Класс для поиска инструментов по различным критериям.
    """

    def __init__(
        self,
        session: Optional[Session] = None,
        limit: Optional[int] = None,
        formatter: Optional[ToolFormatter] = None,
    ):
        """
        Инициализация поисковика.

        Args:
            session (Session, optional): Сессия БД. Если не указана, будет создана новая.
            limit (int, optional): Глобальный лимит для всех запросов
            formatter (ToolFormatter, optional): Форматтер для результатов. По умолчанию ListFormatter
        """
        self.session: Session = session or get_session()
        self._builder: QueryBuilder = QueryBuilder(self.session)
        self._global_limit: int = limit
        self._formatter: ToolFormatter = formatter or ListFormatter()

        if self._global_limit:
            self._builder.limit(self._global_limit)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    def set_limit(self, limit: Optional[int]) -> "ToolFinder":
        """
        Устанавливает глобальный лимит для всех запросов.

        Args:
            limit (int, optional): Новое значение лимита. None для отключения лимита.

        Returns:
            ToolFinder: self для цепочки вызовов
        """
        self._global_limit = limit
        return self

    def get_limit(self) -> Optional[int]:
        """
        Возвращает текущее значение глобального лимита.

        Returns:
            Optional[int]: Текущее значение лимита
        """
        return self._global_limit

    def _apply_limit(self, limit: Optional[int] = None) -> "ToolFinder":
        """
        Применяет лимит к запросу.

        Args:
            limit (int, optional): Локальный лимит для текущего запроса

        Returns:
            ToolFinder: self для цепочки вызовов
        """
        # Используем локальный лимит, если он указан, иначе глобальный
        actual_limit = limit if limit is not None else self._global_limit
        if actual_limit is not None:
            self._builder.limit(actual_limit)
        return self

    def set_formatter(self, formatter: ToolFormatter) -> "ToolFinder":
        """
        Устанавливает форматтер для результатов запросов.

        Args:
            formatter (ToolFormatter): Экземпляр форматтера

        Returns:
            ToolFinder: self для цепочки вызовов
        """
        self._formatter = formatter
        return self

    def find_by_id(self, tool_id: Union[int, List[int]], limit: int = None) -> List[Any]:
        """Получение инструментов по ID

        Args:
            tool_id (Union[int, List[int]]): ID инструмента или список ID
            limit (int, optional): Ограничение количества результатов
        """
        builder = self._builder.filter_by_id(tool_id)

        if limit:
            builder = builder.limit(limit)

        tools = builder.execute()
        self.reset_builder()
        return self._formatter.format(tools)

    def find_by_marking(
        self, marking: str, case_sensitive: bool = False, exact_match: bool = True, limit: int = None
    ) -> List[Any]:
        """Поиск инструментов по обозначению

        Args:
            marking (str): Обозначение инструмента для поиска
            case_sensitive (bool, optional): Учитывать регистр. По умолчанию False
            exact_match (bool, optional): Точное совпадение. По умолчанию True
            limit (int, optional): Ограничение количества результатов
        """
        builder = self._builder.filter_by_marking(
            marking=marking, case_sensitive=case_sensitive, exact_match=exact_match
        )

        if limit:
            builder = builder.limit(limit)

        tools = builder.execute()
        self.reset_builder()
        return self._formatter.format(tools)

    def find_by_group(self, group: Union[str, List[str]], limit: int = None) -> List[Any]:
        """Получение инструментов по группе

        Args:
            group (Union[str, List[str]]): Группа инструмента или список групп
            limit (int, optional): Ограничение количества результатов
        """
        builder = self._builder.filter_by_group(group)

        if limit:
            builder = builder.limit(limit)

        tools = builder.execute()
        self.reset_builder()
        return self._formatter.format(tools)

    def find_by_standard(self, standard: Union[str, List[str]], limit: int = None) -> List[Any]:
        """Получение инструментов по стандарту

        Args:
            standard (Union[str, List[str]]): Стандарт или список стандартов
            limit (int, optional): Ограничение количества результатов
        """
        builder = self._builder.filter_by_standard(standard)

        if limit:
            builder = builder.limit(limit)

        tools = builder.execute()
        self.reset_builder()
        return self._formatter.format(tools)

    def find_by_marking_and_group(
        self,
        marking: str,
        group: Union[str, List[str]],
        case_sensitive: bool = False,
        exact_match: bool = True,
        limit: int = None,
    ) -> List[Any]:
        """Поиск инструментов по обозначению и группе

        Args:
            marking (str): Обозначение инструмента для поиска
            group (Union[str, List[str]]): Группа инструмента или список групп
            case_sensitive (bool, optional): Учитывать регистр. По умолчанию False
            exact_match (bool, optional): Точное совпадение. По умолчанию True
            limit (int, optional): Ограничение количества результатов
        """
        builder = self._builder.filter_by_marking(
            marking=marking, case_sensitive=case_sensitive, exact_match=exact_match
        ).filter_by_group(group)

        if limit:
            builder = builder.limit(limit)

        tools = builder.execute()
        self.reset_builder()
        return self._formatter.format(tools)

    def find_by_group_and_standard(
        self, group: Union[str, List[str]], standard: Union[str, List[str]], limit: int = None
    ) -> List[Any]:
        """Поиск инструментов по группе и стандарту"""
        builder = self._builder.filter_by_group(group).filter_by_standard(standard)

        if limit:
            builder = builder.limit(limit)

        tools = builder.execute()
        self.reset_builder()
        return self._formatter.format(tools)

    def find_all(self, limit: int = None) -> List[Any]:
        """Получение всех инструментов

        Args:
            limit (int, optional): Ограничение количества результатов
        """
        builder = self._builder

        if limit:
            builder = builder.limit(limit)

        tools = builder.execute()
        self.reset_builder()
        return self._formatter.format(tools)

    def reset_builder(self):
        """Сброс всех параметров поиска"""
        self._builder = QueryBuilder(self.session)
        if self._global_limit:
            self._builder.limit(self._global_limit)


# Пример использования:
if __name__ == "__main__":
    # Использование как контекстный менеджер
    with ToolFinder(limit=5) as finder:  # Устанавливаем глобальный лимит
        # Получение инструментов в виде списка схем (по умолчанию)
        tools_by_group = finder.find_by_group(["Фреза", "Сверло"])
        print("Инструменты группы Фреза и Сверло:")
        for tool_schema in tools_by_group:
            print(f"- {tool_schema.marking} ({tool_schema.group}) - {type(tool_schema).__name__}")

        # Переключение на словарь схем
        finder.set_formatter(DictFormatter())
        tools_by_marking = finder.find_by_marking("2100", exact_match=False)
        print("\nИнструменты с обозначением содержащим '2100' (словарь схем):")
        for marking, tool_schema in tools_by_marking.items():
            print(
                f"- {marking}: группа={tool_schema.group}, стандарт={tool_schema.standard}, тип={type(tool_schema).__name__}"
            )

        # Возврат к списку схем
        finder.set_formatter(ListFormatter())
        all_tools = finder.find_all()
        print(f"\nВсе инструменты (список схем): {len(all_tools)} записей")

        # Поиск по конкретному обозначению
        tools = finder.find_by_marking("2100-0001", exact_match=True)
        if tools:
            tool_schema = tools[0]
            print(f"\nНайден инструмент:")
            print(f"Тип схемы: {type(tool_schema).__name__}")
            print(f"Обозначение: {tool_schema.marking}")
            print(f"Группа: {tool_schema.group}")
            print(f"Стандарт: {tool_schema.standard}")
        else:
            print("Инструмент не найден")

        # Поиск по нескольким группам
        tools_by_groups = finder.find_by_group(["Резец", "Развертка", "Зенкер"])
        print(f"\nПоиск по нескольким группам: {len(tools_by_groups)} инструментов")
        for tool_schema in tools_by_groups:
            print(f"- {tool_schema.marking} ({tool_schema.group}) - {type(tool_schema).__name__}")

    # Пример с индексированным форматтером
    with ToolFinder() as finder:
        finder.set_formatter(IndexedNameFormatter())

        # получение информации о инструментах с индексами
        indexed_tools = finder.find_all(limit=10)
        print(f"\nПервые 10 инструментов с индексами:")
        for index, tool_schema in indexed_tools.items():
            print(f"{index}. {tool_schema.marking} ({tool_schema.group}) - {type(tool_schema).__name__}")

        # получение информации о конкретном инструменте
        tools = finder.find_by_marking("2100", exact_match=False)
        if len(tools) == 1:
            tool_schema = tools[0]
            if tool_schema:
                print(f"\nИнструмент: {tool_schema.marking}")
                print(f"Тип схемы: {type(tool_schema).__name__}")
                print(f"Группа: {tool_schema.group}")
                print(f"Стандарт: {tool_schema.standard}")
            else:
                print("Инструмент не найден")

        # Поиск по группе и обозначению
        tools = finder.find_by_marking_and_group("2100", ["Фреза", "Сверло"], exact_match=False)
        print(f"\nИнструменты с '2100' в обозначении из групп Фреза/Сверло:")
        for index, tool_schema in tools.items():
            print(f"{index}. {tool_schema.marking} ({tool_schema.group}) - {type(tool_schema).__name__}")

    # Пример демонстрации работы с конкретными схемами
    with ToolFinder() as finder:
        finder.set_formatter(ListFormatter())

        # Поиск фрез
        milling_cutters = finder.find_by_group("Фреза", limit=3)
        print(f"\n=== Демонстрация работы с фрезами ===")
        for cutter in milling_cutters:
            print(f"Тип схемы: {type(cutter).__name__}")
            print(f"Обозначение: {cutter.marking}")
            print(f"Группа: {cutter.group}")
            # Если это фреза, показываем специфичные свойства
            if hasattr(cutter, 'type_cutter'):
                print(f"Тип фрезы: {cutter.type_cutter}")
            print("---")

        # Поиск сверл
        drilling_tools = finder.find_by_group("Сверло", limit=3)
        print(f"\n=== Демонстрация работы со сверлами ===")
        for drill in drilling_tools:
            print(f"Тип схемы: {type(drill).__name__}")
            print(f"Обозначение: {drill.marking}")
            print(f"Группа: {drill.group}")
            print("---")
