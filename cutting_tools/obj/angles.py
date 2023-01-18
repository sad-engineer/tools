#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.abstract_classes import AnglesController
from cutting_tools.obj.data_classes import AnglesData
from cutting_tools.obj.sizes import SizeValidator


class Angles(AnglesData, AnglesController, SizeValidator):
    """ Управляет полями класса "Angles" """
    def update_main_angle_grad(self, new_angle: float):
        self.main_angle_grad = self.check_size(new_angle)

    def update_front_angle_grad(self, new_angle: float):
        self.front_angle_grad = self.check_size(new_angle)

    def update_inclination_of_main_blade(self, new_angle: float):
        self.inclination_of_main_blade_grad = self.check_size(new_angle)
