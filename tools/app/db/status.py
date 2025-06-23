#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт проверки статуса базы данных.

Этот скрипт проверяет:
1. Доступность базы данных
2. Существование таблиц
3. Выводит детальную информацию о состоянии БД
"""

import logging
from typing import List

from sqlalchemy import inspect, text

from tools.app.config import get_settings
from tools.app.db.session_manager import get_engine

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Список имен таблиц
TABLE_NAMES = [
    "tools",
    "geometry_countersinking_cutter",
    "geometry_deployment_cutter",
    "geometry_drilling_cutter",
    "geometry_milling_cutters",
    "geometry_turning_cutters",
]


def check_database_exists() -> bool:
    """
    Проверяет существование базы данных.

    Returns:
        bool: True если база данных существует, False в противном случае
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("✅ База данных доступна")
        return True
    except Exception as e:
        logger.error(f"❌ База данных недоступна: {e}")
        return False


def check_tables_exist(table_names: List[str]) -> List[str]:
    """
    Проверяет существование указанных таблиц.

    Args:
        table_names (List[str]): Список имен таблиц для проверки

    Returns:
        List[str]: Список существующих таблиц
    """
    existing_tables = []

    try:
        engine = get_engine()
        inspector = inspect(engine)
        all_tables = inspector.get_table_names()

        logger.info(f"Найдены таблицы: {all_tables}")

        for table_name in table_names:
            if table_name in all_tables:
                existing_tables.append(table_name)
                logger.info(f"✅ Таблица '{table_name}' существует")
            else:
                logger.info(f"ℹ️ Таблица '{table_name}' отсутствует")

        return existing_tables

    except Exception as e:
        logger.error(f"❌ Ошибка при проверке таблиц: {e}")
        return []


def get_status():
    """
    Показывает статус базы данных.

    Проверяет доступность БД и выводит список таблиц.
    Используйте для диагностики подключения.

    Пример: tool status
    """
    logger.info("🔍 Проверка статуса базы данных...")

    try:
        # Проверяем доступность базы данных
        if check_database_exists():
            logger.info("✅ База данных доступна")

            # Показываем таблицы
            existing_tables = check_tables_exist(TABLE_NAMES)
            logger.info(f"📋 Найдено таблиц: {len(existing_tables)}")

            for table in existing_tables:
                logger.info(f"  ✅ {table}")

            missing_tables = [table for table in TABLE_NAMES if table not in existing_tables]
            if missing_tables:
                logger.info(f"❌ Отсутствующие таблицы: {len(missing_tables)}")
                for table in missing_tables:
                    logger.info(f"  ❌ {table}")
        else:
            logger.info("❌ База данных недоступна")

    except Exception as e:
        logger.error(f"❌ Ошибка при проверке статуса: {e}")


if __name__ == "__main__":
    get_status()
