#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import pandas as pd
import logging
from pathlib import Path
from typing import Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def detect_encoding(file_path: str) -> str:
    """Определяет кодировку CSV файла."""
    import chardet
    
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        logger.info(f"Обнаружена кодировка: {encoding} (уверенность: {result['confidence']:.2f})")
        return encoding


def extract_milling_cutters(
    input_file: str = "database_backups/tools_old.csv",
    output_file: str = "database_backups/milling_cutters.csv",
    tool_type_column: str = "Тип_инструмента",
    tool_type_value: str = "Фреза"
) -> bool:
    """Извлекает фрезы из CSV файла и сохраняет в отдельный файл.
    
    Args:
        input_file (str): Путь к исходному CSV файлу
        output_file (str): Путь к выходному CSV файлу
        tool_type_column (str): Название колонки с типом инструмента
        tool_type_value (str): Значение для поиска фрез
        
    Returns:
        bool: True если операция успешна, False в противном случае
    """
    try:
        # Определяем путь к файлу
        project_root = Path(__file__).parent.parent.parent.parent
        input_path = project_root / input_file
        output_path = project_root / output_file
        
        # Проверяем существование входного файла
        if not input_path.exists():
            logger.error(f"Файл {input_path} не найден")
            return False
        
        # Определяем кодировку
        encoding = detect_encoding(str(input_path))
        
        # Читаем CSV файл
        logger.info(f"Загружаем данные из {input_path}")
        df = pd.read_csv(input_path, encoding=encoding)
        
        logger.info(f"Исходный файл содержит {len(df)} записей и {len(df.columns)} колонок")
        logger.info(f"Колонки: {list(df.columns)}")
        
        # Проверяем наличие колонки с типом инструмента
        if tool_type_column not in df.columns:
            logger.error(f"Колонка '{tool_type_column}' не найдена")
            logger.info(f"Доступные колонки: {list(df.columns)}")
            return False
        
        # Фильтруем фрезы
        logger.info(f"Ищем записи с '{tool_type_value}' в колонке '{tool_type_column}'")
        milling_cutters = df[df[tool_type_column] == tool_type_value].copy()
        
        logger.info(f"Найдено {len(milling_cutters)} фрез")
        
        if len(milling_cutters) == 0:
            logger.warning("Фрезы не найдены")
            return False
        
        # Удаляем полностью пустые колонки
        logger.info("Удаляем пустые колонки...")
        initial_columns = len(milling_cutters.columns)
        
        # Удаляем колонки, где все значения NaN или пустые строки
        milling_cutters = milling_cutters.dropna(axis=1, how='all')
        
        # Удаляем колонки, где все значения пустые строки
        empty_string_columns = []
        for col in milling_cutters.columns:
            if milling_cutters[col].dtype == 'object':  # Строковые колонки
                if (milling_cutters[col].astype(str).str.strip() == '').all():
                    empty_string_columns.append(col)
        
        if empty_string_columns:
            logger.info(f"Удаляем колонки с пустыми строками: {empty_string_columns}")
            milling_cutters = milling_cutters.drop(columns=empty_string_columns)
        
        final_columns = len(milling_cutters.columns)
        logger.info(f"Удалено {initial_columns - final_columns} пустых колонок")
        logger.info(f"Осталось {final_columns} колонок")
        
        # Показываем статистику по колонкам
        logger.info("Статистика по колонкам:")
        for col in milling_cutters.columns:
            non_null_count = milling_cutters[col].notna().sum()
            logger.info(f"  {col}: {non_null_count}/{len(milling_cutters)} заполненных значений")
        
        # Создаем директорию для выходного файла
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Сохраняем результат
        milling_cutters.to_csv(output_path, index=False, encoding='utf-8')
        
        logger.info(f"✅ Фрезы сохранены в {output_path}")
        logger.info(f"📊 Размер файла: {output_path.stat().st_size / 1024:.1f} KB")
        
        # Показываем первые несколько записей
        logger.info("Первые 3 фрезы:")
        for i, (_, row) in enumerate(milling_cutters.head(3).iterrows(), 1):
            logger.info(f"  {i}. {dict(row)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при обработке файла: {e}")
        return False


def main():
    """Основная функция."""
    try:
        logger.info("🚀 Извлекаем инструменты из CSV файла")
        
        success = extract_milling_cutters(
            tool_type_value="Зенкер",
            output_file="database_backups/countersinking_cutters.txt"
        )
        
        if success:
            logger.info("✅ Операция завершена успешно")
        else:
            logger.error("❌ Операция завершена с ошибками")
            
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        raise


if __name__ == "__main__":
    main()
