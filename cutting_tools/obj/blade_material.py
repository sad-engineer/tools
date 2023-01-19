#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.abstract_classes import BladeMaterialController
from cutting_tools.obj.data_classes import BladeMaterialData
from cutting_tools.obj.checker_in_dict import CheckerInDictionary


class BladeMaterial(BladeMaterialData, BladeMaterialController, CheckerInDictionary):
    """ Управляет полями класса "BladeMaterial" """
    def update_mat_of_cutting_part(self, new_mat):
        self.mat_of_cutting_part = new_mat
        if not self._in_dict(new_mat, None, self.MATS_OF_CUTTING_PART):
            self.mat_of_cutting_part = list(self.MATS_OF_CUTTING_PART.keys())[3]
