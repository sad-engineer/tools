#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт для загрузки данных фрез из CSV файла в таблицу geometry_milling_cutters.

Этот скрипт:
1. Читает CSV файл с данными фрез
2. Фильтрует только строки с типом "Фреза"
3. Загружает данные в таблицу geometry_milling_cutters
4. Связывает фрезы с соответствующими инструментами из таблицы tools
    через поле tool_id
"""

import csv
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from tools.app.db.session_manager import get_session
from tools.app.models.geometry_milling_cutters import GeometryMillingCutters
from tools.app.models.tools import Tool

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Маппинг колонок CSV на поля модели GeometryMillingCutters
MILLING_CUTTER_COLUMN_MAPPING = {
    # Основные геометрические параметры
    'D': 'D',
    'L': 'L',
    'l': 'l',
    'd': 'd',
    'z': 'z',
    # Дополнительные геометрические параметры
    'a_': 'a_',
    'd_1_': 'd_1_',
    'd_2_': 'd_2_',
    'l_': 'l_',
    'L_': 'L_',
    'f_': 'f_',
    'q_': 'q_',
    # Конусы и исполнения
    'Конус_Морзе': 'morse_taper',
    'Исполнение': 'execution',
    'fi_': 'fi_',
    'type_cutter_': 'type_cutter_',
    # Материалы и типы
    'mat_': 'material',
    'type_of_cutting_part_': 'type_of_cutting_part_',
    'Группа': 'group',
    # Дополнительные размеры
    'D_1': 'D_1',
    'f_доп._': 'f_additional_',
    'D_доп.': 'D_additional',
    'P': 'P',
    'l_номин._': 'l_nominal_',
    'd_': 'd_',
    'd_доп._': 'd_additional_',
    'd_1_доп._': 'd_1_additional_',
    # Направление и параметры
    'Направление': 'direction',
    'B': 'B',
    'c_': 'c_',
    'c_доп._': 'c_additional_',
    'h_': 'h_',
    'R': 'R',
    'R_доп.': 'R_additional',
    'm_n0_': 'm_n0_',
    'L_доп.': 'L_additional',
    'K': 'K',
    'K_доп.': 'K_additional',
    # Точность и дополнительные параметры
    'Точность': 'accuracy',
    'D_2': 'D_2',
    'l_1_': 'l_1_',
    'f_откл._': 'f_deviation_',
    'g_': 'g_',
    'g_откл._': 'g_deviation_',
    'zxd_xD': 'zxd_xD',
    'z_0_': 'z_0_',
    'Серия': 'series',
    'Точность_паза': 'groove_accuracy',
    'm_0_': 'm_0_',
    'Подгруппа': 'subgroup',
    'h_доп._': 'h_additional_',
    'm_': 'm_',
    # Метрические параметры
    'Метрический_хвостовик': 'metric_shank',
    'b_': 'b_',
    'S': 'S',
    't_': 't_',
    'd_0_': 'd_0_',
    'l_доп._': 'l_additional_',
    'omega_': 'omega_',
    'l_2_': 'l_2_',
    'r_': 'r_',
    'r_доп._': 'r_additional_',
    'B_доп.': 'B_additional',
    'H': 'H',
    'omega_u_': 'omega_u_',
    'D_откл.': 'D_deviation',
    'c_общего_назначения_': 'c_general_purpose_',
    'c_для_шпоночных_пазов_': 'c_keyway_',
    'Конус_метрический': 'metric_taper',
    'alpha_': 'alpha_',
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


def load_geometry_milling_cutters_from_csv(csv_file_path: str, session: Session) -> int:
    """
    Загружает данные фрез из CSV файла в таблицу geometry_milling_cutters.

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

    logger.info(f"Начинаем загрузку данных фрез из файла: {csv_file_path}")

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row_num, row in enumerate(reader, start=2):  # Начинаем с 2, так как 1 - заголовок
            try:
                # Проверяем, что это фреза
                tool_type = row.get('Тип_инструмента', '').strip()
                if tool_type != 'Фреза':
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

                # Проверяем, не существует ли уже фреза для этого инструмента
                # Теперь проверяем по tool_id
                existing_cutter = (
                    session.query(GeometryMillingCutters).filter(GeometryMillingCutters.tool_id == tool.id).first()
                )
                if existing_cutter:
                    logger.info(f"Строка {row_num}: Фреза для инструмента с id={tool.id} уже существует, пропускаем")
                    skipped_count += 1
                    continue

                # Создаем объект фрезы
                cutter_data = {}

                # Заполняем поля согласно маппингу
                for csv_col, model_field in MILLING_CUTTER_COLUMN_MAPPING.items():
                    if csv_col in row:
                        value = row[csv_col].strip()

                        # Определяем тип поля и парсим значение
                        field_type = getattr(GeometryMillingCutters, model_field).type

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

                        cutter_data[model_field] = parsed_value

                # Устанавливаем связь с инструментом через tool_id
                cutter_data['tool_id'] = tool.id

                # Создаем и сохраняем фрезу
                cutter = GeometryMillingCutters(**cutter_data)
                session.add(cutter)

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
        # Путь к CSV файлу с фрезами
        project_root = Path(__file__).parent.parent.parent.parent
        csv_file_path = project_root / "database_backups" / "tools_old.csv"

        # Получаем сессию базы данных
        with get_session() as session:
            loaded_count = load_geometry_milling_cutters_from_csv(csv_file_path, session)
            print(f"✅ Успешно загружено {loaded_count} записей фрез")

    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {e}")
        raise


if __name__ == "__main__":
    main()
