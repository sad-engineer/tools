#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import text

from tools.app.db.session_manager import session_manager


def show_unique_values(table_name: str, column_name: str) -> None:
    """
    Показывает уникальные значения для указанной колонки в указанной таблице.

    Args:
        table_name (str): Название таблицы
        column_name (str): Название колонки для получения уникальных значений
    """
    with session_manager.engine.connect() as connection:
        query = text(f"SELECT DISTINCT {column_name} FROM {table_name} ORDER BY {column_name}")
        result = connection.execute(query)

        print(f"\nУникальные значения для колонки '{column_name}' в таблице '{table_name}':")
        print("-" * 60)
        for row in result:
            print(row[0])


def show_all_unique_values(table_name: str = "tools") -> None:
    """
    Показывает уникальные значения для всех колонок указанной таблицы
    
    Args:
        table_name (str): Название таблицы (по умолчанию "tools")
    """
    with session_manager.engine.connect() as connection:
        # Получаем список всех колонок
        result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT 1"))
        columns = result.keys()

        # Для каждой колонки получаем уникальные значения
        for column in columns:
            show_unique_values(table_name, column)


if __name__ == "__main__":
    # Пример использования для конкретной колонки
    show_unique_values("tools", "accuracy")
    
    # Пример использования для всех колонок
    # show_all_unique_values("tools")
