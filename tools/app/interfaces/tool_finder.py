#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List, Optional, Protocol, Union


class IToolFinder(Protocol):
    """Протокол для поисковика инструментов."""

    def find_by_id(self, tool_id: Union[int, List[int]], limit: Optional[int] = None) -> List[Any]:
        """
        Поиск инструментов по ID.
        
        Args:
            tool_id (Union[int, List[int]]): ID инструмента или список ID
            limit (Optional[int]): Ограничение количества результатов
            
        Returns:
            List[Any]: Список найденных инструментов
        """
        ...

    def find_by_marking(
        self, marking: str, case_sensitive: bool = False, 
        exact_match: bool = True, limit: Optional[int] = None
    ) -> List[Any]:
        """
        Поиск инструментов по обозначению.
        
        Args:
            marking (str): Обозначение инструмента для поиска
            case_sensitive (bool): Учитывать регистр
            exact_match (bool): Точное совпадение
            limit (Optional[int]): Ограничение количества результатов
            
        Returns:
            List[Any]: Список найденных инструментов
        """
        ...

    def find_by_group(self, group: Union[str, List[str]], limit: Optional[int] = None) -> List[Any]:
        """
        Поиск инструментов по группе.
        
        Args:
            group (Union[str, List[str]]): Группа инструмента или список групп
            limit (Optional[int]): Ограничение количества результатов
            
        Returns:
            List[Any]: Список найденных инструментов
        """
        ...

    def find_by_standard(self, standard: Union[str, List[str]], limit: Optional[int] = None) -> List[Any]:
        """
        Поиск инструментов по стандарту.
        
        Args:
            standard (Union[str, List[str]]): Стандарт или список стандартов
            limit (Optional[int]): Ограничение количества результатов
            
        Returns:
            List[Any]: Список найденных инструментов
        """
        ...

    def find_by_marking_and_group(
        self, marking: str, group: Union[str, List[str]], 
        case_sensitive: bool = False, exact_match: bool = True, limit: Optional[int] = None
    ) -> List[Any]:
        """
        Поиск инструментов по обозначению и группе.
        
        Args:
            marking (str): Обозначение инструмента для поиска
            group (Union[str, List[str]]): Группа инструмента или список групп
            case_sensitive (bool): Учитывать регистр
            exact_match (bool): Точное совпадение
            limit (Optional[int]): Ограничение количества результатов
            
        Returns:
            List[Any]: Список найденных инструментов
        """
        ...

    def find_by_group_and_standard(
        self, group: Union[str, List[str]], standard: Union[str, List[str]], 
        limit: Optional[int] = None
    ) -> List[Any]:
        """
        Поиск инструментов по группе и стандарту.
        
        Args:
            group (Union[str, List[str]]): Группа инструмента или список групп
            standard (Union[str, List[str]]): Стандарт или список стандартов
            limit (Optional[int]): Ограничение количества результатов
            
        Returns:
            List[Any]: Список найденных инструментов
        """
        ...

    def find_all(self, limit: Optional[int] = None) -> List[Any]:
        """
        Поиск всех инструментов.
        
        Args:
            limit (Optional[int]): Ограничение количества результатов
            
        Returns:
            List[Any]: Список всех инструментов
        """
        ...
