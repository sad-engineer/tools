#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class ToolGroups(BaseEnum):
    """Группы инструментов"""

    NONE = None
    INSTRUMENT = "Инструмент"
    CUTTER = "Резец"
    MILLING_CUTTER = "Фреза"
    DRILL = "Сверло"
    COUNTERSINK = "Зенкер"
    REAMER = "Развертка"
    BROACH = "Протяжка"


if __name__ == '__main__':
    # Пример использования в классе
    class Tool:
        def __init__(self):
            self.group = ToolGroups.CUTTER

        def set_group(self, value):
            self.group = ToolGroups.from_value(value)

        def __str__(self):
            return f"Группа инструмента: {self.group.value}"

    # Создание объекта
    tool = Tool()
    print(tool)  # Выведет: Группа инструмента: Резец

    # Изменение группы
    tool.set_group("Фреза")
    print(tool)  # Выведет: Группа инструмента: Фреза

    # Установка значения NONE
    tool.set_group(None)
    print(tool)  # Выведет: Группа инструмента: None

    # Проверка на некорректное значение
    try:
        tool.set_group("Пила")
    except ValueError as e:
        print(f"Ошибка: {e}")
