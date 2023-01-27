#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union, ClassVar

from cutting_tools.obj.constants import MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import HARD_ALLOYS, HIGH_SPEED_STEELS
from cutting_tools.obj.exceptions import InvalidValue
from cutting_tools.obj.abstract_classes import Dictionarer


class BladeMaterial(Dictionarer):
    """ДатаКласс 'Материал лезвия'.

    Parameters:
        mat_of_cutting_part : (str) : материал режущей пластины.
        type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Сostants:
        HARD_ALLOYS : перечень доступных твердосплавных материалов
        HIGH_SPEED_STEELS : перечень доступных быстрорежущих материалов
        MATS_OF_CUTTING_PART : перечень доступных материалов режущей части (общий)
    """
    MATS_OF_CUTTING_PART: ClassVar[dict] = MATERIALS_OF_CUTTING_PART
    HARD_ALLOYS: ClassVar[dict] = HARD_ALLOYS
    HIGH_SPEED_STEELS: ClassVar[dict] = HIGH_SPEED_STEELS

    def __init__(self, mat_of_cutting_part: Union[str, int] = 'Т15К6'):
        self._mat_of_cutting_part = None
        self.mat_of_cutting_part = mat_of_cutting_part

    @property
    def type_of_mat(self):
        return 1 if self.mat_of_cutting_part in self.HARD_ALLOYS else 0

    @property
    def mat_of_cutting_part(self):
        return self._mat_of_cutting_part

    @mat_of_cutting_part.setter
    def mat_of_cutting_part(self, mat):
        if isinstance(mat, (int, float)) and mat not in self.MATS_OF_CUTTING_PART.values():
            raise InvalidValue(f'Неверное значение материала режущей пластины. Значение должно быть из '
                               f'{self.MATS_OF_CUTTING_PART}.')
        if isinstance(mat, str) and mat not in self.MATS_OF_CUTTING_PART:
            raise InvalidValue(f'Неверное значение материала режущей пластины. Значение должно быть из '
                               f'{self.MATS_OF_CUTTING_PART}.')
        if not isinstance(mat, (int, float, str)):
            raise InvalidValue(f'Неверное значение материала режущей пластины. Значение должно быть из '
                               f'{self.MATS_OF_CUTTING_PART}.')
        self._mat_of_cutting_part = mat if isinstance(mat, str) else \
            [k for k, v in self.MATS_OF_CUTTING_PART.items() if v == mat][0]

    def _dict_parameters(self):
        return {"mat_of_cutting_part": self._mat_of_cutting_part, "type_of_mat": self.type_of_mat}
