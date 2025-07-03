#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.mappers.base_mapper import BaseMapper


BROACHING_FIELD_MAPPING = {
    'H': 'height_mm',                 # Высота протяжки -> высота
    'B': 'width_mm',                  # Ширина протяжки -> ширина
    'L': 'length_mm',                 # Длина протяжки -> длина
    'z': 'num_of_cutting_blades',     # Количество зубьев -> количество режущих граней
    't': 'pitch_mm',                  # Шаг зубьев -> шаг зубьев
    'h': 'cutting_depth_mm',          # Глубина резания -> глубина резания
}


class BroachingMapper(BaseMapper):
    """
    Маппер для протяжек.
    
    Преобразует данные из таблицы geometry_broaching_cutter в схему BroachingCutter.
    
    Маппинг полей:
    - H (высота протяжки) -> height_mm
    - B (ширина протяжки) -> width_mm
    - L (длина протяжки) -> length_mm
    - z (количество зубьев) -> num_of_cutting_blades
    - t (шаг зубьев) -> pitch_mm
    - h (глубина резания) -> cutting_depth_mm
    """
    
    def __init__(self):
        super().__init__(
            tool_group="Протяжка",
            field_mapping=BROACHING_FIELD_MAPPING,
            geometry_attr="geometry_broaching_cutter"
        ) 