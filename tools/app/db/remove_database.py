#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Cкрипт удаления базы данных tools.

Этот скрипт проверяет:
1. Проверяет наличие таблиц.
2. Очищает данные в существующих таблицах.
3. Удаляет таблицы.
4. Удаляет базу данных
"""

import argparse
import logging
from typing import List

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import inspect, text

from tools.app.config import get_settings
from tools.app.db.checks import check_database_exists, check_tables_exist
from tools.app.db.session_manager import get_db, get_engine
from tools.app.db.utils import confirm_removal
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

# Список всех моделей для удаления таблиц
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
    Очищает данные в существующих таблицах.

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


def drop_tables(existing_tables: List[str]) -> bool:
    """
    Удаляет существующие таблицы.

    Args:
        existing_tables (List[str]): Список существующих таблиц

    Returns:
        bool: True если таблицы удалены успешно, False в противном случае
    """
    if not existing_tables:
        logger.info("Нет таблиц для удаления")
        return True

    try:
        engine = get_engine()

        # Удаляем таблицы в обратном порядке (из-за внешних ключей)
        for table_name in reversed(existing_tables):
            logger.info(f"Удаляем таблицу '{table_name}'...")

            # Используем SQLAlchemy для удаления таблицы
            for model in MODELS:
                if model.__tablename__ == table_name:
                    model.__table__.drop(engine, checkfirst=True)
                    logger.info(f"✅ Таблица '{table_name}' удалена")
                    break

        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при удалении таблиц: {e}")
        return False


def close_all_connections() -> bool:
    """
    Закрывает все активные соединения с базой данных.

    Returns:
        bool: True если соединения закрыты успешно, False в противном случае
    """
    try:
        # Подключаемся к системной БД postgres
        conn = psycopg2.connect(
            dbname="postgres",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Закрываем все активные соединения с целевой базой данных
        cursor.execute(
            """
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = %s AND pid <> pg_backend_pid()
        """,
            (settings.POSTGRES_DB,),
        )

        terminated_count = cursor.rowcount
        logger.info(f"Закрыто {terminated_count} активных соединений с базой данных")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при закрытии соединений: {e}")
        return False


def drop_database() -> bool:
    """
    Удаляет базу данных.

    Returns:
        bool: True если база данных удалена успешно, False в противном случае
    """
    try:
        # Сначала закрываем все активные соединения
        logger.info("Закрываем все активные соединения...")
        close_all_connections()

        # Подключаемся к системной БД postgres
        conn = psycopg2.connect(
            dbname="postgres",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Проверяем, существует ли база данных
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.POSTGRES_DB,))
        exists = cursor.fetchone()

        if exists:
            # Удаляем базу данных
            cursor.execute(f"DROP DATABASE {settings.POSTGRES_DB}")
            logger.info(f"✅ База данных '{settings.POSTGRES_DB}' удалена")
        else:
            logger.info(f"ℹ️ База данных '{settings.POSTGRES_DB}' не существует")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при удалении базы данных: {e}")
        return False


def remove_database() -> bool:
    """
    Полное удаление базы данных.

    Returns:
        bool: True если удаление прошло успешно, False в противном случае
    """
    logger.info("🗑️ Начинаем удаление базы данных...")

    # Шаг 1: Проверяем существование базы данных
    if not check_database_exists():
        logger.info("База данных не существует, нечего удалять")
        return True

    # Шаг 2: Проверяем существование таблиц
    existing_tables = check_tables_exist(TABLE_NAMES)

    # Шаг 3: Очищаем данные в существующих таблицах
    logger.info("Очищаем данные в таблицах...")
    if not clear_tables_data(existing_tables):
        logger.error("❌ Не удалось очистить данные в таблицах")
        return False

    # Шаг 4: Удаляем таблицы
    logger.info("Удаляем таблицы...")
    if not drop_tables(existing_tables):
        logger.error("❌ Не удалось удалить таблицы")
        return False

    # Шаг 5: Закрываем все соединения с базой данных
    logger.info("Закрываем все соединения...")
    close_all_connections()

    # Шаг 6: Удаляем базу данных
    logger.info("Удаляем базу данных...")
    if not drop_database():
        logger.error("❌ Не удалось удалить базу данных")
        return False

    logger.info("🎉 Удаление базы данных завершено успешно!")
    return True


def remove_database_with_options(quiet: bool = False) -> bool:
    """
    Удаляет базу данных с опциями.

    Args:
        quiet (bool): Если True, удаляет без запроса подтверждения.
                     Если False, запрашивает подтверждение.

    Returns:
        bool: True если удаление прошло успешно, False в противном случае
    """
    if quiet:
        # Тихое удаление без подтверждения
        logger.info("🗑️ Тихая удаление базы данных...")
        success = remove_database()

        if success:
            logger.info("✅ База данных удалена")
        else:
            logger.error("❌ Удаление базы данных не удалось")

        return success
    else:
        # Удаление с подтверждением
        if not confirm_removal():
            logger.info("❌ Удаление отменено пользователем")
            return False

        success = remove_database()

        if not success:
            logger.error("❌ Удаление базы данных не удалось")

        return success


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Удаление базы данных')
    parser.add_argument('--quiet', '-q', action='store_true', help='Тихое удаление без запроса подтверждения')

    args = parser.parse_args()

    # Выполняем удаление с опциями
    remove_database_with_options(quiet=args.quiet)
