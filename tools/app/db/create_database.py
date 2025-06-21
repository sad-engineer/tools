#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from tools.app.config import get_settings

settings = get_settings()


def create_database():
    """Создает базу данных tools"""
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
        
        # Проверяем, существует ли база данных
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.POSTGRES_DB,))
        exists = cursor.fetchone()
        
        if exists:
            print(f"✅ База данных '{settings.POSTGRES_DB}' уже существует")
        else:
            # Создаем базу данных
            cursor.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
            print(f"✅ База данных '{settings.POSTGRES_DB}' создана успешно")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании базы данных: {e}")
        return False


if __name__ == "__main__":
    create_database()
