#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.mappers.base_mapper import BaseMapper


DRILLING_FIELD_MAPPING = {
    'D': 'dia_mm',                    # Диаметр сверла -> диаметр
    'L': 'length_mm',                 # Общая длина -> длина
    'l': 'cutting_length_mm',         # Длина резания -> длина резания
    'd': 'shank_dia_mm',              # Диаметр хвостовика -> диаметр хвостовика
    'fi': 'point_angle_grad',         # Угол при вершине -> угол при вершине
}


class DrillingMapper(BaseMapper):
    """
    Маппер для сверл.
    
    Преобразует данные из таблицы geometry_drilling_cutter в схему DrillingCutter.
    
    Маппинг полей:
    - D (диаметр сверла) -> dia_mm
    - L (общая длина) -> length_mm
    - l (длина резания) -> cutting_length_mm
    - d (диаметр хвостовика) -> shank_dia_mm
    - fi (угол при вершине) -> point_angle_grad
    """
    
    def __init__(self):
        super().__init__(
            tool_group="Сверло",
            field_mapping=DRILLING_FIELD_MAPPING,
            geometry_attr="geometry_drilling_cutter"
        ) 