#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.abstract_classes import SizesValidator
from cutting_tools.obj.data_classes import AxialSizesData, PrismaticSizesData
from cutting_tools.obj.exceptions import InvalidValue


class SizeValidator(SizesValidator):
    """ Абстрактный класс, реализует проверку размера или угла (должен быть типа int, float и больше 0), изменение
    значения размера или угла """
    @staticmethod
    def _is_correct_type_size(size):
        return isinstance(size, (int, float))

    @staticmethod
    def _is_correct_value_size(size: [int, float]):
        return size >= 0

    def _is_correct_size(self, size):
        return self._is_correct_value_size(size) if self._is_correct_type_size(size) else False

    def _is_correct_sizes(self, sizes: list):
        result = []
        for size in sizes:
            result.append(self._is_correct_size(size))
        return result

    def check_size(self, size):
        if self._is_correct_size(size):
            return size
        else:
            raise InvalidValue(f"Неверное значение размера(или угла): {size} мм(град)")


class AxialSizesInterface(AxialSizesData, SizeValidator):
    """Управляет полями класса 'AxialSizes'. """
    @property
    def gabarit_volume(self):
        return self.dia_mm ** 2 * self.length_mm

    @property
    def gabarit_str(self):
        return f"øDxL: ø{self.dia_mm}x{self.length_mm} мм"

    def update_dia(self, new_dia_mm: float):
        self.dia_mm = self.check_size(new_dia_mm)

    def update_length(self, new_length_mm: float):
        self.length_mm = self.check_size(new_length_mm)


class PrismaticSizesInterface(PrismaticSizesData, SizeValidator):
    """Управляет полями класса 'PrismaticSizes'. """
    @property
    def gabarit_volume(self):
        return self.height_mm * self.width_mm * self.length_mm

    @property
    def gabarit_str(self):
        return f"LxBxH: ø{self.length_mm}x{self.width_mm}x{self.height_mm} мм"

    def update_length(self, new_length_mm: float):
        self.length_mm = self.check_size(new_length_mm)

    def update_width(self, new_width_mm: float):
        self.width_mm = self.check_size(new_width_mm)

    def update_height(self, new_height_mm: float):
        self.height_mm = self.check_size(new_height_mm)
