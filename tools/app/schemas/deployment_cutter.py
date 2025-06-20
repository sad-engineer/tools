#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from pydantic import Field

from tools.app.enumerations import ToolGroups
from tools.app.schemas.axial_cutting_tool import AxialCuttingTool


class DeploymentCutter(AxialCuttingTool):
    """Развертка - это инструмент класса AxialCuttingTool с 8 (или более) режущими кромками.

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
    group : (str) : возвращает группу инструмента (всегда "Развертка").
    gabarit_volume : (float) : возвращает габаритный объем.
    gabarit_str : (str) : возвращает габарит, записанный строкой.
    type_of_mat : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
    to_dict : (dict) : возвращает словарь всех параметров и свойств.
    """

    _group = ToolGroups.REAMER
    num_of_cutting_blades: int = Field(default=8, gt=0, description="Количество режущих граней")

    def to_dict(self):
        """Возвращает словарь всех параметров и свойств развертки.
        
        Returns:
            dict: Словарь с параметрами развертки
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
    # Пример использования DeploymentCutter
    print("=== Пример использования DeploymentCutter ===")
    
    # Создание развертки с дефолтными значениями
    reamer = DeploymentCutter()
    print(f"Развертка по умолчанию: {reamer}")
    print(f"Группа: {reamer.group}")
    print(f"Имя: {reamer.name}")
    print(f"Количество режущих граней: {reamer.num_of_cutting_blades}")
    print(f"Диаметр: {reamer.dia_mm} мм")
    print(f"Длина: {reamer.length_mm} мм")
    print(f"Габарит: {reamer.gabarit_str}")
    print(f"Материал: {reamer.mat_of_cutting_part}")
    print(f"Тип материала: {reamer.type_of_mat}")
    print(f"Допуск: {reamer.tolerance}")
    
    # Изменение параметров
    print("\n=== Изменение параметров ===")
    reamer.marking = "РАЗВ-15-120"
    reamer.standard = "ГОСТ 1672-80"
    reamer.dia_mm = 15.0
    reamer.length_mm = 120.0
    reamer.num_of_cutting_blades = 10
    reamer.mat_of_cutting_part = "Р18"
    reamer.main_angle_grad = 0
    reamer.front_angle_grad = 0
    reamer.inclination_of_main_blade_grad = 0
    reamer.radius_of_cutting_vertex = 0.5
    
    print(f"Обновленная развертка: {reamer}")
    print(f"Новое имя: {reamer.name}")
    print(f"Группа осталась: {reamer.group}")
    print(f"Габарит: {reamer.gabarit_str}")
    print(f"Объем: {reamer.gabarit_volume} мм³")
    
    # Получение всех параметров
    print("\n=== Все параметры развертки ===")
    parameters = reamer.to_dict()
    for key, value in parameters.items():
        print(f"{key}: {value}")
    
    # Проверка валидации
    print("\n=== Проверка валидации ===")
    try:
        reamer.num_of_cutting_blades = 0  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации количества граней: {e}")
    
    try:
        reamer.dia_mm = -5  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации диаметра: {e}")
    
    # Создание развертки с кастомными параметрами
    print("\n=== Создание развертки с кастомными параметрами ===")
    custom_reamer = DeploymentCutter(
        marking="РАЗВ-20-150",
        standard="ГОСТ 1672-80",
        dia_mm=20.0,
        length_mm=150.0,
        num_of_cutting_blades=12,
        mat_of_cutting_part="Т15К6",
        main_angle_grad=0,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        radius_of_cutting_vertex=1.0
    )
    
    print(f"Кастомная развертка: {custom_reamer}")
    print(f"Имя: {custom_reamer.name}")
    print(f"Группа: {custom_reamer.group}")
    print(f"Количество граней: {custom_reamer.num_of_cutting_blades}")
    print(f"Материал: {custom_reamer.mat_of_cutting_part}")
    print(f"Тип материала: {custom_reamer.type_of_mat}")
    
    # Демонстрация наследования свойств
    print("\n=== Демонстрация наследования ===")
    print(f"Развертка наследует от Tool: {reamer.name}")
    print(f"Развертка наследует от AxialSizes: {reamer.gabarit_volume} мм³")
    print(f"Развертка наследует от BladeMaterial: {reamer.type_of_mat}")
    print(f"Развертка наследует от Angles: {reamer.main_angle_grad}°")
    
    # Проверка сериализации
    print("\n=== Сериализация в dict ===")
    reamer_dict = reamer.model_dump()
    print(f"Dict: {reamer_dict}")
    
    # Проверка десериализации
    print("\n=== Десериализация из dict ===")
    reamer_from_dict = DeploymentCutter(**reamer_dict)
    print(f"Развертка из dict: {reamer_from_dict}")
    print(f"Идентичны: {reamer == reamer_from_dict}")
