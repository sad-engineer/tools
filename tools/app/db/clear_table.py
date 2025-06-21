#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import psycopg2
import logging

from tools.app.config import get_settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def clear_tools_table():
    """Очищает таблицу tools"""
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
        cursor.execute("SELECT COUNT(*) FROM tools")
        count = cursor.fetchone()[0]
        
        logger.info(f"Найдено {count} записей в таблице tools")
        
        if count > 0:
            # Очищаем таблицу
            cursor.execute("DELETE FROM tools")
            conn.commit()
            
            logger.info(f"✅ Удалено {count} записей из таблицы tools")
        else:
            logger.info("Таблица tools уже пуста")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при очистке таблицы: {e}")
        return False


if __name__ == "__main__":
    clear_tools_table() 