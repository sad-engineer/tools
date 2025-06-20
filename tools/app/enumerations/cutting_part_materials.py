#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from tools.app.enumerations.base import BaseEnum


class CuttingPartMaterials(BaseEnum):
    """Материалы режущей части"""

    NONE = None
    T5K12V = "Т5К12В"
    T5K10 = "Т5К10"
    T14K8 = "Т14К8"
    T15K6 = "Т15К6"
    T30K4 = "Т30К4"
    VK3 = "ВК3"
    VK4 = "ВК4"
    VK6 = "ВК6"
    VK8 = "ВК8"
    R18 = "Р18"
    R6M5 = "Р6М5"
    X9C = "9ХС"
    XGV = "ХГВ"
    U12A = "У12А"


if __name__ == '__main__':
    # Пример использования в классе
    class CuttingPart:
        def __init__(self):
            self.material = CuttingPartMaterials.T5K12V

        def set_material(self, value):
            self.material = CuttingPartMaterials.from_value(value)

        def __str__(self):
            return f"Материал режущей части: {self.material.value}"

    # Создание объекта
    part = CuttingPart()
    print(part)  # Выведет: Материал режущей части: Т5К12В (Твердый сплав)

    # Изменение материала
    part.set_material("Р18")
    print(part)  # Выведет: Материал режущей части: Р18 (Быстрорежущая сталь)

    # Установка значения NONE
    part.set_material(None)
    print(part)  # Выведет: Материал режущей части: None (Неизвестный материал)

    # Проверка на некорректное значение
    try:
        part.set_material("Сталь")
    except ValueError as e:
        print(f"Ошибка: {e}")
