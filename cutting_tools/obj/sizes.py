#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.abstract_classes import Size
from cutting_tools.obj.abstract_classes import Dictionarer


class AxialSizes(Size, Dictionarer):
    """"Управляет полями класса 'AxialSizes'.

    Parameters:
        dia_mm : (float >= 0) : диаметр инструмента.
        length_mm : (float >= 0) : длина инструмента.

    Properties:
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.

    Methods:
        dict_parameters : (dict) : возвращает словарь параметров и свойств.
    """
    def __init__(self, dia_mm: float = 50, length_mm: float = 100):
        self._dia_mm = None
        self._length_mm = None

        self.dia_mm = dia_mm
        self.length_mm = length_mm

    @property
    def dia_mm(self):
        return self._dia_mm

    @property
    def length_mm(self):
        return self._length_mm

    @dia_mm.setter
    def dia_mm(self, any_dia):
        if not isinstance(any_dia, (int, float)):
            raise InvalidValue(f'Диаметр должен быть числом (передано {any_dia})')
        if any_dia < 0:
            raise InvalidValue(f'Диаметр должен быть больше 0 (передано {any_dia})')
        self._dia_mm = any_dia

    @length_mm.setter
    def length_mm(self, any_length):
        if not isinstance(any_length, (int, float)):
            raise InvalidValue(f'Длина должна быть числом (передано {any_length})')
        if any_length < 0:
            raise InvalidValue(f'Длина должна быть больше 0 (передано {any_length})')
        self._length_mm = any_length

    @property
    def gabarit_volume(self):
        return self._dia_mm * self._dia_mm * self._length_mm

    @property
    def gabarit_str(self):
        return f"øDxL: ø{self._dia_mm}x{self._length_mm} мм."

    def _dict_parameters(self):
        return {"dia_mm": self.dia_mm, "length_mm": self.length_mm, "gabarit_volume": self.gabarit_volume,
                "gabarit_str": self.gabarit_str}


class PrismaticSizes(Size, Dictionarer):
    """Управляет полями класса 'PrismaticSizes'.

    Parameters:
        length_mm : (float >= 0) : длина инструмента.
        width_mm : (float >= 0) : ширина инструмента.
        height_mm : (float >= 0) : высота инструмента.

    Properties:
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.

    Methods:
        dict_parameters : (dict) : возвращает словарь параметров и свойств.
    """
    def __init__(self, length_mm: float = 100, width_mm: float = 25, height_mm: float = 25):
        self._length_mm = None
        self._width_mm = None
        self._height_mm = None

        self.length_mm = length_mm
        self.width_mm = width_mm
        self.height_mm = height_mm

    @property
    def length_mm(self):
        return self._length_mm

    @property
    def width_mm(self):
        return self._width_mm

    @property
    def height_mm(self):
        return self._height_mm

    @length_mm.setter
    def length_mm(self, any_size):
        if not isinstance(any_size, (int, float)):
            raise InvalidValue(f'Длина должна быть числом (передано {any_size})')
        if any_size < 0:
            raise InvalidValue(f'Длина должна быть больше 0 (передано {any_size})')
        self._length_mm = any_size

    @width_mm.setter
    def width_mm(self, any_size):
        if not isinstance(any_size, (int, float)):
            raise InvalidValue(f'Ширина должна быть числом (передано {any_size})')
        if any_size < 0:
            raise InvalidValue(f'Ширина должна быть больше 0 (передано {any_size})')
        self._width_mm = any_size

    @height_mm.setter
    def height_mm(self, any_size):
        if not isinstance(any_size, (int, float)):
            raise InvalidValue(f'Высота должна быть числом (передано {any_size})')
        if any_size < 0:
            raise InvalidValue(f'Высота должна быть больше 0 (передано {any_size})')
        self._height_mm = any_size

    @property
    def gabarit_volume(self):
        return self.height_mm * self.width_mm * self.length_mm

    @property
    def gabarit_str(self):
        return f"LxBxH: {self.length_mm}x{self.width_mm}x{self.height_mm} мм."

    def _dict_parameters(self):
        return {"length_mm": self._length_mm, "width_mm": self._width_mm, "height_mm": self._height_mm,
                "gabarit_volume": self.gabarit_volume, "gabarit_str": self.gabarit_str}
