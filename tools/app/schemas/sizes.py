#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional

from pydantic import BaseModel, Field


class AxialSizes(BaseModel, validate_assignment=True):
    """Диаметральные размеры инструмента.

    Parameters:
    dia_mm : (float >= 0) : диаметр инструмента в мм.
    length_mm : (float >= 0) : длина инструмента в мм.
    radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины в мм.

    Properties:
    gabarit_volume : (float) : возвращает габаритный объем в мм³.
    gabarit_str : (str) : возвращает габарит, записанный строкой.
    _parameters : (dict) : возвращает словарь параметров и свойств.

    Methods:
    _parameters : (dict) : возвращает словарь всех параметров и свойств.
    """

    dia_mm: float = Field(default=6, ge=0, description="Диаметр инструмента в мм")
    length_mm: float = Field(default=100, ge=0, description="Длина инструмента в мм")
    radius_of_cutting_vertex: Optional[float] = Field(default=None, ge=0, description="Радиус режущей вершины в мм")

    @property
    def gabarit_volume(self) -> float:
        """Габаритный объем в мм³"""
        return self.dia_mm * self.dia_mm * self.length_mm

    @property
    def gabarit_str(self) -> str:
        """Строковое представление габаритов"""
        return f"øDxL: ø{self.dia_mm}x{self.length_mm} мм."

    @property
    def _parameters(self) -> dict:
        return {
            "dia_mm": self.dia_mm,
            "length_mm": self.length_mm,
            "radius_of_cutting_vertex": self.radius_of_cutting_vertex,
            "gabarit_volume": self.gabarit_volume,
            "gabarit_str": self.gabarit_str,
        }


class PrismaticSizes(BaseModel, validate_assignment=True):
    """Размеры призматического инструмента.

    Parameters:
    length_mm : (float >= 0) : длина инструмента в мм.
    width_mm : (float >= 0) : ширина инструмента в мм.
    height_mm : (float >= 0) : высота инструмента в мм.
    radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины в мм.

    Properties:
    gabarit_volume : (float) : возвращает габаритный объем в мм³.
    gabarit_str : (str) : возвращает габарит, записанный строкой.
    _parameters : (dict) : возвращает словарь параметров и свойств.

    Methods:
    _parameters : (dict) : возвращает словарь всех параметров и свойств.
    """

    length_mm: float = Field(default=100, ge=0, description="Длина инструмента в мм")
    width_mm: float = Field(default=16, ge=0, description="Ширина инструмента в мм")
    height_mm: float = Field(default=25, ge=0, description="Высота инструмента в мм")
    radius_of_cutting_vertex: float = Field(default=1, ge=0, description="Радиус режущей вершины в мм")

    @property
    def gabarit_volume(self) -> float:
        """Габаритный объем в мм³"""
        return self.height_mm * self.width_mm * self.length_mm

    @property
    def gabarit_str(self) -> str:
        """Строковое представление габаритов"""
        return f"LxBxH: {self.length_mm}x{self.width_mm}x{self.height_mm} мм."

    @property
    def _parameters(self) -> dict:
        return {
            "length_mm": self.length_mm,
            "width_mm": self.width_mm,
            "height_mm": self.height_mm,
            "radius_of_cutting_vertex": self.radius_of_cutting_vertex,
            "gabarit_volume": self.gabarit_volume,
            "gabarit_str": self.gabarit_str,
        }


class Angles(BaseModel, validate_assignment=True):
    """Углы инструмента.

    Parameters:
    main_angle_grad : (float >= 0, <= 360) : главный угол в плане в градусах.
    front_angle_grad : (float >= 0, <= 360) : передний угол в градусах.
    inclination_of_main_blade_grad : (float >= 0, <= 360) : наклон передней грани в градусах.

    Properties:
    _parameters : (dict) : возвращает словарь параметров и свойств.

    Methods:
    _parameters : (dict) : возвращает словарь всех параметров и свойств.
    """

    main_angle_grad: float = Field(default=0, ge=0, le=360, description="Главный угол в плане в градусах")
    front_angle_grad: float = Field(default=0, ge=0, le=360, description="Передний угол в градусах")
    inclination_of_main_blade_grad: float = Field(
        default=0, ge=0, le=360, description="Наклон передней грани в градусах"
    )

    @property
    def _parameters(self) -> dict:
        return {
            "main_angle_grad": self.main_angle_grad,
            "front_angle_grad": self.front_angle_grad,
            "inclination_of_main_blade_grad": self.inclination_of_main_blade_grad,
        }


if __name__ == '__main__':
    # Пример использования AxialSizes
    print("=== AxialSizes ===")
    axial = AxialSizes()
    print(axial)
    print('Габаритный объем:', axial.gabarit_volume, "мм³")
    print('Габарит строка:', axial.gabarit_str)
    print('Параметры:', axial._parameters)

    # Изменение размеров
    axial.dia_mm = 10
    axial.length_mm = 150
    print('Новый габарит:', axial.gabarit_str)

    # Пример использования PrismaticSizes
    print("\n=== PrismaticSizes ===")
    prismatic = PrismaticSizes()
    print(prismatic)
    print('Габаритный объем:', prismatic.gabarit_volume, "мм³")
    print('Габарит строка:', prismatic.gabarit_str)
    print('Параметры:', prismatic._parameters)

    # Изменение размеров
    prismatic.length_mm = 200
    print('Новый габарит:', prismatic.gabarit_str)

    # Пример использования Angles
    print("\n=== Angles ===")
    angles = Angles()
    print(angles)
    print('Параметры:', angles._parameters)

    # Изменение углов
    angles.main_angle_grad = 45
    angles.front_angle_grad = 10
    print('Новые углы:', angles._parameters)

    # Проверка валидации
    try:
        angles.main_angle_grad = 400  # Должно вызвать ошибку
    except Exception as e:
        print(f"Ошибка валидации: {e}")
