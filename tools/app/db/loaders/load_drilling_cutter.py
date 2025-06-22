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

from tools.app.db.loaders.base_loader import BaseGeometryLoader
from tools.app.models.geometry_drilling_cutter import GeometryDrillingCutter

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

# Создаем загрузчик
loader = BaseGeometryLoader(tool_type="Сверло", model_class=GeometryDrillingCutter, column_mapping=DRILL_COLUMN_MAPPING)

def load_drilling_cutters():
    loader.run()

if __name__ == "__main__":
    load_drilling_cutters()
