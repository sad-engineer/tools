#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class LoadTypes(BaseEnum):
    """Типы нагрузок на резец"""

    NONE = None
    UNIFORM = "Равномерная"
    NON_UNIFORM = "Неравномерная"
    HIGHLY_NON_UNIFORM = "Неравномерная с большой неравномерностью"


if __name__ == '__main__':
    # Пример использования в классе
    class Cutter:
        def __init__(self):
            self.load_type = LoadTypes.UNIFORM

        def set_load_type(self, value):
            self.load_type = LoadTypes.from_value(value)

        def __str__(self):
            return f"Тип нагрузки: {self.load_type.value}"

    # Создание объекта
    cutter = Cutter()
    print(cutter)  # Выведет: Тип нагрузки: Равномерная

    # Изменение типа нагрузки
    cutter.set_load_type("Неравномерная")
    print(cutter)  # Выведет: Тип нагрузки: Неравномерная

    # Установка значения NONE
    cutter.set_load_type(None)
    print(cutter)  # Выведет: Тип нагрузки: None

    # Проверка на некорректное значение
    try:
        cutter.set_load_type("Импульсная")
    except ValueError as e:
        print(f"Ошибка: {e}")
