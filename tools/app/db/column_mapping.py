#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Настройки сопоставления колонок CSV файла с полями модели Tool.

Этот файл содержит словарь, который определяет, какие колонки из CSV файла
соответствуют каким полям в модели Tool.
"""

# Сопоставление колонок CSV с полями модели
CSV_TO_MODEL_MAPPING = {
    # Основные поля
    'Обозначение': 'marking',
    'Группа': 'group',
    'Стандарт': 'standard',
    # Альтернативные названия колонок (если они могут отличаться)
    'Обозначение инструмента': 'marking',
    'Группа инструмента': 'group',
    'Нормативный документ': 'standard',
    'ГОСТ': 'standard',
    # Английские названия (если есть)
    'marking': 'marking',
    'group': 'group',
    'standard': 'standard',
}

# Обязательные поля (должны присутствовать в CSV)
REQUIRED_FIELDS = ['marking']

# Поля, которые могут быть пустыми
OPTIONAL_FIELDS = ['group', 'standard']


# Функция для поиска подходящей колонки
def find_column_mapping(csv_columns: list) -> dict:
    """
    Находит сопоставление между колонками CSV и полями модели.

    Args:
        csv_columns (list): Список названий колонок в CSV

    Returns:
        dict: Словарь {поле_модели: название_колонки_csv}
    """
    mapping = {}

    for csv_col in csv_columns:
        if csv_col in CSV_TO_MODEL_MAPPING:
            model_field = CSV_TO_MODEL_MAPPING[csv_col]
            mapping[model_field] = csv_col
            print(f"✅ Найдено сопоставление: '{csv_col}' → {model_field}")

    # Проверяем обязательные поля
    missing_fields = []
    for field in REQUIRED_FIELDS:
        if field not in mapping:
            missing_fields.append(field)

    if missing_fields:
        print(f"❌ Не найдены обязательные поля: {missing_fields}")
        print(f"Доступные колонки в CSV: {csv_columns}")
        raise ValueError(f"Отсутствуют обязательные поля: {missing_fields}")

    return mapping
