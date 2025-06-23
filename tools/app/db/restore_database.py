#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Cкрипт восстановления базы данных tools.

Этот скрипт проверяет:
1. Проверяет наличие таблиц.
2. Если какой либо таблицы нет - создает ее.
3. Очищает данные в существующих таблицах.
4. Загружает данные из cvs файла.
"""

import argparse
import logging
from typing import List

from tools.app.config import get_settings
from tools.app.db.checks import check_database_exists, get_missing_tables
from tools.app.db.clear_database import clear_database
from tools.app.db.create_database import create_database
from tools.app.db.loaders import (
    load_all_geometry,
    load_main_data,
)
from tools.app.db.session_manager import get_db, get_engine
from tools.app.db.utils import confirm_restore
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

# Список всех моделей для создания таблиц
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


def create_missing_tables(missing_tables: List[str]) -> bool:
    """
    Создает отсутствующие таблицы.

    Args:
        missing_tables (List[str]): Список отсутствующих таблиц

    Returns:
        bool: True если все таблицы созданы успешно, False в противном случае
    """
    if not missing_tables:
        logger.info("Все таблицы уже существуют")
        return True

    try:
        engine = get_engine()

        # Создаем только отсутствующие таблицы
        for model in MODELS:
            table_name = model.__tablename__
            if table_name in missing_tables:
                logger.info(f"Создаем таблицу '{table_name}'...")
                model.__table__.create(engine, checkfirst=True)
                logger.info(f"✅ Таблица '{table_name}' создана")

        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при создании таблиц: {e}")
        return False


def restore_database() -> bool:
    """
    Полное восстановление базы данных.

    Returns:
        bool: True если восстановление прошло успешно, False в противном случае
    """
    logger.info("🚀 Начинаем восстановление базы данных...")

    # Шаг 1: Проверяем существование базы данных
    if not check_database_exists():
        logger.info("Создаем базу данных...")
        if not create_database():
            logger.error("❌ Не удалось создать базу данных")
            return False

    # Шаг 2: Очищаем существующие данные
    logger.info("Очищаем существующие данные...")
    try:
        clear_database()
        logger.info("✅ Данные очищены")
    except Exception as e:
        logger.error(f"❌ Ошибка при очистке данных: {e}")
        return False

    # Шаг 3: Загружаем данные
    logger.info("Загружаем данные...")
    try:
        # Загружаем основные данные
        logger.info("Загружаем основные данные...")
        load_main_data()

        # Загружаем геометрические данные
        logger.info("Загружаем геометрические данные...")
        load_all_geometry()

        logger.info("✅ Данные загружены успешно")

    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке данных: {e}")
        return False

    logger.info("🎉 Восстановление базы данных завершено успешно!")
    return True


def verify_restoration() -> bool:
    """
    Проверяет результат восстановления базы данных.

    Returns:
        bool: True если восстановление прошло успешно, False в противном случае
    """
    logger.info("Проверяем результат восстановления...")

    try:
        with get_db() as session:
            # Проверяем количество записей в каждой таблице
            for model in MODELS:
                count = session.query(model).count()
                logger.info(f"Таблица '{model.__tablename__}': {count} записей")

                if count == 0:
                    logger.warning(f"⚠️ Таблица '{model.__tablename__}' пуста")

        logger.info("✅ Проверка завершена")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при проверке: {e}")
        return False


def restore_database_with_options(quiet: bool = False) -> bool:
    """
    Восстанавливает базу данных с опциями.

    Args:
        quiet (bool): Если True, восстанавливает без запроса подтверждения.
                     Если False, запрашивает подтверждение.

    Returns:
        bool: True если восстановление прошло успешно, False в противном случае
    """
    if quiet:
        # Тихая восстановление без подтверждения
        logger.info("🚀 Тихая восстановление базы данных...")
        success = restore_database()

        if success:
            logger.info("✅ База данных восстановлена")
            # Проверяем результат
            verify_restoration()
        else:
            logger.error("❌ Восстановление базы данных не удалось")

        return success
    else:
        # Восстановление с подтверждением
        if not confirm_restore():
            logger.info("❌ Восстановление отменено пользователем")
            return False

        success = restore_database()

        if success:
            # Проверяем результат
            verify_restoration()
        else:
            logger.error("❌ Восстановление базы данных не удалось")

        return success


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Восстановление базы данных')
    parser.add_argument('--quiet', '-q', action='store_true', help='Тихое восстановление без запроса подтверждения')

    args = parser.parse_args()

    # Выполняем восстановление с опциями
    restore_database_with_options(quiet=args.quiet)
