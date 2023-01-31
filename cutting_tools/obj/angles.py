#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.abstract_classes import Dictionarer


class Angles(Dictionarer):
    """ Управляет полями класса "Angles"

    Parameters:
        main_angle_grad : (float >= 0) : главный угол в плане.
        front_angle_grad  : (float >= 0) : передний угол.
        inclination_of_main_blade_grad  : (float >= 0) : наклон передней грани

    Methods:
        dict_parameters : (dict) : возвращает словарь параметров и свойств.
    """
    def __init__(self, main_angle_grad: float = 45, front_angle_grad: float = 45,
                 inclination_of_main_blade_grad: float = 0):
        self._main_angle_grad = None
        self._front_angle_grad = None
        self._inclination_of_main_blade_grad = None

        self.main_angle_grad = main_angle_grad
        self.front_angle_grad = front_angle_grad
        self.inclination_of_main_blade_grad = inclination_of_main_blade_grad

    @property
    def main_angle_grad(self):
        return self._main_angle_grad

    @property
    def front_angle_grad(self):
        return self._front_angle_grad

    @property
    def inclination_of_main_blade_grad(self):
        return self._inclination_of_main_blade_grad

    @main_angle_grad.setter
    def main_angle_grad(self, any_angle_grad):
        if not isinstance(any_angle_grad, (int, float)):
            raise InvalidValue(f'Значение угла должно быть целым или дробным.')
        self._main_angle_grad = any_angle_grad

    @front_angle_grad.setter
    def front_angle_grad(self, any_angle_grad):
        if not isinstance(any_angle_grad, (int, float)):
            raise InvalidValue(f'Значение угла должно быть целым или дробным.')
        self._front_angle_grad = any_angle_grad

    @inclination_of_main_blade_grad.setter
    def inclination_of_main_blade_grad(self, any_angle_grad):
        if not isinstance(any_angle_grad, (int, float)):
            raise InvalidValue(f'Значение угла должно быть целым или дробным.')
        self._inclination_of_main_blade_grad = any_angle_grad

    def _dict_parameters(self):
        return {"main_angle_grad": self._main_angle_grad, "front_angle_grad": self._front_angle_grad,
                "inclination_of_main_blade_grad": self._inclination_of_main_blade_grad, }