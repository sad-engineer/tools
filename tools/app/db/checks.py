#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import logging
from typing import List

import psycopg2
from sqlalchemy import inspect, text

from tools.app.config import get_settings
from tools.app.db.session_manager import get_engine

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def check_connection():
    """
    Проверяет подключение к серверу PostgreSQL.
    """
    try:
        # Пробуем подключиться к postgres
        conn = psycopg2.connect(
            dbname="postgres",  # Подключаемся к системной БД postgres
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

        # Получаем информацию о подключении
        logger.info(f"Подключение к PostgreSQL на {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}...")

        # Проверяем подключение
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            logger.info(f"Версия PostgreSQL: {version}")

        conn.close()
        logger.info("✅ Подключение установлено успешно")
        return True

    except Exception as e:
        logger.error("❌ Ошибка подключения к PostgreSQL!")
        logger.error(f"Детали ошибки: {str(e)}")
        logger.error("\nУбедитесь, что:")
        logger.error("1. Сервер PostgreSQL запущен")
        logger.error("2. Настройки подключения корректны")
        logger.error("3. Пользователь имеет права доступа")
        return False


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


def check_database_exists_via_postgres() -> bool:
    """
    Проверяет существование базы данных через подключение к системной БД postgres.

    Этот метод используется когда нужно проверить существование БД
    до её создания.

    Returns:
        bool: True если база данных существует, False в противном случае
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

        cursor = conn.cursor()

        # Проверяем существование базы данных
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.POSTGRES_DB,))
        exists = cursor.fetchone()

        cursor.close()
        conn.close()

        if exists:
            logger.info(f"✅ База данных '{settings.POSTGRES_DB}' существует")
            return True
        else:
            logger.warning(f"❌ База данных '{settings.POSTGRES_DB}' не существует")
            return False

    except Exception as e:
        logger.error(f"❌ Ошибка при проверке базы данных: {e}")
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


def check_tables_exist_detailed(table_names: List[str]) -> bool:
    """
    Проверяет существование всех указанных таблиц (детальная проверка).

    Args:
        table_names (List[str]): Список имен таблиц для проверки

    Returns:
        bool: True если все таблицы существуют, False в противном случае
    """
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

        cursor = conn.cursor()

        # Проверяем каждую таблицу
        for table in table_names:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                )
            """,
                (table,),
            )

            exists = cursor.fetchone()[0]
            if exists:
                logger.info(f"✅ Таблица '{table}' существует")
            else:
                logger.warning(f"❌ Таблица '{table}' не существует")
                cursor.close()
                conn.close()
                return False

        cursor.close()
        conn.close()
        logger.info("✅ Все необходимые таблицы существуют")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при проверке таблиц: {e}")
        return False


def get_missing_tables(table_names: List[str]) -> List[str]:
    """
    Получает список отсутствующих таблиц.

    Args:
        table_names (List[str]): Список имен таблиц для проверки

    Returns:
        List[str]: Список отсутствующих таблиц
    """
    missing_tables = []

    try:
        engine = get_engine()
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        logger.info(f"Найдены таблицы: {existing_tables}")

        for table_name in table_names:
            if table_name not in existing_tables:
                missing_tables.append(table_name)
                logger.warning(f"❌ Таблица '{table_name}' отсутствует")
            else:
                logger.info(f"✅ Таблица '{table_name}' существует")

        return missing_tables

    except Exception as e:
        logger.error(f"❌ Ошибка при проверке таблиц: {e}")
        return table_names  # Возвращаем все таблицы как отсутствующие


if __name__ == "__main__":
    check_connection()
