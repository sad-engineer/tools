#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from pydantic import Field

from tools.app.enumerations import ToolGroups
from tools.app.schemas.axial_cutting_tool import AxialCuttingTool


class DrillingCutter(AxialCuttingTool):
    """Сверло - это инструмент класса AxialCuttingTool с двумя режущими кромками.

    Наследует параметры от AxialCuttingTool:
    - Tool: group, marking, standard
    - AxialSizes: dia_mm, length_mm, radius_of_cutting_vertex
    - BladeMaterial: mat_of_cutting_part
    - Angles: main_angle_grad, front_angle_grad, inclination_of_main_blade_grad
    - tolerance: допуск инструмента

    Parameters:
    num_of_cutting_blades : (int >= 0) : количество режущих граней (по умолчанию 2).

    Properties:
    name : (str) : возвращает название инструмента.
    group : (str) : возвращает группу инструмента (всегда "Сверло").
    gabarit_volume : (float) : возвращает габаритный объем.
    gabarit_str : (str) : возвращает габарит, записанный строкой.
    type_of_mat : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
    to_dict : (dict) : возвращает словарь всех параметров и свойств.
    """

    _group = ToolGroups.DRILL
    num_of_cutting_blades: int = Field(default=2, gt=0, description="Количество режущих граней")

    def to_dict(self):
        """Возвращает словарь всех параметров и свойств сверла.
        
        Returns:
            dict: Словарь с параметрами сверла
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
    # Пример использования DrillingCutter
    print("=== Пример использования DrillingCutter ===")

    # Создание сверла с дефолтными значениями
    drill = DrillingCutter()
    print(f"Сверло по умолчанию: {drill}")
    print(f"Группа: {drill.group}")
    print(f"Группа должна быть 'Сверло': {drill.group == 'Сверло'}")
    print(f"Допуск: {drill.tolerance}")

    print(f"Имя: {drill.name}")
    print(f"Количество режущих граней: {drill.num_of_cutting_blades}")
    print(f"Диаметр: {drill.dia_mm} мм")
    print(f"Длина: {drill.length_mm} мм")
    print(f"Габарит: {drill.gabarit_str}")
    print(f"Материал: {drill.mat_of_cutting_part}")
    print(f"Тип материала: {drill.type_of_mat}")

    # Демонстрация защиты поля group
    print("\n=== Демонстрация защиты поля group ===")
    print(f"Текущая группа: {drill.group}")
    try:
        drill.group = "Фреза"  # Попытка изменить группу
    except AttributeError as e:
        print(f"Ошибка при попытке изменить группу: {e}")
    print(f"Группа осталась неизменной: {drill.group}")

    # Изменение других параметров
    print("\n=== Изменение других параметров ===")
    drill.marking = "СВ-10-100"
    drill.standard = "ГОСТ 10903-77"
    drill.dia_mm = 10.0
    drill.length_mm = 100.0
    drill.num_of_cutting_blades = 2
    drill.mat_of_cutting_part = "Т15К6"
    drill.main_angle_grad = 118
    drill.front_angle_grad = 0
    drill.inclination_of_main_blade_grad = 0
    drill.radius_of_cutting_vertex = 0.5

    print(f"Обновленное сверло: {drill}")
    print(f"Новое имя: {drill.name}")
    print(f"Группа осталась: {drill.group}")
    print(f"Габарит: {drill.gabarit_str}")
    print(f"Объем: {drill.gabarit_volume} мм³")

    # Проверка валидации количества режущих граней
    print("\n=== Проверка валидации количества граней ===")
    try:
        drill.num_of_cutting_blades = 0  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации количества граней: {e}")

    # Проверка валидации диаметра
    print("\n=== Проверка валидации диаметра ===")
    try:
        drill.dia_mm = -5  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации диаметра: {e}")

    # Получение всех параметров
    print("\n=== Все параметры сверла ===")
    parameters = drill.to_dict()
    for key, value in parameters.items():
        print(f"{key}: {value}")

    # Создание сверла с кастомными параметрами
    print("\n=== Создание сверла с кастомными параметрами ===")
    custom_drill = DrillingCutter(
        marking="СВ-20-150",
        standard="ГОСТ 886-77",
        dia_mm=20.0,
        length_mm=150.0,
        num_of_cutting_blades=4,
        mat_of_cutting_part="Р18",
        main_angle_grad=120,
        front_angle_grad=5,
        inclination_of_main_blade_grad=2,
        radius_of_cutting_vertex=1.0,
    )

    print(f"Кастомное сверло: {custom_drill}")
    print(f"Имя: {custom_drill.name}")
    print(f"Группа: {custom_drill.group}")
    print(f"Габарит: {custom_drill.gabarit_str}")
    print(f"Количество граней: {custom_drill.num_of_cutting_blades}")
    print(f"Материал: {custom_drill.mat_of_cutting_part}")
    print(f"Тип материала: {custom_drill.type_of_mat}")

    # Демонстрация наследования свойств
    print("\n=== Демонстрация наследования ===")
    print(f"Сверло наследует от Tool: {drill.name}")
    print(f"Сверло наследует от AxialSizes: {drill.gabarit_volume} мм³")
    print(f"Сверло наследует от BladeMaterial: {drill.type_of_mat}")
    print(f"Сверло наследует от Angles: {drill.main_angle_grad}°")

    # Проверка сериализации
    print("\n=== Сериализация в dict ===")
    drill_dict = drill.to_dict()
    print(f"Dict: {drill_dict}")

    # Проверка десериализации
    print("\n=== Десериализация из dict ===")
    drill_from_dict = DrillingCutter(**drill_dict)
    print(f"Сверло из dict: {drill_from_dict}")
    print(f"Идентичны: {drill == drill_from_dict}")

    # Демонстрация создания сверла с явным указанием группы
    print("\n=== Создание сверла с явным указанием группы ===")
    try:
        drill_with_group = DrillingCutter(group=ToolGroups.DRILL)
        print(f"Сверло с явной группой: {drill_with_group}")
        print(f"Группа: {drill_with_group.group}")

        # Попытка изменить группу после создания
        try:
            drill_with_group.group = ToolGroups.MILLING_CUTTER
        except AttributeError as e:
            print(f"Ошибка при попытке изменить группу: {e}")
    except Exception as e:
        print(f"Ошибка при создании: {e}")
