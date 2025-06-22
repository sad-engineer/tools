#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from pydantic import Field
from tolerance import Tolerance

from tools.app.schemas.blade_material import BladeMaterial
from tools.app.schemas.sizes import Angles, PrismaticSizes
from tools.app.schemas.tool import Tool


class PrismaticCuttingTool(
    Tool, PrismaticSizes, BladeMaterial, Angles, validate_assignment=True, arbitrary_types_allowed=True
):
    """Призматический режущий инструмент.

    Наследует параметры от:
    - Tool: group, marking, standard
    - PrismaticSizes: length_mm, width_mm, height_mm, radius_of_cutting_vertex
    - BladeMaterial: mat_of_cutting_part
    - Angles: main_angle_grad, front_angle_grad, inclination_of_main_blade_grad

    Parameters:
    num_of_cutting_blades : (int >= 0) : количество режущих граней.
    tolerance : (Tolerance) : допуск инструмента.

    Properties:
    name : (str) : возвращает название инструмента.
    gabarit_volume : (float) : возвращает габаритный объем.
    gabarit_str : (str) : возвращает габарит, записанный строкой.
    type_of_mat : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
    to_dict : (dict) : возвращает словарь всех параметров и свойств.
    """

    num_of_cutting_blades: int = Field(default=1, gt=0, description="Количество режущих граней")
    tolerance: Tolerance = Tolerance.set_from_string("H14")

    def to_dict(self):
        """Возвращает словарь всех параметров и свойств призматического инструмента.

        Returns:
            dict: Словарь с параметрами инструмента
        """
        # Получаем параметры из базовых классов через их свойства _parameters
        tool_parameters = Tool._parameters.__get__(self)  # Параметры из Tool
        size_parameters = PrismaticSizes._parameters.__get__(self)  # Параметры из PrismaticSizes
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
    # Пример использования PrismaticCuttingTool
    print("=== Пример использования PrismaticCuttingTool ===")

    # Создание призматического инструмента с дефолтными значениями
    tool = PrismaticCuttingTool()
    print(f"Инструмент по умолчанию: {tool}")
    print(f"Группа: {tool.group}")
    print(f"Имя: {tool.name}")
    print(f"Количество режущих граней: {tool.num_of_cutting_blades}")
    print(f"Длина: {tool.length_mm} мм")
    print(f"Ширина: {tool.width_mm} мм")
    print(f"Высота: {tool.height_mm} мм")
    print(f"Габарит: {tool.gabarit_str}")
    print(f"Материал: {tool.mat_of_cutting_part}")
    print(f"Тип материала: {tool.type_of_mat}")
    print(f"Допуск: {tool.tolerance}")

    # Изменение параметров
    print("\n=== Изменение параметров ===")
    tool.marking = "ПРИЗМ-25-16-25"
    tool.standard = "ГОСТ 1000-90"
    tool.length_mm = 200.0
    tool.width_mm = 20.0
    tool.height_mm = 30.0
    tool.num_of_cutting_blades = 4
    tool.mat_of_cutting_part = "Р18"
    tool.main_angle_grad = 45
    tool.front_angle_grad = 5
    tool.inclination_of_main_blade_grad = 2
    tool.radius_of_cutting_vertex = 1.0

    print(f"Обновленный инструмент: {tool}")
    print(f"Новое имя: {tool.name}")
    print(f"Габарит: {tool.gabarit_str}")
    print(f"Объем: {tool.gabarit_volume} мм³")

    # Получение всех параметров
    print("\n=== Все параметры инструмента ===")
    parameters = tool.to_dict()
    for key, value in parameters.items():
        print(f"{key}: {value}")

    # Проверка валидации
    print("\n=== Проверка валидации ===")
    try:
        tool.num_of_cutting_blades = 0  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации количества граней: {e}")

    try:
        tool.length_mm = -5  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации длины: {e}")

    # Создание инструмента с кастомными параметрами
    print("\n=== Создание инструмента с кастомными параметрами ===")
    custom_tool = PrismaticCuttingTool(
        marking="ПРИЗМ-30-20-35",
        standard="ГОСТ 1000-90",
        length_mm=250.0,
        width_mm=25.0,
        height_mm=40.0,
        num_of_cutting_blades=6,
        mat_of_cutting_part="Т15К6",
        main_angle_grad=60,
        front_angle_grad=10,
        inclination_of_main_blade_grad=5,
        radius_of_cutting_vertex=1.5,
    )

    print(f"Кастомный инструмент: {custom_tool}")
    print(f"Имя: {custom_tool.name}")
    print(f"Группа: {custom_tool.group}")
    print(f"Количество граней: {custom_tool.num_of_cutting_blades}")
    print(f"Материал: {custom_tool.mat_of_cutting_part}")
    print(f"Тип материала: {custom_tool.type_of_mat}")

    # Демонстрация наследования свойств
    print("\n=== Демонстрация наследования ===")
    print(f"Инструмент наследует от Tool: {tool.name}")
    print(f"Инструмент наследует от PrismaticSizes: {tool.gabarit_volume} мм³")
    print(f"Инструмент наследует от BladeMaterial: {tool.type_of_mat}")
    print(f"Инструмент наследует от Angles: {tool.main_angle_grad}°")

    # Проверка сериализации
    print("\n=== Сериализация в dict ===")
    tool_dict = tool.model_dump()
    print(f"Dict: {tool_dict}")

    # Проверка десериализации
    print("\n=== Десериализация из dict ===")
    tool_from_dict = PrismaticCuttingTool(**tool_dict)
    print(f"Инструмент из dict: {tool_from_dict}")
    print(f"Идентичны: {tool == tool_from_dict}")
