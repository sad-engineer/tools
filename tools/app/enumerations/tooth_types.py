#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class ToothTypes(BaseEnum):
    """Типы частоты шага"""

    NONE = None
    COARSE = "Крупный шаг"
    FINE = "Мелкий шаг"


if __name__ == '__main__':
    # Пример использования в классе
    class Thread:
        def __init__(self):
            self.tooth_type = ToothTypes.COARSE

        def set_tooth_type(self, value: str):
            self.tooth_type = ToothTypes.from_value(value)

        def __str__(self):
            return f"Резьба с {self.tooth_type.value}"

    # Создание объекта
    thread = Thread()
    print(thread)  # Выведет: Резьба с Крупный шаг

    # Изменение типа шага
    thread.set_tooth_type("Мелкий шаг")
    print(thread)  # Выведет: Резьба с Мелкий шаг

    # Получение всех возможных значений
    print("\nВсе возможные типы шага:")
    for name, value in ToothTypes.get_display_names().items():
        print(f"- {value}")

    # Проверка на некорректное значение
    try:
        thread.set_tooth_type("Средний шаг")
    except ValueError as e:
        print(f"\nОшибка: {e}")
