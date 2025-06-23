#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт для загрузки данных токарных резцов из CSV файла в таблицу geometry_turning_cutters.

Этот скрипт:
1. Читает CSV файл с данными токарных резцов
2. Фильтрует только строки с типом "Резец"
3. Загружает данные в таблицу geometry_turning_cutters
4. Связывает резцы с соответствующими инструментами из таблицы tools
    через поле tool_id
"""

from tools.app.db.loaders.base_loader import BaseGeometryLoader
from tools.app.models.geometry_turning_cutters import GeometryTurningCutters

# Маппинг колонок CSV на поля модели GeometryTurningCutters
TURNING_COLUMN_MAPPING = {
    # Основные геометрические параметры
    'a_': 'a_',
    'D': 'D',
    'l_': 'l_',
    'L': 'L',
    # Исполнение и углы
    'Исполнение': 'execution',
    'fi_': 'fi_',
    # Материал и группа
    'mat_': 'mat_',
    'Группа': 'group',
    # Дополнительные размеры
    'D_1': 'D_1',
    'd_': 'd_',
    # Направление и параметры
    'Направление': 'direction',
    'B': 'B',
    'h_': 'h_',
    'l_1_': 'l_1_',
    'm_': 'm_',
    'l_2_': 'l_2_',
    'r_': 'r_',
    'H': 'H',
    # Углы резца
    'fi_1_': 'fi_1_',
    'gamma_': 'gamma_',
    'lambda_': 'lambda_',
    # Дополнительные параметры
    'n_': 'n_',
    'bl_': 'bl_',
    # Тип резца и группа
    'Тип_резца': 'cutter_type',
    'h_1_': 'h_1_',
    'Группа_резца': 'cutter_group',
}

# Создаем загрузчик
loader = BaseGeometryLoader(
    tool_type="Резец", model_class=GeometryTurningCutters, column_mapping=TURNING_COLUMN_MAPPING
)


def load_turning_cutters():
    loader.run()


if __name__ == "__main__":
    load_turning_cutters()
