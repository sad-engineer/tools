#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union

from pydantic import BaseModel

from tools.app.enumerations import CuttingPartMaterials

"""Конфигурация материалов режущих пластин.

Словарь содержит информацию о типе и описании каждого материала:
- type: 0 - быстрорежущая сталь, 1 - твердый сплав
- description: текстовое описание типа материала
"""
MATERIAL_CONFIG = {
    CuttingPartMaterials.T5K12V: {"type": 1, "description": "Твердый сплав"},
    CuttingPartMaterials.T5K10: {"type": 1, "description": "Твердый сплав"},
    CuttingPartMaterials.T14K8: {"type": 1, "description": "Твердый сплав"},
    CuttingPartMaterials.T15K6: {"type": 1, "description": "Твердый сплав"},
    CuttingPartMaterials.T30K4: {"type": 1, "description": "Твердый сплав"},
    CuttingPartMaterials.VK3: {"type": 1, "description": "Твердый сплав"},
    CuttingPartMaterials.VK4: {"type": 1, "description": "Твердый сплав"},
    CuttingPartMaterials.VK6: {"type": 1, "description": "Твердый сплав"},
    CuttingPartMaterials.VK8: {"type": 1, "description": "Твердый сплав"},
    CuttingPartMaterials.R18: {"type": 0, "description": "Быстрорежущая сталь"},
    CuttingPartMaterials.R6M5: {"type": 0, "description": "Быстрорежущая сталь"},
    CuttingPartMaterials.X9C: {"type": 0, "description": "Быстрорежущая сталь"},
    CuttingPartMaterials.XGV: {"type": 0, "description": "Быстрорежущая сталь"},
    CuttingPartMaterials.U12A: {"type": 0, "description": "Быстрорежущая сталь"},
}


class BladeMaterial(BaseModel, validate_assignment=True):
    """Материал лезвия.

    Parameters:
    _mat_of_cutting_part : (CuttingPartMaterials) : внутреннее поле для хранения материала режущей пластины.

    Properties:
    mat_of_cutting_part : (str) : материал режущей пластины (доступен для чтения и записи).
    type_of_mat : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.
    description_type : (str) : описание типа материала (быстрорежущая сталь или твердый сплав).
    _parameters : (dict) : возвращает словарь параметров и свойств.

    Notes:
    - При установке mat_of_cutting_part можно передавать как строку, так и объект CuttingPartMaterials
    - type_of_mat автоматически определяется на основе установленного материала
    - MATERIAL_CONFIG содержит конфигурацию всех доступных материалов
    """

    _mat_of_cutting_part: CuttingPartMaterials = CuttingPartMaterials.from_value("Т15К6")

    @property
    def mat_of_cutting_part(self) -> str:
        """Материал режущей пластины.

        Returns:
            str: Строковое представление материала режущей пластины
        """
        return self._mat_of_cutting_part.value

    @mat_of_cutting_part.setter
    def mat_of_cutting_part(self, value: Union[str, CuttingPartMaterials]) -> None:
        """Установка материала режущей пластины.

        Args:
            value: Материал в виде строки или объекта CuttingPartMaterials

        Raises:
            ValueError: Если передан неизвестный материал
        """
        if isinstance(value, CuttingPartMaterials):
            self._mat_of_cutting_part = value
        else:
            self._mat_of_cutting_part = CuttingPartMaterials.from_value(value)

    @property
    def type_of_mat(self) -> int:
        """Тип материала режущей пластины.

        Returns:
            int: 0 - быстрорежущая сталь, 1 - твердый сплав, -1 - неизвестный материал
        """
        return MATERIAL_CONFIG.get(self._mat_of_cutting_part, {}).get("type", -1)

    @property
    def description_type(self) -> str:
        """Описание типа материала.

        Returns:
            str: Текстовое описание типа материала (быстрорежущая сталь или твердый сплав)
        """
        return MATERIAL_CONFIG.get(self._mat_of_cutting_part, {}).get("description", "Неизвестный материал")

    @property
    def _parameters(self) -> dict:
        return {
            "mat_of_cutting_part": self.mat_of_cutting_part,
            "type_of_mat": self.type_of_mat,
            "description_type": self.description_type,
        }


if __name__ == '__main__':
    # Пример использования класса BladeMaterial
    blade = BladeMaterial()
    print(blade)  # Выведет объект с дефолтными значениями
    print('Материал режущей части:', blade.mat_of_cutting_part)
    print('Тип материала:', blade.type_of_mat)
    print('Параметры:', blade._parameters)

    # Изменение материала
    blade.mat_of_cutting_part = "Р18"
    print('Новый материал:', blade.mat_of_cutting_part)
    print('Тип материала:', blade.type_of_mat)
    print('Параметры:', blade._parameters)

    # Проверка валидации материала
    try:
        blade.mat_of_cutting_part = "НЕИЗВЕСТНЫЙ_МАТЕРИАЛ"
    except ValueError as e:
        print(f"Ошибка валидации материала: {e}")

    # Установка материала через строку
    blade.mat_of_cutting_part = "ВК8"
    print('Материал через строку:', blade.mat_of_cutting_part)
    print('Параметры:', blade._parameters)
