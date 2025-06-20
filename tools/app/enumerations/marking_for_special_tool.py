#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class MarkingForSpecialTool(BaseEnum):
    SPECIAL_NY = 'специальный'
    SPECIAL_NAYA = 'специальная'
    SPECIAL_NOE = 'специальное'


if __name__ == '__main__':
    # Пример использования в классе
    class SpecialTool:
        def __init__(self):
            self.marking = MarkingForSpecialTool.SPECIAL_NY

        def set_marking(self, value):
            self.marking = MarkingForSpecialTool.from_value(value)

        def __str__(self):
            return f"Маркировка: {self.marking.value}"

    # Создание объекта
    tool = SpecialTool()
    print(tool)  # Выведет: Маркировка: специальный

    # Изменение маркировки
    tool.set_marking("специальная")
    print(tool)  # Выведет: Маркировка: специальная

    tool.set_marking("специальное")
    print(tool)  # Выведет: Маркировка: специальное

    # Проверка на некорректное значение
    try:
        tool.set_marking("особый")
    except ValueError as e:
        print(f"Ошибка: {e}")
