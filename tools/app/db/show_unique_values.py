#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт для показа уникальных значений в колонках таблиц
"""

import logging

from sqlalchemy import text

from tools.app.db.session_manager import get_session

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def show_unique_values(table_name: str, column_name: str):
    """Показывает уникальные значения в указанной колонке таблицы"""

    with get_session() as session:
        # Получаем уникальные значения
        result = session.execute(text(f"SELECT DISTINCT {column_name} FROM {table_name} ORDER BY {column_name}"))
        rows = result.fetchall()

        logger.info(f"\nУникальные значения для колонки '{column_name}' в таблице '{table_name}':")
        logger.info("-" * 60)

        for row in rows:
            logger.info(row[0])


def show_all_unique_values(table_name: str = "tools") -> None:
    """
    Показывает уникальные значения для всех колонок указанной таблицы

    Args:
        table_name (str): Название таблицы (по умолчанию "tools")
    """
    with get_session() as session:
        # Получаем список всех колонок
        result = session.execute(text(f"SELECT * FROM {table_name} LIMIT 1"))
        columns = result.keys()

        # Для каждой колонки получаем уникальные значения
        for column in columns:
            show_unique_values(table_name, column)


if __name__ == "__main__":
    # Пример использования для конкретной колонки
    show_unique_values("tools", "accuracy")

    # Пример использования для всех колонок
    # show_all_unique_values("tools")
