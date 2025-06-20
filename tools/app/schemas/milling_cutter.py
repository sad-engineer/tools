#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union

from pydantic import Field

from tools.app.enumerations import AccuracyClassStandards, CuttingPartTypes, MillingCutterTypes, ToolGroups, ToothTypes
from tools.app.schemas.axial_cutting_tool import AxialCuttingTool


class MillingCutter(AxialCuttingTool):
    """Фреза - это инструмент класса AxialCuttingTool с 12 (или более) режущими кромками.
    
    Наследует параметры от AxialCuttingTool:
    - Tool: group, marking, standard
    - AxialSizes: dia_mm, length_mm, radius_of_cutting_vertex
    - BladeMaterial: mat_of_cutting_part
    - Angles: main_angle_grad, front_angle_grad, inclination_of_main_blade_grad
    - tolerance: допуск инструмента

    Parameters:
    num_of_cutting_blades : (int >= 0) : количество режущих граней (по умолчанию 12).
    cutter_number : (int >= 0) : номер инструмента для формирования обозначения.
    module : (float >= 0) : модуль нарезки зубьев в мм.

    Properties:
    name : (str) : возвращает название инструмента.
    group : (str) : возвращает группу инструмента (всегда "Фреза").
    gabarit_volume : (float) : возвращает габаритный объем.
    gabarit_str : (str) : возвращает габарит, записанный строкой.
    type_of_mat : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.
    type_cutter : (str) : тип фрезы (доступен для чтения и записи).
    type_of_cutting_part : (str) : тип режущей части (доступен для чтения и записи).
    large_tooth : (str) : крупность зуба (доступен для чтения и записи).
    accuracy_class : (str) : класс точности (доступен для чтения и записи).

    Methods:
    to_dict : (dict) : возвращает словарь всех параметров и свойств.
    """

    _group = ToolGroups.MILLING_CUTTER
    _type_cutter: MillingCutterTypes = MillingCutterTypes.CYLINDRICAL
    _type_of_cutting_part: CuttingPartTypes = CuttingPartTypes.SOLID
    _large_tooth: ToothTypes = ToothTypes.COARSE
    _accuracy_class: AccuracyClassStandards = AccuracyClassStandards.NONE
    num_of_cutting_blades: int = Field(default=12, gt=0, description="Количество режущих граней")
    cutter_number: int = Field(default=0, ge=0, description="Номер инструмента (для формирования обозначения)")
    module: float = Field(default=0.0, ge=0, description="Модуль нарезки зубьев")

    @property
    def type_cutter(self) -> str:
        return self._type_cutter.value

    @type_cutter.setter
    def type_cutter(self, value: Union[str, MillingCutterTypes]) -> None:
        if isinstance(value, MillingCutterTypes):
            self._type_cutter = value
        else:
            self._type_cutter = MillingCutterTypes.from_value(value)

    @property
    def type_of_cutting_part(self) -> str:
        return self._type_of_cutting_part.value

    @type_of_cutting_part.setter
    def type_of_cutting_part(self, value: Union[str, CuttingPartTypes]) -> None:
        if isinstance(value, CuttingPartTypes):
            self._type_of_cutting_part = value
        else:
            self._type_of_cutting_part = CuttingPartTypes.from_value(value)

    @property
    def large_tooth(self) -> str:
        return self._large_tooth.value

    @large_tooth.setter
    def large_tooth(self, value: Union[str, ToothTypes]) -> None:
        if isinstance(value, ToothTypes):
            self._large_tooth = value
        else:
            self._large_tooth = ToothTypes.from_value(value)

    @property
    def accuracy_class(self) -> str:
        return self._accuracy_class.value

    @accuracy_class.setter
    def accuracy_class(self, value: Union[str, AccuracyClassStandards]) -> None:
        if isinstance(value, AccuracyClassStandards):
            self._accuracy_class = value
        else:
            self._accuracy_class = AccuracyClassStandards.from_value(value)

    def to_dict(self):
        """Возвращает словарь всех параметров и свойств фрезы.
        
        Returns:
            dict: Словарь с параметрами фрезы
        """
        # Получаем параметры из базового класса
        base_parameters = super().to_dict()
        
        # Создаем словарь с параметрами текущего класса
        current_parameters = {
            "type_cutter": self.type_cutter,
            "type_of_cutting_part": self.type_of_cutting_part,
            "large_tooth": self.large_tooth,
            "num_of_cutting_blades": self.num_of_cutting_blades,
            "accuracy_class": self.accuracy_class,
            "cutter_number": self.cutter_number,
            "module": self.module,
        }
        
        # Объединяем параметры
        return base_parameters | current_parameters


