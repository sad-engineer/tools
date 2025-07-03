#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.mappers.base_mapper import BaseMapper


TURNING_FIELD_MAPPING = {
    'H': 'height_mm',                 # Высота резца -> высота
    'B': 'width_mm',                  # Ширина резца -> ширина
    'L': 'length_mm',                 # Длина резца -> длина
    'r': 'nose_radius_mm',            # Радиус при вершине -> радиус при вершине
    'fi': 'main_angle_grad',          # Главный угол -> главный угол
    'fi1': 'auxiliary_angle_grad',    # Вспомогательный угол -> вспомогательный угол
}


class TurningMapper(BaseMapper):
    """
    Маппер для резцов.
    
    Преобразует данные из таблицы geometry_turning_cutters в схему TurningCutter.
    
    Маппинг полей:
    - H (высота резца) -> height_mm
    - B (ширина резца) -> width_mm
    - L (длина резца) -> length_mm
    - r (радиус при вершине) -> nose_radius_mm
    - fi (главный угол) -> main_angle_grad
    - fi1 (вспомогательный угол) -> auxiliary_angle_grad
    """
    
    def __init__(self):
        super().__init__(
            tool_group="Резец",
            field_mapping=TURNING_FIELD_MAPPING,
            geometry_attr="geometry_turning_cutters"
        ) 