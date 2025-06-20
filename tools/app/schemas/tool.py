#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from tools.app.enumerations import MarkingForSpecialTool, StandardTypes, ToolGroups


class BaseTool(BaseModel, validate_assignment=True):
    """Базовый класс для инструментов.

    Parameters:
    standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
    _name : (Optional[str]) : внутреннее поле для сохранения кастомного имени инструмента.
    _group : (Optional[ToolGroups]) : внутреннее поле для сохранения группы инструмента.

    Properties:
    name : (str) : возвращает название инструмента.
    group : (str is GROUPS_TOOL) : группа инструмента (только для чтения).

    Methods:
    marking : (str) : абстрактный метод, возвращает обозначение инструмента.
    _parameters : (dict) : возвращает словарь параметров и свойств.
    __eq__ : (bool) : сравнивает объекты по всем полям.

    Notes:
    - Поле group защищено от изменений после создания объекта
    - Поле name может быть установлено кастомно или генерируется автоматически
    """

    _name: Optional[str] = None  # Для сохранения кастомного имени инструмента
    _group: Optional[ToolGroups] = ToolGroups.INSTRUMENT  # Для сохранения группы инструмента
    standard: str = Field(
        "ГОСТ 1000-90", description=f"Стандарт инструмента. Должен содержать одно из [{StandardTypes.get_values()}]"
    )

    @property
    def name(self) -> str:
        if self._name is not None:
            return self._name
        return " ".join([self.group, self.marking, self.standard])

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def group(self) -> str:
        return self._group.value

    @group.setter
    def group(self, value) -> None:
        raise AttributeError(
            "Поле 'group' защищено от изменений. " "Группа инструмента не может быть изменена после создания объекта."
        )

    @property
    @abstractmethod
    def marking(self) -> str:
        """Обозначение инструмента. Должно быть реализовано в наследниках."""
        pass

    @property
    def _parameters(self) -> dict:
        return {
            "group": self.group,
            "marking": self.marking,
            "standard": self.standard,
            "name": self.name,
        }

    def __eq__(self, other):
        """Переопределяем сравнение для учета всех полей включая группу"""
        if not isinstance(other, BaseTool):
            return False

        # Сравниваем все поля модели через model_dump
        self_dict = self.model_dump()
        other_dict = other.model_dump()

        return self_dict == other_dict


class Tool(BaseTool):
    """Управляет полями класса 'Инструмент'.

    Parameters:
    marking : (str) : обозначение инструмента.
    standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
    _marking : (str) : внутреннее поле для сохранения маркировки.

    Properties:
    name : (str) : возвращает название инструмента.
    group : (str is GROUPS_TOOL) : группа инструмента (только для чтения).
    marking : (str) : обозначение инструмента (доступно для чтения и записи).
    _parameters : (dict) : возвращает словарь параметров и свойств.

    Methods:
    validate_standard : (str) : валидатор для проверки корректности стандарта.
    _parameters : (dict) : возвращает словарь всех параметров и свойств.

    Notes:
    - Поле marking может быть изменено через сеттер
    - Стандарт валидируется на соответствие допустимым значениям
    """

    _marking: str = "ХХХХ-ХХХХ"  # Для сохранения маркировки

    @property
    def marking(self) -> str:
        return self._marking

    @marking.setter
    def marking(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f'Неверное обозначение инструмента. Ожидается строковое выражение. Получено: {value}')
        self._marking = value

    @field_validator('standard')
    def validate_standard(cls, value):
        """Валидатор для проверки корректности стандарта инструмента.
        
        Args:
            value: Строка с названием стандарта
            
        Returns:
            str: Проверенное значение стандарта
            
        Raises:
            ValueError: Если стандарт не соответствует допустимым значениям
        """
        for st in StandardTypes.get_values():
            if st:
                if st in value:
                    return value
        raise ValueError(
            f"Ожидается строка, содержащая название стандарта инструмента (например: "
            f"{', '.join(str(i) for i in StandardTypes.get_values() if i)}). Получено значение: {value}"
        )


class CustomTool(BaseTool):
    """Специальный инструмент.
    
    В этом инструменте в поле marking указывается только 'специальный' а поле standard
    можно оставлять пустым.

    Parameters:
    _marking : (MarkingForSpecialTool) : внутреннее поле для сохранения маркировки специального инструмента.

    Properties:
    name : (str) : возвращает название инструмента.
    group : (str is GROUPS_TOOL) : группа инструмента (только для чтения).
    marking : (str) : обозначение инструмента (доступно для чтения и записи).
    _parameters : (dict) : возвращает словарь параметров и свойств.

    Methods:
    _parameters : (dict) : возвращает словарь всех параметров и свойств.

    Notes:
    - Поле marking автоматически устанавливается как "специальный"
    - Поле standard может быть пустым для специальных инструментов
    """

    _marking: MarkingForSpecialTool = MarkingForSpecialTool.SPECIAL_NY  # Для сохранения маркировки

    @property
    def marking(self) -> str:
        return self._marking.value

    @marking.setter
    def marking(self, value) -> None:
        if isinstance(value, MarkingForSpecialTool):
            self._marking = value
        else:
            self._marking = MarkingForSpecialTool.from_value(value)


if __name__ == '__main__':
    # Пример использования класса Tool
    tool = Tool()
    print(tool)  # Выведет объект с дефолтными значениями
    print('Имя инструмента:', tool.name)
    print('Параметры:', tool._parameters)

    # Изменение полей
    tool.marking = "1234-5678"
    tool.standard = "ГОСТ 1234-56"
    print('Новое имя:', tool.name)
    print('Параметры:', tool._parameters)
    print('Параметры:', tool.model_dump())
    # Проверка валидации стандарта
    try:
        tool.standard = "НЕИЗВЕСТНЫЙ СТАНДАРТ"
        tool = Tool(standard="НЕИЗВЕСТНЫЙ СТАНДАРТ")
    except ValueError as e:
        print(f"Ошибка валидации стандарта: {e}")

    # Кастомное имя
    tool.name = "Мой инструмент"
    print('Кастомное имя:', tool.name)

    # Пример использования класса CustomTool
    custom_tool = CustomTool()
    print(custom_tool)  # Выведет объект с дефолтными значениями
    print('Имя специального инструмента:', custom_tool.name)
    print('Маркировка:', custom_tool.marking)  # Теперь возвращает строку
    print('Параметры:', custom_tool._parameters)

    # Изменение маркировки
    custom_tool.marking = "специальная"
    print('Новая маркировка:', custom_tool.marking)
    print('Параметры:', custom_tool._parameters)

    # Проверка валидации маркировки
    try:
        custom_tool.marking = "неверная_маркировка"
    except ValueError as e:
        print(f"Ошибка валидации маркировки: {e}")

    # Демонстрация работы с объектом перечисления
    custom_tool.marking = MarkingForSpecialTool.SPECIAL_NAYA
    print('Маркировка через объект:', custom_tool.marking)
