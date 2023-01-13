#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from cutting_tools.obj.sizes_validator import SizesValidator


@dataclass
class CuttingToolAngles(SizesValidator):
    """ДатаКласс 'Углы режущего инструмента'. Хранит состояние инструмента

    Parameters:
        main_angle_grad : (float) : главный угол инструмента в плане .
        front_angle_grad : (float) : передний угол в плане.
        inclination_of_main_blade : (float) : угол наклона переднего лезвия.
    """
    main_angle_grad: float = 45
    front_angle_grad: float = 45  # gamma передний угол в плане
    inclination_of_main_blade_grad: float = 0  # lambda угол наклона переднего лезвия

    def update_main_angle_grad(self, new_angle: float):
        self.main_angle_grad = self.check_size(new_angle)

    def update_front_angle_grad(self, new_angle: float):
        self.front_angle_grad = self.check_size(new_angle)

    def update_inclination_of_main_blade(self, new_angle: float):
        self.inclination_of_main_blade_grad = self.check_size(new_angle)

