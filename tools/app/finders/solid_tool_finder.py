#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List, Optional, Union

from sqlalchemy.orm import Session

from tools.app.db.query_builder import QueryBuilder
from tools.app.db.session_manager import SessionManager
from tools.app.formatters import ListFormatter, ToolFormatter
from tools.app.mappers import MapperManager
from tools.app.interfaces import (
    ISessionManager, IQueryBuilder, ISearchStrategy, IFormatter, IMapperManager, IToolFinder
)
from tools.app.factories import default_strategy_factory


# Удаляем старую реализацию SessionManager, так как теперь используем адаптер


# Удаляем адаптер, так как теперь используем QueryBuilder напрямую


class SolidToolFinder(IToolFinder):
    """
    Рефакторенная версия ToolFinder, соответствующая принципам SOLID.
    
    S - Single Responsibility: Каждый класс имеет одну ответственность
    O - Open/Closed: Новые стратегии поиска можно добавлять без изменения кода
    L - Liskov Substitution: Все зависимости используют интерфейсы
    I - Interface Segregation: Интерфейсы разделены по функциональности
    D - Dependency Inversion: Зависит от абстракций, а не от конкретных классов
    """

    def __init__(
        self,
        session_manager: Optional[ISessionManager] = None,
        formatter: Optional[IFormatter] = None,
        mapper_manager: Optional[IMapperManager] = None,
        global_limit: Optional[int] = None,
        strategy_factory=None,
    ):
        """
        Инициализация поисковика.

        Args:
            session_manager (ISessionManager, optional): Менеджер сессий
            formatter (IFormatter, optional): Форматтер результатов
            mapper_manager (IMapperManager, optional): Менеджер мапперов
            global_limit (int, optional): Глобальный лимит результатов
            strategy_factory: Фабрика стратегий (по умолчанию используется default_strategy_factory)
        """
        self._session_manager = session_manager or SessionManager()
        self._formatter = formatter or ListFormatter()
        self._mapper_manager = mapper_manager or MapperManager()
        self._global_limit = global_limit
        self._strategy_factory = strategy_factory or default_strategy_factory
        
        # Инициализация стратегий поиска
        self._strategies = self._strategy_factory.get_all()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session_manager.close_session()

    def find_by_id(self, tool_id: Union[int, List[int]], limit: Optional[int] = None) -> List[Any]:
        """Поиск инструментов по ID."""
        return self._execute_search(
            strategy=self._strategies['by_id'],
            tool_id=tool_id,
            limit=limit
        )

    def find_by_marking(
        self, marking: str, case_sensitive: bool = False, 
        exact_match: bool = True, limit: Optional[int] = None
    ) -> List[Any]:
        """Поиск инструментов по обозначению."""
        return self._execute_search(
            strategy=self._strategies['by_marking'],
            marking=marking,
            case_sensitive=case_sensitive,
            exact_match=exact_match,
            limit=limit
        )

    def find_by_group(self, group: Union[str, List[str]], limit: Optional[int] = None) -> List[Any]:
        """Поиск инструментов по группе."""
        return self._execute_search(
            strategy=self._strategies['by_group'],
            group=group,
            limit=limit
        )

    def find_by_standard(self, standard: Union[str, List[str]], limit: Optional[int] = None) -> List[Any]:
        """Поиск инструментов по стандарту."""
        return self._execute_search(
            strategy=self._strategies['by_standard'],
            standard=standard,
            limit=limit
        )

    def find_by_marking_and_group(
        self, marking: str, group: Union[str, List[str]], 
        case_sensitive: bool = False, exact_match: bool = True, limit: Optional[int] = None
    ) -> List[Any]:
        """Поиск инструментов по обозначению и группе."""
        return self._execute_search(
            strategy=self._strategies['by_marking_and_group'],
            marking=marking,
            group=group,
            case_sensitive=case_sensitive,
            exact_match=exact_match,
            limit=limit
        )

    def find_by_group_and_standard(
        self, group: Union[str, List[str]], standard: Union[str, List[str]], limit: Optional[int] = None
    ) -> List[Any]:
        """Поиск инструментов по группе и стандарту."""
        return self._execute_search(
            strategy=self._strategies['by_group_and_standard'],
            group=group,
            standard=standard,
            limit=limit
        )

    def find_all(self, limit: Optional[int] = None) -> List[Any]:
        """Поиск всех инструментов."""
        return self._execute_search(
            strategy=self._strategies['all'],
            limit=limit
        )

    def _execute_search(self, strategy: ISearchStrategy, limit: Optional[int] = None, **kwargs) -> List[Any]:
        """
        Выполняет поиск с использованием стратегии.
        
        Args:
            strategy (ISearchStrategy): Стратегия поиска
            limit (Optional[int]): Локальный лимит
            **kwargs: Дополнительные параметры поиска
            
        Returns:
            List[Any]: Результаты поиска
        """
        # Создаем QueryBuilder напрямую
        query_builder = QueryBuilder(self._session_manager.get_session())
        
        # Применяем лимит
        actual_limit = limit if limit is not None else self._global_limit
        if actual_limit is not None:
            query_builder.limit(actual_limit)
        
        # Выполняем поиск
        tools = strategy.execute(query_builder, **kwargs)
        
        # Сбрасываем состояние
        query_builder.reset_builder()
        
        # Форматируем результаты
        return self._formatter.format(tools, self._mapper_manager)

    # Методы для управления зависимостями (для обратной совместимости)
    def set_formatter(self, formatter: IFormatter) -> "SolidToolFinder":
        """Устанавливает форматтер."""
        self._formatter = formatter
        return self

    def set_mapper_manager(self, mapper_manager: IMapperManager) -> "SolidToolFinder":
        """Устанавливает менеджер мапперов."""
        self._mapper_manager = mapper_manager
        return self

    def register_mapper(self, mapper) -> "SolidToolFinder":
        """Регистрирует маппер."""
        self._mapper_manager.register_mapper(mapper)
        return self

    def set_mapper(self, mapper) -> "SolidToolFinder":
        """Заменяет маппер."""
        old_mapper = self._mapper_manager.get_mapper_for_tool_type(mapper.get_tool_type())
        if old_mapper:
            self._mapper_manager.unregister_mapper(old_mapper)
        self._mapper_manager.register_mapper(mapper)
        return self

    def add_search_strategy(self, name: str, strategy: ISearchStrategy) -> "SolidToolFinder":
        """Добавляет новую стратегию поиска."""
        self._strategy_factory.register(name, strategy)
        self._strategies = self._strategy_factory.get_all()
        return self

    def remove_search_strategy(self, name: str) -> "SolidToolFinder":
        """Удаляет стратегию поиска."""
        self._strategy_factory.unregister(name)
        self._strategies = self._strategy_factory.get_all()
        return self

    def get_strategy_names(self) -> list[str]:
        """Возвращает список имен доступных стратегий."""
        return self._strategy_factory.get_names() 