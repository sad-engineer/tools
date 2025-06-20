#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations import ToolGroups
from tools.app.schemas.prismatic_cutting_tool import PrismaticCuttingTool


class TurningCutter(PrismaticCuttingTool):
    """Резец - призматический режущий инструмент для токарной обработки.

    Наследует параметры от PrismaticCuttingTool:
    - Tool: group, marking, standard
    - PrismaticSizes: length_mm, width_mm, height_mm, radius_of_cutting_vertex
    - BladeMaterial: mat_of_cutting_part
    - Angles: main_angle_grad, front_angle_grad, inclination_of_main_blade_grad
    - tolerance: допуск инструмента
    - num_of_cutting_blades: количество режущих граней

    Parameters:
    Все параметры наследуются от PrismaticCuttingTool.

    Properties:
    name : (str) : возвращает название инструмента.
    group : (str) : возвращает группу инструмента (всегда "Резец").
    gabarit_volume : (float) : возвращает габаритный объем.
    gabarit_str : (str) : возвращает габарит, записанный строкой.
    type_of_mat : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
    to_dict : (dict) : возвращает словарь всех параметров и свойств.
    """

    _group = ToolGroups.CUTTER

    def to_dict(self):
        """Возвращает словарь всех параметров и свойств резца.
        
        Returns:
            dict: Словарь с параметрами резца
        """
        # Получаем параметры из базового класса
        base_parameters = super().to_dict()
        
        # Создаем словарь с параметрами текущего класса
        current_parameters = {
            # Резец не добавляет новых параметров, но может переопределить существующие
        }
        
        # Объединяем параметры
        return base_parameters | current_parameters


if __name__ == '__main__':
    # Пример использования TurningCutter
    print("=== Пример использования TurningCutter ===")
    
    # Создание резца с дефолтными значениями
    cutter = TurningCutter()
    print(f"Резец по умолчанию: {cutter}")
    print(f"Группа: {cutter.group}")
    print(f"Имя: {cutter.name}")
    print(f"Количество режущих граней: {cutter.num_of_cutting_blades}")
    print(f"Длина: {cutter.length_mm} мм")
    print(f"Ширина: {cutter.width_mm} мм")
    print(f"Высота: {cutter.height_mm} мм")
    print(f"Габарит: {cutter.gabarit_str}")
    print(f"Материал: {cutter.mat_of_cutting_part}")
    print(f"Тип материала: {cutter.type_of_mat}")
    print(f"Допуск: {cutter.tolerance}")
    
    # Изменение параметров
    print("\n=== Изменение параметров ===")
    cutter.marking = "РЕЗЕЦ-25-16-25"
    cutter.standard = "ГОСТ 18877-73"
    cutter.length_mm = 150.0
    cutter.width_mm = 16.0
    cutter.height_mm = 25.0
    cutter.num_of_cutting_blades = 1
    cutter.mat_of_cutting_part = "Т15К6"
    cutter.main_angle_grad = 45
    cutter.front_angle_grad = 5
    cutter.inclination_of_main_blade_grad = 2
    cutter.radius_of_cutting_vertex = 0.5
    
    print(f"Обновленный резец: {cutter}")
    print(f"Новое имя: {cutter.name}")
    print(f"Группа осталась: {cutter.group}")
    print(f"Габарит: {cutter.gabarit_str}")
    print(f"Объем: {cutter.gabarit_volume} мм³")
    
    # Получение всех параметров
    print("\n=== Все параметры резца ===")
    parameters = cutter.to_dict()
    for key, value in parameters.items():
        print(f"{key}: {value}")
    
    # Проверка валидации
    print("\n=== Проверка валидации ===")
    try:
        cutter.num_of_cutting_blades = 0  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации количества граней: {e}")
    
    try:
        cutter.length_mm = -5  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации длины: {e}")
    
    # Создание резца с кастомными параметрами
    print("\n=== Создание резца с кастомными параметрами ===")
    custom_cutter = TurningCutter(
        marking="РЕЗЕЦ-30-20-35",
        standard="ГОСТ 18877-73",
        length_mm=200.0,
        width_mm=20.0,
        height_mm=35.0,
        num_of_cutting_blades=1,
        mat_of_cutting_part="Р18",
        main_angle_grad=60,
        front_angle_grad=10,
        inclination_of_main_blade_grad=5,
        radius_of_cutting_vertex=1.0
    )
    
    print(f"Кастомный резец: {custom_cutter}")
    print(f"Имя: {custom_cutter.name}")
    print(f"Группа: {custom_cutter.group}")
    print(f"Количество граней: {custom_cutter.num_of_cutting_blades}")
    print(f"Материал: {custom_cutter.mat_of_cutting_part}")
    print(f"Тип материала: {custom_cutter.type_of_mat}")
    
    # Демонстрация наследования свойств
    print("\n=== Демонстрация наследования ===")
    print(f"Резец наследует от Tool: {cutter.name}")
    print(f"Резец наследует от PrismaticSizes: {cutter.gabarit_volume} мм³")
    print(f"Резец наследует от BladeMaterial: {cutter.type_of_mat}")
    print(f"Резец наследует от Angles: {cutter.main_angle_grad}°")
    
    # Проверка сериализации
    print("\n=== Сериализация в dict ===")
    cutter_dict = cutter.model_dump()
    print(f"Dict: {cutter_dict}")
    
    # Проверка десериализации
    print("\n=== Десериализация из dict ===")
    cutter_from_dict = TurningCutter(**cutter_dict)
    print(f"Резец из dict: {cutter_from_dict}")
    print(f"Идентичны: {cutter == cutter_from_dict}")
