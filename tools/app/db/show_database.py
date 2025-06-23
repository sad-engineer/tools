#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт для показа содержимого таблиц в базе данных
"""

import logging

from sqlalchemy import text

from tools.app.db.session_manager import get_session

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def show_database(limit: int = 10):
    """Показывает содержимое таблицы tools"""

    with get_session() as session:
        # Получаем список всех таблиц
        result = session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]

        for table_name in tables:
            logger.info(f"Таблица: {table_name}")

            # Получаем данные из таблицы
            result = session.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}"))
            rows = result.fetchall()

            if rows:
                # Получаем названия колонок
                columns = result.keys()
                logger.info(" | ".join(columns))
                logger.info("-" * 80)

                # Выводим данные
                for row in rows:
                    logger.info(" | ".join(str(value) for value in row))
            else:
                logger.info("Таблица пуста")


if __name__ == "__main__":
    show_database()
