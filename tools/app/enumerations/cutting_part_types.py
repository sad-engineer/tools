#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class CuttingPartTypes(BaseEnum):
    """Типы режущей части фрезы"""

    NONE = None
    HELICAL_INSERTS = "Винтовые пластинки"
    SOLID = "Цельная"
    CROWN = "Коронка"


if __name__ == '__main__':
    # Пример использования в классе
    class MillingCutter:
        def __init__(self):
            self.cutting_part_type = CuttingPartTypes.HELICAL_INSERTS

        def set_cutting_part_type(self, value):
            self.cutting_part_type = CuttingPartTypes.from_value(value)

        def __str__(self):
            return f"Тип режущей части: {self.cutting_part_type.value}"

    # Создание объекта
    cutter = MillingCutter()
    print(cutter)  # Выведет: Тип режущей части: Винтовые пластинки

    # Изменение типа режущей части
    cutter.set_cutting_part_type("Цельная")
    print(cutter)  # Выведет: Тип режущей части: Цельная

    # Установка значения NONE
    cutter.set_cutting_part_type(None)
    print(cutter)  # Выведет: Тип режущей части: None

    # Проверка на некорректное значение
    try:
        cutter.set_cutting_part_type("Пайка")
    except ValueError as e:
        print(f"Ошибка: {e}")
