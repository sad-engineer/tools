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

from tools.app.db.loaders.base_loader import BaseGeometryLoader
from tools.app.models.geometry_milling_cutters import GeometryMillingCutters

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

# Создаем загрузчик
loader = BaseGeometryLoader(
    tool_type="Фреза", model_class=GeometryMillingCutters, column_mapping=MILLING_CUTTER_COLUMN_MAPPING
)

def load_milling_cutters():
    loader.run()

if __name__ == "__main__":
    load_milling_cutters()
