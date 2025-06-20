#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class MillingCutterTypes(BaseEnum):
    """Типы фрез"""

    NONE = None
    CYLINDRICAL = "Цилиндрическая"
    FACE = "Торцовая"
    FACE_CYLINDRICAL = "Торцовая, Цилиндрическая"
    DISC_FACE = "Дисковая, обработка торца"
    DISC_GROOVE = "Дисковая, обработка паза"
    DISC = "Дисковая"
    GROOVE = "Пазовая"
    CUT_OFF = "Отрезная"
    SLITTING = "Прорезная"
    END_FACE = "Концевая, обработка торца"
    END_GROOVE = "Концевая, обработка паза"
    END = "Концевая"
    END_T_SLOT = "Концевая (для T-образных пазов)"
    ANGULAR = "Угловая"
    FORM_CONVEX = "Фасонная, с выпуклым профилем"
    FORM = "Фасонная"
    FORM_CONCAVE = "Фасонная, с вогнутым профилем"
    KEYWAY = "Шпоночная"
    THREAD = "Резьбовая"
    WORM = "Червячная"


if __name__ == '__main__':
    # Пример использования в классе
    class MillingCutter:
        def __init__(self):
            self.cutter_type = MillingCutterTypes.CYLINDRICAL

        def set_cutter_type(self, value):
            self.cutter_type = MillingCutterTypes.from_value(value)

        def __str__(self):
            return f"Тип фрезы: {self.cutter_type.value}"

    # Создание объекта
    cutter = MillingCutter()
    print(cutter)  # Выведет: Тип фрезы: Цилиндрическая

    # Изменение типа фрезы
    cutter.set_cutter_type("Торцовая")
    print(cutter)  # Выведет: Тип фрезы: Торцовая

    # Установка значения NONE
    cutter.set_cutter_type(None)
    print(cutter)  # Выведет: Тип фрезы: None

    # Проверка на некорректное значение
    try:
        cutter.set_cutter_type("Пальцевая")
    except ValueError as e:
        print(f"Ошибка: {e}")
