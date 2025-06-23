#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт очистки базы данных tools.

Этот скрипт:
1. Проверяет наличие таблиц.
2. Очищает данные в существующих таблицах в правильном порядке.
3. Таблица tools очищается последней.
"""

import argparse
import logging
from typing import List

from sqlalchemy import text

from tools.app.config import get_settings
from tools.app.db.checks import check_database_exists, check_tables_exist
from tools.app.db.session_manager import get_db
from tools.app.db.utils import confirm_clear
from tools.app.models import (
    GeometryCountersinkingCutter,
    GeometryDeploymentCutter,
    GeometryDrillingCutter,
    GeometryMillingCutters,
    GeometryTurningCutters,
    Tool,
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Список всех моделей
MODELS = [
    Tool,
    GeometryCountersinkingCutter,
    GeometryDeploymentCutter,
    GeometryDrillingCutter,
    GeometryMillingCutters,
    GeometryTurningCutters,
]

# Список имен таблиц
TABLE_NAMES = settings.TABLE_NAMES


def clear_tables_data(existing_tables: List[str]) -> bool:
    """
    Очищает данные в существующих таблицах в правильном порядке.

    Args:
        existing_tables (List[str]): Список существующих таблиц

    Returns:
        bool: True если данные очищены успешно, False в противном случае
    """
    if not existing_tables:
        logger.info("Нет таблиц для очистки")
        return True

    try:
        with get_db() as session:
            # Сначала очищаем все таблицы кроме tools
            geometry_tables = [table for table in existing_tables if table != "tools"]
            tools_table = [table for table in existing_tables if table == "tools"]

            # Очищаем геометрические таблицы
            for table_name in geometry_tables:
                logger.info(f"Очищаем таблицу '{table_name}'...")

                # Получаем количество записей
                count = session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()

                if count > 0:
                    # Очищаем таблицу
                    session.execute(text(f"DELETE FROM {table_name}"))
                    session.commit()
                    logger.info(f"✅ Удалено {count} записей из таблицы '{table_name}'")
                else:
                    logger.info(f"ℹ️ Таблица '{table_name}' уже пуста")

            # Затем очищаем таблицу tools (последней)
            for table_name in tools_table:
                logger.info(f"Очищаем таблицу '{table_name}'...")

                # Получаем количество записей
                count = session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()

                if count > 0:
                    # Очищаем таблицу
                    session.execute(text(f"DELETE FROM {table_name}"))
                    session.commit()
                    logger.info(f"✅ Удалено {count} записей из таблицы '{table_name}'")
                else:
                    logger.info(f"ℹ️ Таблица '{table_name}' уже пуста")

        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при очистке данных: {e}")
        return False


def clear_database() -> bool:
    """
    Полная очистка базы данных.

    Returns:
        bool: True если очистка прошла успешно, False в противном случае
    """
    logger.info("🧹 Начинаем очистку базы данных...")

    # Шаг 1: Проверяем существование базы данных
    if not check_database_exists():
        logger.error("❌ База данных недоступна")
        return False

    # Шаг 2: Проверяем существование таблиц
    existing_tables = check_tables_exist(TABLE_NAMES)

    if not existing_tables:
        logger.info("ℹ️ Нет таблиц для очистки")
        return True

    # Шаг 3: Очищаем данные в существующих таблицах
    logger.info("Очищаем данные в таблицах...")
    if not clear_tables_data(existing_tables):
        logger.error("❌ Не удалось очистить данные в таблицах")
        return False

    logger.info("🎉 Очистка базы данных завершена успешно!")
    return True


def clear_database_with_options(quiet: bool = False) -> bool:
    """
    Очищает базу данных с опциями.

    Args:
        quiet (bool): Если True, очищает без запроса подтверждения.
                     Если False, запрашивает подтверждение.

    Returns:
        bool: True если очистка прошла успешно, False в противном случае
    """
    if quiet:
        # Тихая очистка без подтверждения
        logger.info("🧹 Тихая очистка базы данных...")
        success = clear_database()

        if success:
            logger.info("✅ База данных очищена")
        else:
            logger.error("❌ Очистка базы данных не удалась")

        return success
    else:
        # Очистка с подтверждением
        if not confirm_clear():
            logger.info("❌ Очистка отменена пользователем")
            return False

        success = clear_database()

        if not success:
            logger.error("❌ Очистка базы данных не удалась")

        return success


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Очистка базы данных')
    parser.add_argument('--quiet', '-q', action='store_true', help='Тихая очистка без запроса подтверждения')

    args = parser.parse_args()

    # Выполняем очистку с опциями
    clear_database_with_options(quiet=args.quiet)
