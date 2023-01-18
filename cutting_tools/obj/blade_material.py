#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.abstract_classes import BladeMaterialController, BladeMaterialValidator
from cutting_tools.obj. data_classes import BladeMaterialData


class BladeMaterial(BladeMaterialData, BladeMaterialValidator, BladeMaterialController):
    """ Управляет полями класса "BladeMaterial" """
    def update_mat_of_cutting_part(self, new_mat_of_cutting_part):
        self.mat_of_cutting_part = new_mat_of_cutting_part
        if not self._is_correct_mat_of_cutting_part:
            self.mat_of_cutting_part = list(self.MATS_OF_CUTTING_PART.keys())[3]

    @property
    def _is_correct_mat_of_cutting_part(self):
        if isinstance(self.mat_of_cutting_part, str):
            return self.mat_of_cutting_part in self.MATS_OF_CUTTING_PART
        return False
