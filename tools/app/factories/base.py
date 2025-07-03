#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import Dict, Optional, TypeVar, Generic

from tools.app.interfaces.factory import IFactory

T = TypeVar('T')


class BaseFactory(IFactory[T], ABC, Generic[T]):
    """
    Базовый класс для фабрик.
    
    Предоставляет общую реализацию для управления объектами.
    """

    def __init__(self):
        """Инициализация фабрики."""
        self._items: Dict[str, T] = {}
        self._register_defaults()

    @abstractmethod
    def _register_defaults(self) -> None:
        """
        Регистрирует дефолтные объекты.
        
        Должен быть реализован в подклассах.
        """
        pass

    def create(self, name: str) -> Optional[T]:
        """
        Создает объект по имени.
        
        Args:
            name (str): Имя объекта
            
        Returns:
            Optional[T]: Экземпляр объекта или None, если не найден
        """
        return self._items.get(name)

    def register(self, name: str, item: T) -> None:
        """
        Регистрирует новый объект.
        
        Args:
            name (str): Имя объекта
            item (T): Экземпляр объекта
        """
        self._items[name] = item

    def unregister(self, name: str) -> bool:
        """
        Удаляет объект из регистрации.
        
        Args:
            name (str): Имя объекта
            
        Returns:
            bool: True, если объект был удален, False, если не найден
        """
        if name in self._items:
            del self._items[name]
            return True
        return False

    def get_all(self) -> Dict[str, T]:
        """
        Возвращает все зарегистрированные объекты.
        
        Returns:
            Dict[str, T]: Словарь всех объектов
        """
        return self._items.copy()

    def get_names(self) -> list[str]:
        """
        Возвращает список имен всех объектов.
        
        Returns:
            list[str]: Список имен объектов
        """
        return list(self._items.keys())

    def has(self, name: str) -> bool:
        """
        Проверяет, существует ли объект с указанным именем.
        
        Args:
            name (str): Имя объекта
            
        Returns:
            bool: True, если объект существует
        """
        return name in self._items

    def clear(self) -> None:
        """Очищает все зарегистрированные объекты."""
        self._items.clear()

    def reset_to_defaults(self) -> None:
        """Сбрасывает фабрику к дефолтным объектам."""
        self.clear()
        self._register_defaults() 