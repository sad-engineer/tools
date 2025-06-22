#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Базовый класс для загрузки данных из CSV файла в таблицы геометрии инструментов.

Этот класс содержит общую логику для всех скриптов загрузки:
- Парсинг CSV файла
- Фильтрация по типу инструмента
- Поиск соответствующего инструмента в таблице tools
- Проверка существования записи
- Парсинг значений
- Сохранение в базу данных
"""

import csv
import logging
from abc import ABC
from pathlib import Path
from typing import Any, Dict, Optional, Type

from sqlalchemy.orm import Session

from tools.app.db.session_manager import get_session
from tools.app.models.tools import Tool

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseGeometryLoader(ABC):
    """Базовый класс для загрузки геометрических данных инструментов."""

    def __init__(self, tool_type: str, model_class: Type, column_mapping: Dict[str, str]):
        """
        Инициализация загрузчика.

        Args:
            tool_type: Тип инструмента для фильтрации (например, "Фреза", "Сверло")
            model_class: Класс модели SQLAlchemy
            column_mapping: Маппинг колонок CSV на поля модели
        """
        self.tool_type = tool_type
        self.model_class = model_class
        self.column_mapping = column_mapping

    @staticmethod
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

    @staticmethod
    def parse_int(value: str) -> Optional[int]:
        """Парсит строку в int, возвращает None если не удается."""
        if not value or value.strip() == '':
            return None
        try:
            return int(float(value))  # Сначала парсим как float, затем конвертируем в int
        except (ValueError, TypeError):
            return None

    @staticmethod
    def get_tool_id(row: Dict[str, str], row_num: int) -> Optional[int]:
        """Получает и валидирует ID инструмента из строки CSV."""
        id_str = row.get('index', '').strip()
        if not id_str:
            logger.warning(f"Строка {row_num}: Отсутствует id инструмента")
            return None

        try:
            return int(id_str)
        except ValueError:
            logger.warning(f"Строка {row_num}: Некорректный id '{id_str}' - не является числом")
            return None

    @staticmethod
    def find_tool(session: Session, tool_id: int, row_num: int) -> Optional[Tool]:
        """Находит инструмент в таблице tools по ID."""
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
            return None
        return tool

    def check_existing_record(self, session: Session, tool_id: int, row_num: int) -> bool:
        """Проверяет, существует ли уже запись для данного инструмента."""
        existing_record = session.query(self.model_class).filter(self.model_class.tool_id == tool_id).first()

        if existing_record:
            logger.info(f"Строка {row_num}: {self.tool_type} для инструмента с id={tool_id} уже существует, пропускаем")
            return True
        return False

    def parse_row_data(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Парсит данные строки CSV в словарь для модели."""
        data = {}

        for csv_col, model_field in self.column_mapping.items():
            if csv_col in row:
                value = row[csv_col].strip()

                # Определяем тип поля и парсим значение
                field_type = getattr(self.model_class, model_field).type

                if hasattr(field_type, 'python_type'):
                    if field_type.python_type == float:
                        parsed_value = self.parse_float(value)
                    elif field_type.python_type == int:
                        parsed_value = self.parse_int(value)
                    else:
                        parsed_value = value if value else None
                else:
                    # Для сложных типов (например, DateTime) оставляем как есть
                    parsed_value = value if value else None

                data[model_field] = parsed_value

        return data

    def process_row(self, row: Dict[str, str], row_num: int, session: Session) -> bool:
        """
        Обрабатывает одну строку CSV.

        Returns:
            bool: True если запись была загружена, False если пропущена
        """
        try:
            # Проверяем тип инструмента
            tool_type = row.get('Тип_инструмента', '').strip()
            if tool_type != self.tool_type:
                return False

            # Получаем ID инструмента
            tool_id = self.get_tool_id(row, row_num)
            if tool_id is None:
                return False

            # Ищем инструмент в базе
            tool = self.find_tool(session, tool_id, row_num)
            if tool is None:
                return False

            # Проверяем существование записи
            if self.check_existing_record(session, tool_id, row_num):
                return False

            # Парсим данные
            data = self.parse_row_data(row)
            data['tool_id'] = tool_id

            # Создаем и сохраняем запись
            record = self.model_class(**data)
            session.add(record)

            return True

        except Exception as e:
            logger.error(f"Ошибка при обработке строки {row_num}: {e}")
            session.rollback()
            return False

    def load_from_csv(self, csv_file_path: str, session: Session) -> int:
        """
        Загружает данные из CSV файла в таблицу.

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

        logger.info(f"Начинаем загрузку данных {self.tool_type} из файла: {csv_file_path}")

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row_num, row in enumerate(reader, start=2):  # Начинаем с 2, так как 1 - заголовок
                if self.process_row(row, row_num, session):
                    loaded_count += 1
                    if loaded_count % 100 == 0:
                        logger.info(f"Загружено {loaded_count} записей...")
                else:
                    skipped_count += 1

        # Сохраняем все изменения
        try:
            session.commit()
            logger.info(f"Загрузка завершена. Загружено: {loaded_count}, Пропущено: {skipped_count}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных: {e}")
            session.rollback()
            raise

        return loaded_count

    def run(self, csv_file_path: str = None) -> int:
        """
        Основная функция для запуска загрузки.

        Args:
            csv_file_path: Путь к CSV файлу (если не указан, используется tools_old.csv)

        Returns:
            Количество загруженных записей
        """
        if csv_file_path is None:
            # Определяем путь к CSV файлу относительно корня проекта
            project_root = Path(__file__).parent.parent.parent.parent
            csv_file_path = project_root / "database_backups" / "tools_old.csv"

        try:
            with get_session() as session:
                loaded_count = self.load_from_csv(csv_file_path, session)
                print(f"✅ Успешно загружено {loaded_count} записей {self.tool_type}")
                return loaded_count

        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            raise
