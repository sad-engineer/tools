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

from tools.app.db.loaders.base_loader import BaseGeometryLoader
from tools.app.models.geometry_countersinking_cutter import GeometryCountersinkingCutter

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

# Создаем загрузчик
loader = BaseGeometryLoader(
    tool_type="Зенкер", model_class=GeometryCountersinkingCutter, column_mapping=COUNTERSINKING_COLUMN_MAPPING
)

def load_countersinking_cutters():
    loader.run()    
    
if __name__ == "__main__":
    load_countersinking_cutters()
