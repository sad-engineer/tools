#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod


class AnglesController(ABC):
    """ Управляет полями класса "Angles" """
    @abstractmethod
    def update_main_angle_grad(self, new_angle: float): pass

    @abstractmethod
    def update_front_angle_grad(self, new_angle: float): pass

    @abstractmethod
    def update_inclination_of_main_blade(self, new_angle: float): pass


class BladeMaterialController(ABC):
    """ Абстрактный класс, реализует обновления полей класса "BladeMaterial" """
    @abstractmethod
    def update_mat_of_cutting_part(self, new_mat_of_cutting_part: str): pass


class SizesValidator(ABC):
    """ Абстрактный класс, реализует проверку размера или угла (должен быть типа int, float и больше 0), изменение
    значения размера или угла """
    @staticmethod
    @abstractmethod
    def _is_correct_type_size(size): pass

    @staticmethod
    @abstractmethod
    def _is_correct_value_size(size: [int, float]): pass

    @abstractmethod
    def _is_correct_size(self, size): pass

    @abstractmethod
    def _is_correct_sizes(self, sizes: list): pass

    @abstractmethod
    def check_size(self, size): pass


class ToolValidator(ABC):
    """ Абстрактный класс, реализует проверки полей стандартного инструмента """

    @abstractmethod
    def _is_correct_standard(self, any_standard): pass

    @abstractmethod
    def check_standard(self, standard): pass

    @staticmethod
    @abstractmethod
    def check_marking(marking): pass


class ToolController(ABC):
    """ Абстрактный класс, реализует управление полями класса "Tool" """

    @abstractmethod
    def update_group(self, new_group): pass

    @abstractmethod
    def update_marking(self, new_marking): pass

    @abstractmethod
    def update_standard(self, new_standard): pass


class MillingCutterController(ABC):
    """ Абстрактный класс, реализует проверки полей класса "MillingCutter" """
    @abstractmethod
    def update_type_cutter(self, new_type): pass

    @abstractmethod
    def update_type_of_cutting_part(self, new_type): pass

    @abstractmethod
    def update_num_of_cutting_blades(self, new_num_of_cutting_blades): pass

    @abstractmethod
    def update_radius_of_cutting_vertex(self, new_radius): pass

    @abstractmethod
    def update_large_tooth(self, new_large_tooth): pass
