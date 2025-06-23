#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import logging
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
from sqlalchemy import text

from tools.app.config import get_settings
from tools.app.db.session_manager import get_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def get_table_list() -> List[str]:
    """Получает список всех таблиц в базе данных.

    Returns:
        List[str]: Список названий таблиц
    """
    with get_db() as session:
        # SQL запрос для получения списка таблиц
        result = session.execute(
            text(
                """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """
            )
        )

        tables = [row[0] for row in result]
        logger.info(f"Найдено таблиц: {len(tables)}")
        return tables


def export_table_to_csv(table_name: str, output_dir: str = None, encoding: str = 'utf-8') -> str:
    """Экспортирует таблицу в CSV файл.

    Args:
        table_name (str): Название таблицы для экспорта
        output_dir (str): Директория для сохранения файла
        encoding (str): Кодировка файла

    Returns:
        str: Путь к созданному CSV файлу
    """
    if output_dir is None:
        # Создаем директорию по умолчанию
        project_root = Path(__file__).parent.parent.parent.parent
        output_dir = project_root / "database_backups"

    # Создаем директорию, если её нет
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        with get_db() as session:
            # Получаем данные из таблицы
            logger.info(f"Загружаем данные из таблицы '{table_name}'")

            # Используем pandas для чтения данных
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, session.bind)

            logger.info(f"Загружено {len(df)} записей из таблицы '{table_name}'")
            logger.info(f"Колонки: {list(df.columns)}")

            # Создаем имя файла с временной меткой
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{table_name}_{timestamp}.csv"
            filepath = Path(output_dir) / filename

            # Сохраняем в CSV
            df.to_csv(filepath, index=False, encoding=encoding)

            logger.info(f"✅ Таблица '{table_name}' экспортирована в {filepath}")
            logger.info(f"📊 Размер файла: {filepath.stat().st_size / 1024:.1f} KB")

            return str(filepath)

    except Exception as e:
        logger.error(f"❌ Ошибка при экспорте таблицы '{table_name}': {e}")
        raise


def export_all_tables(output_dir: str = None, encoding: str = 'utf-8') -> List[str]:
    """Экспортирует все таблицы в CSV файлы.

    Args:
        output_dir (str): Директория для сохранения файлов
        encoding (str): Кодировка файлов

    Returns:
        List[str]: Список путей к созданным файлам
    """
    tables = get_table_list()
    exported_files = []

    for table in tables:
        try:
            filepath = export_table_to_csv(table, output_dir, encoding)
            exported_files.append(filepath)
        except Exception as e:
            logger.error(f"Не удалось экспортировать таблицу '{table}': {e}")
            continue

    logger.info(f"✅ Экспортировано {len(exported_files)} из {len(tables)} таблиц")
    return exported_files


def export_table_to_csv_with_options(all_tables: bool = False):
    """Основная функция экспорта.
    
    Args:
        all_tables (bool): Экспортировать все таблицы (тихий режим)
    """
    try:
        if all_tables:
            # Тихий режим - экспорт всех таблиц
            logger.info("🚀 Экспортируем все таблицы (тихий режим)")
            exported_files = export_all_tables()
            logger.info(f"✅ Экспорт завершен! Создано файлов: {len(exported_files)}")
            for filepath in exported_files:
                logger.info(f"  📄 {filepath}")

        else:
            # Интерактивный режим (по умолчанию)
            tables = get_table_list()

            if not tables:
                logger.warning("В базе данных нет таблиц")
                return

            print("\n📋 Доступные таблицы:")
            for i, table_name in enumerate(tables, 1):
                print(f"  {i}. {table_name}")

            print(f"\n  {len(tables) + 1}. Экспортировать все таблицы")
            print("  0. Выход")

            try:
                choice = int(input("\nВыберите таблицу (номер): "))

                if choice == 0:
                    logger.info("Выход из программы")
                    return
                elif choice == len(tables) + 1:
                    logger.info("🚀 Экспортируем все таблицы")
                    exported_files = export_all_tables()
                    logger.info(f"✅ Экспорт завершен! Создано файлов: {len(exported_files)}")
                    for filepath in exported_files:
                        logger.info(f"  📄 {filepath}")
                elif 1 <= choice <= len(tables):
                    table_name = tables[choice - 1]
                    logger.info(f"🚀 Экспортируем таблицу '{table_name}'")
                    filepath = export_table_to_csv(table_name)
                    logger.info(f"✅ Экспорт завершен! Файл: {filepath}")
                else:
                    logger.error("Неверный выбор")

            except ValueError:
                logger.error("Введите число")
            except KeyboardInterrupt:
                logger.info("Операция прервана пользователем")

    except Exception as e:
        logger.error(f"❌ Ошибка при экспорте: {e}")
        raise


def export_table_to_csv_cli():
    """CLI функция для запуска с аргументами командной строки."""
    import argparse

    parser = argparse.ArgumentParser(description='Экспорт таблиц из БД в CSV')
    parser.add_argument('--all', '-a', action='store_true', help='Экспортировать все таблицы (тихий режим)')

    args = parser.parse_args()
    export_table_to_csv_with_options(all_tables=args.all)


if __name__ == "__main__":
    export_table_to_csv_cli()
