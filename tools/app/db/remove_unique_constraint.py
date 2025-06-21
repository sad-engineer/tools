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


def remove_unique_constraint():
    """Удаляет ограничение уникальности на поле marking"""
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
        
        # Проверяем существование ограничения
        cursor.execute("""
            SELECT constraint_name 
            FROM information_schema.table_constraints 
            WHERE table_name = 'tools' 
            AND constraint_type = 'UNIQUE'
            AND constraint_name = 'tools_marking_key'
        """)
        
        constraint_exists = cursor.fetchone()
        
        if constraint_exists:
            logger.info("Найдено ограничение уникальности tools_marking_key")
            
            # Удаляем ограничение
            cursor.execute("ALTER TABLE tools DROP CONSTRAINT tools_marking_key")
            conn.commit()
            
            logger.info("✅ Ограничение уникальности успешно удалено")
        else:
            logger.info("Ограничение уникальности не найдено")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при удалении ограничения: {e}")
        return False


if __name__ == "__main__":
    remove_unique_constraint() 