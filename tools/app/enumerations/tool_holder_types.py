#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class ToolHolderTypes(BaseEnum):
    """Типы установки резца"""

    NONE = None
    HOLDER = "В резцедержателе"
    TURRET = "В револьверной головке"


if __name__ == '__main__':
    # Пример использования в классе
    class Tool:
        def __init__(self):
            self.holder_type = ToolHolderTypes.HOLDER

        def set_holder_type(self, value):
            self.holder_type = ToolHolderTypes.from_value(value)

        def __str__(self):
            return f"Инструмент установлен: {self.holder_type.value}"

    # Создание объекта
    tool = Tool()
    print(tool)  # Выведет: Инструмент установлен: В резцедержателе

    # Изменение типа установки
    tool.set_holder_type("В револьверной головке")
    print(tool)  # Выведет: Инструмент установлен: В револьверной головке

    # Установка значения NONE
    tool.set_holder_type(None)
    print(tool)  # Выведет: Инструмент установлен: None

    # Проверка на некорректное значение
    try:
        tool.set_holder_type("В патроне")
    except ValueError as e:
        print(f"Ошибка: {e}")
