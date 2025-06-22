#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт для загрузки данных разверток из CSV файла в таблицу geometry_deployment_cutter.

Этот скрипт:
1. Читает CSV файл с данными разверток
2. Фильтрует только строки с типом "Развертка"
3. Загружает данные в таблицу geometry_deployment_cutter
4. Связывает развертки с соответствующими инструментами из таблицы tools
    через поле tool_id
"""

import csv
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from tools.app.db.session_manager import get_session
from tools.app.models.geometry_deployment_cutter import GeometryDeploymentCutter
from tools.app.models.tools import Tool

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Маппинг колонок CSV на поля модели GeometryDeploymentCutter
DEPLOYMENT_COLUMN_MAPPING = {
    # Основные геометрические параметры
    'D': 'D',
    'd_1_': 'd_1_',
    'd_2_': 'd_2_',
    'l_': 'l_',
    'L': 'L',
    'z': 'z',
    # Конусы и исполнения
    'Конус_Морзе': 'morse_taper',
    'Исполнение': 'execution',
    'fi_': 'fi_',
    # Материал и группа
    'mat_': 'mat_',
    'Группа': 'group',
    # Дополнительные размеры
    'D_1': 'D_1',
    'd_': 'd_',
    'h_': 'h_',
    'l_1_': 'l_1_',
    'l_2_': 'l_2_',
    'r_': 'r_',
    'l_0_': 'l_0_',
    # Тип развертки и углы
    'Тип_развертки': 'reamer_type',
    'fi_1_': 'fi_1_',
    'gamma_': 'gamma_',
    'lambda_': 'lambda_',
    # Конусность и дополнительные параметры
    'Конусность_развертки': 'reamer_taper',
    'd_2_доп.': 'd_2_additional',
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


def load_deployment_cutters_from_csv(csv_file_path: str, session: Session) -> int:
    """
    Загружает данные разверток из CSV файла в таблицу geometry_deployment_cutter.

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

    logger.info(f"Начинаем загрузку данных разверток из файла: {csv_file_path}")

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row_num, row in enumerate(reader, start=2):  # Начинаем с 2, так как 1 - заголовок
            try:
                # Проверяем, что это развертка
                tool_type = row.get('Тип_инструмента', '').strip()
                if tool_type != 'Развертка':
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

                # Проверяем, не существует ли уже развертка для этого инструмента
                existing_deployment = (
                    session.query(GeometryDeploymentCutter).filter(GeometryDeploymentCutter.tool_id == tool_id).first()
                )
                if existing_deployment:
                    logger.info(
                        f"Строка {row_num}: Развертка для инструмента с id={tool_id} уже существует, пропускаем"
                    )
                    skipped_count += 1
                    continue

                # Создаем объект развертки
                deployment_data = {}

                # Заполняем поля согласно маппингу
                for csv_col, model_field in DEPLOYMENT_COLUMN_MAPPING.items():
                    if csv_col in row:
                        value = row[csv_col].strip()

                        # Определяем тип поля и парсим значение
                        field_type = getattr(GeometryDeploymentCutter, model_field).type

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

                        deployment_data[model_field] = parsed_value

                # Устанавливаем tool_id развертки равным id инструмента
                deployment_data['tool_id'] = tool_id

                # Создаем и сохраняем развертку
                deployment = GeometryDeploymentCutter(**deployment_data)
                session.add(deployment)

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
        # Путь к CSV файлу с развертками
        project_root = Path(__file__).parent.parent.parent.parent
        csv_file_path = project_root / "database_backups" / "tools_old.csv"

        # Получаем сессию базы данных
        with get_session() as session:
            loaded_count = load_deployment_cutters_from_csv(csv_file_path, session)
            print(f"✅ Успешно загружено {loaded_count} записей разверток")

    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {e}")
        raise


if __name__ == "__main__":
    main()
