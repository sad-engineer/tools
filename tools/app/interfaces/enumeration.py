#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Protocol


class IEnumeration(Protocol):
    """
    Интерфейс для перечислений.
    
    Определяет базовый контракт для работы с перечислениями.
    """

    @classmethod
    def get_values(cls) -> list[Any]:
        """
        Получить список всех значений перечисления.

        Returns:
            list[Any]: Список значений
        """
        ...

    @classmethod
    def get_names(cls) -> list[str]:
        """
        Получить список всех имен перечисления.

        Returns:
            list[str]: Список имен
        """
        ...

    @classmethod
    def get_items(cls) -> list[tuple[str, Any]]:
        """
        Получить список кортежей (имя, значение).

        Returns:
            list[tuple[str, Any]]: Список кортежей
        """
        ...

    @classmethod
    def get_dict(cls) -> dict[str, Any]:
        """
        Получить словарь {имя: значение}.

        Returns:
            dict[str, Any]: Словарь имен и значений
        """
        ...

    @classmethod
    def from_value(cls, value: Any) -> 'IEnumeration':
        """
        Преобразует значение в элемент перечисления.

        Args:
            value (Any): Значение

        Returns:
            IEnumeration: Элемент перечисления

        Raises:
            ValueError: Если значение не соответствует ни одному из допустимых
        """
        ...

    @classmethod
    def get_display_names(cls) -> dict[str, str]:
        """
        Получить словарь с отображаемыми названиями.

        Returns:
            dict[str, str]: Словарь {код: название}
        """
        ...

    def __str__(self) -> str:
        """
        Строковое представление элемента перечисления.

        Returns:
            str: Строковое представление
        """
        ... 