if __name__ == '__main__':
    # Пример использования MillingCutter
    print("=== Пример использования MillingCutter ===")

    # Создание фрезы с дефолтными значениями
    cutter = MillingCutter()
    print(f"Фреза по умолчанию: {cutter}")
    print(f"Группа: {cutter.group}")
    print(f"Тип фрезы: {cutter.type_cutter}")
    print(f"Тип режущей части: {cutter.type_of_cutting_part}")
    print(f"Крупность зуба: {cutter.large_tooth}")
    print(f"Класс точности: {cutter.accuracy_class}")
    print(f"Количество режущих граней: {cutter.num_of_cutting_blades}")

    # Демонстрация работы сеттеров
    print("\n=== Демонстрация работы сеттеров ===")

    # Изменение типа фрезы
    cutter.type_cutter = "Торцовая"
    print(f"Новый тип фрезы: {cutter.type_cutter}")

    # Изменение типа режущей части
    cutter.type_of_cutting_part = "Винтовые пластинки"
    print(f"Новый тип режущей части: {cutter.type_of_cutting_part}")

    # Изменение крупности зуба
    cutter.large_tooth = "Мелкий шаг"
    print(f"Новая крупность зуба: {cutter.large_tooth}")

    # Изменение класса точности
    cutter.accuracy_class = "B"
    print(f"Новый класс точности: {cutter.accuracy_class}")

    # Демонстрация работы с объектами перечислений
    print("\n=== Демонстрация работы с объектами перечислений ===")
    from tools.app.enumerations import AccuracyClassStandards, CuttingPartTypes, MillingCutterTypes, ToothTypes

    cutter.type_cutter = MillingCutterTypes.END
    print(f"Тип фрезы через объект: {cutter.type_cutter}")

    cutter.type_of_cutting_part = CuttingPartTypes.CROWN
    print(f"Тип режущей части через объект: {cutter.type_of_cutting_part}")

    # Получение всех параметров
    print("\n=== Все параметры фрезы ===")
    parameters = cutter.to_dict()
    for key, value in parameters.items():
        print(f"{key}: {value}")

    # Проверка валидации
    print("\n=== Проверка валидации ===")
    try:
        cutter.type_cutter = "НЕИЗВЕСТНЫЙ_ТИП"
    except ValueError as e:
        print(f"Ошибка валидации типа фрезы: {e}")

    try:
        cutter.large_tooth = "НЕИЗВЕСТНЫЙ_ШАГ"
    except ValueError as e:
        print(f"Ошибка валидации крупности зуба: {e}")

    # Создание фрезы с кастомными параметрами
    print("\n=== Создание фрезы с кастомными параметрами ===")
    custom_cutter = MillingCutter(
        marking="ФРЕЗ-50-200",
        standard="ГОСТ 17025-71",
        dia_mm=50.0,
        length_mm=200.0,
        num_of_cutting_blades=16,
        mat_of_cutting_part="Т15К6",
        main_angle_grad=90,
        front_angle_grad=5,
        inclination_of_main_blade_grad=2,
        radius_of_cutting_vertex=2.0,
        type_cutter="Торцовая",
        type_of_cutting_part="Составная",
        large_tooth="Мелкий шаг",
        accuracy_class="B",
        cutter_number=1,
        module=2.0
    )
    
    print(f"Кастомная фреза: {custom_cutter}")
    print(f"Имя: {custom_cutter.name}")
    print(f"Группа: {custom_cutter.group}")
    print(f"Тип фрезы: {custom_cutter.type_cutter}")
    print(f"Тип режущей части: {custom_cutter.type_of_cutting_part}")
    print(f"Крупность зуба: {custom_cutter.large_tooth}")
    print(f"Класс точности: {custom_cutter.accuracy_class}")
    print(f"Количество граней: {custom_cutter.num_of_cutting_blades}")
    print(f"Номер инструмента: {custom_cutter.cutter_number}")
    print(f"Модуль: {custom_cutter.module}")
    
    # Демонстрация наследования свойств
    print("\n=== Демонстрация наследования ===")
    print(f"Фреза наследует от Tool: {cutter.name}")
    print(f"Фреза наследует от AxialSizes: {cutter.gabarit_volume} мм³")
    print(f"Фреза наследует от BladeMaterial: {cutter.type_of_mat}")
    print(f"Фреза наследует от Angles: {cutter.main_angle_grad}°")
    print(f"Фреза наследует tolerance: {cutter.tolerance}")
    
    # Проверка сериализации
    print("\n=== Сериализация в dict ===")
    cutter_dict = cutter.model_dump()
    print(f"Dict: {cutter_dict}")
    
    # Проверка десериализации
    print("\n=== Десериализация из dict ===")
    cutter_from_dict = MillingCutter(**cutter_dict)
    print(f"Фреза из dict: {cutter_from_dict}")
    print(f"Идентичны: {cutter == cutter_from_dict}")
