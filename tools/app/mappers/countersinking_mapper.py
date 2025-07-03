#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.mappers.base_mapper import BaseMapper


COUNTERSINKING_FIELD_MAPPING = {
    'D': 'dia_mm',                    # Диаметр зенкера -> диаметр
    'L': 'length_mm',                 # Общая длина -> длина
    'z': 'num_of_cutting_blades',     # Количество зубьев -> количество режущих граней
    'fi_': 'main_angle_grad',         # Угол fi -> главный угол
    'l_': 'radius_of_cutting_vertex', # Длина рабочей части -> радиус режущей вершины
}


class CountersinkingMapper(BaseMapper):
    """
    Маппер для зенкеров.
    
    Преобразует данные из таблицы geometry_countersinking_cutter в схему CountersinkingCutter.
    
    Маппинг полей:
    - D (диаметр зенкера) -> dia_mm
    - L (общая длина) -> length_mm
    - z (количество зубьев) -> num_of_cutting_blades
    - fi_ (угол fi) -> main_angle_grad
    - l_ (длина рабочей части) -> radius_of_cutting_vertex (как радиус режущей вершины)
    """
    
    def __init__(self):
        super().__init__(
            tool_group="Зенкер",
            field_mapping=COUNTERSINKING_FIELD_MAPPING,
            geometry_attr="geometry_countersinking_cutter"
        )
