#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Dict, Type

from tools.app.models.tools import Tool
from tools.app.schemas import (
    BroachingCutter,
    CountersinkingCutter,
    DeploymentCutter,
    DrillingCutter,
    MillingCutter,
    TurningCutter,
)
from tools.app.schemas.tool import BaseTool


class ToolSchemaFactory:
    """
    Фабрика для создания схем инструментов на основе группы инструмента.

    Сопоставляет группы инструментов с соответствующими схемами данных.
    """

    # Словарь сопоставления групп инструментов с классами схем
    _tool_schemas: Dict[str, Type[BaseTool]] = {
        "Фреза": MillingCutter,
        "Сверло": DrillingCutter,
        "Резец": TurningCutter,
        "Развертка": DeploymentCutter,
        "Зенкер": CountersinkingCutter,
        "Протяжка": BroachingCutter,
    }

    @classmethod
    def create_schema(cls, tool: Tool) -> BaseTool:
        """
        Создает схему инструмента на основе данных из базы данных.

        Args:
            tool (Tool): Объект инструмента из базы данных

        Returns:
            BaseTool: Схема инструмента соответствующего типа

        Raises:
            ValueError: Если группа инструмента не поддерживается
        """
        group = tool.group

        if group not in cls._tool_schemas:
            raise ValueError(f"Неподдерживаемая группа инструмента: {group}")

        schema_class = cls._tool_schemas[group]

        # Создаем пустой объект схемы
        schema = schema_class()

        # Устанавливаем базовые поля через сеттеры
        schema.marking = tool.marking
        schema.standard = tool.standard

        # Здесь можно добавить установку дополнительных полей из базы данных
        # если они есть в таблице tool или связанных таблицах

        return schema

    @classmethod
    def create_schema_with_geometry(cls, tool: Tool, geometry_data: dict = None) -> BaseTool:
        """
        Создает схему инструмента с геометрическими данными.

        Args:
            tool (Tool): Объект инструмента из базы данных
            geometry_data (dict, optional): Геометрические данные инструмента

        Returns:
            BaseTool: Схема инструмента соответствующего типа
        """
        # Создаем базовую схему
        schema = cls.create_schema(tool)

        # Если есть геометрические данные, устанавливаем их
        if geometry_data:
            for field_name, value in geometry_data.items():
                if hasattr(schema, field_name):
                    setattr(schema, field_name, value)

        return schema

    @classmethod
    def get_supported_groups(cls) -> list[str]:
        """
        Возвращает список поддерживаемых групп инструментов.

        Returns:
            list[str]: Список групп инструментов
        """
        return list(cls._tool_schemas.keys())

    @classmethod
    def is_group_supported(cls, group: str) -> bool:
        """
        Проверяет, поддерживается ли группа инструмента.

        Args:
            group (str): Группа инструмента для проверки

        Returns:
            bool: True если группа поддерживается, False в противном случае
        """
        return group in cls._tool_schemas

    @classmethod
    def register_schema(cls, group: str, schema_class: Type[BaseTool]) -> None:
        """
        Регистрирует новую схему для группы инструментов.

        Args:
            group (str): Группа инструмента
            schema_class (Type[BaseTool]): Класс схемы
        """
        if not issubclass(schema_class, BaseTool):
            raise ValueError(f"Класс схемы должен наследоваться от BaseTool: {schema_class}")

        cls._tool_schemas[group] = schema_class

    @classmethod
    def unregister_schema(cls, group: str) -> None:
        """
        Удаляет регистрацию схемы для группы инструментов.

        Args:
            group (str): Группа инструмента
        """
        if group in cls._tool_schemas:
            del cls._tool_schemas[group]


# Пример использования:
if __name__ == "__main__":
    # Создаем тестовый объект инструмента
    from tools.app.db.session_manager import get_session

    with get_session() as session:
        # Получаем инструмент из базы данных
        from tools.app.models.tools import Tool

        tool = session.query(Tool).first()
        if tool:
            print(f"Тестовый инструмент: {tool.marking} ({tool.group})")

            try:
                # Создаем схему через фабрику
                schema = ToolSchemaFactory.create_schema(tool)
                print(f"Создана схема: {type(schema).__name__}")
                print(f"Обозначение: {schema.marking}")
                print(f"Группа: {schema.group}")
                print(f"Стандарт: {schema.standard}")

            except ValueError as e:
                print(f"Ошибка создания схемы: {e}")

        # Показываем поддерживаемые группы
        print(f"\nПоддерживаемые группы: {ToolSchemaFactory.get_supported_groups()}")

        # Проверяем поддержку группы
        test_group = "Фреза"
        is_supported = ToolSchemaFactory.is_group_supported(test_group)
        print(f"Группа '{test_group}' поддерживается: {is_supported}")
