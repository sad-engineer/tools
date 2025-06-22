#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт для загрузки данных зенкеров из CSV файла в таблицу geometry_countersinking_cutter.

Этот скрипт:
1. Читает CSV файл с данными зенкеров
2. Фильтрует только строки с типом "Зенкер"
3. Загружает данные в таблицу geometry_countersinking_cutter
4. Связывает зенкеры с соответствующими инструментами из таблицы tools
    через поле tool_id
"""

import csv
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from tools.app.db.session_manager import get_session
from tools.app.models.tools import Tool
from tools.app.models.geometry_countersinking_cutter import GeometryCountersinkingCutter


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Маппинг колонок CSV на поля модели GeometryCountersinkingCutter
COUNTERSINKING_COLUMN_MAPPING = {
    # Основные геометрические параметры
    'D': 'D',
    'l_': 'l_',
    'L': 'L',
    'z': 'z',
    
    # Конусы и исполнения
    'Конус_Морзе': 'morse_taper',
    'Исполнение': 'execution',
    'fi_': 'fi_',
    
    # Группа и типы
    'Группа': 'group',
    
    # Дополнительные размеры
    'D_доп.': 'D_additional',
    'd_': 'd_',
    
    # Тип отверстия
    'Тип_отверстия': 'hole_type',
}


def parse_float(value: str) -> Optional[float]:
    """Парсит строку в float, возвращает None если не удается."""
    if not value or value.strip() == '':
        return None
    try:
        # Заменяем запятую на точку для корректного парсинга
        cleaned_value = value.replace(',', '.')
        return float(cleaned_value)
    except (ValueError, TypeError):
        return None


def parse_int(value: str) -> Optional[int]:
    """Парсит строку в int, возвращает None если не удается."""
    if not value or value.strip() == '':
        return None
    try:
        return int(float(value))  # Сначала парсим как float, затем конвертируем в int
    except (ValueError, TypeError):
        return None


def load_countersinking_cutters_from_csv(csv_file_path: str, session: Session) -> int:
    """
    Загружает данные зенкеров из CSV файла в таблицу geometry_countersinking_cutter.
    
    Args:
        csv_file_path: Путь к CSV файлу
        session: Сессия базы данных
        
    Returns:
        Количество загруженных записей
    """
    csv_path = Path(csv_file_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV файл не найден: {csv_path}")
    
    loaded_count = 0
    skipped_count = 0
    
    logger.info(f"Начинаем загрузку данных зенкеров из файла: {csv_file_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, start=2):  # Начинаем с 2, так как 1 - заголовок
            try:
                # Проверяем, что это зенкер
                tool_type = row.get('Тип_инструмента', '').strip()
                if tool_type != 'Зенкер':
                    skipped_count += 1
                    continue
                
                # Получаем id инструмента
                id_str = row.get('index', '').strip()
                if not id_str:
                    logger.warning(f"Строка {row_num}: Отсутствует id инструмента")
                    skipped_count += 1
                    continue
                
                # Конвертируем id в число
                try:
                    tool_id = int(id_str)
                except ValueError:
                    logger.warning(f"Строка {row_num}: Некорректный id '{id_str}' - не является числом")
                    skipped_count += 1
                    continue
                
                # Ищем соответствующий инструмент в таблице tools по id
                tool = session.query(Tool).filter(Tool.id == tool_id).first()
                if not tool:
                    logger.warning(f"Строка {row_num}: Инструмент с id '{tool_id}' не найден в таблице tools")
                    # Добавляем отладочную информацию
                    total_tools = session.query(Tool).count()
                    logger.debug(f"Всего инструментов в БД: {total_tools}")
                    
                    # Показываем несколько примеров id из базы
                    if row_num <= 5:
                        sample_tools = session.query(Tool.id, Tool.marking).limit(5).all()
                        logger.info(f"Примеры инструментов в БД: {sample_tools}")
                    
                    skipped_count += 1
                    continue
                
                # Проверяем, не существует ли уже зенкер для этого инструмента
                existing_countersink = session.query(GeometryCountersinkingCutter).filter(GeometryCountersinkingCutter.tool_id == tool_id).first()
                if existing_countersink:
                    logger.info(f"Строка {row_num}: Зенкер для инструмента с id={tool_id} уже существует, пропускаем")
                    skipped_count += 1
                    continue
                
                # Создаем объект зенкера
                countersink_data = {}
                
                # Заполняем поля согласно маппингу
                for csv_col, model_field in COUNTERSINKING_COLUMN_MAPPING.items():
                    if csv_col in row:
                        value = row[csv_col].strip()
                        
                        # Определяем тип поля и парсим значение
                        field_type = getattr(GeometryCountersinkingCutter, model_field).type
                        
                        if hasattr(field_type, 'python_type'):
                            if field_type.python_type == float:
                                parsed_value = parse_float(value)
                            elif field_type.python_type == int:
                                parsed_value = parse_int(value)
                            else:
                                parsed_value = value if value else None
                        else:
                            # Для сложных типов (например, DateTime) оставляем как есть
                            parsed_value = value if value else None
                        
                        countersink_data[model_field] = parsed_value
                
                # Устанавливаем tool_id зенкера равным id инструмента
                countersink_data['tool_id'] = tool_id
                
                # Создаем и сохраняем зенкер
                countersink = GeometryCountersinkingCutter(**countersink_data)
                session.add(countersink)
                
                loaded_count += 1
                
                if loaded_count % 100 == 0:
                    logger.info(f"Загружено {loaded_count} записей...")
                
            except Exception as e:
                logger.error(f"Ошибка при обработке строки {row_num}: {e}")
                session.rollback()
                continue
    
    # Сохраняем все изменения
    try:
        session.commit()
        logger.info(f"Загрузка завершена. Загружено: {loaded_count}, Пропущено: {skipped_count}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении данных: {e}")
        session.rollback()
        raise
    
    return loaded_count


def main():
    """Основная функция для запуска загрузки."""
    try:
        # Путь к CSV файлу со зенкерами
        project_root = Path(__file__).parent.parent.parent.parent
        csv_file_path = project_root / "database_backups" / "tools_old.csv"

        # Получаем сессию базы данных
        with get_session() as session:
            loaded_count = load_countersinking_cutters_from_csv(csv_file_path, session)
            print(f"✅ Успешно загружено {loaded_count} записей зенкеров")

    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {e}")
        raise


if __name__ == "__main__":
    main() 