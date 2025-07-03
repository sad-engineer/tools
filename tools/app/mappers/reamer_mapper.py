#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.mappers.base_mapper import BaseMapper


REAMER_FIELD_MAPPING = {
    'D': 'dia_mm',                    # Диаметр развертки -> диаметр
    'L': 'length_mm',                 # Общая длина -> длина
    'l': 'cutting_length_mm',         # Длина резания -> длина резания
    'z': 'num_of_cutting_blades',     # Количество зубьев -> количество режущих граней
    'fi': 'main_angle_grad',          # Главный угол -> главный угол
    'd': 'shank_dia_mm',              # Диаметр хвостовика -> диаметр хвостовика
}


class ReamerMapper(BaseMapper):
    """
    Маппер для разверток.
    
    Преобразует данные из таблицы geometry_reamer в схему ReamerCutter.
    
    Маппинг полей:
    - D (диаметр развертки) -> dia_mm
    - L (общая длина) -> length_mm
    - l (длина резания) -> cutting_length_mm
    - z (количество зубьев) -> num_of_cutting_blades
    - fi (главный угол) -> main_angle_grad
    - d (диаметр хвостовика) -> shank_dia_mm
    """
    
    def __init__(self):
        super().__init__(
            tool_group="Развертка",
            field_mapping=REAMER_FIELD_MAPPING,
            geometry_attr="geometry_reamer"
        ) 