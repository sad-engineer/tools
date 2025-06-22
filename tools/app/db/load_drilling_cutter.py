#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт для загрузки данных сверл из CSV файла в таблицу geometry_drilling_cutter.

Этот скрипт:
1. Читает CSV файл с данными сверл
2. Фильтрует только строки с типом "Сверло"
3. Загружает данные в таблицу geometry_drilling_cutter
4. Связывает сверла с соответствующими инструментами из таблицы tools
    через поле tool_id
"""

import csv
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from tools.app.db.session_manager import get_session
from tools.app.models.tools import Tool
from tools.app.models.geometry_drilling_cutter import GeometryDrillingCutter

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Маппинг колонок CSV на поля модели GeometryDrillingCutter
DRILL_COLUMN_MAPPING = {
    # Основные геометрические параметры
    'a_': 'a_',
    'D': 'D',
    'd_1_': 'd_1_',
    'd_2_': 'd_2_',
    'l_': 'l_',
    'L': 'L',
    'f_': 'f_',
    'z': 'z',

    # Конусы и исполнения
    'Конус_Морзе': 'morse_taper',
    'Исполнение': 'execution',
    'fi_': 'fi_',

    # Группа и типы
    'Группа': 'group',

    # Дополнительные размеры
    'D_1': 'D_1',
    'P': 'P',
    'd_': 'd_',

    # Направление и параметры
    'Направление': 'direction',
    'B': 'B',
    'K': 'K',

    # Точность и дополнительные параметры
    'Точность': 'accuracy',
    'D_2': 'D_2',
    'l_1_': 'l_1_',
    'Серия': 'series',
    'omega_': 'omega_',
    'r_': 'r_',

    # Номинальные размеры
    'D_ном.': 'D_nominal',
    'D_1_доп.': 'D_1_additional',
    'D_2_доп.': 'D_2_additional',

    # Длины
    'L_1': 'L_1',
    'L_2': 'L_2',
    'L_3': 'L_3',
    'L_3_доп.': 'L_3_additional',

    # Разряд и тип хвостовика
    'Разряд': 'rank',
    'Тип_хвостовика': 'shank_type',

    # Отклонения
    'l_откл._': 'l_deviation',
    'L_откл.': 'L_deviation',
    'r_откл._': 'r_deviation',
    'l_0_': 'l_0_',
    'k_': 'k_',
    'K_откл.': 'K_deviation',
    'a_откл._': 'a_deviation',
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


def load_drills_from_csv(csv_file_path: str, session: Session) -> int:
    """
    Загружает данные сверл из CSV файла в таблицу geometry_drilling_cutter.

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

    logger.info(f"Начинаем загрузку данных сверл из файла: {csv_file_path}")

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row_num, row in enumerate(reader, start=2):  # Начинаем с 2, так как 1 - заголовок
            try:
                # Проверяем, что это сверло
                tool_type = row.get('Тип_инструмента', '').strip()
                if tool_type != 'Сверло':
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

                # Проверяем, не существует ли уже сверло для этого инструмента
                existing_drill = session.query(GeometryDrillingCutter).filter(GeometryDrillingCutter.tool_id == tool_id).first()
                if existing_drill:
                    logger.info(f"Строка {row_num}: Сверло для инструмента с id={tool_id} уже существует, пропускаем")
                    skipped_count += 1
                    continue

                # Создаем объект сверла
                drill_data = {}

                # Заполняем поля согласно маппингу
                for csv_col, model_field in DRILL_COLUMN_MAPPING.items():
                    if csv_col in row:
                        value = row[csv_col].strip()

                        # Определяем тип поля и парсим значение
                        field_type = getattr(GeometryDrillingCutter, model_field).type

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

                        drill_data[model_field] = parsed_value

                # Устанавливаем tool_id сверла равным id инструмента
                drill_data['tool_id'] = tool_id

                # Создаем и сохраняем сверло
                drill = GeometryDrillingCutter(**drill_data)
                session.add(drill)

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
        # Путь к CSV файлу со сверлами
        project_root = Path(__file__).parent.parent.parent.parent
        csv_file_path = project_root / "database_backups" / "tools_old.csv"

        # Получаем сессию базы данных
        with get_session() as session:
            loaded_count = load_drills_from_csv(csv_file_path, session)
            print(f"✅ Успешно загружено {loaded_count} записей сверл")

    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {e}")
        raise


if __name__ == "__main__":
    main()
