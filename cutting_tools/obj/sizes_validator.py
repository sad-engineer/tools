#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from cutting_tools.obj.exceptions import InvalidValue


class SizesValidator(ABC):
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
