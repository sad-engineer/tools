#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from pydantic import Field

from tools.app.enumerations import MarkingForSpecialTool, ToolGroups
from tools.app.schemas.tool import CustomTool


class BroachingCutter(CustomTool):
    """Протяжка - специальный инструмент для протягивания отверстий.

    Наследует параметры от CustomTool:
    - group: группа инструмента (всегда "Протяжка")
    - marking: обозначение инструмента (всегда "специальная")
    - standard: стандарт инструмента

    Parameters:
    angle_of_inclination: (float) : Угол наклона зубьев протяжки в градусах.
    pitch_of_teeth: (float >= 0) : Шаг зубьев протяжки в мм.
    number_teeth_section: (int >= 0) : Число зубьев секции протяжки.
    difference: (float >= 0) : Подача на зуб протяжки (размерный перепад между соседними зубьями) в мм.
    length_of_working_part: (float >= 0) : Длина режущей части протяжки в мм.

    Properties:
        name : (str) : возвращает название инструмента.
    group : (str) : возвращает группу инструмента (всегда "Протяжка").

    Methods:
    to_dict : (dict) : возвращает словарь всех параметров и свойств.
    """

    _group = ToolGroups.BROACH
    _marking: MarkingForSpecialTool = MarkingForSpecialTool.SPECIAL_NAYA
    angle_of_inclination: float = Field(default=0, ge=0, le=360, description="Угол наклона зубьев протяжки")
    pitch_of_teeth: float = Field(default=0, ge=0, description="Шаг зубьев протяжки")
    number_teeth_section: int = Field(default=0, ge=0, description="Число зубьев секции протяжки")
    difference: float = Field(
        default=0, ge=0, description="Подача на зуб протяжки (размерный перепад между соседними зубьями)"
    )
    length_of_working_part: float = Field(default=0, ge=0, description="Длина режущей части протяжки")

    def to_dict(self):
        """Возвращает словарь всех параметров и свойств протяжки.

        Returns:
            dict: Словарь с параметрами протяжки
        """
        # Получаем параметры из базового класса
        base_parameters = super()._parameters

        # Создаем словарь с параметрами текущего класса
        current_parameters = {
            "angle_of_inclination": self.angle_of_inclination,
            "pitch_of_teeth": self.pitch_of_teeth,
            "number_teeth_section": self.number_teeth_section,
            "difference": self.difference,
            "length_of_working_part": self.length_of_working_part,
        }

        # Объединяем параметры
        return base_parameters | current_parameters


if __name__ == '__main__':
    # Пример использования BroachingCutter
    print("=== Пример использования BroachingCutter ===")

    # Создание протяжки с дефолтными значениями
    broach = BroachingCutter()
    print(f"Протяжка по умолчанию: {broach}")
    print(f"Группа: {broach.group}")
    print(f"Имя: {broach.name}")
    print(f"Обозначение: {broach.marking}")
    print(f"Стандарт: {broach.standard}")

    # Демонстрация параметров протяжки
    print(f"Угол наклона зубьев: {broach.angle_of_inclination}°")
    print(f"Шаг зубьев: {broach.pitch_of_teeth} мм")
    print(f"Число зубьев секции: {broach.number_teeth_section}")
    print(f"Подача на зуб: {broach.difference} мм")
    print(f"Длина режущей части: {broach.length_of_working_part} мм")

    # Изменение параметров
    print("\n=== Изменение параметров ===")
    broach.standard = "ГОСТ 5009-82"
    broach.angle_of_inclination = 15.0
    broach.pitch_of_teeth = 8.0
    broach.number_teeth_section = 12
    broach.difference = 0.02
    broach.length_of_working_part = 150.0

    print(f"Обновленная протяжка: {broach}")
    print(f"Новое имя: {broach.name}")

    # Получение всех параметров
    print("\n=== Все параметры протяжки ===")
    parameters = broach.to_dict()
    for key, value in parameters.items():
        print(f"{key}: {value}")

    # Проверка валидации
    print("\n=== Проверка валидации ===")
    try:
        broach.angle_of_inclination = 400  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации угла наклона: {e}")

    try:
        broach.pitch_of_teeth = -5  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации шага зубьев: {e}")

    # Создание протяжки с кастомными параметрами
    print("\n=== Создание протяжки с кастомными параметрами ===")
    custom_broach = BroachingCutter(
        standard="ГОСТ 5009-82",
        angle_of_inclination=20.0,
        pitch_of_teeth=10.0,
        number_teeth_section=15,
        difference=0.03,
        length_of_working_part=200.0,
    )

    print(f"Кастомная протяжка: {custom_broach}")
    print(f"Имя: {custom_broach.name}")
    print(f"Группа: {custom_broach.group}")

    # Демонстрация наследования
    print("\n=== Демонстрация наследования ===")
    print(f"Протяжка наследует от CustomTool: {broach.name}")
    print(f"Протяжка наследует группу: {broach.group}")
    print(f"Протяжка наследует обозначение: {broach.marking}")
