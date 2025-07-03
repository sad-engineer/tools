#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Dict, Optional, TypeVar, Generic

T = TypeVar('T')


class IFactory(Generic[T]):
    """
    Универсальный интерфейс для фабрик.
    
    Определяет базовый контракт для создания и управления объектами.
    """

    def create(self, name: str) -> Optional[T]:
        """
        Создает объект по имени.
        
        Args:
            name (str): Имя объекта
            
        Returns:
            Optional[T]: Экземпляр объекта или None, если не найден
        """
        ...

    def register(self, name: str, item: T) -> None:
        """
        Регистрирует новый объект.
        
        Args:
            name (str): Имя объекта
            item (T): Экземпляр объекта
        """
        ...

    def unregister(self, name: str) -> bool:
        """
        Удаляет объект из регистрации.
        
        Args:
            name (str): Имя объекта
            
        Returns:
            bool: True, если объект был удален, False, если не найден
        """
        ...

    def get_all(self) -> Dict[str, T]:
        """
        Возвращает все зарегистрированные объекты.
        
        Returns:
            Dict[str, T]: Словарь всех объектов
        """
        ...

    def get_names(self) -> list[str]:
        """
        Возвращает список имен всех объектов.
        
        Returns:
            list[str]: Список имен объектов
        """
        ...

    def has(self, name: str) -> bool:
        """
        Проверяет, существует ли объект с указанным именем.
        
        Args:
            name (str): Имя объекта
            
        Returns:
            bool: True, если объект существует
        """
        ...

    def clear(self) -> None:
        """Очищает все зарегистрированные объекты."""
        ...

    def reset_to_defaults(self) -> None:
        """Сбрасывает фабрику к дефолтным объектам."""
        ... 