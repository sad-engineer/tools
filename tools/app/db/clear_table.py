#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import logging

import psycopg2

from tools.app.config import get_settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def clear_table(table_name: str):
    """Очищает указанную таблицу

    Args:
        table_name (str): Название таблицы для очистки
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

        # Получаем количество записей
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]

        logger.info(f"Найдено {count} записей в таблице {table_name}")

        if count > 0:
            # Очищаем таблицу
            cursor.execute(f"DELETE FROM {table_name}")
            conn.commit()

            logger.info(f"✅ Удалено {count} записей из таблицы {table_name}")
        else:
            logger.info(f"Таблица {table_name} уже пуста")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка при очистке таблицы {table_name}: {e}")
        return False


if __name__ == "__main__":
    clear_table("geometry_countersinking_cutter")
    # clear_table("tools")
