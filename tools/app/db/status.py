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

from tools.app.config import get_settings
from tools.app.db.checks import check_database_exists, check_tables_exist

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Список имен таблиц
TABLE_NAMES = settings.TABLE_NAMES


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
