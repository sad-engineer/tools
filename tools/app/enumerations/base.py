#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum
from typing import Any, TypeVar

T = TypeVar('T')


class BaseEnum(Enum):
    """Базовый класс для перечислений с общими методами"""

    @classmethod
    def get_values(cls) -> list[Any]:
        """
        Получить список всех значений перечисления.

        Returns:
            list[Any]: Список значений
        """
        return [member.value for member in cls]

    @classmethod
    def get_names(cls) -> list[str]:
        """
        Получить список всех имен перечисления.

        Returns:
            list[str]: Список имен
        """
        return [member.name for member in cls]

    @classmethod
    def get_items(cls) -> list[tuple[str, Any]]:
        """
        Получить список кортежей (имя, значение).

        Returns:
            list[tuple[str, Any]]: Список кортежей
        """
        return [(member.name, member.value) for member in cls]

    @classmethod
    def get_dict(cls) -> dict[str, Any]:
        """
        Получить словарь {имя: значение}.

        Returns:
            dict[str, Any]: Словарь имен и значений
        """
        return {member.name: member.value for member in cls}

    @classmethod
    def from_value(cls, value: Any) -> 'BaseEnum':
        """
        Преобразует значение в элемент перечисления.

        Args:
            value (Any): Значение

        Returns:
            BaseEnum: Элемент перечисления

        Raises:
            ValueError: Если значение не соответствует ни одному из допустимых
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Недопустимое значение: {value}. Допустимые значения: {cls.get_values()}")

    @classmethod
    def get_display_names(cls) -> dict[str, str]:
        """
        Получить словарь с отображаемыми названиями типов частоты шага.

        Returns:
            dict[str, str]: Словарь {код: название}
        """
        return {member.name: str(member.value) if member.value is not None else 'None' for member in cls}

    def __str__(self):
        return self.value
