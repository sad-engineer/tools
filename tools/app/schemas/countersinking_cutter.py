#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from pydantic import Field

from tools.app.enumerations import ToolGroups
from tools.app.schemas.axial_cutting_tool import AxialCuttingTool


class CountersinkingCutter(AxialCuttingTool):
    """Зенкер - это инструмент класса AxialCuttingTool с 8 (или более) режущими кромками.

    Наследует параметры от AxialCuttingTool:
    - Tool: group, marking, standard
    - AxialSizes: dia_mm, length_mm, radius_of_cutting_vertex
    - BladeMaterial: mat_of_cutting_part
    - Angles: main_angle_grad, front_angle_grad, inclination_of_main_blade_grad
    - tolerance: допуск инструмента

    Parameters:
    num_of_cutting_blades : (int >= 0) : количество режущих граней (по умолчанию 8).

    Properties:
    name : (str) : возвращает название инструмента.
    group : (str) : возвращает группу инструмента (всегда "Зенкер").
    gabarit_volume : (float) : возвращает габаритный объем.
    gabarit_str : (str) : возвращает габарит, записанный строкой.
    type_of_mat : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
    to_dict : (dict) : возвращает словарь всех параметров и свойств.
    """

    _group = ToolGroups.COUNTERSINK
    num_of_cutting_blades: int = Field(default=8, gt=0, description="Количество режущих граней")

    def to_dict(self):
        """Возвращает словарь всех параметров и свойств зенкера.

        Returns:
            dict: Словарь с параметрами зенкера
        """
        # Получаем параметры из базового класса
        base_parameters = super().to_dict()

        # Создаем словарь с параметрами текущего класса
        current_parameters = {
            "num_of_cutting_blades": self.num_of_cutting_blades,
        }

        # Объединяем параметры
        return base_parameters | current_parameters


if __name__ == '__main__':
    # Пример использования CountersinkingCutter
    print("=== Пример использования CountersinkingCutter ===")

    # Создание зенкера с дефолтными значениями
    countersink = CountersinkingCutter()
    print(f"Зенкер по умолчанию: {countersink}")
    print(f"Группа: {countersink.group}")
    print(f"Имя: {countersink.name}")
    print(f"Количество режущих граней: {countersink.num_of_cutting_blades}")
    print(f"Диаметр: {countersink.dia_mm} мм")
    print(f"Длина: {countersink.length_mm} мм")
    print(f"Габарит: {countersink.gabarit_str}")
    print(f"Материал: {countersink.mat_of_cutting_part}")
    print(f"Тип материала: {countersink.type_of_mat}")
    print(f"Допуск: {countersink.tolerance}")

    # Изменение параметров
    print("\n=== Изменение параметров ===")
    countersink.marking = "ЗЕН-20-150"
    countersink.standard = "ГОСТ 12489-71"
    countersink.dia_mm = 20.0
    countersink.length_mm = 150.0
    countersink.num_of_cutting_blades = 10
    countersink.mat_of_cutting_part = "Р18"
    countersink.main_angle_grad = 90
    countersink.front_angle_grad = 0
    countersink.inclination_of_main_blade_grad = 0
    countersink.radius_of_cutting_vertex = 1.0

    print(f"Обновленный зенкер: {countersink}")
    print(f"Новое имя: {countersink.name}")
    print(f"Группа осталась: {countersink.group}")
    print(f"Габарит: {countersink.gabarit_str}")
    print(f"Объем: {countersink.gabarit_volume} мм³")

    # Получение всех параметров
    print("\n=== Все параметры зенкера ===")
    parameters = countersink.to_dict()
    for key, value in parameters.items():
        print(f"{key}: {value}")

    # Проверка валидации
    print("\n=== Проверка валидации ===")
    try:
        countersink.num_of_cutting_blades = 0  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации количества граней: {e}")

    try:
        countersink.dia_mm = -5  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации диаметра: {e}")

    # Создание зенкера с кастомными параметрами
    print("\n=== Создание зенкера с кастомными параметрами ===")
    custom_countersink = CountersinkingCutter(
        marking="ЗЕН-25-200",
        standard="ГОСТ 12489-71",
        dia_mm=25.0,
        length_mm=200.0,
        num_of_cutting_blades=12,
        mat_of_cutting_part="Т15К6",
        main_angle_grad=120,
        front_angle_grad=5,
        inclination_of_main_blade_grad=2,
        radius_of_cutting_vertex=1.5,
    )

    print(f"Кастомный зенкер: {custom_countersink}")
    print(f"Имя: {custom_countersink.name}")
    print(f"Группа: {custom_countersink.group}")
    print(f"Количество граней: {custom_countersink.num_of_cutting_blades}")
    print(f"Материал: {custom_countersink.mat_of_cutting_part}")
    print(f"Тип материала: {custom_countersink.type_of_mat}")

    # Демонстрация наследования свойств
    print("\n=== Демонстрация наследования ===")
    print(f"Зенкер наследует от Tool: {countersink.name}")
    print(f"Зенкер наследует от AxialSizes: {countersink.gabarit_volume} мм³")
    print(f"Зенкер наследует от BladeMaterial: {countersink.type_of_mat}")
    print(f"Зенкер наследует от Angles: {countersink.main_angle_grad}°")

    # Проверка сериализации
    print("\n=== Сериализация в dict ===")
    countersink_dict = countersink.model_dump()
    print(f"Dict: {countersink_dict}")

    # Проверка десериализации
    print("\n=== Десериализация из dict ===")
    countersink_from_dict = CountersinkingCutter(**countersink_dict)
    print(f"Зенкер из dict: {countersink_from_dict}")
    print(f"Идентичны: {countersink == countersink_from_dict}")
