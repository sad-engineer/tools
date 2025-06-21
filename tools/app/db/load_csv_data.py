#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import pandas as pd
import logging
import os
from pathlib import Path
from typing import List, Dict, Any

from tools.app.db.session_manager import get_db
from tools.app.models.tools import Tool
from tools.app.config import get_settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def detect_encoding(file_path: str) -> str:
    """Определяет кодировку CSV файла.
    
    Args:
        file_path (str): Путь к CSV файлу
        
    Returns:
        str: Кодировка файла
    """
    import chardet
    
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        logger.info(f"Обнаружена кодировка: {encoding} (уверенность: {result['confidence']:.2f})")
        return encoding


def load_csv_data(csv_file_path: str = None) -> List[Dict[str, Any]]:
    """Загружает данные из CSV файла.
    
    Args:
        csv_file_path (str): Путь к CSV файлу
        
    Returns:
        List[Dict[str, Any]]: Список словарей с данными
    """
    if csv_file_path is None:
        # Определяем путь к CSV файлу относительно корня проекта
        project_root = Path(__file__).parent.parent.parent.parent
        csv_file_path = project_root / "database_backups" / "tools_old.csv"
    
    try:
        # Определяем кодировку
        encoding = detect_encoding(str(csv_file_path))
        
        # Читаем CSV файл
        logger.info(f"Загружаем данные из {csv_file_path}")
        df = pd.read_csv(csv_file_path, encoding=encoding)
        
        logger.info(f"Загружено {len(df)} записей")
        logger.info(f"Колонки: {list(df.columns)}")
        
        # Показываем первые несколько строк
        logger.info("Первые 3 записи:")
        for i, row in df.head(3).iterrows():
            logger.info(f"  {i}: {dict(row)}")
        
        return df.to_dict('records')
        
    except Exception as e:
        logger.error(f"Ошибка при загрузке CSV: {e}")
        raise


def map_csv_to_model(csv_data: List[Dict[str, Any]]) -> List[Tool]:
    """Преобразует данные из CSV в модели Tool.
    
    Args:
        csv_data (List[Dict[str, Any]]): Данные из CSV
        
    Returns:
        List[Tool]: Список моделей Tool
    """
    tools = []
    
    for i, row in enumerate(csv_data):
        try:
            # Извлекаем основные поля
            index = row.get('index')
            marking = str(row.get('Обозначение', f'unknown-{i}'))
            group = str(row.get('Тип_инструмента', ''))
            standard = str(row.get('Стандарт', ''))
            
            # Проверяем, что index является числом
            if index is None or pd.isna(index):
                logger.warning(f"Строка {i}: Отсутствует index, пропускаем")
                continue
            
            try:
                tool_id = int(index)
            except (ValueError, TypeError):
                logger.warning(f"Строка {i}: Некорректный index '{index}', пропускаем")
                continue
            
            # Создаем модель с указанным id
            tool = Tool(
                id=tool_id,  # Используем index из CSV как id
                marking=marking,
                group=group if group != 'nan' else None,
                standard=standard if standard != 'nan' else None
            )
            
            tools.append(tool)
            
        except Exception as e:
            logger.error(f"Ошибка при обработке строки {i}: {e}")
            logger.error(f"Данные строки: {row}")
            continue
    
    logger.info(f"Создано {len(tools)} моделей Tool")
    return tools


def save_tools_to_db(tools: List[Tool]) -> int:
    """Сохраняет инструменты в базу данных.
    
    Args:
        tools (List[Tool]): Список инструментов для сохранения
        
    Returns:
        int: Количество сохраненных записей
    """
    saved_count = 0
    
    with get_db() as session:
        try:
            # Очищаем таблицу tools перед загрузкой новых данных
            logger.info("Очищаем таблицу tools...")
            session.query(Tool).delete()
            session.commit()
            logger.info("Таблица tools очищена")
            
            for i, tool in enumerate(tools):
                try:
                    # Проверяем, существует ли уже инструмент с таким id
                    existing = session.query(Tool).filter(Tool.id == tool.id).first()
                    if existing:
                        logger.warning(f"Инструмент с id {tool.id} уже существует, пропускаем")
                        continue
                    
                    session.add(tool)
                    saved_count += 1
                    
                    # Логируем прогресс каждые 100 записей
                    if (i + 1) % 100 == 0:
                        logger.info(f"Обработано {i + 1} записей...")
                        
                except Exception as e:
                    logger.error(f"Ошибка при сохранении инструмента {tool.marking} (id={tool.id}): {e}")
                    session.rollback()
                    continue
            
            # Сохраняем все изменения
            session.commit()
            logger.info(f"Успешно сохранено {saved_count} инструментов")
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении в БД: {e}")
            session.rollback()
            raise
    
    return saved_count


def main():
    """Основная функция загрузки данных."""
    try:
        logger.info("🚀 Начинаем загрузку данных из CSV в базу данных")
        
        # Загружаем данные из CSV
        csv_data = load_csv_data()
        
        # Преобразуем в модели
        tools = map_csv_to_model(csv_data)
        
        # Сохраняем в БД
        saved_count = save_tools_to_db(tools)
        
        logger.info(f"✅ Загрузка завершена! Сохранено {saved_count} инструментов")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке данных: {e}")
        raise


if __name__ == "__main__":
    main()
