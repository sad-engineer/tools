#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from pydantic import Field
from tolerance import Tolerance

from tools.app.schemas.blade_material import BladeMaterial
from tools.app.schemas.sizes import Angles, AxialSizes
from tools.app.schemas.tool import Tool


class AxialCuttingTool(Tool, AxialSizes, BladeMaterial, Angles, validate_assignment=True, arbitrary_types_allowed=True):
    """Осевой режущий инструмент.

    Наследует параметры от:
    - Tool: group, marking, standard
    - AxialSizes: dia_mm, length_mm, radius_of_cutting_vertex
    - BladeMaterial: mat_of_cutting_part
    - Angles: main_angle_grad, front_angle_grad, inclination_of_main_blade_grad

    Parameters:
    num_of_cutting_blades : (int >= 0) : количество режущих граней.
    tolerance : (Tolerance) : допуск инструмента.

    Properties:
    name : (str) : возвращает название инструмента.
    gabarit_volume : (float) : возвращает габаритный объем.
    gabarit_str : (str) : возвращает габарит, записанный строкой.
    type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
    to_dict : (dict) : возвращает словарь всех параметров и свойств инструмента.
    """

    num_of_cutting_blades: int = Field(default=1, gt=0, description="Количество режущих граней")
    tolerance: Tolerance = Tolerance.set_from_string("H14")

    def to_dict(self):
        # Получаем параметры из базовых классов через их свойства _parameters
        tool_parameters = Tool._parameters.__get__(self)  # Параметры из Tool
        size_parameters = AxialSizes._parameters.__get__(self)  # Параметры из AxialSizes
        blade_material_parameters = BladeMaterial._parameters.__get__(self)  # Параметры из BladeMaterial
        angles_parameters = Angles._parameters.__get__(self)  # Параметры из Angles

        # Создаем словарь с параметрами текущего класса
        current_parameters = {
            "tolerance_parameters": str(self.tolerance),
            "num_of_cutting_blades": self.num_of_cutting_blades,
        }

        # Объединяем все параметры
        return tool_parameters | size_parameters | blade_material_parameters | angles_parameters | current_parameters


if __name__ == '__main__':
    # Пример использования AxialCuttingTool
    print("=== Пример использования AxialCuttingTool ===")

    # Создание осевого режущего инструмента с дефолтными значениями
    tool = AxialCuttingTool()
    print(f"Инструмент по умолчанию: {tool}")
    print(f"Группа: {tool.group}")
    print(f"Имя: {tool.name}")
    print(f"Количество режущих граней: {tool.num_of_cutting_blades}")
    print(f"Диаметр: {tool.dia_mm} мм")
    print(f"Длина: {tool.length_mm} мм")
    print(f"Габарит: {tool.gabarit_str}")
    print(f"Материал: {tool.mat_of_cutting_part}")
    print(f"Тип материала: {tool.type_of_mat}")
    print(f"Допуск: {tool.tolerance}")

    # Демонстрация метода to_dict
    print("\n=== Все параметры инструмента ===")
    parameters = tool.to_dict()
    for key, value in parameters.items():
        print(f"{key}: {value}")

    # Изменение параметров
    print("\n=== Изменение параметров ===")
    tool.marking = "ИНСТ-10-100"
    tool.standard = "ГОСТ 1000-90"
    tool.dia_mm = 10.0
    tool.length_mm = 100.0
    tool.num_of_cutting_blades = 4
    tool.mat_of_cutting_part = "Р18"
    tool.main_angle_grad = 45
    tool.front_angle_grad = 5
    tool.inclination_of_main_blade_grad = 2
    tool.radius_of_cutting_vertex = 0.5

    print(f"Обновленный инструмент: {tool}")
    print(f"Новое имя: {tool.name}")
    print(f"Габарит: {tool.gabarit_str}")
    print(f"Объем: {tool.gabarit_volume} мм³")

    # Проверка валидации
    print("\n=== Проверка валидации ===")
    try:
        tool.num_of_cutting_blades = 0  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации количества граней: {e}")

    try:
        tool.dia_mm = -5  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации диаметра: {e}")
