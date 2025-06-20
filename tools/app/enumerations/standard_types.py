#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class StandardTypes(BaseEnum):
    """Типы стандартов инструмента"""

    NONE = None
    GOST = "ГОСТ"
    OST = "ОСТ"
    DIN = "DIN"
    ISO = "ИСО"


if __name__ == '__main__':
    # Пример использования в классе
    class Tool:
        def __init__(self):
            self.standard = StandardTypes.GOST

        def set_standard(self, value):
            self.standard = StandardTypes.from_value(value)

        def __str__(self):
            return f"Стандарт инструмента: {self.standard.value}"

    # Создание объекта
    tool = Tool()
    print(tool)  # Выведет: Стандарт инструмента: ГОСТ

    # Изменение стандарта
    tool.set_standard("DIN")
    print(tool)  # Выведет: Стандарт инструмента: DIN

    # Установка значения NONE
    tool.set_standard(None)
    print(tool)  # Выведет: Стандарт инструмента: None

    # Проверка на некорректное значение
    try:
        tool.set_standard("ANSI")
    except ValueError as e:
        print(f"Ошибка: {e}")
