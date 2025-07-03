#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.mappers.base_mapper import BaseMapper


MILLING_FIELD_MAPPING = {
    'D': 'dia_mm',                    # Диаметр фрезы -> диаметр
    'L': 'length_mm',                 # Общая длина -> длина
    'z': 'num_of_cutting_blades',     # Количество зубьев -> количество режущих граней
    'l': 'cutting_length_mm',         # Длина резания -> длина резания
    'd': 'shank_dia_mm',              # Диаметр хвостовика -> диаметр хвостовика
}


class MillingMapper(BaseMapper):
    """
    Маппер для фрез.
    
    Преобразует данные из таблицы geometry_milling_cutters в схему MillingCutter.
    
    Маппинг полей:
    - D (диаметр фрезы) -> dia_mm
    - L (общая длина) -> length_mm
    - z (количество зубьев) -> num_of_cutting_blades
    - l (длина резания) -> cutting_length_mm
    - d (диаметр хвостовика) -> shank_dia_mm
    """
    
    def __init__(self):
        super().__init__(
            tool_group="Фреза",
            field_mapping=MILLING_FIELD_MAPPING,
            geometry_attr="geometry_milling_cutters"
        ) 