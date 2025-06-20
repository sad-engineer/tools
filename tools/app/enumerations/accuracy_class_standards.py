#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class AccuracyClassStandards(BaseEnum):
    """Классы точности инструмента"""

    NONE = None
    AAA = "AAA"
    AA = "AA"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    AAA_CYR = "ААА"
    AA_CYR = "АА"
    A_CYR = "А"
    B_CYR = "В"
    C_CYR = "С"
    D_CYR = "Д"


if __name__ == '__main__':
    # Пример использования в классе
    class Tool:
        def __init__(self):
            self.accuracy_class = AccuracyClassStandards.A

        def set_accuracy_class(self, value):
            self.accuracy_class = AccuracyClassStandards.from_value(value)

        def __str__(self):
            return f"Класс точности: {self.accuracy_class.value}"

    # Создание объекта
    tool = Tool()
    print(tool)  # Выведет: Класс точности: A

    # Изменение класса точности
    tool.set_accuracy_class("AA")
    print(tool)  # Выведет: Класс точности: AA

    # Установка значения NONE
    tool.set_accuracy_class(None)
    print(tool)  # Выведет: Класс точности: None

    # Проверка на кириллические значения
    tool.set_accuracy_class("АА")
    print(tool)  # Выведет: Класс точности: АА

    # Проверка на некорректное значение
    try:
        tool.set_accuracy_class("E")
    except ValueError as e:
        print(f"Ошибка: {e}")
