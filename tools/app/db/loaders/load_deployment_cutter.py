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

from tools.app.db.loaders.base_loader import BaseGeometryLoader
from tools.app.models.geometry_deployment_cutter import GeometryDeploymentCutter

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

# Создаем загрузчик
loader = BaseGeometryLoader(
    tool_type="Развертка", model_class=GeometryDeploymentCutter, column_mapping=DEPLOYMENT_COLUMN_MAPPING
)


def load_deployment_cutters():
    loader.run()


if __name__ == "__main__":
    load_deployment_cutters()
