#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Cкрипт инициализации базы данных tools.

Этот скрипт проверяет:
1. Запущен ли PostgreSQL сервер
2. Существует ли база данных tools
3. Созданы ли все необходимые таблицы
4. Есть ли данные в таблицах

Если хоть одно условие не выполняется - выполняет полную инициализацию.
"""

import logging
import sys

from tools.app.config import get_settings
from tools.app.db.checks import check_connection, check_database_exists_via_postgres, check_tables_exist_detailed
from tools.app.db.create_database import create_database
from tools.app.db.loaders import load_all_geometry, load_main_data
from tools.app.db.session_manager import get_session
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

# Список необходимых таблиц
REQUIRED_TABLES = settings.TABLE_NAMES


def check_tables_have_data() -> bool:
    """Проверяет, есть ли данные в таблицах"""
    try:
        with get_session() as session:
            # Проверяем основную таблицу tools
            tools_count = session.query(Tool).count()
            logger.info(f"Записей в таблице tools: {tools_count}")

            if tools_count == 0:
                logger.warning("❌ Таблица tools пуста")
                return False

            # Проверяем таблицы геометрии
            geometry_tables = [
                (GeometryMillingCutters, "geometry_milling_cutters"),
                (GeometryDrillingCutter, "geometry_drilling_cutter"),
                (GeometryCountersinkingCutter, "geometry_countersinking_cutter"),
                (GeometryDeploymentCutter, "geometry_deployment_cutter"),
                (GeometryTurningCutters, "geometry_turning_cutters"),
            ]

            for model, table_name in geometry_tables:
                count = session.query(model).count()
                logger.info(f"Записей в таблице {table_name}: {count}")

                if count == 0:
                    logger.warning(f"❌ Таблица {table_name} пуста")
                    return False

            logger.info("✅ Все таблицы содержат данные")
            return True

    except Exception as e:
        logger.error(f"❌ Ошибка при проверке данных в таблицах: {e}")
        return False


def create_tables():
    """Создает все необходимые таблицы"""
    try:
        logger.info("Создаю таблицы...")

        # Импортируем Base и все модели для создания таблиц
        from tools.app.db.session_manager import get_engine
        from tools.app.models import Base

        engine = get_engine()
        Base.metadata.create_all(engine)

        logger.info("✅ Таблицы созданы успешно")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при создании таблиц: {e}")
        return False


def load_data_from_csv():
    """Загружает данные из CSV файлов"""
    try:
        logger.info("🔄 Начинаю загрузку данных из CSV файлов...")

        # Загружаем основные данные инструментов
        logger.info("Загружаю основные данные инструментов...")
        load_main_data()

        # Загружаем геометрические данные
        logger.info("Загружаю геометрические данные...")
        load_all_geometry()

        logger.info("✅ Загрузка данных завершена успешно")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке данных: {e}")
        return False


def init_database():
    """Основная функция инициализации базы данных"""
    logger.info("🚀 Начинаю инициализацию базы данных tools")

    # Шаг 1: Проверяем подключение к PostgreSQL
    logger.info("Проверяю подключение к PostgreSQL...")
    if not check_connection():
        logger.error("❌ Не удалось подключиться к PostgreSQL. Убедитесь, что сервер запущен.")
        return False

    # Шаг 2: Проверяем существование базы данных
    logger.info("Проверяю существование базы данных...")
    if not check_database_exists_via_postgres():
        logger.info("Создаю базу данных...")
        if not create_database():
            logger.error("❌ Не удалось создать базу данных")
            return False

    # Шаг 3: Проверяем существование таблиц
    logger.info("Проверяю существование таблиц...")
    if not check_tables_exist_detailed(REQUIRED_TABLES):
        logger.info("Создаю таблицы...")
        if not create_tables():
            logger.error("❌ Не удалось создать таблицы")
            return False

    # Шаг 4: Проверяем наличие данных в таблицах
    logger.info("Проверяю наличие данных в таблицах...")
    if not check_tables_have_data():
        logger.info("Загружаю данные из CSV файлов...")
        if not load_data_from_csv():
            logger.error("❌ Не удалось загрузить данные")
            return False
    else:
        logger.info("✅ База данных уже содержит данные, инициализация не требуется")

    logger.info("🎉 Инициализация базы данных завершена успешно!")
    return True


if __name__ == "__main__":
    try:
        success = init_database()
        if success:
            logger.info("✅ Инициализация завершена успешно")
            sys.exit(0)
        else:
            logger.error("❌ Инициализация завершена с ошибками")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("⏹️  Инициализация прервана пользователем")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
